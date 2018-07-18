#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to implement the CPlayer class for the the BBC Football Manager program.
'''

# System libraries.

# Application Libraries.
import modANSI


DEFENSE = 1
MIDFIELD = 2
ATTACK = 3


class CPlayer:
    ''' Class to represent a player in the BBC Football Manager game. '''



    def __init__(self):
        ''' Class constructor. '''
        self.name = 'Error'
        self.skill = 1
        self.engergy = 10
        self.position = DEFENSE
        self.index = 0
        self.in_squad = False
        self.in_team = False



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
            self.name = 'Peter Shilton'
        elif nIndex == 2:
            self.name = 'Gary Bailey'
        elif nIndex == 25:
            self.name = 'Mark Hughes'
        elif nIndex == 26:
            self.name = 'Gary Lineker'



    def WriteRow(self):
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
        print('{:2} {:<20}{:>2}{:>3}'.format(self.index, self.name, self.skill, self.energy), end = '')
        print(modANSI.RESET_ALL)


