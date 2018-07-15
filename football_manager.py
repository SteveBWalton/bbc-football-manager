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
import modANSI
import modGame



def Run():
    ''' Main entry point for the program. '''
    # Create a game object.
    oGame = modGame.CGame()
    oGame.Football()

    # Get the player settings.
    print()
    oGame.player_name = input('Please enter your name: ')
    print('Hello {}{}{}.'.format(modANSI.RED, oGame.player_name, modANSI.RESET_ALL))




if __name__ == '__main__':
    # Process the command line arguments.
    # This might end the program (--help).
    oParse = argparse.ArgumentParser(prog='football_manager', description='Convertion of the BBC Basic Football Manager program.')
    oArgs = oParse.parse_args()

    # Welcome message.
    print('{}BBC Football Manager{} by Steve Walton.'.format(modANSI.RED, modANSI.RESET_ALL))
    print('Developed 2018.  Original BBC Basic verison developed 1982-1989, 2000')
    print('Python Version {}.{}.{} (expecting Python 3).'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
    print('Operating System is "{}".  Desktop is "{}".'.format(platform.system(), os.environ.get('DESKTOP_SESSION')))

    # Main loop.
    Run()

    print('Goodbye from the {}BBC Football Manager{} program.'.format(modANSI.RED, modANSI.RESET_ALL))
