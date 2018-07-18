#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to implement the CGame class for the the BBC Football Manager program.
'''

# System libraries.

# Application Libraries.
import modANSI
import modInkey
import modTeam



class CGame:
    ''' Class to represent the BBC Football Manager game. '''



    def __init__(self):
        ''' Class constructor for the BBC Football manager game. '''
        self.player_name = ''
        self.level = 1
        self.team_name = ''
        self.team_colour = modANSI.WHITE


    def Run(self):
        ''' Execute the football manager game. '''
        self.keyboard = modInkey.CInkey()

        modANSI.CLS()
        self.Football()

        # Get the player settings.
        print()
        self.player_name = input('Please enter your name: ')

        # Select the level.
        print('Enter level [1-4]')
        self.level = int(self.GetKeyboardCharacter(['1', '2', '3', '4']))
        print('Level {} was selected'.format(self.level))

        # Load a game.
        print('Do you want to load a game?')
        if self.YesNo():
            print('Yes')
        else:
            print('No')
            self.NewGame()



    def NewGame(self):
        ''' Initialise a new game. '''
        self.PickTeam()



    def PickTeam(self):
        ''' Replacement for PROCPICKTEAM in the BBC Basic version. '''
        nDivision = 1
        while True:
            modANSI.CLS()
            print(' 0 More Teams')
            print(' 1 Own Team')
            for nIndex in range(2, 17):
                oTeam = modTeam.CTeam()
                oTeam.GetTeam(nDivision, nIndex - 1)
                print('{:2} {}'.format(nIndex, oTeam.GetColouredName()))
            nNumber = self.EnterNumber('Enter Team Number ')
            if nNumber >= 2 and nNumber <= 17:
                oTeam.GetTeam(nDivision, nNumber - 1)
                self.team_name = oTeam.name
                self.team_colour = oTeam.colour
                break;
            if nNumber == 1:
                self.team_name = input('Enter Team name ')
                self.team_colour = modANSI.CYAN
                break;
            nDivision = 1 + (nDivision & 3)
        print('You manage {}{}{}'.format(self.team_colour, self.team_name, modANSI.RESET_ALL))



    def EnterNumber(self, sMessage):
        ''' Enter a number at the keyboard. '''
        nNumber = 0
        try:
            nNumber = int(input(sMessage))
        except:
            nNumber = 0
        return nNumber



    def YesNo(self):
        ''' Replacement for FNYES in the BBC Basic version.  Returns True if 'Y' is pressed or False if 'N' is pressed. '''
        sCharacter = self.GetKeyboardCharacter(['y', 'n'])
        if sCharacter == 'y':
            return True
        return False



    def GetKeyboardCharacter(self, allowed):
        ''' Return a keyboard character from the allowed characters. '''
        # No Repeat Until in Python.
        sCharacter = modInkey.getwch()
        while not (sCharacter in allowed):
            sCharacter = modInkey.getwch()
        self.keyboard.Stop()
        return sCharacter



    def Football(self):
        ''' Implementation of DEFPROCfootball().  Display a title. '''
        print('┏━━             ┃       ┃ ┃   ┏━┳━┓')
        print('┃            ┃  ┃       ┃ ┃   ┃ ┃ ┃' )
        print('┣━━ ┏━┓ ┏━┓ ━#━ ┣━┓ ━━┓ ┃ ┃   ┃   ┃ ━━┓ ━┳━┓ ━━┓ ┏━┓ ┏━┓ ┏━')
        print('┃   ┃ ┃ ┃ ┃  ┃  ┃ ┃ ┏━┫ ┃ ┃   ┃   ┃ ┏━┃  ┃ ┃ ┏━┫ ┃ ┃ ┣━┛ ┃')
        print('┃   ┗━┛ ┗━┛  ┃  ┗#┛ ┗━┛ ┃ ┃   ┃   ┃ ┗━┛  ┃ ┃ ┗━┛ ┗━┫ ┗━━ ┃')
        print('                                                   ┃')
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')
        print('By Steve Walton BBC BASIC 1982-1989, 2000, Python 2018.')


