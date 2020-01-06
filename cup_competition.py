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
        self.isIn = isEntered
        self.isEntered = isEntered


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
