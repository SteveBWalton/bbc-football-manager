#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to implement the Game class for the the BBC Football Manager program.
'''

# System libraries.
import random
import math
import json
import time
import sys
from typing import Dict     # This is for type hinting only.
import codecs

# Application Libraries.
import ansi
from inkey import InKey
from team import Team
from player import Player
from cup_competition import CupCompetition



class Game:
    ''' Class to represent the BBC Football Manager game. '''



    def __init__(self, args):
        ''' Class constructor for the BBC Football manager game. '''
        self.playerName = ''
        self.level = 1
        self.teamName = ''
        self.teamColour = ansi.WHITE
        self.teamIndex = None
        self.numSquad = 0
        self.numTeam = 0
        self.numInjured = 0
        self.formation = [0, 0, 0]
        self.args = args

        self.titles = 0

        self.homeWins = 0
        self.homeDraws = 0
        self.homeLoses = 0
        self.homeFor = 0
        self.homeAgainst = 0
        self.awayWins = 0
        self.awayDraws = 0
        self.awayLoses = 0
        self.awayFor = 0
        self.awayAgainst = 0

        self.faCup = None
        self.leagueCup = None
        self.europeanCup = None

        self.status = 0
        self.subStatus = 0
        self.html = 'Hello World'



    def run(self):
        ''' Execute the football manager game. '''
        if sys.stdout.encoding.lower() != 'utf-8':
            print('sys.stdout.encoding = {}'.format(sys.stdout.encoding))
            print('Switch stdout to utf-8')
            sys.stdout.reconfigure(encoding='utf-8')

        if self.args.graphical:
            self.runGraphical()
        else:
            self.runConsole()



    def runGraphical(self):
        ''' Execute the football manager game in a wx window. '''
        import main_window
        graphical = main_window.WxApp(self)
        graphical.runMainLoop()



    def runConsole(self):
        ''' Execute the football manager game in the console. '''
        self.keyboard = InKey()
        random.seed()

        ansi.doCls()
        self.football()

        # Get the player settings.
        print()
        self.playerName = input('Please enter your name: ')
        if self.playerName == '':
            self.playerName = 'Steve'

        # Select the level.
        print('Enter level [1-4]')
        self.level = int(self.getKeyboardCharacter(['1', '2', '3', '4']))
        print('Level {} was selected'.format(self.level))

        # Load a game.
        print('Do you want to load a game?')
        if self.getYesNo():
            print('Yes')
            self.load()
            self.sortDivision()
        else:
            print('No')
            self.newGame()

        # Play the game.
        nYear = 0
        while True:
            self.newSeason()

            # Play a season.
            while self.numMatches < self.MATCHES_PER_SEASON:
                ansi.doCls()
                print('{} MANAGER: {}'.format(self.team.getColouredName(), self.playerName))
                print('LEVEL: {}'.format(self.level))
                print()
                self.displayCupStatus()
                self.displayTitles()
                print()
                print('1 .. Sell Players / View Squad')
                print('2 .. Bank')
                print('3 .. Rename Player')
                print('4 .. Continue')
                print('5 .. Save Game')
                print('6 .. Restart')
                print('7 .. League Table')
                print('8 .. Quit')
                keyPress = self.getKeyboardCharacter(['1', '2', '3', '4', '5', '6', '7', '8'])
                if keyPress == '1':
                    self.sellPlayer()
                elif keyPress == '2':
                    self.bank()
                elif keyPress == '3':
                    # PROCRENAME
                    pass
                elif keyPress == '4':
                    # Continue.
                    self.playWeek()
                elif keyPress == '5':
                    self.save(True)
                    time.sleep(5)
                elif keyPress == '6':
                    # PROCRESTART
                    pass
                elif keyPress == '7':
                    ansi.doCls()
                    self.displayLeague()
                    self.wait()
                elif keyPress == '8':
                    # Confirm with the user.
                    print('Are you sure you want to exit the program (Y/N) ?')
                    if self.getYesNo():
                        return

            # Season has finished.
            self.endSeason()



    def endSeason(self, isGraphical=False):
        ansi.doCls()
        print('Season has finished.')
        self.html = '<h1>Season has finished</h1>'
        self.displayLeague()
        if isGraphical == False:
            self.wait()

        europeanCup = 0
        self.titles = self.titles & ~7
        if self.teamIndex == 0:
            print('{} are division {} champions'.format(self.teamName, self.division))
            self.html += '<p>{} are division {} champions</p>'.format(self.teamName, self.division)
            self.titles += self.division
            if self.division == 1:
                europeanCup = 3
        elif self.teamIndex <= 2 and self.division == 1:
            europeanCup = 1

        if self.division == 1:
            print('Qualify for Europe')
            self.html += '<h2>Qualify for Europe</h2><p>'
        else:
            print('Promotion')
            self.html += '<h2>Promotion</h2><p>'
        for index in range(0, 3):
            print(self.teams[index].getColouredName())
            self.html += '{}<br />'.format(self.teams[index].name)
        self.html += '</p>'
        if self.division != 4:
            print('Relegation')
            self.html += '<h2>Relegation</h2><p>'
            for index in range(13, 16):
                print(self.teams[index].getColouredName())
                self.html += '{}<br />'.format(self.teams[index].name)
            self.html += '</p>'

        if self.titles & 8 == 8:
            if europeanCup == 0:
                europeanCup = 1
        if self.titles & 16 == 16:
            if europeanCup != 3:
                europeanCup = 2
        if self.titles & 32 == 32:
            europeanCup = 3
        if self.titles & 64 == 64:
            if europeanCup != 3:
                europeanCup = 2
        if self.titles & 128 == 128:
            if europeanCup == 0:
                europeanCup = 1

        if europeanCup == 3:
            print('{} qualify for the European Cup.'.format(self.teamName))
            self.html += '{} qualify for the European Cup.'.format(self.teamName)
            self.europeanCup = CupCompetition(self, 'European Cup', 32, ~(32|64|128))
        elif europeanCup == 2:
            print('{} qualify for the European Cup Winners Cup.'.format(self.teamName))
            self.html += '{} qualify for the European Cup Winners Cup.'.format(self.teamName)
            self.europeanCup = CupCompetition(self, 'European Cup Winners Cup', 64, ~(32|64|128))
        elif europeanCup == 1:
            print('{} qualify for the UEFA Cup.'.format(self.teamName))
            self.html += '{} qualify for the UEFA Cup.'.format(self.teamName)
            self.europeanCup = CupCompetition(self, 'UEFA Cup', 128, ~(32|64|128))
        else:
            self.europeanCup = None

        # Rebuild the new league.
        exclued = []
        if self.division != 1 and self.teamIndex <= 2:
            # Promotion.
            self.division -= 1
            print('{} are promoted to division {}'.format(self.teams[self.teamIndex].getColouredName(), self.division))
            self.html += '<p>{} are promoted to division {}</p>'.format(self.teams[self.teamIndex].name, self.division)
            for index in range(3, 13):
                exclued.append(self.teams[index].name)
                self.teams[index].name = ''
        elif self.division != 4 and self.teamIndex >= 13:
            # Relegation.
            self.division += 1
            print('{} are relegated to division {}'.format(self.teams[self.teamIndex].getColouredName(), self.division))
            self.html += '<p>{} are relegated to division {}</p>'.format(self.teams[self.teamIndex].name, self.division)
            for index in range(0, 13):
                exclued.append(self.teams[index].name)
                self.teams[index].name = ''
        else:
            # Same division.
            print('{} stay in division {}'.format(self.teams[self.teamIndex].getColouredName(), self.division))
            self.html += '<p>{} stay in division {}</p>'.format(self.teams[self.teamIndex].name, self.division)
            if self.division != 1:
                for index in range(0, 3):
                    exclued.append(self.teams[index].name)
                    self.teams[index].name = ''
            if self.division != 4:
                for index in range(13, 16):
                    exclued.append(self.teams[index].name)
                    self.teams[index].name = ''
        self.setTeamsForDivision(exclued)

        # Reskill the players.
        self.numTeam = 0
        self.numInjured = 0
        self.formation = [0, 0, 0]
        skillBonus = 1 if self.division <= 2 else 0
        for player in self.players:
            player.skill = random.randint(1, 5) + skillBonus
            player.energy = random.randint(1, 20)
            player.inTeam = False
            player.injured = False
            player.caps = 0
            player.goals = 0
        for index in range(4):
            player = random.randint(0, 25)
            self.players[player].skill = 5 + skillBonus

        self.newSeason()

        self.wait(isGraphical)



    def newSeason(self):
        ''' This is called by endSeason() and before the first season. '''
        self.moneyStart = self.money - self.debt
        self.moneyMessage = ''

        self.faCup = CupCompetition(self, 'FA Cup', 16, ~16)
        self.leagueCup = CupCompetition(self, 'League Cup', 8, ~8)

        self.numMatches = 0
        self.weeks = []

        self.homeWins = 0
        self.homeDraws = 0
        self.homeLoses = 0
        self.homeFor = 0
        self.homeAgainst = 0
        self.awayWins = 0
        self.awayDraws = 0
        self.awayLoses = 0
        self.awayFor = 0
        self.awayAgainst = 0



    def decodeParameters(self, parameters: str) -> Dict[str, str]:
        '''
        :param string parameters: Specifies the parameters as a string. eg. "id=1&name=steve".
        :returns: A dictionary of the parameters and their values.

        Decode the parameters from a link into a dictionary object.
        '''
        # Create an empty dictionary.
        dictionary = {}

        # Split into Key Value pairs by the '&' character.
        items = parameters.split('&')
        for item in items:
            if item != '':
                key, value = item.split('=')
                dictionary[key] = value

        # Return the dictionary object built.
        return dictionary



    def getNextPage(self, response):
        ''' Advance the game to the next user response. '''
        # Deal with the response.
        #if response != '':
        #    print(response)
        if response == '':
            parameters = []
        elif response[0] == '?':
            parameters = self.decodeParameters(response[1:])
        else:
            parameters = []

        # Deal with the response.
        if self.status == 0:
            # Enter player details.
            if response != '':
                if 'name' in parameters:
                    self.playerName = parameters['name']
                    self.playerName = self.playerName.replace('+', ' ')
                    if self.playerName == '':
                        self.playerName = 'Steve'
                    self.status = 1
                self.level = 1
                if 'level' in parameters:
                    self.level = parameters['level']
                if 'load' in parameters:
                    if parameters['load'] == '2':
                        self.load()
                        self.sortDivision()
                        self.status = 100
                        self.newSeason()
        elif self.status == 1:
            # Select team.
            if 'team' in parameters:
                teamIndex = int(parameters['team'])
                if teamIndex == 0:
                    self.status = 2
                else:
                    team = Team()
                    team.getTeam(teamIndex // 100, teamIndex % 100)
                    self.teamName = team.name
                    self.teamColour = team.colour
                    self.status = 100
                    self.newGame(True)
                    self.newSeason()

        elif self.status == 2:
            # Enter own team name.
            if 'name' in parameters:
                self.teamName = parameters['name']
                self.teamName = self.teamName.replace('+', ' ')
                if self.teamName == '':
                    self.teamName = 'Racing Warwick'
                self.teamColour = ansi.CYAN
                self.status = 100
                self.newGame(True)
                self.newSeason()

        elif self.status == 100:
            if 'response' in parameters:
                response = int(parameters['response'])
                # print(response)
                if response == 1:
                    # Sell Player
                    self.status = 110
                if response == 2:
                    # Bank
                    self.status = 120
                elif response == 4:
                    self.numMatches += 1

                    # Decide if a cup match.
                    if self.numMatches % 6 == 2:
                        # League Cup.
                        if self.leagueCup.isIn:
                            self.activeCup = self.leagueCup
                            self.status = 200
                            self.subStatus = -1
                    if self.numMatches % 6 == 4:
                        # FA Cup.
                        if self.faCup.isIn:
                            self.activeCup = self.faCup
                            self.status = 200
                            self.subStatus = -1
                    if self.numMatches % 6 == 0 or (self.numMatches % 6 == 3 and self.args.debug):
                        # European Cup.
                        if self.europeanCup != None:
                            if self.europeanCup.isIn:
                                self.activeCup = self.europeanCup
                                self.status = 200
                                self.subStatus = -1

                    # League match.
                    if self.status == 100:
                        self.status = 300
                        self.subStatus = -1
                elif response == 5:
                    # Save game.
                    self.save(True)
                    self.status = 150
                elif response == 7:
                    # Show League.
                    self.status = 170
        elif self.status == 110:
            # Sell Player.
            if 'player' in parameters:
                player = int(parameters['player'])
                self.subStatus = player
                self.status = 115
            if 'response' in parameters:
                if parameters['response'] == 'c':
                    self.status = 100
        elif self.status == 115:
            if 'response' in parameters:
                if parameters['response'] == 'y':
                    self.htmlSellPlayerPart3()
                    self.status = 100
                if parameters['response'] == 'n':
                    self.status = 100
        elif self.status == 120:
            # Bank.
            if 'amount' in parameters:
                try:
                    amountString = parameters['amount']
                    amountString = amountString.replace('k', '000')
                    amount = int(amountString)
                except:
                    amount = 0
                if amount != 0:
                    self.subStatus = amount
                    self.status = 125
            if 'sign' in parameters:
                # print('sign = {}'.format(parameters['sign']))
                if parameters['sign'] == '1':
                    self.subStatus = -self.subStatus
            if 'response' in parameters:
                if parameters['response'] == 'c':
                    self.status = 100
        elif self.status == 125:
            self.status = 100
        elif self.status == 150:
            self.status = 100
        elif self.status == 170:
            self.status = 100
        elif self.status == 200:
            # Cup Match.
            if 'response' in parameters:
                if parameters['response'] == 'c':
                    self.status = 210
                if parameters['response'] == 't':
                    self.status = 220
                    self.subStatus = 0
        elif self.status == 210:
            if 'player' in parameters:
                playerIndex = int(parameters['player']) - 1
                if self.players[playerIndex].inSquad:
                    if self.players[playerIndex].inTeam:
                        self.dropPlayer(playerIndex)
                    else:
                        self.addPlayer(playerIndex)
            if 'response' in parameters:
                if parameters['response'] == 'b':
                    self.status = 200
        elif self.status == 220:
            if 'response' in parameters:
                if parameters['response'] == 'c':
                    self.status = 230
        elif self.status == 230:
            if 'response' in parameters:
                if parameters['response'] == 'c':
                    if self.homeScore == self.awayScore:
                        # Replay
                        self.status = 200
                        self.subStatus = 0
                        self.isHomeMatch = not self.isHomeMatch
                    else:
                        # Next step, league match.
                        self.status = 300
                        self.subStatus = -1
        elif self.status == 300:
            # League Match.
            if 'response' in parameters:
                if parameters['response'] == 'c':
                    self.status = 310
                if parameters['response'] == 't':
                    self.status = 400
                    self.subStatus = 0
        elif self.status == 310:
            if 'player' in parameters:
                playerIndex = int(parameters['player']) - 1
                if self.players[playerIndex].inSquad:
                    if self.players[playerIndex].inTeam:
                        self.dropPlayer(playerIndex)
                    else:
                        self.addPlayer(playerIndex)
            if 'response' in parameters:
                if parameters['response'] == 'b':
                    self.status = 300
        elif self.status == 400:
            if 'response' in parameters:
                if parameters['response'] == 'c':
                    self.status = 410
        elif self.status == 410:
            if 'response' in parameters:
                if parameters['response'] == 'c':
                    self.status = 430
        elif self.status == 430:
            if 'response' in parameters:
                if parameters['response'] == 'c':
                    self.status = 440
        elif self.status == 440:
            # Player Market.
            self.status = 450
            if 'bid' in parameters:
                try:
                    bidAmount = parameters['bid']
                    bidAmount = bidAmount.replace('k', '000')
                    bid = int(bidAmount)
                except:
                    bid = 0
                if bid > 0:
                    self.status = 445
                    self.subStatus2 = bid
        elif self.status == 445:
            self.status = 450
        elif self.status == 450:
            self.status = 460
        elif self.status == 460:
            self.status = 470
        elif self.status == 470:
            # Back to start of week or end of season.
            if self.numMatches < self.MATCHES_PER_SEASON:
                self.status = 100
            else:
                self.status = 1000
        elif self.status == 1000:
            self.status = 100


        # Defaults.
        responseOptions = ''

        # Render the next page.
        if self.status == 0:
            # Initial page.  Get player name and level.
            self.html = ''
            self.football()
            self.html += '<form action="app:" method="get"><p>Please enter your name <input type="text" name="name" /></p>'
            self.html += '<p>Please select your level <select name="level"><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option></select></p>'
            self.html += '<p>Do you want to load a game <select name="load"><option value="1">No</option><option value="2">Yes</option></select></p>'
            self.html += '<p><input type="submit" name="ok" value="OK" /></p>'
            self.html += '</form>'
        elif self.status == 1:
            # Second initial page.  Get the players team.
            self.html = '<form action="app:" method="get">'
            self.html += '<p>Please select your team <select name="team">'
            self.html += '<option value="0">Own Team</option>'
            for division in range(1, 4):
                for index in range(1, 16):
                    team = Team()
                    team.getTeam(division, index)
                    self.html += '<option value="{}">{}</option>'.format(100 * division + index, team.name)
            self.html += '</select>'
            self.html += '<p><input type="submit" name="ok" value="OK" /></p>'
            self.html += '</form>'
        elif self.status == 2:
            # Optional initialise, name own team.
            self.html = '<form action="app:" method="get">'
            self.html += '<p>Please enter your team name <input type="text" name="name"></p>'
            self.html += '<p><input type="submit" name="ok" value="OK" /></p>'
            self.html += '</form>'
        elif self.status == 100:
            self.html = '<h1 style="display: inline">{} </h1><p style="display: inline">Manager {}</p>'.format(self.teamName, self.playerName)
            self.html += '<p>Level {}</p>'.format(self.level)
            self.displayCupStatus()
            self.displayTitles()
            self.html += '<p style="margin-top:10px;"><a href="app:?response=1">1 .. Sell Players / View Squad</a><br />'
            self.html += '<a href="app:?response=2">2 .. Bank</a><br />'
            self.html += '<a href="app:?response=3">3 .. Rename Player</a><br />'
            self.html += '<a href="app:?response=4">4 .. Continue</a><br />'
            self.html += '<a href="app:?response=5">5 .. Save Game</a><br />'
            self.html += '<a href="app:?response=6">6 .. Restart</a><br />'
            self.html += '<a href="app:?response=7">7 .. League Table</a><br />'
        elif self.status == 110:
            self.htmlSellPlayerPart1()
        elif self.status == 115:
            self.htmlSellPlayerPart2()
        elif self.status == 120:
            self.htmlBankPart1()
        elif self.status == 125:
            self.htmlBankPart2()
        elif self.status == 150:
            self.html += '<p>Saving game.</p>'
            responseOptions = 'delay: 2000'
        elif self.status == 170:
            self.html = ''
            self.displayLeague()
            self.wait(True)
        elif self.status == 200:
            # Cup Match.
            self.playCupMatch()
        elif self.status == 220:
            if self.isHomeMatch:
                responseOptions = self.htmlPlayMatch(self.teams[self.teamIndex], self.cupTeam)
            else:
                responseOptions = self.htmlPlayMatch(self.cupTeam, self.teams[self.teamIndex])
        elif self.status == 230:
            self.reportCupMatch()
        elif self.status == 300:
            # print('status = {}, subStatus = {}'.format(self.status, self.subStatus))
            if self.subStatus == -1:
                self.findLeagueOpponent()
                self.subStatus = 0
            # League Match.
            self.html = '<h1>Division {}</h1>'.format(self.division)
            if self.isHomeMatch:
                self.displayMatch(True, self.teams[self.teamIndex], self.teams[self.opponentIndex])
            else:
                self.displayMatch(True, self.teams[self.opponentIndex], self.teams[self.teamIndex])
        elif self.status == 210 or self.status == 310:
            self.pickPlayers(True)
        elif self.status == 400:
            if self.isHomeMatch:
                responseOptions = self.htmlPlayMatch(self.teams[self.teamIndex], self.teams[self.opponentIndex])
            else:
                responseOptions = self.htmlPlayMatch(self.teams[self.opponentIndex], self.teams[self.teamIndex])
            # print('responseOptions {}'.format(responseOptions))
        elif self.status == 410:
            if self.isHomeMatch:
                self.applyPoints(self.teams[self.teamIndex], self.teams[self.opponentIndex], self.homeScore, self.awayScore)
            else:
                self.applyPoints(self.teams[self.opponentIndex], self.teams[self.teamIndex], self.homeScore, self.awayScore)

            # Calculate the gate money.
            if self.isHomeMatch:
                self.gateMoney = (9000 + (15 - self.teamIndex - self.opponentIndex) * 500) * (5 - self.division) + random.randint(0, 1000)
                if abs(self.teams[self.teamIndex].pts - self.teams[self.opponentIndex].pts) < 4:
                    self.gateMoney += (5 - self.division) * 3000
            else:
                self.gateMoney = 0

            # Decided the fixtures for the league was at half time of the playmatch.
            self.decideFixtures(self.opponentIndex)

            self.rest()
            self.sortDivision()

            # Store the data for progress.
            if self.isHomeMatch:
                week = 0
                if self.homeScore == self.awayScore:
                    self.homeDraws += 1
                elif self.homeScore > self.awayScore:
                    self.homeWins += 1
                else:
                    self.homeLoses += 1
                self.homeFor += self.homeScore
                self.homeAgainst += self.awayScore
            else:
                week = 256
                if self.homeScore == self.awayScore:
                    self.awayDraws += 1
                elif self.awayScore > self.homeScore:
                    self.awayWins += 1
                else:
                    self.awayLoses += 1
                self.awayFor += self.awayScore
                self.awayAgainst += self.homeScore
            if self.homeScore == self.awayScore:
                week |= 64
            elif (self.isHomeMatch and self.homeScore > self.awayScore) or (not self.isHomeMatch and self.homeScore < self.awayScore):
                week |= 128
            week += self.teamIndex
            self.weeks.append(week)
            self.wait(True)
        elif self.status == 430:
            self.html = ''
            self.displayLeague()
            self.wait(True)
        elif self.status == 440:
            self.htmlMarketPart1()
        elif self.status == 445:
            self.htmlMarketPart2()
        elif self.status == 450:
            self.report()
            self.wait(True)
        elif self.status == 460:
            self.progress()
            self.wait(True)
        elif self.status == 470:
            self.playerCaps()
            self.wait(True)
        elif self.status == 1000:
            self.endSeason(True)
        else:
            self.html = '<p>Error Help.</p><p>status = {}</p>'.format(self.status)




        return responseOptions



    def findLeagueOpponent(self):
        ''' Find the opponent for the next league match. '''
        print('findLeagueOpponent()')
        self.team.isPlayedHome = True
        self.team.isPlayedAway = True
        while True:
            self.opponentIndex = random.randint(0, 15)
            self.isHomeMatch = (self.numMatches & 1) == 1
            if self.isHomeMatch:
                if self.teams[self.opponentIndex].isPlayedHome == False:
                    self.teams[self.opponentIndex].isPlayedHome = True
                    break;
            else:
                if self.teams[self.opponentIndex].isPlayedAway == False:
                    self.teams[self.opponentIndex].isPlayedAway = True
                    break;
        # Debugging only.
        if self.isHomeMatch:
            print('Home match against {}'.format(self.teams[self.opponentIndex].name))
        else:
            print('Away match against {}'.format(self.teams[self.opponentIndex].name))



    def playWeek(self):
        ''' This is the block of code that was after the menu in the week loop of the BBC Basic version. Line 740 onward.'''
        self.numMatches += 1

        # Decide and play any cup matches.
        self.activeCup = None
        if self.numMatches % 6 == 2:
            # League Cup.
            if self.leagueCup.isIn:
                self.activeCup = self.leagueCup
                self.status = 200
                self.subStatus = -1
        if self.numMatches % 6 == 4:
            # FA Cup.
            if self.faCup.isIn:
                self.activeCup = self.faCup
                self.status = 200
                self.subStatus = -1
        if self.numMatches % 6 == 0 or (self.numMatches % 6 == 3 and self.args.debug):
            # European Cup.
            if self.europeanCup != None:
                if self.europeanCup.isIn:
                    self.activeCup = self.europeanCup
                    self.status = 200
                    self.subStatus = -1

        if self.activeCup != None:

            while True:
                while True:
                    ansi.doCls()
                    self.playCupMatch()
                    keyPress = self.getKeyboardCharacter(['c', '\t'])
                    if keyPress == '\t':
                        break;
                    # Pick the player.
                    self.pickPlayers()

                if self.isHomeMatch:
                    self.playMatch(self.teams[self.teamIndex], self.cupTeam, 0.5, 0)
                else:
                    self.playMatch(self.cupTeam, self.teams[self.teamIndex], 0.5, 0)
                self.playerEngergy()
                self.playerInjured()

                self.reportCupMatch()
                self.wait()
                if self.homeScore != self.awayScore:
                    break;

        # Choose an opponent for the league match.
        self.findLeagueOpponent()

        # Let the player select the players for the team.
        while True:
            ansi.doCls()
            print('Division {}'.format(self.division))
            if self.isHomeMatch:
                self.displayMatch(True, self.teams[self.teamIndex], self.teams[self.opponentIndex])
            else:
                self.displayMatch(True, self.teams[self.opponentIndex], self.teams[self.teamIndex])
            keyPress = self.getKeyboardCharacter(['c', '\t'])
            if keyPress == '\t':
                break;
            # Pick the player.
            self.pickPlayers()

        ansi.doCursorUp(2)
        print(ansi.ERASE_LINE)
        print(ansi.ERASE_LINE)

        # Play the match.
        if self.isHomeMatch:
            playerGoals, opponentGoals = self.playMatch(self.teams[self.teamIndex], self.teams[self.opponentIndex], 0.5, 0)
            self.applyPoints(self.teams[self.teamIndex], self.teams[self.opponentIndex], playerGoals, opponentGoals)
        else:
            opponentGoals, playerGoals = self.playMatch(self.teams[self.opponentIndex], self.teams[self.teamIndex], 0.5, 0)
            self.applyPoints(self.teams[self.opponentIndex], self.teams[self.teamIndex], opponentGoals, playerGoals)

        # Calculate the gate money.
        if self.isHomeMatch:
            self.gateMoney = (9000 + (15 - self.teamIndex - self.opponentIndex) * 500) * (5 - self.division) + random.randint(0, 1000)
            if abs(self.teams[self.teamIndex].pts - self.teams[self.opponentIndex].pts) < 4:
                self.gateMoney += (5 - self.division) * 3000
        else:
            self.gateMoney = 0

        # PROCPLAYERS
        self.playerEngergy()
        self.playerInjured()
        # Decided the fixtures for the league was at half time of the playmatch.
        self.decideFixtures(self.opponentIndex)

        self.wait()

        self.rest()
        self.sortDivision()

        # Store the data for progress.
        if self.isHomeMatch:
            week = 0
            if self.homeScore == self.awayScore:
                self.homeDraws += 1
            elif self.homeScore > self.awayScore:
                self.homeWins += 1
            else:
                self.homeLoses += 1
            self.homeFor += self.homeScore
            self.homeAgainst += self.awayScore
        else:
            week = 256
            if self.homeScore == self.awayScore:
                self.awayDraws += 1
            elif self.awayScore > self.homeScore:
                self.awayWins += 1
            else:
                self.awayLoses += 1
            self.awayFor += self.awayScore
            self.awayAgainst += self.homeScore
        if playerGoals == opponentGoals:
            week |= 64
        elif playerGoals > opponentGoals:
            week |= 128
        week += self.teamIndex
        self.weeks.append(week)

        self.wait()

        ansi.doCls()
        self.displayLeague()
        self.wait()

        self.market()
        self.report()
        self.wait()
        self.progress()
        self.wait()
        ansi.doCls()
        self.playerCaps()
        self.wait()



    def applyPoints(self, home, away, homeGoals, awayGoals):
        ''' Apply the points to the league. '''
        home.numHomeGames += 1
        if homeGoals == awayGoals:
            home.pts += 1
            away.pts += 1
            home.draw += 1
            away.draw += 1
        else:
            if homeGoals > awayGoals:
                home.pts += 3
                home.win += 1
                away.lost += 1
            else:
                away.pts += 3
                home.lost += 1
                away.win += 1
            home.difference += homeGoals - awayGoals
            away.difference += awayGoals - homeGoals



    def playerEngergy(self):
        ''' Replacement for PROCRESET (line 3200) in the BBC Basic version. '''
        self.teams[self.teamIndex].energy = 0
        for player in self.players:
            if player.inSquad:
                if player.inTeam:
                    player.energy -= random.randint(1, 2)
                    if player.energy < 1:
                        player.energy = 1
                    self.teams[self.teamIndex].energy += player.energy
                    player.caps += 1
                else:
                    player.energy += 5 + random.randint(0, 4)
                    if player.energy > 20:
                        player.energy = 20



    def playerInjured(self):
        '''
        Replacement for PROCINJ (line 5100) in the BBC Basic version.
        This gives players an injury.
        '''
        player = random.randint(0, 25)
        if self.players[player].injured:
            print('{}No injuries.{}'.format(ansi.GREEN, ansi.RESET_ALL))
            self.html += 'No injuries.'
            return
        self.dropPlayer(player)
        self.players[player].injured = True
        if self.players[player].inSquad:
            print('{}{} has been injured.{}'.format(ansi.RED, self.players[player].name, ansi.RESET_ALL))
            self.html += '{} has been injured.'.format(self.players[player].name)
            self.numInjured += 1
        else:
            print('{}No injuries.{}'.format(ansi.GREEN, ansi.RESET_ALL))
            self.html += 'No injuries.'



    def playerFit(self):
        ''' This was part of PROCPROGRESS in the BBC Basic version. '''
        extraStyle = ' border-top: 3px solid purple; padding-top: 15px;'
        count = 0
        numInjured = self.numInjured
        for player in self.players:
            if player.injured:
                if player.inSquad:
                    count += 1
                    if count == numInjured:
                        extraStyle += ' border-bottom: 3px solid purple; padding-bottom: 15px;'
                        # print('extraStyle = {}'.format(extraStyle))
                if random.randint(1, 3) == 1:
                    player.injured = False
                    if player.inSquad:
                        message = '{} is fit.'.format(player.name)
                        print('{}┃{}{:>2}{} {:<35}{}┃{}'.format(ansi.MAGENTA, ansi.WHITE, count, ansi.GREEN, message, ansi.MAGENTA, ansi.RESET_ALL))
                        self.html += '<tr><td style="text-align: right; border-left: 3px solid purple;{}";>{}</td><td colspan="4" style="color: green; border-right: 3px solid purple;{}";>{}</td></tr>'.format(extraStyle, count, extraStyle, message)
                        extraStyle = ''
                        self.numInjured -= 1
                        if self.numInjured < 0:
                            self.numInjured = 0
                else:
                    if player.inSquad:
                        message = '{} is injured.'.format(player.name)
                        print('{}┃{}{:>2}{} {:<35}{}┃{}'.format(ansi.MAGENTA, ansi.WHITE, count, ansi.RED, message, ansi.MAGENTA, ansi.RESET_ALL))
                        self.html += '<tr><td style="text-align: right; border-left: 3px solid purple;{}";>{}</td><td colspan="4" style="color: red; border-right: 3px solid purple;{}";>{}</td></tr>'.format(extraStyle, count, extraStyle, message)
                        extraStyle = ''
        print('{}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{}'.format(ansi.MAGENTA, ansi.RESET_ALL))



    def displaySquad(self):
        ''' Replacement for PROCPTEAM (line 2130) in the BBC Basic version. '''
        print('   Player        Skill Energy')
        self.html = '<table>'
        self.html += '<tr><td colspan="2">Player</td><td>Skill</td><td>Energy</td>'
        for player in self.players:
            if player.inSquad:
                player.writeRow()
                self.html += player.htmlRow()
        self.html += '</table>'



    def pickPlayers(self, isGraphical=False):
        ''' Replacement for PROCPICK (line 2260) in the BBC Basic version. '''
        if isGraphical:
            self.displaySquad()
            if self.numTeam <= 11:
                self.html += '<p>{} Picked, {} Squad, {} Injured.</p>'.format(self.numTeam, self.numSquad, self.numInjured)
                self.html += '<p><a href="app:?response=b">Back to Match</a></p>'
            else:
                self.html += '<p>Select Player to drop.</a>'
        else:
            while True:
                ansi.doCls()
                self.displaySquad()
                if self.numTeam <= 11:
                    number = self.enterNumber('>')
                    if number == 0:
                        break;
                    if number >= 1 and number <= 26:
                        number -= 1
                        if self.players[number].inSquad:
                            if self.players[number].inTeam:
                                self.dropPlayer(number)
                            else:
                                self.addPlayer(number)
                else:
                    number = self.enterNumber('Enter Player to Drop ')
                    if number >= 1 and number <= 26:
                        self.dropPlayer(number - 1)



    def dropPlayer(self, index):
        ''' Replacement for PROCDROP (line 1630) in the BBC Basic version. '''
        player = self.players[index]
        if player.inTeam == False:
            return
        player.inTeam = False
        if player.position == Player.DEFENSE:
            self.team.defence -= player.skill
        elif player.position == Player.MIDFIELD:
            self.team.midfield -= player.skill
        else:
            self.team.attack -= player.skill
        self.team.energy -= player.energy
        self.numTeam -= 1
        self.formation[player.position] -= 1
        self.team.formation = '{}-{}-{}'.format(self.formation[Player.DEFENSE]-1, self.formation[Player.MIDFIELD], self.formation[Player.ATTACK])



    def addPlayer(self, index):
        ''' Replacement for PROCIN (line 1580) in the BBC Basic version. '''
        player = self.players[index]
        if player.inTeam:
            return
        if player.injured:
            return
        player.inTeam = True
        if player.position == Player.DEFENSE:
            self.team.defence += player.skill
        elif player.position == Player.MIDFIELD:
            self.team.midfield += player.skill
        else:
            self.team.attack += player.skill
        self.team.energy += player.energy
        self.numTeam += 1
        self.formation[player.position] += 1
        self.team.formation = '{}-{}-{}'.format(self.formation[Player.DEFENSE]-1, self.formation[Player.MIDFIELD], self.formation[Player.ATTACK])



    def sellPlayer(self):
        ''' Replacement for PROCSELL (line 1950) in the BBC Basic version. '''
        ansi.doCls()
        self.displaySquad()
        print('Enter <RETURN> to return to menu.')
        print('Else enter player number to be sold')
        playerNumber = self.enterNumber('>')
        if playerNumber >= 1 and playerNumber <= 26:
            playerNumber -= 1
            if self.players[playerNumber].inSquad:
                price = int((self.players[playerNumber].skill + random.uniform(0, 1)) * 5000 * (5 - self.division))
                print('You are offered £{:,.2f}'.format(price))
                print('Do you accept (Y/N)?')
                if self.getYesNo():
                    self.numSquad -= 1
                    self.dropPlayer(playerNumber)
                    self.players[playerNumber].inSquad = False
                    self.money += price
                    self.moneyMessage += self.financialLine(self.players[playerNumber].name + ' sold', price, 0) + "\n";
            else:
                print('On range')
            self.wait()



    def htmlSellPlayerPart1(self):
        self.displaySquad()
        self.html += '<p><a href="app:?response=c">Click Here to return to main menu.</a></p>'
        self.html += '<p>Otherwise click player to be sold.</p>'



    def htmlSellPlayerPart2(self):
        playerNumber = self.subStatus - 1
        if self.players[playerNumber].inSquad:
            self.html += '<p>{}</p>'.format(self.players[playerNumber].name)
            price = int((self.players[playerNumber].skill + random.uniform(0, 1)) * 5000 * (5 - self.division))
            self.subStatus2 = price
            self.html += '<p>You are offered £{:,.2f}</p>'.format(price)
            self.html += 'Do you accept ( <a href="app:?response=y">Yes</a> / <a href="app?response=n">No</a> ) ?'



    def htmlSellPlayerPart3(self):
        playerNumber = self.subStatus - 1
        price = self.subStatus2

        self.numSquad -= 1
        self.dropPlayer(playerNumber)
        self.players[playerNumber].inSquad = False
        self.money += price
        self.moneyMessage += self.financialLine(self.players[playerNumber].name + ' sold', price, 0) + "\n";



    def market(self):
        ''' Replacement for PROCMARKET (line 3330) in the BBC Basic version. '''
        if self.numSquad >= 18:
            # ansi.doCls()
            print('{}F.A. rules state that one team may not have more that 18 players. You already have 18 players therefore you may not buy another.{}'.format(ansi.RED, ansi.RESET_ALL))
        else:
            while True:
                player = random.randint(0, 25)
                if self.players[player].inSquad == False:
                    break;
            # ansi.doCls()
            # Skill Boost.  This made the game too easy.
            if random.randint(1, 5) == 1:
                self.players[player].skill = max(self.players[player].skill, random.randint(1, 5) + (1 if self.division <= 2 else 0))
            if self.players[player].position == Player.DEFENSE:
                print('Defence')
            elif self.players[player].position == Player.MIDFIELD:
                print('Mid-field')
            else:
                print('Attack')
            self.players[player].writeRow(5000 * (5 - self.division))
            print('You have £{:,.2f}'.format(self.money))
            bid = self.enterNumber('Enter your bid: ')
            if bid <= 0:
                return
            price = self.players[player].skill * (5000 * (5 - self.division)) + random.randint(1, 10000) - 5000
            if bid > self.money:
                print('{}You do not have enough money{}'.format(ansi.RED, ansi.RESET_ALL))
            elif bid > price:
                print('{}{} is added to your squad.{}'.format(ansi.GREEN, self.players[player].name, ansi.RESET_ALL))
                self.numSquad += 1
                self.players[player].inSquad = True
                self.money -= bid
                self.moneyMessage += self.financialLine(self.players[player].name + ' bought', 0, bid) + "\n";
                if self.players[player].injured:
                    self.numInjured += 1
            else:
                if bid > 0:
                    print('{}Your bid of £{:,.2f} is turned down.{}'.format(ansi.RED, bid, ansi.RESET_ALL))
        self.wait()



    def htmlMarketPart1(self):
        if self.numSquad >= 18:
            self.html = '<p>F.A. rules state that one team may not have more that 18 players. You already have 18 players therefore you may not buy another.</p>'
            self.wait(True)
        else:
            while True:
                player = random.randint(0, 25)
                if self.players[player].inSquad == False:
                    break;
            # Skill Boost.  This made the game too easy.
            if random.randint(1, 5) == 1:
                self.players[player].skill = max(self.players[player].skill, random.randint(1, 5) + (1 if self.division <= 2 else 0))
            if self.players[player].position == Player.DEFENSE:
                self.html = '<p>Defence</p>'
            elif self.players[player].position == Player.MIDFIELD:
                self.html = '<p>Mid-field</p>'
            else:
                self.html = '<p>Attack</p>'
            self.html += '<table>'
            self.html += self.players[player].htmlRow(5000 * (5 - self.division))
            self.html += '</table>'
            self.html += '<p>You have £{:,.2f}</p>'.format(self.money)
            self.html += '<form action="app:" method="get">'
            self.html += '<p>Enter your bid <input type="text" name="bid" /></p>'
            self.html += '<p><input type="submit" name="button" value="Bid" /></p>'
            self.html += '</form>'
            # self.wait(True)
            self.subStatus = player



    def htmlMarketPart2(self):
        player = self.subStatus
        bid = self.subStatus2
        price = self.players[player].skill * (5000 * (5 - self.division)) + random.randint(1, 10000) - 5000
        if bid > self.money:
            self.html += '<p>You do not have enough money</p>'
            print('You do not have enough money.')
        elif bid > price:
            self.html += '<p>{} is added to your squad.'.format(self.players[player].name)
            print('{} is added to your squad.'.format(self.players[player].name))

            self.numSquad += 1
            self.players[player].inSquad = True
            self.money -= bid
            self.moneyMessage += self.financialLine(self.players[player].name + ' bought', 0, bid) + "\n";
            if self.players[player].injured:
                self.numInjured += 1
        else:
            if bid > 0:
                self.html += '<p>Your bid of £{:,.2f} is turned down.</p>'.format(bid)
                print('Your bid is turned down.')
            else:
                print('No bid.')
        self.wait(True)



    def report(self):
        ''' Replacement for PROCREPORT ( line 3970 ) in the BBC Basic version. '''
        self.html = '<h1>Financial Report</h1>'
        self.html += '<table>'
        if self.gateMoney > 0:
            print(self.financialLine('Gate Money', self.gateMoney, 0))
            self.html += '<tr style="color: green;"><td>Gate Money</td><td style="text-align: right;">£{:,.0f}</td><tr>'.format(self.gateMoney)
            self.money += self.gateMoney
        print(self.financialLine('Paid to Squad', 0, self.numSquad * 500 * (5 - self.division)))
        self.html += '<tr style="color: red;"><td>Paid to Squad</td><td style="text-align: right;">(£{:,.0f})</td><tr>'.format(self.numSquad * 500 * (5 - self.division))
        self.money -= self.numSquad * 500 * (5 - self.division)
        if self.moneyMessage != '':
            print(self.moneyMessage, end = '')
            messages = self.moneyMessage.split('\n')
            for message in messages:
                if len(message) >= 39:
                    if message[:5] == ansi.GREEN:
                        self.html += '<tr style="color: green">'
                    else:
                        self.html += '<tr style="color: red">'
                    self.html += '<td>{}</td><td style="text-align: right;">{}</td></tr>'.format(message[5:30], message[34:45])
        if self.debt > 0:
            nInterest = int (self.debt * 0.005)
            print(self.financialLine('Interest', 0, nInterest))
            self.html += '<tr style="color: red;"><td>Interest</td><td style="text-align: right;">(£{:,.0f})</td><tr>'.format(nInterest)
            self.money = self.money - nInterest
        print('━' * 40)
        self.html += '<tr><td colspan="2"><hr /><td></tr>'
        if self.money - self.debt >= self.moneyStart:
            print(self.financialLine('Profit', self.money - self.debt - self.moneyStart, 0))
            self.html += '<tr style="color: green;"><td>Profit</td><td style="text-align: right;">£{:,.0f}</td><tr>'.format(self.money - self.debt - self.moneyStart)
        else:
            print(self.financialLine('Loss', 0, self.moneyStart - self.money + self.debt))
            self.html += '<tr style="color: red;"><td>Loss</td><td style="text-align: right;">(£{:,.0f})</td><tr>'.format(self.moneyStart - self.money + self.debt)
        print('━' * 40)
        self.html += '<tr><td colspan="2"><hr /><td></tr>'

        if self.money < 0:
             self.debt -= self.money
             self.money = 0
        print(self.financialLine('Cash', self.money, 0))
        print(self.financialLine('Debt', 0, self.debt))
        self.html += '<tr style="color: green;"><td>Cash</td><td style="text-align: right;">£{:,.0f}</td><tr>'.format(self.money)
        self.html += '<tr style="color: red;"><td>Debt</td><td style="text-align: right;">£{:,.0f}</td><tr>'.format(self.debt)
        self.html += '</table>'

        # Reset the counters.
        self.moneyStart = self.money - self.debt
        self.moneyMessage = ''



    def financialLine(self, title, profit, loss):
        ''' Build a line of financial information. '''
        if profit - loss >= 0:
            description = '£{:,.0f}'.format(profit - loss)
            return '{}{:<25} {:>13} {}'.format(ansi.GREEN, title, description, ansi.RESET_ALL)
        description = '(£{:,.0f})'.format(loss - profit)
        return '{}{:<25}{:>15}{}'.format(ansi.RED, title, description, ansi.RESET_ALL)



    def bank(self):
        ''' Replacement for PROCLEND ( line 4170 ) in the BBC Basic version. '''
        ansi.doCls()
        print('Bank')
        print('You have £{:,.2f}'.format(self.money))
        if self.debt > 0:
            print('You owe £{:,.2f}'.format(self.debt))
        else:
            print('In Bank £{:,.2f}'.format(-self.debt))
        print('Do you want to Deposit, Withdraw or Exit (D/W/E)?')
        keyPress = self.getKeyboardCharacter(['d', 'w', 'e'])
        if keyPress == 'e':
            return
        if keyPress == 'd':
            print('Deposit')
        else:
            print('Withdraw')
        amount = self.enterNumber('Enter the amount >')
        if keyPress == 'd':
            amount = -amount
        self.money += amount
        self.debt += amount
        MAX_DEBT = 2e6 # 1e6
        if self.debt > MAX_DEBT:
            print('You can not have that much')
            self.money -= self.debt - MAX_DEBT
            self.debt = MAX_DEBT
        if self.money < 0:
             self.debt -= self.money
             self.money = 0
        print('You have £{:,.2f}'.format(self.money))
        if self.debt > 0:
            print('You owe £{:,.2f}'.format(self.debt))
        else:
            print('In Bank £{:,.2f}'.format(-self.debt))
        self.wait()



    def htmlBankPart1(self):
        self.html = '<h1>Bank</h1>'
        self.html += '<form action="app:" method="get">'
        self.html += '<p>You have £{:,.2f}</p>'.format(self.money)
        if self.debt > 0:
            self.html += '<p>You owe £{:,.2f}</p>'.format(self.debt)
        else:
            self.html += '<p>In Bank £{:,.2f}</p>'.format(-self.debt)
        self.html += '<p>Do you want to Deposit or Withdraw? <select name="sign"><option value="0">Withdraw</option><option value="1">Deposit</option></select></p>'
        self.html += '<p>Enter the amount <input type="text" name="amount" /></p>'
        self.html += '<p><input type="submit" name="transact" value="Transact" /></p>'
        self.wait(True)



    def htmlBankPart2(self):
        amount = self.subStatus
        self.money += amount
        self.debt += amount
        MAX_DEBT = 2e6 # 1e6
        if self.debt > MAX_DEBT:
            self.html += '<p>You can not have that much.</p>'
            self.money -= self.debt - MAX_DEBT
            self.debt = MAX_DEBT
        if self.money < 0:
             self.debt -= self.money
             self.money = 0
        self.html += '<p>You have £{:,.2f}</p>'.format(self.money)
        if self.debt > 0:
            self.html += '<p>You owe £{:,.2f}</p>'.format(self.debt)
        else:
            self.html += '<p>In Bank £{:,.2f}</p>'.format(-self.debt)
        self.wait(True)



    def playerCaps(self):
        ''' This was part of PROCPROGRESS (line 6190) in the BBC Basic version. '''
        playersByCaps = sorted(self.players, key=lambda Player: Player.caps, reverse=True)
        print('{}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{}'.format(ansi.MAGENTA, ansi.RESET_ALL))
        print('{}┃{}   Player        Position  Caps Goals {}┃{}'.format(ansi.MAGENTA, ansi.RESET_ALL, ansi.MAGENTA, ansi.RESET_ALL))
        self.html = '<h1>Player Appearances</h1>'
        self.html += '<table>'
        self.html += '<tr><td style="border-top: 3px solid purple; border-left: 3px solid purple;"></td><td style="border-top: 3px solid purple;">Player</td><td style="border-top: 3px solid purple;">Position</td><td style="border-top: 3px solid purple;">Apperances</td><td style="border-top: 3px solid purple; border-right: 3px solid purple;">Goals</td></tr>'
        for index in range(11):
            player = playersByCaps[index]
            if index == 10:
                extraStyle = ' border-bottom: 3px solid purple; padding-bottom: 15px;'
            else:
                extraStyle = ''
            if player.injured:
                playerColour = ansi.RED
                htmlColour = ' color: red;'
            elif player.inTeam:
                playerColour = ansi.GREEN
                htmlColour = ' color: green;'
            else:
                playerColour = ansi.RESET_ALL
                htmlColour = ''
            print('{}┃{}{:>2}{} {:<14}{:<9}{:>5}{:>6} {}┃{}'.format(ansi.MAGENTA, ansi.WHITE, index + 1, playerColour, player.name, player.getPosition(), player.caps, player.goals, ansi.MAGENTA, ansi.RESET_ALL))
            self.html += '<tr><td style="text-align: right; border-left: 3px solid purple;{}">{}</td><td style="{}{}">{}</td><td style="{}{}">{}</td><td style="text-align: right;{}{}">{}</td><td style="text-align: right; border-right: 3px solid purple;{}{}">{}</td></tr>'.format(extraStyle, index + 1, extraStyle, htmlColour, player.name, extraStyle, htmlColour, player.getPosition(), extraStyle, htmlColour, player.caps, extraStyle, htmlColour, player.goals)

        # Top Scorers.
        playersByGoals = sorted(self.players, key=lambda Player: Player.goals, reverse=True)
        print('{}┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫{}'.format(ansi.MAGENTA, ansi.RESET_ALL))
        print('{}┃{}   Player        Position  Caps Goals {}┃{}'.format(ansi.MAGENTA, ansi.RESET_ALL, ansi.MAGENTA, ansi.RESET_ALL))
        for index in range(5):
            player = playersByGoals[index]
            if index == 0:
                extraStyle = ' border-top: 3px solid purple; padding-top: 15px;'
            elif index == 4:
                extraStyle = ' border-bottom: 3px solid purple; padding-bottom: 15px;'
            else:
                extraStyle = ''
            if player.injured:
                playerColour = ansi.RED
                htmlColour = ' color: red;'
            elif player.inTeam:
                playerColour = ansi.GREEN
                htmlColour = ' color: green;'
            else:
                playerColour = ansi.RESET_ALL
                htmlColour = ''
            if player.goals > 0:
                print('{}┃{}{:>2}{} {:<14}{:<9}{:>5}{:>6} {}┃{}'.format(ansi.MAGENTA, ansi.WHITE, index + 1, playerColour, player.name, player.getPosition(), player.caps, player.goals, ansi.MAGENTA, ansi.RESET_ALL))
                self.html += '<tr><td style="text-align: right; border-left: 3px solid purple;{}">{}</td><td style="{}{}">{}</td><td style="{}{}">{}</td><td style="text-align: right;{}{}">{}</td><td style="text-align: right; border-right: 3px solid purple;{}{}">{}</td></tr>'.format(extraStyle, index + 1, extraStyle, htmlColour, player.name, extraStyle, htmlColour, player.getPosition(), extraStyle, htmlColour, player.caps, extraStyle, htmlColour, player.goals)
        print('{}┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫{}'.format(ansi.MAGENTA, ansi.RESET_ALL))

        self.playerFit()

        self.html += '</table>'



    def displayMatch(self, isLeague, homeTeam, awayTeam):
        ''' Replacement for PROCDISPLAY in the BBC Basic version. '''
        print('   {}{:^18}{}{:^18}{}'.format(homeTeam.colour, homeTeam.name, awayTeam.colour, awayTeam.name, ansi.RESET_ALL))
        if isLeague:
            print('Pos{:^18}{:^18}'.format(homeTeam.position, awayTeam.position))
        print('Eng{:^18}{:^18}'.format(homeTeam.energy // 10, awayTeam.energy // 10))
        print('Mor{:^18}{:^18}'.format(homeTeam.moral, awayTeam.moral))
        print('For{:^18}{:^18}'.format(homeTeam.formation, awayTeam.formation))
        print('Def{:^18}{:^18}'.format(homeTeam.defence, awayTeam.defence))
        print('Mid{:^18}{:^18}'.format(homeTeam.midfield, awayTeam.midfield))
        print('Att{:^18}{:^18}'.format(homeTeam.attack, awayTeam.attack))
        print()
        print('{} Picked, {} Squad, {} Injured.'.format(self.numTeam, self.numSquad, self.numInjured))
        print('Press C to change team')
        print('Press TAB to play match.')

        self.html += '<table>'
        self.html += '<tr><td style="text-align: center;"></td><td style="text-align: center;">{}</td><td style="text-align: center;">{}</td></tr>'.format(homeTeam.name, awayTeam.name)
        if isLeague:
            self.html += '<tr><td style="text-align: center;">Position</td><td style="text-align: center;">{}</td><td style="text-align: center;">{}</td></tr>'.format(homeTeam.position, awayTeam.position)
        self.html += '<tr><td style="text-align: center;">Energy</td><td style="text-align: center;">{}</td><td style="text-align: center;">{}</td></tr>'.format(homeTeam.energy // 10, awayTeam.energy // 10)
        self.html += '<tr><td style="text-align: center;">Moral</td><td style="text-align: center;">{}</td><td style="text-align: center;">{}</td></tr>'.format(homeTeam.moral, awayTeam.moral)
        self.html += '<tr><td style="text-align: center;">Formation</td><td style="text-align: center;">{}</td><td style="text-align: center;">{}</td></tr>'.format(homeTeam.formation, awayTeam.formation)
        self.html += '<tr><td style="text-align: center;">Defence</td><td style="text-align: center;">{}</td><td style="text-align: center;">{}</td></tr>'.format(homeTeam.defence, awayTeam.defence)
        self.html += '<tr><td style="text-align: center;">Midfield</td><td style="text-align: center;">{}</td><td style="text-align: center;">{}</td></tr>'.format(homeTeam.midfield, awayTeam.midfield)
        self.html += '<tr><td style="text-align: center;">Attack</td><td style="text-align: center;">{}</td><td style="text-align: center;">{}</td></tr>'.format(homeTeam.attack, awayTeam.attack)
        self.html += '</table>'
        self.html += '<p>{} Picked, {} Squad, {} Injured.</p>'.format(self.numTeam, self.numSquad, self.numInjured)
        self.html += '<p><a href="app:?response=c">Press C to change team.</a></p>'
        self.html += '<p><a href="app:?response=t">Press TAB to play match.</a></p>'



    def wait(self, isGraphical=False):
        ''' Replacement for PROCWAIT in the BBC Basic version. '''
        if isGraphical:
            self.html += '<p><a href="app:?response=c">Click to continue</a></p>'
        else:
            print('{}{}{} Press SPACE to continue {}{}'.format(ansi.BACKGROUND_BLUE, ansi.YELLOW, '━' * 7, '━' * 8, ansi.RESET_ALL))
            self.getKeyboardCharacter([' '])
            print('{}{}'.format(ansi.getCursorUp(1), ansi.ERASE_LINE), end = '\r')



    def displayLeague(self):
        ''' Replacement for PROCLEAGUE in the BBC Basic version. '''
        print('Division {}'.format(self.division))
        print('   Team             W  D  L Pts Dif')
        self.html += '<h1>Division {}</h1>'.format(self.division)
        self.html += '<table>'
        self.html += '<tr><td></td><td>Team</td><td>Won</td><td>Draw</td><td>Lost</td><td>Pts</td><td>Dif</td><tr>'
        for team in self.teams:
            team.writeTableRow(self.args.debug)
            self.html += team.htmlTableRow(self.args.debug)
        print('Matches Played: {}'.format(self.numMatches))
        print('{} position: {}'.format(self.team.getColouredName(), self.teamIndex+1))
        self.html += '</table>'
        self.html += '<p style="margin-bottom: 0px;">Matches Played: {}</p>'.format(self.numMatches)
        self.html += '<p style="margin-top: 0px;">{} position: {}</p>'.format(self.team.name, self.teamIndex+1)



    def sortDivision(self):
        ''' Replacement for PROCSORT in the BBC Basic version. '''
        self.teams = sorted(self.teams, key=lambda Team: (Team.pts, Team.difference), reverse=True)
        position = 1
        for team in self.teams:
            team.position = position
            if team.name == self.teamName:
                self.teamIndex = position - 1
                self.team = team
            position += 1



    def newGame(self, isGraphical=False):
        ''' Initialise a new game. '''
        if isGraphical == False:
            self.pickTeam()

        # Initialise variables.
        self.numMatches = 0
        self.money = 50000
        self.debt = 200000
        self.weeks = []
        self.MATCHES_PER_SEASON = 30
        if self.args.debug:
            self.MATCHES_PER_SEASON = 4

        # Initialise the players.
        self.players = []
        for index in range(1, 27):
            player = Player()
            player.getPlayer(index)
            player.skill = random.randint(1, 5)
            player.energy = random.randint(1, 20)
            self.players.append(player)
        for index in range(4):
            player = random.randint(0, 25)
            self.players[player].skill = 5

        # Pick 12 players.
        self.numSquad = 12
        for index in range(self.numSquad):
            player = random.randint(0, 25)
            while self.players[player].inSquad:
                player = random.randint(0, 25)
            self.players[player].inSquad = True

        # Initialise the teams.
        self.teams = None
        self.division = 4
        self.setTeamsForDivision([])
        self.sortDivision()

        # Pick a default selection of players.
        self.numTeam = 0
        self.numInjured = 0
        for index in range(26):
            if self.players[index].inSquad:
                if self.numTeam < 11:
                    self.addPlayer(index)



    def setTeamsForDivision(self, existingNames):
        ''' Replacement for PROCDIVISON (line 3520) in the BBC Basic version. '''
        if self.teams == None:
            self.teams = []
            for nTeam in range(16):
                team = Team()
                team.name = ''
                self.teams.append(team)
            self.teams[0].name = self.teamName
            self.teams[0].colour = self.teamColour
            self.teams[0].position = 1
        division = self.division

        # Record the existing team names.
        for team in self.teams:
            if team.name != '':
                existingNames.append(team.name)

        newTeam = 1
        for team in self.teams:
            if team.name == '':
                team.getTeam(division, newTeam)
                # Check that this team is unique.
                while team.name in existingNames:
                    newTeam += 1
                    team.getTeam(division, newTeam)

                existingNames.append(team.name)
                newTeam += 1

            if team.name == self.teamName:
                # Initialise the players team.
                team.zero()
            else:
                # Initialise the opponent team.
                team.initialise(self.division)



    def multiRandomInt(self, rndRange, rndNumber):
        ''' Replacement for FNRND() (Line 6640) in the BBC Basic version. '''
        numTotal = 0
        for count in range(rndNumber):
            numTotal += random.randint(1, rndRange)
        return numTotal



    def multiRandom(self, rndRange, rndNumber):
        ''' Replacement of FNRND (Line 6640) in the BBC Basic version. This gives a floating point result.  It is usually expected that rndRange will be '1.0'.'''
        numTotal = 0
        for count in range(rndNumber):
            numTotal += random.uniform(0, rndRange)
        return numTotal



    def pickTeam(self):
        ''' Replacement for PROCPICKTEAM in the BBC Basic version. '''
        division = 1
        while True:
            ansi.doCls()
            print(' 0 More Teams')
            print(' 1 Own Team')
            for index in range(2, 17):
                team = Team()
                team.getTeam(division, index - 1)
                print('{:2} {}'.format(index, team.getColouredName()))
            selectedNumber = self.enterNumber('Enter Team Number ')
            if selectedNumber >= 2 and selectedNumber <= 17:
                team.getTeam(division, selectedNumber - 1)
                self.teamName = team.name
                self.teamColour = team.colour
                break
            if selectedNumber == 1:
                self.teamName = input('Enter Team name ')
                if self.teamName == '':
                    self.teamName = 'Morley Town'
                self.teamColour = ansi.CYAN
                break
            division = 1 + (division & 3)
        print('You manage {}{}{}'.format(self.teamColour, self.teamName, ansi.RESET_ALL))



    def enterNumber(self, message):
        ''' Enter a number at the keyboard. '''
        number = 0
        try:
            message = input(message)
            message = message.replace('k', '000')
            number = int(message)
        except:
            number = 0
        return number



    def getYesNo(self):
        ''' Replacement for FNYES in the BBC Basic version.  Returns True if 'Y' is pressed or False if 'N' is pressed. '''
        character = self.getKeyboardCharacter(['y', 'n'])
        if character == 'y':
            return True
        return False



    def getKeyboardCharacter(self, allowed):
        ''' Return a keyboard character from the allowed characters. '''
        # No Repeat Until in Python.
        # character = modInkey.getwch()
        character = self.keyboard.getKey()
        while not (character in allowed):
            # character = modInkey.getwch()
            character = self.keyboard.getKey()
        self.keyboard.stop()
        return character



    def football(self):
        '''
        Implementation of DEFPROCfootball().
        Display a title.
        This is using 'Box-drawing characters' or 'Line-drawing characters.'
        '''
        print('┏━━             ┃       ┃ ┃   ┏━┳━┓')
        print('┃            ┃  ┃       ┃ ┃   ┃ ┃ ┃' )
        print('┣━━ ┏━┓ ┏━┓ ━╋━ ┣━┓ ━━┓ ┃ ┃   ┃   ┃ ━━┓ ━┳━┓ ━━┓ ┏━┓ ┏━┓ ┏━')
        print('┃   ┃ ┃ ┃ ┃  ┃  ┃ ┃ ┏━┫ ┃ ┃   ┃   ┃ ┏━┃  ┃ ┃ ┏━┫ ┃ ┃ ┣━┛ ┃')
        print('┃   ┗━┛ ┗━┛  ┃  ┗━┛ ┗━┛ ┃ ┃   ┃   ┃ ┗━┛  ┃ ┃ ┗━┛ ┗━┫ ┗━━ ┃')
        print('                                                   ┃')
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')
        print('By Steve Walton BBC BASIC 1982-1989, 2000, Python 2018-2021.')

        self.html += '<pre>'
        self.html += '┏━━             ┃       ┃ ┃   ┏━┳━┓\n'
        self.html += '┃            ┃  ┃       ┃ ┃   ┃ ┃ ┃\n'
        self.html += '┣━━ ┏━┓ ┏━┓ ━╋━ ┣━┓ ━━┓ ┃ ┃   ┃   ┃ ━━┓ ━┳━┓ ━━┓ ┏━┓ ┏━┓ ┏━\n'
        self.html += '┃   ┃ ┃ ┃ ┃  ┃  ┃ ┃ ┏━┫ ┃ ┃   ┃   ┃ ┏━┃  ┃ ┃ ┏━┫ ┃ ┃ ┣━┛ ┃\n'
        self.html += '┃   ┗━┛ ┗━┛  ┃  ┗━┛ ┗━┛ ┃ ┃   ┃   ┃ ┗━┛  ┃ ┃ ┗━┛ ┗━┫ ┗━━ ┃\n'
        self.html += '                                                   ┃\n'
        self.html += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n'
        self.html += 'By Steve Walton BBC BASIC 1982-1989, 2000, Python 2018-2021.\n'
        self.html += '</pre>'



    def save(self, isInteractive):
        ''' Implementation of DEFPROCSAVE (5420) from the BBC Basic version. '''
        outputFile = open('save.game', 'w')

        json.dump(self.numMatches, outputFile)
        outputFile.write('\n')
        json.dump(self.money, outputFile)
        outputFile.write('\n')
        json.dump(self.debt, outputFile)
        outputFile.write('\n')
        json.dump(self.numSquad, outputFile)
        outputFile.write('\n')
        json.dump(self.numTeam, outputFile)
        outputFile.write('\n')
        json.dump(self.numInjured, outputFile)
        outputFile.write('\n')
        json.dump(self.division, outputFile)
        outputFile.write('\n')
        json.dump(self.teamName, outputFile)
        outputFile.write('\n')
        json.dump(self.teamColour, outputFile)
        outputFile.write('\n')
        json.dump(self.formation, outputFile)
        outputFile.write('\n')
        json.dump(self.homeWins, outputFile)
        outputFile.write('\n')
        json.dump(self.homeDraws, outputFile)
        outputFile.write('\n')
        json.dump(self.homeLoses, outputFile)
        outputFile.write('\n')
        json.dump(self.homeFor, outputFile)
        outputFile.write('\n')
        json.dump(self.homeAgainst, outputFile)
        outputFile.write('\n')
        json.dump(self.awayWins, outputFile)
        outputFile.write('\n')
        json.dump(self.awayDraws, outputFile)
        outputFile.write('\n')
        json.dump(self.awayLoses, outputFile)
        outputFile.write('\n')
        json.dump(self.awayFor, outputFile)
        outputFile.write('\n')
        json.dump(self.awayAgainst, outputFile)
        outputFile.write('\n')

        # Save the weeks.
        json.dump(self.weeks, outputFile)
        outputFile.write('\n')

        # Save the players.
        for player in self.players:
            player.dump(outputFile)

        # Save the teams.
        for team in self.teams:
            team.dump(outputFile)

        outputFile.close()

        print('Game Saved.')



    def load(self):
        ''' Implementation of DEFPROCLOAD (line 5530) from the BBC Basic version. '''
        self.MATCHES_PER_SEASON = 30

        inputFile = open('save.game', 'r')

        line = inputFile.readline()
        self.numMatches = json.loads(line)
        line = inputFile.readline()
        self.money = json.loads(line)
        line = inputFile.readline()
        self.debt = json.loads(line)
        line = inputFile.readline()
        self.numSquad = json.loads(line)
        line = inputFile.readline()
        self.numTeam = json.loads(line)
        line = inputFile.readline()
        self.numInjured = json.loads(line)
        line = inputFile.readline()
        self.division = json.loads(line)
        line = inputFile.readline()
        self.teamName = json.loads(line)
        line = inputFile.readline()
        self.teamColour = json.loads(line)
        line = inputFile.readline()
        self.formation = json.loads(line)
        line = inputFile.readline()
        self.homeWins = json.loads(line)
        line = inputFile.readline()
        self.homeDraws = json.loads(line)
        line = inputFile.readline()
        self.homeLoses = json.loads(line)
        line = inputFile.readline()
        self.homeFor = json.loads(line)
        line = inputFile.readline()
        self.homeAgainst = json.loads(line)
        line = inputFile.readline()
        self.awayWins = json.loads(line)
        line = inputFile.readline()
        self.awayDraws = json.loads(line)
        line = inputFile.readline()
        self.awayLoses = json.loads(line)
        line = inputFile.readline()
        self.awayFor = json.loads(line)
        line = inputFile.readline()
        self.awayAgainst = json.loads(line)

        # Load the weeks.
        line = inputFile.readline()
        self.weeks = json.loads(line)

        # Load the players.
        self.players = []
        for index in range(26):
            player = Player()
            player.load(inputFile)
            self.players.append(player)

        # Load the teams.
        self.teams = []
        for index in range(16):
            team = Team()
            team.load(inputFile)
            self.teams.append(team)

        inputFile.close()



    def decideFixtures(self, opponent):
        ''' Replacement for PROCFIXTURES (line 247) in the BBC Basic version. '''
        for team in self.teams:
            team.fixture = 0

        self.teams[self.teamIndex].fixture = -1
        self.teams[opponent].fixture = -1
        for match in range(1, 8):
            while True:
                home = random.randint(0, 15)
                if self.teams[home].fixture == 0:
                    break;
            self.teams[home].fixture = match * 2 - 1
            while True:
                away = random.randint(0, 15)
                if self.teams[away].fixture == 0:
                    break;
            self.teams[away].fixture = match * 2

            # Swap if the away team has fewer home matches.
            if self.teams[home].numHomeGames > self.teams[away].numHomeGames:
                home, away = away, home
                self.teams[home].fixture = match * 2 - 1
                self.teams[away].fixture = match * 2



    def rest(self):
        '''
        Replacement for DEFPROCREST (line 2710) in the BBC Basic version.
        This is play and display the rest of the matches in the league.
        '''
        self.html = '<table>'
        if self.isHomeMatch:
            self.html += '<tr><td style="text-align: right;">{}</td><td style="text-align: center;">{} - {}</td><td>{}</td></tr>'.format(self.teams[self.teamIndex].name, self.homeScore, self.awayScore, self.teams[self.opponentIndex].name)
        else:
            self.html += '<tr><td style="text-align: right;">{}</td><td style="text-align: center;">{} - {}</td><td>{}</td></tr>'.format(self.teams[self.opponentIndex].name, self.homeScore, self.awayScore, self.teams[self.teamIndex].name)
        for match in range(1, 8):
            for index in range(16):
                if self.teams[index].fixture == 2 * match - 1:
                    home = index
                if self.teams[index].fixture == 2 * match:
                    away = index

            homeGoals, awayGoals = self.match(self.teams[home], self.teams[away], 0.5, 0)
            print('{}{:>17}{} {} - {} {}'.format(self.teams[home].colour, self.teams[home].name, ansi.RESET_ALL, homeGoals, awayGoals, self.teams[away].getColouredName()))
            self.html += '<tr><td style="text-align: right;">{}</td><td style="text-align: center;">{} - {}</td><td>{}</td></tr>'.format(self.teams[home].name, homeGoals, awayGoals, self.teams[away].name)
            self.applyPoints(self.teams[home], self.teams[away], homeGoals, awayGoals)
        self.html += '</table>'



    def htmlPlayMatch(self, homeTeam, awayTeam):
        ''' Display the current match status in html. '''
        if self.subStatus == 0:
            # Play the match.
            homeGoals, awayGoals = self.playMatch(homeTeam, awayTeam, 0.5, 0, True)
            self.homeScore = 0
            self.awayScore = 0
            self.homeGoalScorers = ''
            self.awayGoalScorers = ''
        else:
            if self.subStatus in self.homeGoalsTimes:
                self.homeScore += 1
                if homeTeam.name == self.teamName:
                    goalScorer = random.randint(0, len(self.goalScorers)-1)
                    if self.homeGoalScorers == '':
                        self.homeGoalScorers = '{} {}'.format(self.subStatus, self.goalScorers[goalScorer].name)
                    else:
                        self.homeGoalScorers = '{}<br />{} {}'.format(self.homeGoalScorers, self.subStatus, self.goalScorers[goalScorer].name)
                    self.goalScorers[goalScorer].goals += 1
                else:
                    if self.homeGoalScorers == '':
                        self.homeGoalScorers = '{} Goal'.format(self.subStatus)
                    else:
                        self.homeGoalScorers = '{}<br />{} Goal'.format(self.homeGoalScorers, self.subStatus)
            if self.subStatus in self.awayGoalsTimes:
                self.awayScore += 1
                if awayTeam.name == self.teamName:
                    goalScorer = random.randint(0, len(self.goalScorers)-1)
                    if self.awayGoalScorers == '':
                        self.awayGoalScorers = '{} {}'.format(self.subStatus, self.goalScorers[goalScorer].name)
                    else:
                        self.awayGoalScorers = '{}<br />{} {}'.format(self.awayGoalScorers, self.subStatus, self.goalScorers[goalScorer].name)
                    self.goalScorers[goalScorer].goals += 1
                else:
                    if self.awayGoalScorers == '':
                        self.awayGoalScorers = '{} Goal'.format(self.subStatus)
                    else:
                        self.awayGoalScorers = '{}<br />{} Goal'.format(self.awayGoalScorers, self.subStatus)

        self.html = '<table>'
        self.html += '<tr><td style="text-align: right;">{}</td><td style="text-align: center;">{}</td><td style="text-align: center;">{}</td><td>{}</td></tr>'.format(homeTeam.name, self.homeScore, self.awayScore, awayTeam.name)
        if self.subStatus == 90:
            self.subStatus = 1000
        if self.subStatus == 45:
            self.html += '<tr><td colspan="4" style="text-align: center;">Half Time</td></tr>'.format(self.subStatus)
            response = 'delay: 4000'
        elif self.subStatus >= 1000:
            self.html += '<tr><td colspan="4" style="text-align: center;">Full Time</td></tr>'.format(self.subStatus)
            response = ''
        else:
            self.html += '<tr><td colspan="4" style="text-align: center;">Time {}</td></tr>'.format(self.subStatus)
            response = 'delay: 200'
        self.html += '<td style="text-align: right; vertical-align: top;">{}</td><td></td><td></td><td style="vertical-align: top;">{}</td>'.format(self.homeGoalScorers, self.awayGoalScorers)
        self.html += '</table>'
        self.subStatus += 1

        if self.subStatus >= 1000:
            # PROCPLAYERS
            self.playerEngergy()
            self.playerInjured()
            self.wait(True)

        return response



    def playMatch(self, homeTeam, awayTeam, homeBonus, awayBonus, isGraphical=False):
        ''' Replacement for DEFPROCPLAYMATCH (Line 1680) in the BBC Basic version. '''
        homeGoals, awayGoals = self.match(homeTeam, awayTeam, homeBonus, awayBonus)
        # Not implemented yet.

        # Decide when the goals are scored.
        self.homeGoalsTimes = []
        for goal in range(homeGoals):
            goalTime = random.randint(1, 90)
            while goalTime in self.homeGoalsTimes:
                goalTime = (goalTime % 90) + 1
            self.homeGoalsTimes.append(goalTime)
        self.awayGoalsTimes = []
        for goal in range(awayGoals):
            goalTime = random.randint(1, 90)
            while goalTime in self.awayGoalsTimes:
                goalTime = (goalTime % 90) + 1
            self.awayGoalsTimes.append(goalTime)

        # Decide who might score.
        self.goalScorers = []
        for player in self.players:
            if player.inTeam:
                if player.position == Player.DEFENSE:
                    self.goalScorers.append(player)
                elif player.position == Player.MIDFIELD:
                    for count in range(player.skill):
                        self.goalScorers.append(player)
                else:
                    for count in range(player.skill * 3):
                        self.goalScorers.append(player)

        if isGraphical == False:
            self.homeScore = 0
            self.awayScore = 0
            # print('{} {} - {} {}'.format(self.teams[homeTeam].getColouredName(), homeScore, awayScore, self.teams[awayTeam].getColouredName()))
            print('{}{:>17}{} {} - {} {}'.format(homeTeam.colour, homeTeam.name, ansi.RESET_ALL, self.homeScore, self.awayScore, awayTeam.getColouredName()))
            for goalTime in range(91):
                realTime = time.time()

                if goalTime in self.homeGoalsTimes:
                    self.homeScore += 1
                    ansi.doCursorUp(1)
                    print('{}{:>17}{} {} - {} {}'.format(homeTeam.colour, homeTeam.name, ansi.RESET_ALL, self.homeScore, self.awayScore, awayTeam.getColouredName()))
                    totalScore = self.homeScore + self.awayScore
                    if homeTeam.name == self.teamName:
                        ansi.doCursorDown(totalScore)
                        goalScorer = random.randint(0, len(self.goalScorers)-1)
                        print('{} {}'.format(goalTime, self.goalScorers[goalScorer].name), end = '\r')
                        self.goalScorers[goalScorer].goals += 1
                        ansi.doCursorUp(totalScore)
                    else:
                        ansi.doCursorDown(totalScore)
                        print('{} Goal'.format(goalTime), end = '\r')
                        ansi.doCursorUp(totalScore)

                if goalTime in self.awayGoalsTimes:
                    self.awayScore += 1
                    ansi.doCursorUp(1)
                    print('{}{:>17}{} {} - {} {}'.format(homeTeam.colour, homeTeam.name, ansi.RESET_ALL, self.homeScore, self.awayScore, awayTeam.getColouredName()))
                    totalScore = self.homeScore + self.awayScore
                    if awayTeam.name == self.teamName:
                        ansi.doCursorDown(totalScore)
                        goalScorer = random.randint(0, len(self.goalScorers)-1)
                        print('{}{} {}'.format(' ' * 22, goalTime, self.goalScorers[goalScorer].name), end = '\r')
                        self.goalScorers[goalScorer].goals += 1
                        ansi.doCursorUp(totalScore)
                    else:
                        ansi.doCursorDown(totalScore)
                        print('{}{} Goal'.format(' ' * 22, goalTime), end = '\r')
                        ansi.doCursorUp(totalScore)

                print('{}Time {}   '.format(' ' * 17, goalTime), end = '\r')
                sys.stdout.flush()
                time.sleep(realTime + 0.2 - time.time())

                if goalTime == 45:
                    print('{}Half Time.'.format(' ' * 16, goalTime), end = '\r')
                    sys.stdout.flush()
                    # Did the fixture calculations here in the BBC Basic version.
                    time.sleep(4)

            # Move down.
            ansi.doCursorDown(homeGoals + awayGoals + 1)
            print('Final Score')
            print('{}{:>17}{} {} - {} {}'.format(homeTeam.colour, homeTeam.name, ansi.RESET_ALL, homeGoals, awayGoals, awayTeam.getColouredName()))
        else:
            # Debuging only.
            print('{}{:>17}{} {} - {} {}'.format(homeTeam.colour, homeTeam.name, ansi.RESET_ALL, homeGoals, awayGoals, awayTeam.getColouredName()))
            #for goalTime in self.homeGoalsTimes:
            #    print(goalTime)
            #for goalT in self.awayGoalsTimes:
            #    print('                          {}'.format(goalTime))
        return homeGoals, awayGoals



    def poisson(self, mean, probability):
        ''' Replacement for DEFNPOIS (Line 7040) in the BBC Basic version.

        :param double mean: Specifies the mean value of the poisson distribution.
        :param double probability: Specifies the point on the cumulative distribution function (cdf) to return the value from.
        '''
        answer = 0
        # 'pdf' is the probability distribution function at this 'answer'.
        pdf = math.exp(-mean)
        if probability < pdf:
            return answer
        cdf = pdf
        while True:
            answer += 1
            pdf *= mean / answer
            cdf += pdf
            if probability < cdf:
                break;
        return answer



    def match(self, home, away, homeBonus, awayBonus):
        ''' Replacement for DEFPROCMATCH (Line 6920) in the BBC Basic version. '''
        homeAverageGoals = homeBonus + (4.0 * home.attack / away.defence) * home.midfield / (home.midfield + away.midfield) + (home.moral - 10.0) / 40.0 - (away.energy - 100.0) / 400.0
        awayAverageGoals = awayBonus + (4.0 * away.attack / home.defence) * away.midfield / (away.midfield + home.midfield) + (away.moral - 10.0) / 40.0 - (home.energy - 100.0) / 400.0
        homeGoals = self.poisson(homeAverageGoals, self.multiRandom(1, 2) / 2)
        awayGoals = self.poisson(awayAverageGoals, self.multiRandom(1, 2) / 2)

        # Set the moral for the teams.
        if homeGoals == awayGoals:
            home.moral = 10
            away.moral = 10
        else:
            if homeGoals > awayGoals:
                home.moral = max(home.moral, 10)
                away.moral = min(away.moral, 10)
                home.moral = min(home.moral + homeGoals - awayGoals, 20)
                away.moral = max(away.moral + awayGoals - homeGoals, 1)
            else:
                home.moral = min(home.moral, 10)
                away.moral = max(away.moral, 10)
                home.moral = max(home.moral + homeGoals - awayGoals, 1)
                away.moral = min(away.moral + awayGoals - homeGoals, 20)
        return homeGoals, awayGoals



    def progress(self):
        ''' Replacement for DEFPROCPROGRESS (line 5790) in the BBC Basic version. '''
        ansi.doCls()
        print("{}'s progress in division {}".format(self.team.getColouredName(), self.division))

        # Display FA Cup status.
        # Display League Cup status.
        # Display European Cup status.
        self.displayCupStatus()

        # Show league results summary.
        print(' [--- Home ---] [--- Away ---]')
        print('  W  D  L  F  A  W  D  L  F  A Pts')
        print('{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>4}'.format(self.homeWins, self.homeDraws, self.homeLoses, self.homeFor, self.homeAgainst, self.awayWins, self.awayDraws, self.awayLoses, self.awayFor, self.awayAgainst, 3 * (self.homeWins + self.awayWins) + self.homeDraws + self.awayDraws))
        self.html = '<h1>{} progress in division {}</h1>'.format(self.team.name, self.division)
        self.html += '<table>'
        self.html += '<tr><td colspan="5" style="text-align: center; border: 2px solid purple;">Home</td><td colspan="5" style="text-align:center; border: 2px solid purple;">Away</td><td style="border-top: 2px solid purple; border-left: 2px solid purple; border-right: 2px solid purple;"></td></tr>'
        self.html += '<tr><td style="text-align: right; border-left: 2px solid purple; border-bottom: 2px solid purple;">Win</td><td style="text-align: right; border-bottom: 2px solid purple;">Draw</td><td style="text-align: right; border-bottom: 2px solid purple;">Lose</td><td style="text-align: right; border-bottom: 2px solid purple;">For</td><td style="text-align: right; border-bottom: 2px solid purple; border-right: 2px solid purple;">Agn</td><td style="text-align: right; border-bottom: 2px solid purple; border-left: 2px solid purple;">Win</td><td style="text-align: right; border-bottom: 2px solid purple;">Draw</td><td style="text-align: right; border-bottom: 2px solid purple;">Lose</td><td style="text-align: right; border-bottom: 2px solid purple;">For</td><td style="text-align: right; border-bottom: 2px solid purple; border-right: 2px solid purple;">Agn</td><td style="text-align: right; border-bottom: 2px solid purple; border-left: 2px solid purple; border-right: 2px solid purple;">Points</td></tr>'
        self.html += '<tr><td style="text-align: right; border-left: 2px solid purple; border-bottom: 2px solid purple;">{}</td><td style="text-align: right; border-bottom: 2px solid purple;">{}</td><td style="text-align: right; border-bottom: 2px solid purple;">{}</td><td style="text-align: right; border-bottom: 2px solid purple;">{}</td><td style="text-align: right; border-bottom: 2px solid purple; border-right: 2px solid purple;">{}</td><td style="text-align: right; border-bottom: 2px solid purple; border-left: 2px solid purple;">{}</td><td style="text-align: right; border-bottom: 2px solid purple;">{}</td><td style="text-align: right; border-bottom: 2px solid purple;">{}</td><td style="text-align: right; border-bottom: 2px solid purple;">{}</td><td style="text-align: right; border-bottom: 2px solid purple; border-right: 2px solid purple;">{}</td><td style="text-align: right; border: 2px solid purple; padding-right: 10px;">{}</td></tr>'.format(self.homeWins, self.homeDraws, self.homeLoses, self.homeFor, self.homeAgainst, self.awayWins, self.awayDraws, self.awayLoses, self.awayFor, self.awayAgainst, 3 * (self.homeWins + self.awayWins) + self.homeDraws + self.awayDraws)
        self.html += '</table>'

        # Show league results details.
        count = 0
        for week in reversed(self.weeks):
            count += 1
            if count <= 10:
                if week & 256 == 0:
                    homeAway = 'Home'
                else:
                    homeAway = 'Away'
                if week & 192 == 0:
                    result = ansi.LIGHT_RED + 'Lost ' + ansi.RESET_ALL
                elif week & 192 == 128:
                    result = ansi.LIGHT_GREEN + 'Won  ' + ansi.RESET_ALL
                else:
                    result = ansi.LIGHT_YELLOW + 'Drawn' + ansi.RESET_ALL
                # There are positions 1 to 16. 16-14, 13-4, 3-2, 1
                position = 1 + (week & 63)
                # The bar is one element short because the number is the final element.
                bar = ''
                if position < 14:
                    bar = ansi.BACKGROUND_LIGHT_RED + '  ' * 3
                    if position < 4:
                        bar += ansi.BACKGROUND_LIGHT_MAGENTA + '  ' * 10
                        if position == 3:
                            bar += ansi.BACKGROUND_LIGHT_GREEN + ansi.DARK_GRAY
                        elif position == 2:
                            bar += ansi.BACKGROUND_LIGHT_GREEN + '  ' + ansi.DARK_GRAY
                        else:
                            bar += ansi.BACKGROUND_LIGHT_GREEN + '    ' + ansi.BACKGROUND_YELLOW
                    else:
                        bar += ansi.BACKGROUND_LIGHT_MAGENTA + '  ' * (13 - position)
                else:
                    bar = ansi.BACKGROUND_LIGHT_RED + '  ' * (16 - position)

                # Add the final element as the number.
                bar = '{}{:>2}'.format(bar, 1 + week & 63)
                print('{} {} {}{}'.format(homeAway, result, bar, ansi.RESET_ALL))



    def displayTitles(self):
        ''' Display the titles held by the team. '''
        if self.titles == 0:
            return
        # print('titles = {}'.format(self.titles))
        self.html += '<p>'
        division = self.titles & 7
        if division != 0:
            print('Division {} Champions'.format(division))
            self.html += 'Division {} Champions<br />'.format(division)
        if self.titles & 8 == 8:
            print('League Cup Champions')
            self.html += 'League Cup Champions<br />'
        if self.titles & 16 == 16:
            print('FA Cup Champions')
            self.html += 'FA Cup Champions<br />'
        if self.titles & 32 == 32:
            print('European Cup Champions')
            self.html += 'European Cup Champions<br />'
        if self.titles & 64 == 64:
            print('European Cup Winners Cup Champions')
            self.html += 'European Cup Winners Cup Champions<br />'
        if self.titles & 128 == 128:
            print('UEFA Cup Champions')
            self.html += 'UEFA Cup Champions<br />'
        self.html += '</p>'



    def displayCupStatus(self):
        ''' Display the status of the cup competitions. '''
        self.html += '<p>'
        if self.faCup.isIn:
            print('FA Cup: {}in {}{}.'.format(ansi.GREEN, self.faCup.getRoundName(), ansi.RESET_ALL))
            self.html += 'FA Cup: <span style="color: green;">in {}</span><br />'.format(self.faCup.getRoundName())
        else:
            print('FA Cup: {}out {}{}.'.format(ansi.RED, self.faCup.getRoundName(), ansi.RESET_ALL))
            self.html += 'FA Cup: <span style="color: red;">out {}</span><br />'.format(self.faCup.getRoundName())
        if self.leagueCup.isIn:
            print('League Cup: {}in {}{}.'.format(ansi.GREEN, self.leagueCup.getRoundName(), ansi.RESET_ALL))
            self.html += 'League Cup: <span style="color: green;">in {}</span><br />'.format(self.leagueCup.getRoundName())
        else:
            print('League Cup: {}out {}{}.'.format(ansi.RED, self.leagueCup.getRoundName(), ansi.RESET_ALL))
            self.html += 'League Cup: <span style="color: red;">out {}</span><br />'.format(self.leagueCup.getRoundName())
        if self.europeanCup != None:
            if self.europeanCup.isIn:
                print('{}: {}in {}{}.'.format(self.europeanCup.name, ansi.GREEN, self.europeanCup.getRoundName(), ansi.RESET_ALL))
                self.html += '{}: <span style="color: green;">in {}</span><br />'.format(self.europeanCup.name, self.europeanCup.getRoundName())
            else:
                print('{}: {}out {}{}.'.format(self.europeanCup, ansi.RED, self.europeanCup.getRoundName(), ansi.RESET_ALL))
                self.html += '{}: <span style="color: red;">out {}</span><br />'.format(self.europeanCup.name, self.europeanCup.getRoundName())
        self.html += '</p>'



    def playCupMatch(self):
        ''' Play a cup match in the self.activeCup competition. '''
        if self.subStatus == -1:
            division = 5 - self.activeCup.round
            if division < 1:
                division = 1
            elif division > 1:
                division = random.randint(1, division)

            self.cupTeam = self.activeCup.getTeam(division)
            self.cupTeam.pos = division
            self.isHomeMatch = random.randint(1, 2) == 1
            self.subStatus = 0
        division = self.cupTeam.pos
        print('division = {}'.format(division))

        self.html = '<h1 style="display: inline">{} </h1><p style="display: inline">{}</p>'.format(self.activeCup.name, self.activeCup.getRoundName())
        self.html += self.activeCup.displayResults()

        if self.isHomeMatch:
            self.displayMatch(False, self.teams[self.teamIndex], self.cupTeam)
        else:
            self.displayMatch(False, self.cupTeam, self.teams[self.teamIndex])



    def reportCupMatch(self):
        division = self.cupTeam.pos
        print('division = {}'.format(division))
        self.activeCup.addResult(self.isHomeMatch, self.cupTeam, self.homeScore, self.awayScore)
        print(self.activeCup.name)
        self.html = '<h1>{}</h1>'.format(self.activeCup.name)
        self.html += self.activeCup.displayResults()

        if self.homeScore == self.awayScore:
            print('Replay')
            self.html += '<p>Replay</p>'
        else:
            cupBonus = 55000 - division * 5000 + random.randint(1, 1000) - random.randint(1, 1000)
            if self.activeCup.round == 6:
                cupBonus += 50000
            print('You made £{:,.0f}'.format(cupBonus))
            self.html += '<p>You made £{:,.0f}</p>'.format(cupBonus)
            self.money += cupBonus
            self.moneyMessage += self.financialLine(self.activeCup.name, cupBonus, 0) + "\n";

            if self.activeCup.isIn:
                if self.activeCup.round == 6:
                    print('You have won the {}'.format(self.activeCup.name))
                    self.html += '<p>You have won the {}</p>'.format(self.activeCup.name)
                else:
                    print('You qualify for the {} of the {}'.format(self.activeCup.getRoundName(), self.activeCup.name))
                    self.html += '<p>You qualify for the {} of the {}</p>'.format(self.activeCup.getRoundName(), self.activeCup.name)
            else:
                print('You are out of the {}'.format(self.activeCup.name))
                self.html += '<p>You are out of the {}</p>'.format(self.activeCup.name)

        self.wait(True)
