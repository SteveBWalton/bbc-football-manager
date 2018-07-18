#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to provide the BBC Basic function INKEY.
Scan for a keyboard button press but do not block if no key is available.
Under Windows.
    This works under winpty ( but colours do not work in winpty).
    This does not work under minitty.
'''

import sys
import _thread
import time


try:
    # Try to import Windows version.
    # print('Try to import Windows version')
    # import msvcrt
    from msvcrt import getwch # , kbhit
    # print('Using Windows getwch().')
    UseLinux = False
except ImportError:
    # Define non-Windows version.
    # print('Using Linux getwch().')
    UseLinux = True
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



class CInkey:
    ''' Class to provide a keyboard scan function like BBC Basic InKey(). '''



    def __init__(self):
        ''' Class constructor. '''
        # print('CInKey class constructor.')
        self.sLastKey = None
        if UseLinux:
            fd = sys.stdin.fileno()
            self.old_settings = termios.tcgetattr(fd)
        # print('CInKey class constructor finished.')


    def __del__(self):
        ''' Class destructor. '''
        # print('CInKey class destructor.')
        self.Stop()



    def Start(self):
        ''' Start the keyboard monitoring.  This was in the class constructor initially. '''
        # print('_thread.start_new_thread.')
        _thread.start_new_thread(self._keypress, ())



    def Stop(self):
        ''' Restore the terminal. Sometimes there is an extra setcbreak() call.  So call here at the end to restore the ECHO after this setcbreak() call.'''
        # print('Close')
        if UseLinux:
            self.old_settings[3] = self.old_settings[3] | termios.ECHO
            fd = sys.stdin.fileno()
            termios.tcsetattr(fd, termios.TCSADRAIN, self.old_settings)
            # Use 'stty --all' to see all terminal settings.
            # Use 'stty echo' to turn echo back on (for example).



    def _keypress(self):
        ''' Fetch the last character into a buffer. '''
        # print('_keypress().start')
        # if msvcrt.kbhit():
        # print('_keypress().start')
        # This does not work under minitty.
        # print ('_keypress.getwch()')
        self.sLastKey = getwch()
        # print('_keypress().finish')



    def InKey(self, bContinue=True):
        ''' Return the last (current) keypress or None for no keypress. '''
        if self.sLastKey == None:
            sReturn = None
            # print('No Key pressed.')
        else:
            sReturn = self.sLastKey
            # print('"{}" key pressed.'.format(sReturn))
            self.sLastKey = None
            if bContinue:
                # Scan for the next key.
                _thread.start_new_thread(self._keypress, ())
            else:
                self.Stop()
        return sReturn



def main():
    # print('Hello from modInKey.py')
    oInKey = CInKey()
    # print('CInkey object created.')
    nWait = 10000
    while nWait > 0:
        sCharacter = oInKey.InKey()
        if sCharacter == None:
            pass
            print('No Key pressed.')
        else:
            print('"{}" key pressed.'.format(sCharacter))
            if sCharacter == 'q' or sCharacter == '\x1b':  # x1b is ESC
                break
                nWait = 10
        time.sleep(1)
        nWait = nWait - 1

    time.sleep(1)
    time.sleep(1)
    time.sleep(1)
    time.sleep(1)
    time.sleep(1)
    oInKey.Close()



if __name__ == "__main__":
    print('Press \'q\' to finish.')
    main()
    print('Program finished')
