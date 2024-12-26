import sys
import os
import threading
import time

import posixpath
import ast
import textwrap
import binascii

import serial


try:
    stdout = sys.stdout.buffer
except AttributeError:
    stdout = sys.stdout

def stdout_write_bytes(b):
    b = b.replace(b"\x04", b"")
    stdout.write(b)
    stdout.flush()


class BoardError(BaseException): pass
class DirectoryExistsError(Exception): pass

class Pyboard:
    BUFFER_SIZE = 32

    def __init__(self, device, baudrate=115200, wait=0):  
        delayed = False

        for attempt in range(wait + 1):
            try:
                self.serial = serial.Serial(device, baudrate=baudrate, inter_byte_timeout=1, timeout=0.5)
                break
            except (OSError, IOError): 
                if wait == 0:
                    continue
                if attempt == 0:
                    sys.stdout.write(f"Waiting {wait} seconds for board ")
                    delayed = True
            time.sleep(1)
            sys.stdout.write('.')
            sys.stdout.flush()
        else:
            if delayed:
                print('')
            raise BoardError('failed to access ' + device)
        if delayed:
            print('')

    def close(self):
        self.serial.close()

    def read_until(self, min_num_bytes, ending, timeout=10, data_consumer=None):
        data = self.serial.read(min_num_bytes)
        if data_consumer:
            data_consumer(data)
        timeout_count = 0
        while True:
            if data.endswith(ending):
                break
            elif self.serial.in_waiting > 0:
                new_data = self.serial.read(1)
                data = data + new_data
                if data_consumer:
                    data_consumer(new_data)
                timeout_count = 0
            else:
                timeout_count += 1
                if timeout is not None and timeout_count >= 100 * timeout:
                    break
                time.sleep(0.01)
        return data

    def enter_raw_repl(self):
        self.serial.write(b'\r\x03\x03') # ctrl-C twice: interrupt any running program

        n = self.serial.in_waiting
        while n > 0:
            self.serial.read(n)
            n = self.serial.in_waiting

        self.serial.write(b'\r\x01') # ctrl-A: enter raw REPL
        data = self.read_until(1, b'raw REPL; CTRL-B to exit\r\n>')
        if not data.endswith(b'raw REPL; CTRL-B to exit\r\n>'):
            print(data)
            raise BoardError('could not enter raw repl')

        self.serial.write(b'\x04') # ctrl-D: soft reset
        data = self.read_until(1, b'soft reboot\r\n')
        if not data.endswith(b'soft reboot\r\n'):
            print(data)
            raise BoardError('could not enter raw repl')

        data = self.read_until(1, b'raw REPL; CTRL-B to exit\r\n')
        if not data.endswith(b'raw REPL; CTRL-B to exit\r\n'):
            print(data)
            raise BoardError('could not enter raw repl')

    def exit_raw_repl(self):
        self.serial.write(b'\r\x02') # ctrl-B: enter friendly REPL

    def _follow_write(self, echo):
        import os
        
        try:
            import msvcrt
            def getkey():
                return msvcrt.getch()

            def putkey(ch):
                if ch == b'\r':
                    ch = b'\n'
                msvcrt.putch(ch)
                
        except ImportError:
            import sys, tty, termios
            def getkey():
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(sys.stdin.fileno())
                    ch = sys.stdin.read(1)
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
                return ch
            
            def putkey(ch):
                sys.stdout.write(ch)
                sys.stdout.flush()
        
        while True:
            ch = getkey()
            if ch == b'\x03': # Ctrl + C
                os._exit(0)
            if echo:
                putkey(ch)
            self.serial.write(ch)

    def follow(self, timeout, data_consumer=None, input_stat=None):
        if input_stat[1]:
            from threading import Thread

            th = Thread(target=self._follow_write, args=(input_stat[0],))
            th.daemon = True
            th.start()
        
        data = self.read_until(1, b'\x04', timeout=timeout, data_consumer=data_consumer)
        if not data.endswith(b'\x04'):
            raise BoardError('timeout waiting for first EOF reception')
        data = data[:-1]

        data_err = self.read_until(1, b'\x04', timeout=timeout)
        if not data_err.endswith(b'\x04'):
            raise BoardError('timeout waiting for second EOF reception')
        data_err = data_err[:-1]

        return data, data_err

    def exec_raw_no_follow(self, command):            
        if isinstance(command, bytes):
            command_bytes = command
        else:
            command_bytes = bytes(command, encoding='utf8')

        data = self.read_until(1, b'>')
        if not data.endswith(b'>'):
            raise BoardError('could not enter raw repl')

        for i in range(0, len(command_bytes), 256):
            self.serial.write(command_bytes[i:min(i + 256, len(command_bytes))])
            time.sleep(0.01)
        self.serial.write(b'\x04')

        data = self.read_until(1, b'OK')
        if not data.endswith(b'OK'):
            raise BoardError('could not exec command')

    def exec_raw(self, command, timeout=None, data_consumer=None, input_stat=None):
        self.exec_raw_no_follow(command)
        return self.follow(timeout, data_consumer, input_stat)

    def exec_(self, command, stream_output=False, echo_on=False):
        data_consumer = None
        if stream_output or echo_on:
            data_consumer = stdout_write_bytes
        ret, ret_err = self.exec_raw(command, data_consumer=data_consumer, input_stat=(stream_output, echo_on))
        if ret_err:
            raise BoardError('exception', ret.decode('utf-8'), ret_err.decode('utf-8'))
        return ret
    
    def execfile(self, filename, stream_output=False, echo_on=False):
        with open(filename, 'r+b') as f:
            pyfile = f.read()
        return self.exec_(pyfile, stream_output, echo_on)
    
    def _exec_command(self, command):
        self.enter_raw_repl()
        try:
            out = self.exec_(textwrap.dedent(command))
        except BoardError as ex:
            raise ex
        self.exit_raw_repl()
        return out

    def run(self, filename, stream_output=False, echo_on=False):
        self.enter_raw_repl()
        if not stream_output and not echo_on:       # -n
            with open(filename, "rb") as infile:        # Running without io stream
                self.exec_raw_no_follow(infile.read())
        elif not stream_output and echo_on:         # -in
            self.execfile(filename, False, True)        # Echo off
        elif stream_output and echo_on:             #-i
            self.execfile(filename, True, True)         # Echo on            
        else:                                       # default
            self.execfile(filename, False, True)        # Echo off
        self.exit_raw_repl()
    
    def fs_get(self, filename):
        command = f"""
            import sys
            import ubinascii
            with open('{filename}', 'rb') as infile:
                while True:
                    result = infile.read({self.BUFFER_SIZE})
                    if result == b'':
                        break
                    len = sys.stdout.write(ubinascii.hexlify(result))
        """
        out = self._exec_command(command)
        return binascii.unhexlify(out)

    def fs_ls(self, dir="/"):
        if not dir.startswith("/"):
            dir = "/" + dir
        #if dir.endswith("/"):
        #    dir = dir[:-1]
            
        command = f"""
            import os
            def listdir(dir):
                if dir == '/':                
                    return sorted([dir + f for f in os.listdir(dir)])
                else:
                    return sorted([dir + '/' + f for f in os.listdir(dir)])
            print(listdir('{dir}'))
        """
        out = self._exec_command(command)
        return ast.literal_eval(out.decode("utf-8"))
            
    def fs_is_dir(self, path):
        command = f"""
            vstat = None
            try:
                from os import stat
            except ImportError:
                from os import listdir
                vstat = listdir
            def ls_dir(path):
                if vstat is None:
                    return stat(path)[0] & 0x4000 != 0
                else:
                    try:
                        vstat(path)
                        return True
                    except OSError as e:
                        return False
            print(ls_dir('{path}'))
        """
        out = self._exec_command(command)
        return ast.literal_eval(out.decode("utf-8"))

    def fs_mkdir(self, dir):       
        command = f"""
            import os
            def mkdir(dir):
                parts = dir.split(os.sep)
                dirs = [os.sep.join(parts[:i+1]) for i in range(len(parts))]
                check = 0
                for d in dirs:
                    try:
                        os.mkdir(d)
                    except OSError as e:
                        check += 1
                        if "EEXIST" in str(e):
                            continue
                        else:
                            return False
                return check < len(parts)
            print(mkdir('{dir}'))
        """        
        out = self._exec_command(command)
        return ast.literal_eval(out.decode("utf-8"))

    def fs_putdir(self, local, remote, callback=None):        
        for parent, child_dirs, child_files in os.walk(local, followlinks=True):
            remote_parent = posixpath.normpath(posixpath.join(remote, os.path.relpath(parent, local)))
           
            try:
                self.fs_mkdir(remote_parent)
            except:
                pass
        
            for filename in child_files:
                with open(os.path.join(parent, filename), "rb") as infile:
                    remote_filename = posixpath.join(remote_parent, filename)
                    data = infile.read()

                    total_size = os.path.getsize(os.path.join(parent, filename))                 
                    if callback:
                        th = threading.Thread(target=callback, args=(remote_filename, total_size), daemon=True)
                        th.start()
                        
                    self.fs_put(data, remote_filename)
                    
                    if callback:
                        th.join() 

    def fs_put(self, local_data, remote, callback=None):
        self.enter_raw_repl()
        try:
            self.exec_(f"f = open('{remote}', 'wb')")
        except BoardError as e:
            if "EEXIST" in str(e):
                self.exit_raw_repl()
                self.fs_rm(remote)
                self.fs_put(local_data, remote, callback)
            return

        size = len(local_data)
        if callback:
            th = threading.Thread(target=callback, args=(remote, size), daemon=True)
            th.start()
            
        for i in range(0, size, self.BUFFER_SIZE):
            chunk_size = min(self.BUFFER_SIZE, size - i)
            chunk = repr(local_data[i : i + chunk_size])
            if not chunk.startswith("b"):
                chunk = "b" + chunk
            self.exec_(f"f.write({chunk})")
        
        self.exec_("f.close()")
        self.exit_raw_repl()
        
        if callback:
            th.join() 

    def fs_rm(self, filename):
        command = f"""
            import os
            os.remove('{filename}')
        """
        self._exec_command(command)

    def fs_rmdir(self, dir):
        command = f"""
            import os
            def rmdir(dir):
                os.chdir(dir)
                for f in os.listdir():
                    try:
                        os.remove(f)
                    except OSError:
                        pass
                for f in os.listdir():
                    rmdir(f)
                os.chdir('..')
                os.rmdir(dir)
            rmdir('{dir}')
        """
        self._exec_command(command)

    def fs_format(self, type):
        if type == "lopy":
            command = """ 
                import os
                os.fsformat('/flash')
            """
        elif type == "xbee3":
            command = """
                import os
                os.format()
            """
        elif type == "pico2":
            command = """
                import os
                import rp2
                bdev = rp2.Flash()
                os.VfsFat.mkfs(bdev)
            """
        else:
            return False
        
        self._exec_command(command)
        return True

setattr(Pyboard, "exec", Pyboard.exec_)
