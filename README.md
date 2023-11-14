# BBC Football Manager
Conversion of my BBC Basic Football Manager program into Python.
I wrote the original BBC Basic version between 1982 and 1989.
In 2000, I made changes to allow the program to work on BeebEm under Windows.

In 2018, I started converting the program to Python with the intention that the program be a console program that would work under Linux and Windows.
Currently, just trying to get the console version working under Linux.
  
In 2021, I started to add support for a version that runs in a wx window.  This works under Linux and Windows.

## How to Run
To run the program in a wx window.  Clone project and cd into the top level folder.
```bash
./football_manager.py -g
```
or (Windows)
```bash
python football_manager.py -g
```
The **-g** switch is optional now, graphical mode is now the default.

To run the program in the console.  
```bash
./football_manager.py -t
```
The console mode now only works in Linux.
