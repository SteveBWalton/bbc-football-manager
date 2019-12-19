#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to implement the CTeam class for the the BBC Football Manager program.
'''

# System libraries.
import random
import json

# Application Libraries.
import ansi
import modInkey
import modGame

class CTeam:
    ''' Class to represent a team in the BBC Football Manager game. '''



    def __init__(self):
        ''' Class constructor. '''
        self.name = 'Error'
        self.colour = ansi.WHITE
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
        self.formation = '4-4-2'
        self.fixture = 0
        self.win = 0
        self.draw = 0
        self.lost = 0



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

        self.pts = 0
        self.difference = 0
        self.played_home = False
        self.played_away = False
        self.win = 0
        self.draw = 0
        self.lost = 0


    def Zero(self):
        ''' Initialise the team properties to zero. '''
        self.energy = 0
        self.moral = 10
        self.defence = 0
        self.midfield = 0
        self.attack = 0
        self.formation = '0-0-0'

        self.pts = 0
        self.difference = 0
        self.played_home = False
        self.played_away = False
        self.win = 0
        self.draw = 0
        self.lost = 0




    def WriteTableRow(self):
        ''' Write this team into the league table. '''
        # print('{:>2} {}{:<15}{:>3}{:>3}{:>3}{:>4}{:>4} {} {} {}'.format(self.position, self.colour, self.name, self.win, self.draw, self.lost, self.pts, self.difference, 'Y' if self.played_home else 'N', 'Y' if self.played_away else 'N', ansi.RESET_ALL))
        print('{:>2} {}{:<15}{:>3}{:>3}{:>3}{:>4}{:>4}{}'.format(self.position, self.colour, self.name, self.win, self.draw, self.lost, self.pts, self.difference, ansi.RESET_ALL))



    def GetColouredName(self):
        ''' Returns the team name wrapped in the colour code. '''
        return '{}{}{}'.format(self.colour, self.name, ansi.RESET_ALL)



    def GetTeam(self, nDivision, nIndex):
        ''' This is the replacement for FNGETTEAM(). Populate the object with a prebuilt team. '''
        if nDivision == 1:
            if nIndex == 1:
                self.name = 'Liverpool'
                self.colour = ansi.RED
            elif nIndex == 2:
                self.name = 'Man United'
                self.colour = ansi.RED
            elif nIndex == 3:
                self.name = 'Leeds United'
                self.colour = ansi.YELLOW
            elif nIndex == 4:
                self.name = 'Arsenal'
                self.colour = ansi.RED
            elif nIndex == 5:
                self.name = 'Spurs'
                self.colour = ansi.WHITE
            elif nIndex == 6:
                self.name = 'Aston Villa'
                self.colour = ansi.MAGENTA
            elif nIndex == 7:
                self.name = 'Everton'
                self.colour = ansi.LIGHT_BLUE
            elif nIndex == 8:
                self.name = 'Nottm Forest'
                self.colour = ansi.RED
            elif nIndex == 9:
                self.name = 'Millwall'
                self.colour = ansi.WHITE
            elif nIndex == 10:
                self.name = 'Coventry'
                self.colour = ansi.CYAN
            elif nIndex == 11:
                self.name = 'West Ham'
                self.colour = ansi.MAGENTA
            elif nIndex == 12:
                self.name = 'Norwich'
                self.colour = ansi.YELLOW
            elif nIndex == 13:
                self.name = 'Sheff Wed'
                self.colour = ansi.YELLOW
            elif nIndex == 14:
                self.name = 'Derby'
                self.colour = ansi.WHITE
            elif nIndex == 15:
                self.name = 'Chelsea'
                self.colour = ansi.LIGHT_BLUE
            elif nIndex == 16:
                self.name = 'Newcastle'
                self.colour = ansi.WHITE
            else:
                self.GetTeam(nDivision+1, nIndex-16)
        elif nDivision == 2:
            if nIndex == 1:
                self.name = 'Watford'
                self.colour = ansi.YELLOW
            elif nIndex == 2:
                self.name = 'Stoke City'
                self.colour = ansi.RED
            elif nIndex == 3:
                self.name = 'Brighton'
                self.colour = ansi.LIGHT_BLUE
            elif nIndex == 4:
                self.name = 'Barnsley'
                self.colour = ansi.RED
            elif nIndex == 5:
                self.name = 'Plymouth'
                self.colour = ansi.LIGHT_BLUE
            elif nIndex == 6:
                self.name = 'Hull City'
                self.colour = ansi.MAGENTA
            elif nIndex == 7:
                self.name = 'Notts Co'
                self.colour = ansi.WHITE
            elif nIndex == 8:
                self.name = 'Man City'
                self.colour = ansi.CYAN
            elif nIndex == 9:
                self.name = 'Shrewsbury'
                self.colour = ansi.RED
            elif nIndex == 10:
                self.name = 'Burnley'
                self.colour = ansi.MAGENTA
            elif nIndex == 11:
                self.name = 'Charlton'
                self.colour = ansi.RED
            elif nIndex == 12:
                self.name = 'Sunderland'
                self.colour = ansi.RED
            elif nIndex == 13:
                self.name = 'Bradford'
                self.colour = ansi.RED
            elif nIndex == 14:
                self.name = 'Bury'
                self.colour = ansi.LIGHT_BLUE
            elif nIndex == 15:
                self.name = 'Sheff United'
                self.colour = ansi.RED
            elif nIndex == 16:
                self.name = 'Huddersfield'
                self.colour = ansi.LIGHT_BLUE
            else:
                self.GetTeam(nDivision+1, nIndex-16)
        elif nDivision == 3:
            if nIndex == 1:
                self.name = 'Wolves'
                self.colour = ansi.YELLOW
            elif nIndex == 2:
                self.name = 'Oxford'
                self.colour = ansi.RED
            elif nIndex == 3:
                self.name = 'Swindon'
                self.colour = ansi.RED
            elif nIndex == 4:
                self.name = 'Walsall'
                self.colour = ansi.RED
            elif nIndex == 5:
                self.name = 'Newport'
                self.colour = ansi.GREEN
            elif nIndex == 6:
                self.name = 'Wigan'
                self.colour = ansi.RED
            elif nIndex == 7:
                self.name = 'Wimbledon'
                self.colour = ansi.RED
            elif nIndex == 8:
                self.name = 'Mansfield'
                self.colour = ansi.GREEN
            elif nIndex == 9:
                self.name = 'Southend'
                self.colour = ansi.RED
            elif nIndex == 10:
                self.name = 'Grimsby'
                self.colour = ansi.GREEN
            elif nIndex == 11:
                self.name = 'Blackburn'
                self.colour = ansi.MAGENTA
            elif nIndex == 12:
                self.name = 'Reading'
                self.colour = ansi.RED
            elif nIndex == 13:
                self.name = 'Crewe'
                self.colour = ansi.YELLOW
            elif nIndex == 14:
                self.name = 'Darlington'
                self.colour = ansi.RED
            elif nIndex == 15:
                self.name = 'Port Value'
                self.colour = ansi.LIGHT_BLUE
            elif nIndex == 16:
                self.name = 'Stockport'
                self.colour = ansi.RED
            else:
                self.GetTeam(nDivision+1, nIndex-16)
        else:
            if nIndex == 1:
                self.name = 'Scunthorpe'
                self.colour = ansi.RED
            elif nIndex == 2:
                self.name = 'York'
                self.colour = ansi.GREEN
            elif nIndex == 3:
                self.name = 'Bournemouth'
                self.colour = ansi.LIGHT_BLUE
            elif nIndex == 4:
                self.name = 'Doncaster'
                self.colour = ansi.CYAN
            elif nIndex == 5:
                self.name = 'Lincoln'
                self.colour = ansi.MAGENTA
            elif nIndex == 6:
                self.name = 'Rochdale'
                self.colour = ansi.RED
            elif nIndex == 7:
                self.name = 'Hereford'
                self.colour = ansi.YELLOW
            elif nIndex == 8:
                self.name = 'Hartlepool'
                self.colour = ansi.LIGHT_BLUE
            elif nIndex == 9:
                self.name = 'Halifax'
                self.colour = ansi.RED
            elif nIndex == 10:
                self.name = 'Tranmere'
                self.colour = ansi.RED
            elif nIndex == 11:
                self.name = 'Aldershot'
                self.colour = ansi.YELLOW
            elif nIndex == 12:
                self.name = 'Bristol'
                self.colour = ansi.LIGHT_BLUE
            elif nIndex == 13:
                self.name = 'Wrexham'
                self.colour = ansi.RED
            elif nIndex == 14:
                self.name = 'Torquay'
                self.colour = ansi.GREEN
            elif nIndex == 15:
                self.name = 'Gillingham'
                self.colour = ansi.GREEN
            elif nIndex == 16:
                self.name = 'Exeter'
                self.colour = ansi.RED
            else:
                self.GetTeam(nDivision-1, nIndex-16)



    def MultiRandomInt(self, nRange, nNumber):
        ''' Replacement for FNRND() (Line 6640) in the BBC Basic version. '''
        nTotal = 0
        for nCount in range(nNumber):
            nTotal = nTotal + random.randint(1, nRange)
        return nTotal



    def Dump(self, oFile):
        ''' Write the team into the specified file. '''
        json.dump(self.name, oFile)
        oFile.write('\n')
        json.dump(self.colour, oFile)
        oFile.write('\n')
        json.dump(self.energy, oFile)
        oFile.write('\n')
        json.dump(self.moral, oFile)
        oFile.write('\n')
        json.dump(self.defence, oFile)
        oFile.write('\n')
        json.dump(self.midfield, oFile)
        oFile.write('\n')
        json.dump(self.attack, oFile)
        oFile.write('\n')
        json.dump(self.position, oFile)
        oFile.write('\n')
        json.dump(self.pts, oFile)
        oFile.write('\n')
        json.dump(self.difference, oFile)
        oFile.write('\n')
        json.dump(self.played_home, oFile)
        oFile.write('\n')
        json.dump(self.played_away, oFile)
        oFile.write('\n')
        json.dump(self.formation, oFile)
        oFile.write('\n')
        json.dump(self.fixture, oFile)
        oFile.write('\n')
        json.dump(self.win, oFile)
        oFile.write('\n')
        json.dump(self.draw, oFile)
        oFile.write('\n')
        json.dump(self.lost, oFile)
        oFile.write('\n')



    def Load(self, oFile):
        ''' Load the team from the specified file. '''
        sLine = oFile.readline()
        self.name = json.loads(sLine)
        sLine = oFile.readline()
        self.colour = json.loads(sLine)
        sLine = oFile.readline()
        self.energy = json.loads(sLine)
        sLine = oFile.readline()
        self.moral = json.loads(sLine)
        sLine = oFile.readline()
        self.defence = json.loads(sLine)
        sLine = oFile.readline()
        self.midfield = json.loads(sLine)
        sLine = oFile.readline()
        self.attack = json.loads(sLine)
        sLine = oFile.readline()
        self.position = json.loads(sLine)
        sLine = oFile.readline()
        self.pts = json.loads(sLine)
        sLine = oFile.readline()
        self.difference = json.loads(sLine)
        sLine = oFile.readline()
        self.played_home = json.loads(sLine)
        sLine = oFile.readline()
        self.played_away = json.loads(sLine)
        sLine = oFile.readline()
        self.formation = json.loads(sLine)
        sLine = oFile.readline()
        self.fixture = json.loads(sLine)
        sLine = oFile.readline()
        self.win = json.loads(sLine)
        sLine = oFile.readline()
        self.draw = json.loads(sLine)
        sLine = oFile.readline()
        self.lost = json.loads(sLine)
