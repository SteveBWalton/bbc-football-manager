#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to implement the CupCompetition class for the the BBC Football Manager program.
'''

# System libraries.
import random
import json

# Application Libraries.
import ansi
from team import Team



class CupCompetition:
    ''' Class to represent a cup competition in the BBC Football Manager game. '''



    def __init__(self, game, label, mask, notMask):
        ''' Class constructor. '''
        self.game = game
        self.name = label
        self.mask = mask
        self.notMask = notMask
        self.newSeason()
        random.seed()



    def newSeason(self):
        ''' Reset the competition for a new season. '''
        self.isIn = True
        self.round = 1
        self.results = []
        if self.game.args.debug:
            self.round = 5



    def getRoundName(self):
        ''' Return the string description of the round. '''
        if self.round == 1:
            return '1st Round'
        elif self.round == 2:
            return '2nd Round'
        elif self.round == 3:
            return 'Quarter Final'
        elif self.round == 4:
            return 'Semi Final'
        elif self.round == 5:
            return 'Final'
        elif self.round == 6:
            return 'Winner'
        return 'Error {}'.format(self.round)



    def getTeam(self, division):
        ''' Return the team to play against for the next match.
        This is not working currently.
        Only return a team from the current league.
        This should be a weak team and keep the game easy to debug.
        '''
        if division == self.game.division:
            # Team in same division as team.
            teamIndex = random.randint(0, len(self.game.teams) - 1)
            # Check not already played this team.
            while teamIndex == self.game.teamIndex or self.isPlayedBefore(self.game.teams[teamIndex]):
                teamIndex = random.randint(0, len(self.game.teams) - 1)
            # Return the team.
            return self.game.teams[teamIndex]

        # Create a new team for the division.
        team = Team()
        teamIndex = random.randint(0, len(self.game.teams) - 1)
        team.getTeam(division, teamIndex)
        # Check not already played this team.
        while self.isPlayedBefore(self.game.teams[teamIndex]):
            teamIndex = random.randint(0, len(self.game.teams) - 1)
            team.getTeam(division, teamIndex)
        # Return the team.
        team.initialise(division)
        return team



    def isPlayedBefore(self, team):
        ''' Returns true if played against this team already in the cup. '''
        isResult = False
        for result in self.results:
            if result.opponent == team.name:
                isResult = True
        return isResult



    def addResult(self, isHomeMatch, opponent, homeGoals, awayGoals):
        ''' Add a match result to the cup. '''
        cupResult = CupResult(self.getRoundName(), isHomeMatch, opponent.name, homeGoals, awayGoals)
        self.results.append(cupResult)
        if isHomeMatch:
            if homeGoals > awayGoals:
                self.round += 1
            elif homeGoals < awayGoals:
                self.isIn = False
        else:
            if homeGoals < awayGoals:
                self.round += 1
            elif homeGoals > awayGoals:
                self.isIn = False
        if self.round == 6:
            self.game.titles = self.game.titles | self.mask
        if not self.isIn:
            self.game.titles = self.game.titles & self.notMask


    def displayResults(self):
        ''' Show the previous results in this cup. '''
        html = '<table>'
        for result in self.results:
            html += result.display(self.game.teamName)
        html += '</table>'
        return html



    def dump(self, outputFile):
        ''' Write the cup competition into the specified file. '''
        json.dump(self.name, outputFile)
        outputFile.write('\n')
        json.dump(self.isIn, outputFile)
        outputFile.write('\n')
        json.dump(self.round, outputFile)
        outputFile.write('\n')
        json.dump(self.mask, outputFile)
        outputFile.write('\n')
        json.dump(self.notMask, outputFile)
        outputFile.write('\n')
        json.dump(len(self.results), outputFile)
        outputFile.write('\n')
        for result in self.results:
            result.dump(outputFile)



    def load(self, inputFile):
        ''' Read the cup competition from the specified file. '''
        line = inputFile.readline()
        self.name = json.loads(line)
        line = inputFile.readline()
        self.isIn = json.loads(line)
        line = inputFile.readline()
        self.round = json.loads(line)
        line = inputFile.readline()
        self.mask = json.loads(line)
        line = inputFile.readline()
        self.notMask = json.loads(line)
        line = inputFile.readline()
        numResults = json.loads(line)
        self.results = []
        for i in range(0, numResults):
            cupResult = CupResult('', True, '', 0, 0)
            cupResult.load(inputFile)
            self.results.append(cupResult)



class CupResult:
    ''' Class to represent the results of a single cup match. '''



    def __init__(self, stage, isHomeMatch, opponent, homeGoals, awayGoals):
        ''' Class constructor. '''
        self.stage = stage
        self.isHomeMatch = isHomeMatch
        self.opponent = opponent
        self.homeGoals = homeGoals
        self.awayGoals = awayGoals



    def dump(self, outputFile):
        json.dump(self.stage, outputFile)
        outputFile.write('\n')
        json.dump(self.isHomeMatch, outputFile)
        outputFile.write('\n')
        json.dump(self.opponent, outputFile)
        outputFile.write('\n')
        json.dump(self.homeGoals, outputFile)
        outputFile.write('\n')
        json.dump(self.awayGoals, outputFile)
        outputFile.write('\n')



    def load(self, inputFile):
        line = inputFile.readline()
        self.stage = json.loads(line)
        line = inputFile.readline()
        self.isHomeMatch = json.loads(line)
        line = inputFile.readline()
        self.opponent = json.loads(line)
        line = inputFile.readline()
        self.homeGoals = json.loads(line)
        line = inputFile.readline()
        self.awayGoals = json.loads(line)



    def display(self, teamName):
        ''' Display this result. '''
        html = '<tr>'
        if self.isHomeMatch:
            print('{:>5} {:>20}{:>2} {:<2}{:<20}'.format(self.stage, teamName, self.homeGoals, self.awayGoals, self.opponent))
            html += '<td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(self.stage, teamName, self.homeGoals, self.awayGoals, self.opponent)
        else:
            print('{:>5} {:>20}{:>2} {:<2}{:<20}'.format(self.stage, self.opponent, self.homeGoals, self.awayGoals, teamName))
            html += '<td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(self.stage, self.opponent, self.homeGoals, self.awayGoals, teamName)
        return html
