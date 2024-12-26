import os
import sys
import time
import platform
import re
import threading
import click
import dotenv

from genlib.ansiec import ANSIEC
from xnode.pyboard import Pyboard, BoardError


config = dotenv.find_dotenv(filename=".xnode", usecwd=True)
if config:
    dotenv.load_dotenv(dotenv_path=config)

_board = None
_type = None

def windows_full_port_name(portname):
    m = re.match(r"^COM(\d+)$", portname)
    if m and int(m.group(1)) < 10:
        return portname
    else:
        return "\\\\.\\{0}".format(portname)

@click.group()
@click.option(
    "--sport",
    "-s",
    envvar="SERIAL_PORT",
    required=True,
    type=click.STRING,
    help="Serial port name for connected board.",
    metavar="SPORT",
)
@click.option(
    "--baud",
    '-b',
    envvar="SERIAL_BAUD",
    default=115200,
    type=click.INT,
    help="Baud rate for the serial connection (default 115200).",
    metavar="BAUD",
)
@click.option(
    "--type",
    '-t',
    envvar="DEVICE_TYPE",
    default='xbee3',
    type=click.STRING,
    help="Device type",
    metavar="TYPE",
)
def cli(sport, baud, type):
    global _board, _type

    if platform.system() == "Windows":
        sport = windows_full_port_name(sport)

    _board = Pyboard(sport, baud)
    _type = type.lower().strip()

@cli.command()
@click.argument("remote_file")
@click.argument("local_file", type=click.File("wb"), required=False)
def get(remote_file, local_file):
    contents = _board.fs_get(remote_file)

    if local_file is None:
        print(contents.decode("utf-8"))
    else:
        local_file.write(contents)
    
@cli.command()
@click.argument("dir")
def mkdir(dir):
    if _board.fs_mkdir(dir):
        print(ANSIEC.OP.left() + f"{dir} is " + ANSIEC.FG.BRIGHT_GREEN + "created." + ANSIEC.OP.RESET)
    else:
        print(ANSIEC.OP.left() + f"{dir} is " + ANSIEC.FG.BRIGHT_RED + "already exists." + ANSIEC.OP.RESET)

@cli.command()
@click.argument("dir", default="/")
def ls(dir):  
    try:
        for f in _board.fs_ls(dir):
            f_name = f.split("/")[-1]
            if _board.fs_is_dir(f):
                print(f"{f_name}")
            else:
                print(ANSIEC.OP.left() + ANSIEC.FG.BRIGHT_BLUE + f_name + ANSIEC.OP.RESET)
    except BoardError:
        print(ANSIEC.OP.left() + "The path " + ANSIEC.FG.BRIGHT_RED + "does not exist." + ANSIEC.OP.RESET)
                
