#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to implement the CupCompetition class for the the BBC Football Manager program.
'''

# System libraries.
import json

# Application Libraries.
import ansi



class CupCompetition:
    ''' Class to represent a cup competition in the BBC Football Manager game. '''



    def __init__(self, label, isEntered):
        ''' Class constructor. '''
        self.name = label
        self.isEntered = isEntered
        self.newSeason()



    def newSeason(self):
        ''' Reset the competition for a new season. '''
        self.isIn = True
        self.round = 1



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
        return 'Error {}'.format(self.round)



    def getStatus(self):
        ''' Return the string describing the current status. '''
        if self.isIn:
            return '{}: in {}'.format(self.name, self.getRoundName())
        return '{}: out {}'.format(self.name, self.getRoundName())



    def dump(self, outputFile):
        ''' Write the player into the specified file. '''
        json.dump(self.name, outputFile)
        outputFile.write('\n')
        json.dump(self.isIn, outputFile)
        outputFile.write('\n')
        json.dump(self.isEntered, outputFile)
        outputFile.write('\n')



    def load(self, inputFile):
        ''' Read the player from the specified file. '''
        line = inputFile.readline()
        self.name = json.loads(line)
        line = inputFile.readline()
        self.isIn = json.loads(line)
        line = inputFile.readline()
        self.isEntered = json.loads(line)
