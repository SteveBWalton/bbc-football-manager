#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to provide the BBC Basic function INKEY.
Scan for a keyboard button press but do not block if no key is available.
Under Windows.
    This works under winpty ( but colours do not work in winpty).
    This does not work under minitty.
'''

# System Libraries.
import sys
import threading
import time


# Define a getwch() function.
# Either by importing from msvcrt (windows)
# or by implementation (linux).
try:
    # Try to import Windows version.
    # print('Try to import Windows version')
    # import msvcrt
    from msvcrt import getwch # , kbhit
    # print('Using Windows getwch().')
    isLinux = False
except ImportError:
    # Define non-Windows version.
    # print('Using Linux getwch().')
    isLinux = True
    import tty
    import termios
    def getwch():
        try:
            # This does not work !
            # print('SetRaw')
            # tty.setraw(sys.stdin.fileno())

            # print('\nSetCBreak\n')
            tty.setcbreak(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        except:
            pass
        finally:
            pass
        return ch



class InKey:
    ''' Class to provide a keyboard scan function like BBC Basic InKey(). '''



    def __init__(self):
        ''' Class constructor. '''
        # print('CInKey class constructor.')
        self.lastKey = None
        if isLinux:
            fd = sys.stdin.fileno()
            self.oldSettings = termios.tcgetattr(fd)
        # print('CInKey class constructor finished.')


    def __del__(self):
        ''' Class destructor. '''
        # print('CInKey class destructor.')
        self.stop()



    def start(self):
        ''' Start the keyboard monitoring.  This was in the class constructor initially. '''
        thread = threading.Thread(target=self._keypress, args=())
        thread.start()



    def stop(self):
        ''' Restore the terminal. Sometimes there is an extra setcbreak() call.  So call here at the end to restore the ECHO after this setcbreak() call.'''
        # print('Close')
        if isLinux:
            self.oldSettings[3] = self.oldSettings[3] | termios.ECHO
            fd = sys.stdin.fileno()
            termios.tcsetattr(fd, termios.TCSADRAIN, self.oldSettings)
            # Use 'stty --all' to see all terminal settings.
            # Use 'stty echo' to turn echo back on (for example).



    def _keypress(self):
        ''' Fetch the last character into a buffer. '''
        # print('_keypress().start')
        # if msvcrt.kbhit():
        # print('_keypress().start')
        # This does not work under minitty.
        # print ('_keypress.getwch()')
        self.lastKey = getwch()
        # print('_keypress().finish')



    def inKey(self, isContinue=True):
        ''' Return the last (current) keypress or None for no keypress. '''
        if self.lastKey == None:
            result = None
            # print('No Key pressed.')
        else:
            result = self.lastKey
            # print('"{}" key pressed.'.format(result))
            self.lastKey = None
            if isContinue:
                # Scan for the next key.
                thread = threading.Thread(target=self._keypress, args=())
                thread.start()

            else:
                self.stop()
        return result



    def getKey(self):
        ''' Get a key from the keyboard.  This function will block until a key is pressed. This does not need a start() but it does require a stop() to restore the echo. '''
        return getwch()



def main():
    inKey = InKey()
    inKey.start()
    wait = 10000
    while wait > 0:
        character = inKey.inKey()
        if character == None:
            pass
            print('No Key pressed.')
        else:
            print('"{}" key pressed.'.format(character))
            if character == 'q' or character == '\x1b':  # x1b is ESC
                break
                wait = 10
        time.sleep(1)
        wait -= 1

    time.sleep(1)
    time.sleep(1)
    time.sleep(1)
    time.sleep(1)
    time.sleep(1)
    inKey.stop()



if __name__ == "__main__":
    print('Press \'q\' to finish.')
    main()
    print('Program finished')
