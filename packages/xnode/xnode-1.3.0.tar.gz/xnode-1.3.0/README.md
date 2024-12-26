This is a CLI management tool for MicroPython-based XNode.

### Help
```sh
xnode
```
or
```sh
xnode --help
```

### Find serial port
```sh
xnode scan
```

### Option Rules
- Options and values can have spaces or omit spaces.
- Options and values can be inserted with the = character.

```sh
<option><value>  
<option> <value>
<option>=<value> 
```

### Initialize XNode file system (Only xnode type b)
```sh
xnode -s<com_port_name> init
```
or
```sh
xnode --sport<com_port_name> init
```
> \<com_port_name\> is the port number found by scan. 

### Check list of XNode file systems
```sh
xnode -s<com_port_name> ls
xnode -s<com_port_name> ls /flash/lib/xnode/pop
```

### Put PC file or directroy into XNode
```sh
xnode -s<com_port_name> put my.py /flash/main.py
```
> my.py is the name of the script written on the PC, main.py is the name to be installed on XNode  
>> Automatically runs /flash/main.py if it exists when XNode starts

### Get XNode file to PC
```sh
xnode -s<com_port_name> get /flash/main.py main.py
```

### Delete XNode file or directory
```sh
xnode -s<com_port_name> rm /flash/main.py
```

### Executes the PC's MicroPython script by sequentially passing it to the XNode
```sh
xnode -s<com_port_name> run app.py
```
> Wait for serial output until the script finishes  
>> To force quit in running state, press Ctrl+c

**Additional Options**
   - -in (or default): Does not display the pressed key in the terminal window (Echo off)
   - -i: Display the pressed key in the terminal window (Echo on)
   - -n: Does not wait for serial output, so it appears as if the program has terminated on the PC side.
     - Script continues to run on XNode
     - Used to check data output serially from XNode with other tools (PuTTY, smon, etc.)
