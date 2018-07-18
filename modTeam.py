#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to implement the CTeam class for the the BBC Football Manager program.
'''

# System libraries.

# Application Libraries.
import modANSI
import modInkey

class CTeam:
    ''' Class to represent a team in the BBC Football Manager game. '''



    def __init__(self):
        ''' Class constructor. '''
        self.name = 'Error'
        self.colour = modANSI.WHITE
        self.defense = 1
        self.midfield = 1
        self.attack = 1
        self.position = 1



    def WriteTableRow(self):
        ''' Write this team into the league table. '''
        print('{:>2} {}{:<15}{:>3}{:>3}{:>3}{:>3}{:>3}{}'.format(self.position, self.colour, self.name, 0, 0, 0, 0, 0, modANSI.RESET_ALL))


    def GetColouredName(self):
        ''' Returns the team name wrapped in the colour code. '''
        return '{}{}{}'.format(self.colour, self.name, modANSI.RESET_ALL)



    def GetTeam(self, nDivision, nIndex):
        ''' This is the replacement for FNGETTEAM(). Populate the object with a prebuilt team. '''
        if nDivision == 1:
            if nIndex == 1:
                self.name = 'Leeds United'
                self.colour = modANSI.YELLOW
            elif nIndex == 2:
                self.name = 'Man United'
                self.colour = modANSI.RED
            elif nIndex == 3:
                self.name = 'Liverpool'
                self.colour = modANSI.RED
            elif nIndex == 4:
                self.name = 'Arsenal'
                self.colour = modANSI.RED
            elif nIndex == 5:
                self.name = 'Spurs'
                self.colour = modANSI.WHITE
            elif nIndex == 5:
                self.name = 'Newcastle'
                self.colour = modANSI.WHITE
        elif nDivision == 2:
            if nIndex == 1:
                self.name = 'Man City'
                self.colour = modANSI.CYAN
            elif nIndex == 2:
                self.name = 'Chelsea'
                self.colour = modANSI.LIGHT_BLUE
            elif nIndex == 3:
                self.name = 'West Ham'
                self.colour = modANSI.MAGENTA
            elif nIndex == 4:
                self.name = 'Southampton'
                self.colour = modANSI.RED
            elif nIndex == 5:
                self.name = 'Sheffield United'
                self.colour = modANSI.RED
        elif nDivision == 3:
            if nIndex == 1:
                self.name = 'Sheffield United'
                self.colour = modANSI.RED
        else:
            if nIndex == 1:
                self.name = 'Wigan'
                self.colour = modANSI.RED
            elif nIndex == 2:
                self.name = 'Bradford City'
                self.colour = modANSI.LIGHT_BLUE
            elif nIndex == 3:
                self.name = 'Wimbledon'
                self.colour = modANSI.MAGENTA
            elif nIndex == 4:
                self.name = 'York City'
                self.colour = modANSI.RED
            elif nIndex == 5:
                self.name = 'Peterbrough'
                self.colour = modANSI.RED

