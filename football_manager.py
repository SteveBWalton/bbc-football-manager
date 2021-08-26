#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to run the BBC Football Manager program.
This is a convertion of the BBC Basic Football Manager program to Python.
This is a console program should run under Linux and Windows.
'''

# System libraries.
import sys
import os
import argparse
import platform
import subprocess
import shutil
import datetime
import time
import random

# Application Libraries.
import ansi
from game import Game



def run(args):
    ''' Main entry point for the program. '''
    # Default to graphical mode now.
    if args.text:
        args.graphical = False
    else:
        args.graphical = True

    # Create a game object.
    game = Game(args)
    game.run()



if __name__ == '__main__':
    # Process the command line arguments.
    # This might end the program (--help).
    argParse = argparse.ArgumentParser(prog='football_manager', description='Convertion of the BBC Basic Football Manager program.')
    argParse.add_argument('-d', '--debug', help='Run the program in debug mode.', action='store_true')
    argParse.add_argument('-g', '--graphical', help='Run the program in a graphical wx window.', action='store_true')
    argParse.add_argument('-t', '--text', help='Run the program at the command line.', action='store_true')
    args = argParse.parse_args()

    # Welcome message.
    print('{}BBC Football Manager{} by Steve Walton.'.format(ansi.RED, ansi.RESET_ALL))
    print('Developed 2018-2021.  Original BBC Basic verison developed 1982-1989, 2000')
    print('Python Version {}·{}·{} (expecting Python 3).'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
    print('Operating System is "{}{}{}".  Desktop is "{}".'.format(ansi.YELLOW, platform.system(), ansi.RESET_ALL, os.environ.get('DESKTOP_SESSION')))

    # Main loop.
    run(args)

    print('Goodbye from the {}BBC Football Manager{} program.'.format(ansi.RED, ansi.RESET_ALL))
