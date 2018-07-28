# -*- coding: utf-8 -*-

'''
Module to define ANSI / VT100 formatting and colour codes.
'''

RESET_ALL = '\033[0;m'
RESET_BOLD = '\033[21;m'
RESET_DIM = '\033[22;m'
RESET_UNDERLINE = '\033[24;m'
RESET_BLINK = '\033[25;m'
RESET_REVERSE = '\033[27;m'
RESET_HIDDEN = '\033[28;m'

BOLD = '\033[1m'
DIM = '\033[2;m'
UNDERLINE = '\033[4;m'
BLINK = '\033[5;m'
REVERSE = '\033[7;m'
HIDDEN = '\033[8;m'

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHT_GRAY = '\033[37m'
DARK_GRAY = '\033[90m'
LIGHT_RED = '\033[91m'
LIGHT_GREEN = '\033[92m'
LIGHT_YELLOW = '\033[93m'
LIGHT_BLUE = '\033[94m'
LIGHT_MAGENTA = '\033[95m'
LIGHT_CYAN = '\033[96m'
WHITE = '\033[97m'

BACKGROUND_DEFAULT = '\033[49m'
BACKGROUND_BLACK = '\033[40m'
BACKGROUND_RED = '\033[41m'
BACKGROUND_GREEN = '\033[42m'
BACKGROUND_YELLOW = '\033[43m'
BACKGROUND_BLUE = '\033[44m'
BACKGROUND_MAGENTA = '\033[45m'
BACKGROUND_CYAN = '\033[46m'
BACKGROUND_LIGHT_GRAY = '\033[47m'
BACKGROUND_DARK_GRAY = '\033[100m'
BACKGROUND_LIGHT_RED = '\033[101m'
BACKGROUND_LIGHT_GREEN = '\033[102m'
BACKGROUND_LIGHT_YELLOW = '\033[103m'
BACKGROUND_LIGHT_BLUE = '\033[104m'
BACKGROUND_LIGHT_MAGENTA = '\033[105m'
BACKGROUND_LIGHT_CYAN = '\033[106m'
BACKGROUND_WHITE = '\033[107m'

BOLD_RED = '\033[1;31m'
BOLD_GREEN = '\033[1;32m'
BOLD_YELLOW = '\033[1;33m'
BOLD_BLUE = '\033[1;34m'
BOLD_MAGENTA = '\033[1;35m'
BOLD_CYAN = '\033[1;36m'



def CLS():
    ''' Clear the console window. '''
    print('\033[2J\033[;H', end = '')



def CursorDown(nLines):
    ''' Move the cursor down the specified number of lines. '''
    print('\033[{}B'.format(nLines), end = '\r')



def CursorUp(nLines):
    ''' Move the cursor up the specified number of lines. '''
    print('\033[{}A'.format(nLines), end = '\r')
