#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to implement the Player class for the the BBC Football Manager program.
'''

# System libraries.
import json

# Application Libraries.
import ansi



class Player:
    ''' Class to represent a player in the BBC Football Manager game. '''
    DEFENSE = 0
    MIDFIELD = 1
    ATTACK = 2



    def __init__(self):
        ''' Class constructor. '''
        self.name = 'Error'
        self.skill = 1
        self.energy = 10
        self.position = Player.DEFENSE
        self.index = 0
        self.inSquad = False
        self.inTeam = False
        self.injured = False
        self.caps = 0
        self.goals = 0



    def getPlayer(self, index):
        ''' Populate the object with a prebuilt player. '''
        self.index = index
        if index <= 10:
            self.position = Player.DEFENSE
        elif index <= 20:
            self.position = Player.MIDFIELD
        else:
            self.position = Player.ATTACK

        if index == 1:
            self.name = 'C Woods'
        elif index == 2:
            self.name = 'P Shilton'
        elif index == 3:
            self.name = 'A Hansen'
        elif index == 4:
            self.name = 'P Neal'
        elif index == 5:
            self.name = 'T Butcher'
        elif index == 6:
            self.name = 'K Moran'
        elif index == 7:
            self.name = 'M Lawrenson'
        elif index == 8:
            self.name = 'T Adams'
        elif index == 9:
            self.name = 'M Duxbury'
        elif index == 10:
            self.name = 'G Stevens'
        elif index == 11:
            self.name = 'B Robson'
        elif index == 12:
            self.name = 'G Hoddle'
        elif index == 13:
            self.name = 'S Hodge'
        elif index == 14:
            self.name = 'C Johnston'
        elif index == 15:
            self.name = 'R Wilkins'
        elif index == 16:
            self.name = 'K Dalglish'
        elif index == 17:
            self.name = 'J Barnes'
        elif index == 18:
            self.name = 'G Souness'
        elif index == 19:
            self.name = 'N Webb'
        elif index == 20:
            self.name = 'T Morley'
        elif index == 21:
            self.name = 'M Hughes'
        elif index == 22:
            self.name = 'M Hateley'
        elif index == 23:
            self.name = 'P Beardsley'
        elif index == 24:
            self.name = 'I Rush'
        elif index == 25:
            self.name = 'G Lineker'
        elif index == 26:
            self.name = 'N Whiteside'



    def writeRow(self, exchangeRate=0):
        ''' Display this player on a row. '''
        if self.position == Player.DEFENSE:
            print(ansi.BACKGROUND_LIGHT_BLUE, end = '')
            print(ansi.LIGHT_YELLOW, end = '')
        elif self.position == Player.MIDFIELD:
            print(ansi.BACKGROUND_LIGHT_YELLOW, end = '')
            print(ansi.BLUE, end = '')
        else:
            print(ansi.BACKGROUND_WHITE, end = '')
            print(ansi.BLUE, end = '')
        print(f'{self.index:2} {self.name:<20}{self.skill:>2}{self.energy:>3} ', end = '')
        if exchangeRate != 0:
            print(f'{f"£{self.skill * exchangeRate:,.0f}":>11s}', end = '')
        if self.inTeam:
            print(ansi.BACKGROUND_GREEN, end = '')
            print(ansi.LIGHT_YELLOW, end = '')
            print(' P ', end = '')
        if self.injured:
            print(ansi.BACKGROUND_RED, end = '')
            print(ansi.LIGHT_YELLOW, end = '')
            print(' I ', end = '')
        print(ansi.RESET_ALL)



    def htmlRow(self, exchangeRate=0):
        ''' Display this player on a html table row. '''
        if self.position == Player.DEFENSE:
            html = '<tr style="background-color: blue; color: yellow;">'
            style = 'color: yellow;'
        elif self.position == Player.MIDFIELD:
            html = '<tr style="background-color: yellow; color: blue;">'
            style = 'color: blue;'
        else:
            html = '<tr style="background-color: white; color: blue;">'
            style = 'color: blue;'
        html += f'<td style="text-align: center;"><a style="{style}" href="app:?player={self.index}">{self.index}</a></td><td><a style="{style}" href="app:?player={self.index}">{self.name}</a></td><td style="text-align: right;">{self.skill}</td><td style="text-align: right;">{self.energy}</td>'
        if exchangeRate != 0:
            html += f'<td style="text-align: right;">£{self.skill * exchangeRate:,.0f}</td>'
        if self.inTeam:
            html += '<td style="background-color: green; color: yellow; text-align: center; width: 50px;">P</td>'
        if self.injured:
            html += '<td style="background-color: red; color: yellow; text-align: center; width: 50px;">I</td>'
        html += '</tr>'
        return html



    def getPosition(self):
        ''' Returns the position of the player as a string. '''
        if self.position == Player.DEFENSE:
            return 'Defense'
        if self.position == Player.MIDFIELD:
            return 'Mid-field'
        return 'Attack'



    def dump(self, outputFile):
        ''' Write the player into the specified file. '''
        json.dump(self.name, outputFile)
        outputFile.write('\n')
        json.dump(self.skill, outputFile)
        outputFile.write('\n')
        json.dump(self.energy, outputFile)
        outputFile.write('\n')
        json.dump(self.position, outputFile)
        outputFile.write('\n')
        json.dump(self.index, outputFile)
        outputFile.write('\n')
        json.dump(self.inSquad, outputFile)
        outputFile.write('\n')
        json.dump(self.inTeam, outputFile)
        outputFile.write('\n')
        json.dump(self.injured, outputFile)
        outputFile.write('\n')
        json.dump(self.caps, outputFile)
        outputFile.write('\n')
        json.dump(self.goals, outputFile)
        outputFile.write('\n')



    def load(self, inputFile):
        ''' Read the player from the specified file. '''
        line = inputFile.readline()
        self.name = json.loads(line)
        line = inputFile.readline()
        self.skill = json.loads(line)
        line = inputFile.readline()
        self.energy = json.loads(line)
        line = inputFile.readline()
        self.position = json.loads(line)
        line = inputFile.readline()
        self.index = json.loads(line)
        line = inputFile.readline()
        self.inSquad = json.loads(line)
        line = inputFile.readline()
        self.inTeam = json.loads(line)
        line = inputFile.readline()
        self.injured = json.loads(line)
        line = inputFile.readline()
        self.caps = json.loads(line)
        line = inputFile.readline()
        self.goals = json.loads(line)
