#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to implement the CPlayer class for the the BBC Football Manager program.
'''

# System libraries.
import json

# Application Libraries.
import modANSI


DEFENSE = 0
MIDFIELD = 1
ATTACK = 2


class CPlayer:
    ''' Class to represent a player in the BBC Football Manager game. '''



    def __init__(self):
        ''' Class constructor. '''
        self.name = 'Error'
        self.skill = 1
        self.energy = 10
        self.position = DEFENSE
        self.index = 0
        self.in_squad = False
        self.in_team = False
        self.injured = False
        self.caps = 0
        self.goals = 0



    def GetPlayer(self, nIndex):
        ''' Populate the object with a prebuilt player. '''
        self.index = nIndex
        if nIndex <= 10:
            self.position = DEFENSE
        elif nIndex <= 20:
            self.position = MIDFIELD
        else:
            self.position = ATTACK

        if nIndex == 1:
            self.name = 'C Woods'
        elif nIndex == 2:
            self.name = 'P Shilton'
        elif nIndex == 3:
            self.name = 'A Hansen'
        elif nIndex == 4:
            self.name = 'P Neal'
        elif nIndex == 5:
            self.name = 'T Butcher'
        elif nIndex == 6:
            self.name = 'K Moran'
        elif nIndex == 7:
            self.name = 'M Lawrenson'
        elif nIndex == 8:
            self.name = 'T Adams'
        elif nIndex == 9:
            self.name = 'M Duxbury'
        elif nIndex == 10:
            self.name = 'G Stevens'
        elif nIndex == 11:
            self.name = 'B Robson'
        elif nIndex == 12:
            self.name = 'G Hoddle'
        elif nIndex == 13:
            self.name = 'S Hodge'
        elif nIndex == 14:
            self.name = 'C Johnston'
        elif nIndex == 15:
            self.name = 'R Wilkins'
        elif nIndex == 16:
            self.name = 'K Dalglish'
        elif nIndex == 17:
            self.name = 'J Barnes'
        elif nIndex == 18:
            self.name = 'G Souness'
        elif nIndex == 19:
            self.name = 'N Webb'
        elif nIndex == 20:
            self.name = 'T Morley'
        elif nIndex == 21:
            self.name = 'M Hughes'
        elif nIndex == 22:
            self.name = 'M Hateley'
        elif nIndex == 23:
            self.name = 'P Beardsley'
        elif nIndex == 24:
            self.name = 'I Rush'
        elif nIndex == 25:
            self.name = 'G Lineker'
        elif nIndex == 26:
            self.name = 'N Whiteside'



    def WriteRow(self, nExchangeRate=0):
        ''' Display this player on a row. '''
        if self.position == DEFENSE:
            print(modANSI.BACKGROUND_LIGHT_BLUE, end = '')
            print(modANSI.LIGHT_YELLOW, end = '')
        elif self.position == MIDFIELD:
            print(modANSI.BACKGROUND_LIGHT_YELLOW, end = '')
            print(modANSI.BLUE, end = '')
        else:
            print(modANSI.BACKGROUND_WHITE, end = '')
            print(modANSI.BLUE, end = '')
        print('{:2} {:<20}{:>2}{:>3} '.format(self.index, self.name, self.skill, self.energy), end = '')
        if nExchangeRate != 0:
            print('{:>12s}'.format('£{:,.2f}'.format(self.skill * nExchangeRate)), end = '')
        if self.in_team:
            print(modANSI.BACKGROUND_GREEN, end = '')
            print(modANSI.LIGHT_YELLOW, end = '')
            print(' P ', end = '')
        if self.injured:
            print(modANSI.BACKGROUND_RED, end = '')
            print(modANSI.LIGHT_YELLOW, end = '')
            print(' I ', end = '')
        print(modANSI.RESET_ALL)



    def GetPosition(self):
        ''' Returns the position of the player as a string. '''
        if self.position == DEFENSE:
            return 'Defense'
        if self.position == MIDFIELD:
            return 'Mid-field'
        return 'Attack'



    def Dump(self, oFile):
        ''' Write the player into the specified file. '''
        json.dump(self.name, oFile)
        oFile.write('\n')
        json.dump(self.skill, oFile)
        oFile.write('\n')
        json.dump(self.energy, oFile)
        oFile.write('\n')
        json.dump(self.position, oFile)
        oFile.write('\n')
        json.dump(self.index, oFile)
        oFile.write('\n')
        json.dump(self.in_squad, oFile)
        oFile.write('\n')
        json.dump(self.in_team, oFile)
        oFile.write('\n')
        json.dump(self.injured, oFile)
        oFile.write('\n')
        json.dump(self.caps, oFile)
        oFile.write('\n')
        json.dump(self.goals, oFile)
        oFile.write('\n')



    def Load(self, oFile):
        ''' Read the player from the specified file. '''
        sLine = oFile.readline()
        self.name = json.loads(sLine)
        sLine = oFile.readline()
        self.skill = json.loads(sLine)
        sLine = oFile.readline()
        self.energy = json.loads(sLine)
        sLine = oFile.readline()
        self.position = json.loads(sLine)
        sLine = oFile.readline()
        self.index = json.loads(sLine)
        sLine = oFile.readline()
        self.in_squad = json.loads(sLine)
        sLine = oFile.readline()
        self.in_team = json.loads(sLine)
        sLine = oFile.readline()
        self.injured = json.loads(sLine)
        sLine = oFile.readline()
        self.caps = json.loads(sLine)
        sLine = oFile.readline()
        self.goals = json.loads(sLine)