def show_waiting(remote_filename, total_size):
    copied_size = 0
    bar_length = 40
    print(ANSIEC.OP.left() + ANSIEC.FG.BRIGHT_BLUE + remote_filename + ANSIEC.OP.RESET, flush=True)
    while True:
        progress = min(copied_size / total_size, 1.0)    
        block = int(round(bar_length * progress))
        bar = "#" * block + "-" * (bar_length - block)
        print(ANSIEC.OP.left() + f"[{bar}] {int(progress * 100)}%", end="", flush=True)
        if progress >= 1.0:
            break
        time.sleep(0.1)
        if _type == 'xbee3':
            copied_size += (115200 // 8 // 100) * 0.8
        elif _type == 'pico2':
            copied_size += (115200 // 8 // 100) * 2
                    
    print(flush=True)

@cli.command()
@click.argument("local", type=click.Path(exists=True))
@click.argument("remote", required=False)
def put(local, remote):
    if remote is None:
        remote = os.path.basename(os.path.abspath(local))
    else:
        try:
            if _board.fs_is_dir(remote):
                remote = remote + "/" + os.path.basename(os.path.abspath(local))
        except BoardError:
            pass
        
    if os.path.isdir(local):
        _board.fs_putdir(local, remote, show_waiting)
    else:
        with open(local, "rb") as infile:        
            _board.fs_put(infile.read(), remote, show_waiting)
    
@cli.command()
@click.argument("remote")
def rm(remote):
    if _board.fs_is_dir(remote):
        _board.fs_rmdir(remote)
    else:
        _board.fs_rm(remote)

@cli.command()
@click.argument("local_file")
@click.option(
    "--no-stream",
    "-n",
    is_flag=True,
    help="Do not join input/output stream",
)
@click.option(
    "--input-echo-on",
    "-i",
    is_flag=True,
    help="Turn on echo for input",
)
def run(local_file, no_stream, input_echo_on):
    try:
        _board.run(local_file, not no_stream, input_echo_on)
    except IOError:
        click.echo(
            f"Failed to find or read input file: {local_file}", err=True
        )

serial_reader_running = None
serial_out_put_enable = True
serial_out_put_count = 0

def repl_serial_to_stdout(serial):
    global serial_out_put_count

    def hexsend(string_data=''):
        import binascii
        hex_data = binascii.unhexlify(string_data)
        return hex_data

    try:
        data = b''
        while serial_reader_running:
            count = serial.in_waiting
            if count == 0:
                time.sleep(0.01)
                continue

            if count > 0:
                try:
                    data += serial.read(count)

                    if len(data) < 20:
                        try:
                            data.decode()
                        except UnicodeDecodeError:
                            continue

                    if data != b'':
                        if serial_out_put_enable and serial_out_put_count > 0:
                            if platform.system() == 'Windows':   
                                sys.stdout.buffer.write(data.replace(b"\r", b""))
                            else:
                                sys.stdout.buffer.write(data)
                                
                            sys.stdout.buffer.flush()
                    else:
                        serial.write(hexsend(data))

                    data = b''
                    serial_out_put_count += 1

                except:
                    return
    except KeyboardInterrupt:
        if serial != None:
            serial.close()

@cli.command()
def repl():
    global serial_reader_running
    global serial_out_put_enable
    global serial_out_put_count

    serial_out_put_count = 1

    serial_reader_running = True

    _board.read_until(1, b'\x3E\x3E\x3E', timeout=1) # read prompt >>>

    serial = _board.serial

    repl_thread = threading.Thread(target=repl_serial_to_stdout, args=(serial,), name='REPL')
    repl_thread.daemon = True
    repl_thread.start()

    if platform.system() == 'Windows':   
        import msvcrt as getch
    else:
        import getch
        
    serial.write(b'\r') # Update prompt
    
    count = 0
    print(ANSIEC.OP.left() + ANSIEC.FG.MAGENTA + "Entering REPL mode. Press Ctrl + X to exit." + ANSIEC.OP.RESET)

    while True:
        char = getch.getch()
    
        if char == b'\x16': # Ctrl + V(\x16) to Ctrl + C(\x03)
            char = b'\x03'

        count += 1
        if count == 1000:
            time.sleep(0.01)
            count = 0

        if char == b'\x07':
            serial_out_put_enable = False
            continue

        if char == b'\x0F':
            serial_out_put_enable = True
            serial_out_put_count = 0
            continue

        if char == b'\x00' or not char:
            continue

        if char == b'\x18':   # Ctrl + x to exit repl mode
            serial_reader_running = False
            serial.write(b' ')
            time.sleep(0.01)
            print('')
            break

        if char == b'\n':
            serial.write(b'\r')
        else:
            serial.write(char)

@cli.command()
def format():
    print(ANSIEC.OP.left() + "Formatting...")
    ret = _board.fs_format(_type)
    if ret:
        print(ANSIEC.OP.left() + "Formatting is complete!")
    else:
        print(ANSIEC.OP.left() + "The device type is not supported.")
    return ret

@cli.command()
def init():    
    if not click.Context(format).invoke(format):
        return 
        
    if _type == 'xbee3':
        root = "/flash/lib"
    elif _type == 'pico2':
        root = "/lib"
    else:
        print(ANSIEC.OP.left() + "The device type is not supported.")
        return

    print(_type)
    
    local = os.path.join(os.path.dirname(__file__), "pop")
    remote = root + "/xnode/pop"
    
    print(ANSIEC.OP.left() + "Installing the pop library on the board.")
    
    pycache_path = local + "\\__pycache__"
    import shutil
    if os.path.exists(pycache_path):
        shutil.rmtree(pycache_path)
    
    _board.fs_mkdir(root)
    click.Context(put).invoke(put, local=local, remote=remote)
    
    print(ANSIEC.OP.left() + "The job is done!")

@cli.command()
def scan():
    pass
