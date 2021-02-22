#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to implement the Team class for the the BBC Football Manager program.
'''

# System libraries.
import random
import json

# Application Libraries.
import ansi



class Team:
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
        self.isPlayedHome = False
        self.isPlayedAway = False
        self.formation = '4-4-2'
        self.fixture = 0
        self.win = 0
        self.draw = 0
        self.lost = 0
        self.numHomeGames = 0



    def initialise(self, division):
        ''' Replacement for FNTEAM (Line 3750) in the BBC Basic version. '''
        numDefence = 3 + random.randint(1, 2)
        numMidfield = 2 + random.randint(1, 3)
        numAttack = 11 - numMidfield - numDefence
        bonus = 1 + (1 if division < 4 else 0) + (1 if division == 1 else 0)
        skill = 4 - (division & 1)
        self.energy = self.multiRandomInt(20, 11)
        self.moral = 9 + random.randint(1, 11)
        self.defence = numDefence * bonus + self.multiRandomInt(skill, numDefence)
        self.midfield = numMidfield * bonus + self.multiRandomInt(skill, numMidfield)
        self.attack = numAttack * bonus + self.multiRandomInt(skill, numAttack)
        self.formation = '{}-{}-{}'.format(numDefence-1, numMidfield, numAttack)

        self.pts = 0
        self.difference = 0
        self.isPlayedHome = False
        self.isPlayedAway = False
        self.win = 0
        self.draw = 0
        self.lost = 0
        self.numHomeGames = 0



    def zero(self):
        ''' Initialise the team properties to zero. '''
        self.energy = 0
        self.moral = 10
        self.defence = 0
        self.midfield = 0
        self.attack = 0
        self.formation = '0-0-0'

        self.pts = 0
        self.difference = 0
        self.isPlayedHome = False
        self.isPlayedAway = False
        self.win = 0
        self.draw = 0
        self.lost = 0
        self.numHomeGames = 0



    def writeTableRow(self, isDebug):
        ''' Write this team into the league table. '''
        if isDebug:
            name = '{}({})'.format(self.name, self.numHomeGames)
        else:
            name = self.name
        print('{:>2} {}{:<15}{:>3}{:>3}{:>3}{:>4}{:>4}{}'.format(self.position, self.colour, name, self.win, self.draw, self.lost, self.pts, self.difference, ansi.RESET_ALL))



    def htmlTableRow(self,isDebug):
        ''' Write this team into the league table. '''
        if isDebug:
            name = '{}({})'.format(self.name, self.numHomeGames)
        else:
            name = self.name
        html = '<tr><td style="text-align: right;">{}</td><td>{}</td><td style="text-align: right;">{}</td><td style="text-align: right;">{}</td><td style="text-align: right;">{}</td><td style="text-align: right;">{}</td><td style="text-align: right;">{:+d}</td></tr>'.format(self.position, name, self.win, self.draw, self.lost, self.pts, self.difference)
        return html



    def getColouredName(self):
        ''' Returns the team name wrapped in the colour code. '''
        return '{}{}{}'.format(self.colour, self.name, ansi.RESET_ALL)



    def getTeam(self, division, index):
        ''' This is the replacement for FNGETTEAM(). Populate the object with a prebuilt team. '''
        if division == 1:
            if index == 1:
                self.name = 'Liverpool'
                self.colour = ansi.RED
            elif index == 2:
                self.name = 'Man United'
                self.colour = ansi.RED
            elif index == 3:
                self.name = 'Leeds United'
                self.colour = ansi.YELLOW
            elif index == 4:
                self.name = 'Arsenal'
                self.colour = ansi.RED
            elif index == 5:
                self.name = 'Spurs'
                self.colour = ansi.WHITE
            elif index == 6:
                self.name = 'Aston Villa'
                self.colour = ansi.MAGENTA
            elif index == 7:
                self.name = 'Everton'
                self.colour = ansi.LIGHT_BLUE
            elif index == 8:
                self.name = 'Nottm Forest'
                self.colour = ansi.RED
            elif index == 9:
                self.name = 'Millwall'
                self.colour = ansi.WHITE
            elif index == 10:
                self.name = 'Coventry'
                self.colour = ansi.CYAN
            elif index == 11:
                self.name = 'West Ham'
                self.colour = ansi.MAGENTA
            elif index == 12:
                self.name = 'Norwich'
                self.colour = ansi.YELLOW
            elif index == 13:
                self.name = 'Sheff Wed'
                self.colour = ansi.YELLOW
            elif index == 14:
                self.name = 'Derby'
                self.colour = ansi.WHITE
            elif index == 15:
                self.name = 'Chelsea'
                self.colour = ansi.LIGHT_BLUE
            elif index == 16:
                self.name = 'Newcastle'
                self.colour = ansi.WHITE
            else:
                self.getTeam(division+1, index-16)
        elif division == 2:
            if index == 1:
                self.name = 'Watford'
                self.colour = ansi.YELLOW
            elif index == 2:
                self.name = 'Stoke City'
                self.colour = ansi.RED
            elif index == 3:
                self.name = 'Brighton'
                self.colour = ansi.LIGHT_BLUE
            elif index == 4:
                self.name = 'Barnsley'
                self.colour = ansi.RED
            elif index == 5:
                self.name = 'Plymouth'
                self.colour = ansi.LIGHT_BLUE
            elif index == 6:
                self.name = 'Hull City'
                self.colour = ansi.MAGENTA
            elif index == 7:
                self.name = 'Notts Co'
                self.colour = ansi.WHITE
            elif index == 8:
                self.name = 'Man City'
                self.colour = ansi.CYAN
            elif index == 9:
                self.name = 'Shrewsbury'
                self.colour = ansi.RED
            elif index == 10:
                self.name = 'Burnley'
                self.colour = ansi.MAGENTA
            elif index == 11:
                self.name = 'Charlton'
                self.colour = ansi.RED
            elif index == 12:
                self.name = 'Sunderland'
                self.colour = ansi.RED
            elif index == 13:
                self.name = 'Bradford'
                self.colour = ansi.RED
            elif index == 14:
                self.name = 'Bury'
                self.colour = ansi.LIGHT_BLUE
            elif index == 15:
                self.name = 'Sheff United'
                self.colour = ansi.RED
            elif index == 16:
                self.name = 'Huddersfield'
                self.colour = ansi.LIGHT_BLUE
            else:
                self.getTeam(division+1, index-16)
        elif division == 3:
            if index == 1:
                self.name = 'Wolves'
                self.colour = ansi.YELLOW
            elif index == 2:
                self.name = 'Oxford'
                self.colour = ansi.RED
            elif index == 3:
                self.name = 'Swindon'
                self.colour = ansi.RED
            elif index == 4:
                self.name = 'Walsall'
                self.colour = ansi.RED
            elif index == 5:
                self.name = 'Newport'
                self.colour = ansi.GREEN
            elif index == 6:
                self.name = 'Wigan'
                self.colour = ansi.RED
            elif index == 7:
                self.name = 'Wimbledon'
                self.colour = ansi.RED
            elif index == 8:
                self.name = 'Mansfield'
                self.colour = ansi.GREEN
            elif index == 9:
                self.name = 'Southend'
                self.colour = ansi.RED
            elif index == 10:
                self.name = 'Grimsby'
                self.colour = ansi.GREEN
            elif index == 11:
                self.name = 'Blackburn'
                self.colour = ansi.MAGENTA
            elif index == 12:
                self.name = 'Reading'
                self.colour = ansi.RED
            elif index == 13:
                self.name = 'Crewe'
                self.colour = ansi.YELLOW
            elif index == 14:
                self.name = 'Darlington'
                self.colour = ansi.RED
            elif index == 15:
                self.name = 'Port Value'
                self.colour = ansi.LIGHT_BLUE
            elif index == 16:
                self.name = 'Stockport'
                self.colour = ansi.RED
            else:
                self.getTeam(division+1, index-16)
        else:
            if index == 1:
                self.name = 'Scunthorpe'
                self.colour = ansi.RED
            elif index == 2:
                self.name = 'York'
                self.colour = ansi.GREEN
            elif index == 3:
                self.name = 'Bournemouth'
                self.colour = ansi.LIGHT_BLUE
            elif index == 4:
                self.name = 'Doncaster'
                self.colour = ansi.CYAN
            elif index == 5:
                self.name = 'Lincoln'
                self.colour = ansi.MAGENTA
            elif index == 6:
                self.name = 'Rochdale'
                self.colour = ansi.RED
            elif index == 7:
                self.name = 'Hereford'
                self.colour = ansi.YELLOW
            elif index == 8:
                self.name = 'Hartlepool'
                self.colour = ansi.LIGHT_BLUE
            elif index == 9:
                self.name = 'Halifax'
                self.colour = ansi.RED
            elif index == 10:
                self.name = 'Tranmere'
                self.colour = ansi.RED
            elif index == 11:
                self.name = 'Aldershot'
                self.colour = ansi.YELLOW
            elif index == 12:
                self.name = 'Bristol'
                self.colour = ansi.LIGHT_BLUE
            elif index == 13:
                self.name = 'Wrexham'
                self.colour = ansi.RED
            elif index == 14:
                self.name = 'Torquay'
                self.colour = ansi.GREEN
            elif index == 15:
                self.name = 'Gillingham'
                self.colour = ansi.GREEN
            elif index == 16:
                self.name = 'Exeter'
                self.colour = ansi.RED
            else:
                self.getTeam(division-1, index-16)



    def multiRandomInt(self, rndRange, rndNumber):
        ''' Replacement for FNRND() (Line 6640) in the BBC Basic version. '''
        numTotal = 0
        for count in range(rndNumber):
            numTotal += random.randint(1, rndRange)
        return numTotal



    def dump(self, outputFile):
        ''' Write the team into the specified file. '''
        json.dump(self.name, outputFile)
        outputFile.write('\n')
        json.dump(self.colour, outputFile)
        outputFile.write('\n')
        json.dump(self.energy, outputFile)
        outputFile.write('\n')
        json.dump(self.moral, outputFile)
        outputFile.write('\n')
        json.dump(self.defence, outputFile)
        outputFile.write('\n')
        json.dump(self.midfield, outputFile)
        outputFile.write('\n')
        json.dump(self.attack, outputFile)
        outputFile.write('\n')
        json.dump(self.position, outputFile)
        outputFile.write('\n')
        json.dump(self.pts, outputFile)
        outputFile.write('\n')
        json.dump(self.difference, outputFile)
        outputFile.write('\n')
        json.dump(self.isPlayedHome, outputFile)
        outputFile.write('\n')
        json.dump(self.isPlayedAway, outputFile)
        outputFile.write('\n')
        json.dump(self.formation, outputFile)
        outputFile.write('\n')
        json.dump(self.fixture, outputFile)
        outputFile.write('\n')
        json.dump(self.win, outputFile)
        outputFile.write('\n')
        json.dump(self.draw, outputFile)
        outputFile.write('\n')
        json.dump(self.lost, outputFile)
        outputFile.write('\n')



    def load(self, inputFile):
        ''' load the team from the specified file. '''
        line = inputFile.readline()
        self.name = json.loads(line)
        line = inputFile.readline()
        self.colour = json.loads(line)
        line = inputFile.readline()
        self.energy = json.loads(line)
        line = inputFile.readline()
        self.moral = json.loads(line)
        line = inputFile.readline()
        self.defence = json.loads(line)
        line = inputFile.readline()
        self.midfield = json.loads(line)
        line = inputFile.readline()
        self.attack = json.loads(line)
        line = inputFile.readline()
        self.position = json.loads(line)
        line = inputFile.readline()
        self.pts = json.loads(line)
        line = inputFile.readline()
        self.difference = json.loads(line)
        line = inputFile.readline()
        self.isPlayedHome = json.loads(line)
        line = inputFile.readline()
        self.isPlayedAway = json.loads(line)
        line = inputFile.readline()
        self.formation = json.loads(line)
        line = inputFile.readline()
        self.fixture = json.loads(line)
        line = inputFile.readline()
        self.win = json.loads(line)
        line = inputFile.readline()
        self.draw = json.loads(line)
        line = inputFile.readline()
        self.lost = json.loads(line)
