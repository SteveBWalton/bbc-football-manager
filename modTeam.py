#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to implement the CTeam class for the the BBC Football Manager program.
'''

# System libraries.
import random

# Application Libraries.
import modANSI
import modInkey
import modGame

class CTeam:
    ''' Class to represent a team in the BBC Football Manager game. '''



    def __init__(self):
        ''' Class constructor. '''
        self.name = 'Error'
        self.colour = modANSI.WHITE
        self.energy = 1
        self.moral = 1
        self.defence = 1
        self.midfield = 1
        self.attack = 1
        self.position = 1
        self.pts = 0
        self.difference = 0
        self.played_home = False
        self.played_away = False
        self.sort = 0
        self.formation = '4-4-2'



    def Initialise(self, nDivision):
        ''' Replacement for FNTEAM (Line 3750) in the BBC Basic version. '''
        nNumDefence = 3 + random.randint(1, 2)
        nNumMidfield = 2 + random.randint(1, 3)
        nNumAttack = 11 - nNumMidfield - nNumDefence
        nBonus = 1 + (1 if nDivision < 4 else 0) + (1 if nDivision == 1 else 0)
        nSkill = 4 - (nDivision & 1)
        self.energy = self.MultiRandomInt(20, 11)
        self.moral = 9 + random.randint(1, 11)
        self.defence = nNumDefence * nBonus + self.MultiRandomInt(nSkill, nNumDefence)
        self.midfield = nNumMidfield * nBonus + self.MultiRandomInt(nSkill, nNumMidfield)
        self.attack = nNumAttack * nBonus + self.MultiRandomInt(nSkill, nNumAttack)
        self.formation = '{}-{}-{}'.format(nNumDefence-1, nNumMidfield, nNumAttack)



    def Zero(self):
        ''' Initialise the team properties to zero. '''
        self.energy = 0
        self.moral = 10
        self.defence = 0
        self.midfield = 0
        self.attack = 0
        self.formation = '0-0-0'



    def WriteTableRow(self):
        ''' Write this team into the league table. '''
        print('{:>2} {}{:<15}{:>3}{:>3}{:>3}{:>4}{:>4} {} {} {}'.format(self.position, self.colour, self.name, 0, 0, 0, self.pts, self.difference, 'Y' if self.played_home else 'N', 'Y' if self.played_away else 'N', modANSI.RESET_ALL))



    def GetColouredName(self):
        ''' Returns the team name wrapped in the colour code. '''
        return '{}{}{}'.format(self.colour, self.name, modANSI.RESET_ALL)



    def GetTeam(self, nDivision, nIndex):
        ''' This is the replacement for FNGETTEAM(). Populate the object with a prebuilt team. '''
        if nDivision == 1:
            if nIndex == 1:
                self.name = 'Liverpool'
                self.colour = modANSI.RED
            elif nIndex == 2:
                self.name = 'Man United'
                self.colour = modANSI.RED
            elif nIndex == 3:
                self.name = 'Leeds United'
                self.colour = modANSI.YELLOW
            elif nIndex == 4:
                self.name = 'Arsenal'
                self.colour = modANSI.RED
            elif nIndex == 5:
                self.name = 'Spurs'
                self.colour = modANSI.WHITE
            elif nIndex == 6:
                self.name = 'Aston Villa'
                self.colour = modANSI.MAGENTA
            elif nIndex == 7:
                self.name = 'Everton'
                self.colour = modANSI.LIGHT_BLUE
            elif nIndex == 8:
                self.name = 'Nottm Forest'
                self.colour = modANSI.RED
            elif nIndex == 9:
                self.name = 'Millwall'
                self.colour = modANSI.WHITE
            elif nIndex == 10:
                self.name = 'Coventry'
                self.colour = modANSI.CYAN
            elif nIndex == 11:
                self.name = 'West Ham'
                self.colour = modANSI.MAGENTA
            elif nIndex == 12:
                self.name = 'Norwich'
                self.colour = modANSI.YELLOW
            elif nIndex == 13:
                self.name = 'Sheff Wed'
                self.colour = modANSI.YELLOW
            elif nIndex == 14:
                self.name = 'Derby'
                self.colour = modANSI.WHITE
            elif nIndex == 15:
                self.name = 'Chelsea'
                self.colour = modANSI.LIGHT_BLUE
            elif nIndex == 16:
                self.name = 'Newcastle'
                self.colour = modANSI.WHITE
        elif nDivision == 2:
            if nIndex == 1:
                self.name = 'Watford'
                self.colour = modANSI.YELLOW
            elif nIndex == 2:
                self.name = 'Stoke City'
                self.colour = modANSI.RED
            elif nIndex == 3:
                self.name = 'Brighton'
                self.colour = modANSI.LIGHT_BLUE
            elif nIndex == 4:
                self.name = 'Barnsley'
                self.colour = modANSI.RED
            elif nIndex == 5:
                self.name = 'Plymouth'
                self.colour = modANSI.LIGHT_BLUE
            elif nIndex == 6:
                self.name = 'Hull City'
                self.colour = modANSI.MAGENTA
            elif nIndex == 7:
                self.name = 'Notts Co'
                self.colour = modANSI.WHITE
            elif nIndex == 8:
                self.name = 'Man City'
                self.colour = modANSI.CYAN
            elif nIndex == 9:
                self.name = 'Shrewsbury'
                self.colour = modANSI.RED
            elif nIndex == 10:
                self.name = 'Burnley'
                self.colour = modANSI.MAGENTA
            elif nIndex == 11:
                self.name = 'Charlton'
                self.colour = modANSI.RED
            elif nIndex == 12:
                self.name = 'Sunderland'
                self.colour = modANSI.RED
            elif nIndex == 13:
                self.name = 'Bradford'
                self.colour = modANSI.RED
            elif nIndex == 14:
                self.name = 'Bury'
                self.colour = modANSI.LIGHT_BLUE
            elif nIndex == 15:
                self.name = 'Sheff United'
                self.colour = modANSI.RED
            elif nIndex == 16:
                self.name = 'Huddersfield'
                self.colour = modANSI.LIGHT_BLUE
        elif nDivision == 3:
            if nIndex == 1:
                self.name = 'Wolves'
                self.colour = modANSI.YELLOW
            elif nIndex == 2:
                self.name = 'Oxford'
                self.colour = modANSI.RED
            elif nIndex == 3:
                self.name = 'Swindon'
                self.colour = modANSI.RED
            elif nIndex == 4:
                self.name = 'Walsall'
                self.colour = modANSI.RED
            elif nIndex == 5:
                self.name = 'Newport'
                self.colour = modANSI.GREEN
            elif nIndex == 6:
                self.name = 'Wigan'
                self.colour = modANSI.RED
            elif nIndex == 7:
                self.name = 'Wimbledon'
                self.colour = modANSI.RED
            elif nIndex == 8:
                self.name = 'Mansfield'
                self.colour = modANSI.GREEN
            elif nIndex == 9:
                self.name = 'Southend'
                self.colour = modANSI.RED
            elif nIndex == 10:
                self.name = 'Grimsby'
                self.colour = modANSI.GREEN
            elif nIndex == 11:
                self.name = 'Blackburn'
                self.colour = modANSI.MAGENTA
            elif nIndex == 12:
                self.name = 'Reading'
                self.colour = modANSI.RED
            elif nIndex == 13:
                self.name = 'Crewe'
                self.colour = modANSI.YELLOW
            elif nIndex == 14:
                self.name = 'Darlington'
                self.colour = modANSI.RED
            elif nIndex == 15:
                self.name = 'Port Value'
                self.colour = modANSI.LIGHT_BLUE
            elif nIndex == 16:
                self.name = 'Stockport'
                self.colour = modANSI.RED
        else:
            if nIndex == 1:
                self.name = 'Scunthorpe'
                self.colour = modANSI.RED
            elif nIndex == 2:
                self.name = 'York'
                self.colour = modANSI.GREEN
            elif nIndex == 3:
                self.name = 'Bournemouth'
                self.colour = modANSI.LIGHT_BLUE
            elif nIndex == 4:
                self.name = 'Doncaster'
                self.colour = modANSI.CYAN
            elif nIndex == 5:
                self.name = 'Lincoln'
                self.colour = modANSI.MAGENTA
            elif nIndex == 6:
                self.name = 'Rochdale'
                self.colour = modANSI.RED
            elif nIndex == 7:
                self.name = 'Hereford'
                self.colour = modANSI.YELLOW
            elif nIndex == 8:
                self.name = 'Hartlepool'
                self.colour = modANSI.LIGHT_BLUE
            elif nIndex == 9:
                self.name = 'Halifax'
                self.colour = modANSI.RED
            elif nIndex == 10:
                self.name = 'Tranmere'
                self.colour = modANSI.RED
            elif nIndex == 11:
                self.name = 'Aldershot'
                self.colour = modANSI.YELLOW
            elif nIndex == 12:
                self.name = 'Bristol'
                self.colour = modANSI.LIGHT_BLUE
            elif nIndex == 13:
                self.name = 'Wrexham'
                self.colour = modANSI.RED
            elif nIndex == 14:
                self.name = 'Torquay'
                self.colour = modANSI.GREEN
            elif nIndex == 15:
                self.name = 'Gillingham'
                self.colour = modANSI.GREEN
            elif nIndex == 16:
                self.name = 'Exeter'
                self.colour = modANSI.RED



    def MultiRandomInt(self, nRange, nNumber):
        ''' Replacement for FNRND() (Line 6640) in the BBC Basic version. '''
        nTotal = 0
        for nCount in range(nNumber):
            nTotal = nTotal + random.randint(1, nRange)
        return nTotal
