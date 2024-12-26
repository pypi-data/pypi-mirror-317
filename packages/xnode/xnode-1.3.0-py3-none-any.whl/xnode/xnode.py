import re
import sys
import glob
import time  
import serial

from genlib.ansiec import ANSIEC

from .cli import cli

def main():
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    
    cmd = None
    if len(sys.argv) == 2:
        cmd = sys.argv[1].lower()
  
    if cmd and cmd == "scan":
            if sys.platform.startswith('win'):
                ports = ['COM%s' % (i + 1) for i in range(256)]    
            elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
                ports = glob.glob('/dev/tty[A-Za-z]*')
            elif sys.platform.startswith('darwin'):
                ports = glob.glob('/dev/tty.*')
            else:
                raise EnvironmentError('Unsupported platform')

            color_tbl = (ANSIEC.FG.BRIGHT_YELLOW, ANSIEC.FG.BRIGHT_GREEN, ANSIEC.FG.BRIGHT_BLUE)
            color_pos = 0    
            
            for port in ports:
                try:
                    ser = serial.Serial(port, 115200, timeout=1)
                    ser.write(b'\x03') # Ctrl + C(b'\x03') --> interrupt any running program
                    ser.read_all().decode('utf-8') # >>>
                    ser.write(b'\x02') # Ctrl + B(b'\x02') --> enter normal repl, ref: Ctrl + D(b'\x04') --> soft reset, 
                    time.sleep(0.1)
                    response = ser.read_all().decode('utf-8').strip()
        
                    if 'MicroPython' in response:
                        s = response.find("MicroPython") + len("MicroPython")
                        e = response.find('Type "help()"')
                        print(color_tbl[color_pos] + f"{port}" + ANSIEC.OP.RESET + f" ({response[s:e].strip()})")
                        color_pos = (color_pos + 1) % len(color_tbl)

                    ser.close()
                except (OSError, serial.SerialException):
                    pass
    else:    
        exit_code = cli()
        sys.exit(exit_code)
	
if __name__ == '__main__':
    main()