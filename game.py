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

# Application Libraries.
import ansi
from inkey import InKey
from team import Team
from player import Player



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

        self.status = 0
        self.subStatus = 0
        self.html = 'Hello World'



    def run(self):
        ''' Execute the football manager game. '''
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

        MATCHES_PER_SEASON = 30
        if self. args.debug:
            MATCHES_PER_SEASON = 3

        # Play the game.
        nYear = 0
        while True:
            self.moneyStart = self.money - self.debt
            self.moneyMessage = ''

            # Play a season.
            while self.numMatches < MATCHES_PER_SEASON:
                ansi.doCls()
                print('{} MANAGER: {}'.format(self.team.getColouredName(), self.playerName))
                print('LEVEL: {}'.format(self.level))
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
                elif keyPress == '6':
                    # PROCRESTART
                    pass
                elif keyPress == '7':
                    ansi.doCls()
                    self.showLeague()
                    self.wait()
                elif keyPress == '8':
                    # Confirm with the user.
                    print('Are you sure you want to exit the program (Y/N) ?')
                    if self.getYesNo():
                        return

            # Season has finished.
            ansi.doCls()
            print('Season has finished.')
            self.showLeague()
            self.wait()

            if self.division == 1:
                print('Qualify for Europe')
            else:
                print('Promotion')
            for index in range(0, 3):
                print(self.teams[index].getColouredName())
            if self.division != 4:
                print('Relegation')
                for index in range(13, 16):
                    print(self.teams[index].getColouredName())

            # Rebuild the new league.
            exclued = []
            if self.division != 1 and self.teamIndex <= 2:
                # Promotion.
                self.division = self.division - 1
                print('{} are promoted to division {}'.format(self.teams[self.teamIndex].getColouredName(), self.division))
                for index in range(3, 13):
                    exclued.append(self.teams[index].name)
                    self.teams[index].name = ''
            elif self.division != 4 and self.teamIndex >= 13:
                # Relegation.
                self.division = self.division + 1
                print('{} are relegated to division {}'.format(self.teams[self.teamIndex].getColouredName(), self.division))
                for index in range(0, 13):
                    exclued.append(self.teams[index].name)
                    self.teams[index].name = ''
            else:
                # Same division.
                print('{} stay in division {}'.format(self.teams[self.teamIndex].getColouredName(), self.division))
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
            nSkillBonus = 1 if self.division <= 2 else 0
            for player in self.players:
                player.skill = random.randint(1, 5) + nSkillBonus
                player.energy = random.randint(1, 20)
                player.inTeam = False
                player.injured = False
                player.caps = 0
                player.goals = 0
            for index in range(4):
                nPlayer = random.randint(0, 25)
                self.players[nPlayer].skill = 5 + nSkillBonus

            self.numMatches = 0
            self.weeks = []

            self.wait()



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
                    self.status = 1
                self.level = 1
                if 'level' in parameters:
                    self.level = parameters['level']
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
        elif self.status == 2:
            # Enter own team name.
            if 'name' in parameters:
                self.teamName = parameters['name']
                self.teamColour = ansi.CYAN
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
            self.html += '<p><input type="submit" name="OK" /></p>'
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
            self.html += '<p><input type="submit" name="OK" /></p>'
            self.html += '</form>'
        elif self.status == 2:
            # Optional initialise, name own team.
            self.html = '<form action="app:" method="get">'
            self.html += '<p>Please enter your team name <input type="text" name="name"></p>'
            self.html += '<p><input type="submit" name="OK" /></p>'
            self.html += '</form>'
        elif self.status == 100:
            self.html = '<p>{}</p><p>Manager {}</p>'.format(self.teamName, self.playerName)
        elif self.status == 78:
            if self.subStatus < 90:
                self.subStatus += 1
                self.html = '<p>Game</p><p>Time{}</p>'.format(self.subStatus)
                responseOptions = 'delay:'
            else:
                self.html = '<p>Game</p><p>Finished</p>'
                responseOptions = ' '
        else:
            self.html = '<p>Error Help.</p><p>status = {}</p>'.format(self.status)




        return responseOptions



    def playWeek(self):
        ''' This is the block of code that was after the menu in the week loop of the BBC Basic version. Line 740 onward.'''
        self.numMatches += 1

        # Decide and play any cup matches.

        # Choose an opponent for the league match.
        self.team.isPlayedHome = True
        self.team.isPlayedAway = True
        while True:
            opponent = random.randint(0, 15)
            isHomeMatch = (self.numMatches & 1) == 1
            if isHomeMatch:
                if self.teams[opponent].isPlayedHome == False:
                    self.teams[opponent].isPlayedHome = True
                    break;
            else:
                if self.teams[opponent].isPlayedAway == False:
                    self.teams[opponent].isPlayedAway = True
                    break;

        # Let the player select the players for the team.
        while True:
            ansi.doCls()
            if isHomeMatch:
                self.displayMatch(self.teamIndex, opponent)
            else:
                self.displayMatch(opponent, self.teamIndex)
            keyPress = self.getKeyboardCharacter(['c', '\t'])
            if keyPress == '\t':
                break;
            # Pick the player.
            self.pickPlayers()

        ansi.doCursorUp(2)
        print(ansi.ERASE_LINE)
        print(ansi.ERASE_LINE)

        # Play the match.
        if isHomeMatch:
            playerGoals, opponentGoals = self.playMatch(self.teamIndex, opponent, 0.5, 0)
            self.applyPoints(self.teamIndex, opponent, playerGoals, opponentGoals)
        else:
            opponentGoals, playerGoals = self.playMatch(opponent, self.teamIndex, 0.5, 0)
            self.applyPoints(opponent, self.teamIndex, opponentGoals, playerGoals)

        # Calculate the gate money.
        if isHomeMatch:
            self.gateMoney = (9000 + (15 - self.teamIndex - opponent) * 500) * (5 - self.division) + random.randint(0, 1000)
            if abs(self.teams[self.teamIndex].pts - self.teams[opponent].pts) < 4:
                self.gateMoney += (5 - self.division) * 3000
        else:
            self.gateMoney = 0

        # PROCPLAYERS
        self.playerEngergy()
        self.playerInjured()
        # Decided the fixtures for the league was at half time of the playmatch.
        self.decideFixtures(opponent)

        self.wait()

        self.rest()
        self.sortDivision()

        # Store the data for progress.
        if isHomeMatch:
            week = 0
        else:
            week = 256
        if playerGoals == opponentGoals:
            week |= 64
        elif playerGoals > opponentGoals:
            week |= 128
        week += self.teamIndex
        self.weeks.append(week)

        self.wait()

        ansi.doCls()
        self.showLeague()
        self.wait()

        self.market()
        self.report()
        self.progress()
        ansi.doCls()
        self.playerCaps()
        self.playerFit()
        self.wait()



    def applyPoints(self, home, away, homeGoals, awayGoals):
        ''' Apply the points to the league. '''
        self.teams[home].numHomeGames += 1
        if homeGoals == awayGoals:
            self.teams[home].pts += 1
            self.teams[away].pts += 1
            self.teams[home].draw += 1
            self.teams[away].draw += 1
        else:
            if homeGoals > awayGoals:
                self.teams[home].pts += 3
                self.teams[home].win += 1
                self.teams[away].lost += 1
            else:
                self.teams[away].pts += 3
                self.teams[home].lost += 1
                self.teams[away].win += 1
            self.teams[home].difference += homeGoals - awayGoals
            self.teams[away].difference += awayGoals - homeGoals



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
            return
        self.dropPlayer(player)
        self.players[player].injured = True
        if self.players[player].inSquad:
            print('{}{} has been injured.{}'.format(ansi.RED, self.players[player].name, ansi.RESET_ALL))
            self.numInjured += 1



    def playerFit(self):
        ''' This was part of PROCPROGRESS in the BBC Basic version. '''
        for player in self.players:
            if player.injured:
                if random.randint(1, 3) == 1:
                    player.injured = False
                    if player.inSquad:
                        print('{}{} is fit.{}'.format(ansi.GREEN, player.name, ansi.RESET_ALL))
                        self.numInjured -= 1
                        if self.numInjured < 0:
                            self.numInjured = 0



    def displaySquad(self):
        ''' Replacement for PROCPTEAM (line 2130) in the BBC Basic version. '''
        print('   Player        Skill Energy')
        for player in self.players:
            if player.inSquad:
                player.writeRow()



    def pickPlayers(self):
        ''' Replacement for PROCPICK (line 2260) in the BBC Basic version. '''
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
                    self.moneyMessage = self.moneyMessage + self.financialLine(self.players[playerNumber].name + ' sold', price, 0) + "\n";
            else:
                print('On range')
            self.wait()




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
                    print('{}Your bid is turned down.{}'.format(ansi.RED, ansi.RESET_ALL))
        self.wait()



    def report(self):
        ''' Replacement for PROCREPORT ( line 3970 ) in the BBC Basic version. '''
        if self.gateMoney > 0:
            print(self.financialLine('Gate Money', self.gateMoney, 0))
            self.money += self.gateMoney
        print(self.financialLine('Paid to Squad', 0, self.numSquad * 500 * (5 - self.division)))
        self.money -= self.numSquad * 500 * (5 - self.division)
        if self.moneyMessage != '':
            print(self.moneyMessage, end = '')
        if self.debt > 0:
            nInterest = int (self.debt * 0.005)
            print(self.financialLine('Interest', 0, nInterest))
            self.money = self.money - nInterest
        print('━' * 40)
        if self.money - self.debt >= self.moneyStart:
            print(self.financialLine('Profit', self.money - self.debt - self.moneyStart, 0))
        else:
            print(self.financialLine('Loss', 0, self.moneyStart - self.money + self.debt))
        print('━' * 40)

        print(self.financialLine('Cash', self.money, 0))
        print(self.financialLine('Debt', 0, self.debt))

        # Reset the counters.
        self.moneyStart = self.money - self.debt
        self.moneyMessage = ''

        self.wait()



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



    def playerCaps(self):
        ''' This was part of PROCPROGRESS (line 6190) in the BBC Basic version. '''
        playersByCaps = sorted(self.players, key=lambda Player: Player.caps, reverse=True)
        print('{}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{}'.format(ansi.MAGENTA, ansi.RESET_ALL))
        print('{}┃{}   Player        Position  Caps Goals {}┃{}'.format(ansi.MAGENTA, ansi.RESET_ALL, ansi.MAGENTA, ansi.RESET_ALL))
        for index in range(11):
            player = playersByCaps[index]
            if player.injured:
                playerColour = ansi.RED
            elif player.inTeam:
                playerColour = ansi.GREEN
            else:
                playerColour = ansi.RESET_ALL
            print('{}┃{}{:>2} {:<14}{:<9}{:>5}{:>6} {}┃{}'.format(ansi.MAGENTA, playerColour, index + 1, player.name, player.getPosition(), player.caps, player.goals, ansi.MAGENTA, ansi.RESET_ALL))

        # Top Scorers.
        playersByGoals = sorted(self.players, key=lambda Player: Player.goals, reverse=True)
        print('{}┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫{}'.format(ansi.MAGENTA, ansi.RESET_ALL))
        print('{}┃{}   Player        Position  Caps Goals {}┃{}'.format(ansi.MAGENTA, ansi.RESET_ALL, ansi.MAGENTA, ansi.RESET_ALL))
        for index in range(5):
            player = playersByGoals[index]
            if player.injured:
                playerColour = ansi.RED
            elif player.inTeam:
                playerColour = ansi.GREEN
            else:
                playerColour = ansi.RESET_ALL
            if player.goals > 0:
                print('{}┃{}{:>2} {:<14}{:<9}{:>5}{:>6} {}┃{}'.format(ansi.MAGENTA, playerColour, index + 1, player.name, player.getPosition(), player.caps, player.goals, ansi.MAGENTA, ansi.RESET_ALL))
        print('{}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{}'.format(ansi.MAGENTA, ansi.RESET_ALL))



    def displayMatch(self, home, away):
        ''' Replacement for PROCDISPLAY in the BBC Basic version. '''
        print('   {}{:^18}{}{:^18}{}'.format(self.teams[home].colour, self.teams[home].name, self.teams[away].colour, self.teams[away].name, ansi.RESET_ALL))
        if True:
            print('Pos{:^18}{:^18}'.format(self.teams[home].position, self.teams[away].position))
        print('Eng{:^18}{:^18}'.format(self.teams[home].energy, self.teams[away].energy))
        print('Mor{:^18}{:^18}'.format(self.teams[home].moral, self.teams[away].moral))
        print('For{:^18}{:^18}'.format(self.teams[home].formation, self.teams[away].formation))
        print('Def{:^18}{:^18}'.format(self.teams[home].defence, self.teams[away].defence))
        print('Mid{:^18}{:^18}'.format(self.teams[home].midfield, self.teams[away].midfield))
        print('Att{:^18}{:^18}'.format(self.teams[home].attack, self.teams[away].attack))
        print()
        print('{} Picked, {} Squad, {} Injured.'.format(self.numTeam, self.numSquad, self.numInjured))
        print('Press C to change team')
        print('Press TAB to play match.')



    def wait(self):
        ''' Replacement for PROCWAIT in the BBC Basic version. '''
        print('{}{}{} Press SPACE to continue {}{}'.format(ansi.BACKGROUND_BLUE, ansi.YELLOW, '━' * 7, '━' * 8, ansi.RESET_ALL))
        self.getKeyboardCharacter([' '])
        print('{}{}'.format(ansi.getCursorUp(1), ansi.ERASE_LINE), end = '\r')



    def showLeague(self):
        ''' Replacement for PROCLEAGUE in the BBC Basic version. '''
        print('Division {}'.format(self.division))
        print('   Team             W  D  L Pts Dif')
        for team in self.teams:
            team.writeTableRow(self.args.debug)
        print('Matches Played: {}'.format(self.numMatches))
        print('{} position: {}'.format(self.team.getColouredName(), self.teamIndex+1))



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



    def newGame(self):
        ''' Initialise a new game. '''
        self.pickTeam()

        # Initialise variables
        self.numMatches = 0
        self.money = 50000
        self.debt = 200000
        self.weeks = []

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
                self.teamColour = ansi.CYAN
                break
            division = 1 + (division & 3)
        print('You manage {}{}{}'.format(self.teamColour, self.teamName, ansi.RESET_ALL))



    def enterNumber(self, message):
        ''' Enter a number at the keyboard. '''
        number = 0
        try:
            number = int(input(message))
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

        self.html += '<p>'
        self.html += '┏━━             ┃       ┃ ┃   ┏━┳━┓<br />'
        self.html += '┃            ┃  ┃       ┃ ┃   ┃ ┃ ┃<br />'
        self.html += '┣━━ ┏━┓ ┏━┓ ━╋━ ┣━┓ ━━┓ ┃ ┃   ┃   ┃ ━━┓ ━┳━┓ ━━┓ ┏━┓ ┏━┓ ┏━<br />'
        self.html += '┃   ┃ ┃ ┃ ┃  ┃  ┃ ┃ ┏━┫ ┃ ┃   ┃   ┃ ┏━┃  ┃ ┃ ┏━┫ ┃ ┃ ┣━┛ ┃<br />'
        self.html += '┃   ┗━┛ ┗━┛  ┃  ┗━┛ ┗━┛ ┃ ┃   ┃   ┃ ┗━┛  ┃ ┃ ┗━┛ ┗━┫ ┗━━ ┃<br />'
        self.html += '                                                   ┃<br />'
        self.html += '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛<br />'
        self.html += '</p>'
        self.html += '<p>By Steve Walton BBC BASIC 1982-1989, 2000, Python 2018-2021.</p>'



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
        time.sleep(5)



    def load(self):
        ''' Implementation of DEFPROCLOAD (line 5530) from the BBC Basic version. '''
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
        self.formation= json.loads(line)

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
        for match in range(1, 8):
            for index in range(16):
                if self.teams[index].fixture == 2 * match - 1:
                    home = index
                if self.teams[index].fixture == 2 * match:
                    away = index

            homeGoals, awayGoals = self.match(home, away, 0.5, 0)
            print('{}{:>17}{} {} - {} {}'.format(self.teams[home].colour, self.teams[home].name, ansi.RESET_ALL, homeGoals, awayGoals, self.teams[away].getColouredName()))
            self.applyPoints(home, away, homeGoals, awayGoals)



    def playMatch(self, homeTeam, awayTeam, homeBonus, awayBonus):
        ''' Replacement for DEFPROCPLAYMATCH (Line 1680) in the BBC Basic version. '''
        homeGoals, awayGoals = self.match(homeTeam, awayTeam, homeBonus, awayBonus)
        # Not implemented yet.

        # Decide when the goals are scored.
        homeGoalsTimes = []
        for goal in range(homeGoals):
            goalTime = random.randint(1, 90)
            if not (goalTime in homeGoalsTimes):
                homeGoalsTimes.append(goalTime)
        awayGoalsTimes = []
        for goal in range(awayGoals):
            goalTime = random.randint(1, 90)
            if not (goalTime in awayGoalsTimes):
                awayGoalsTimes.append(goalTime)

        # Decide who might score.
        goalScorers = []
        for player in self.players:
            if player.inTeam:
                if player.position == Player.DEFENSE:
                    goalScorers.append(player)
                elif player.position == Player.MIDFIELD:
                    for count in range(player.skill):
                        goalScorers.append(player)
                else:
                    for count in range(player.skill * 3):
                        goalScorers.append(player)

        homeScore = 0
        awayScore = 0
        # print('{} {} - {} {}'.format(self.teams[homeTeam].getColouredName(), homeScore, awayScore, self.teams[awayTeam].getColouredName()))
        print('{}{:>17}{} {} - {} {}'.format(self.teams[homeTeam].colour, self.teams[homeTeam].name, ansi.RESET_ALL, homeScore, awayScore, self.teams[awayTeam].getColouredName()))
        for goalTime in range(91):
            realTime = time.time()

            if goalTime in homeGoalsTimes:
                homeScore += 1
                ansi.doCursorUp(1)
                print('{}{:>17}{} {} - {} {}'.format(self.teams[homeTeam].colour, self.teams[homeTeam].name, ansi.RESET_ALL, homeScore, awayScore, self.teams[awayTeam].getColouredName()))
                totalScore = homeScore + awayScore
                if homeTeam == self.teamIndex:
                    ansi.doCursorDown(totalScore)
                    goalScorer = random.randint(0, len(goalScorers)-1)
                    print('{} {}'.format(goalTime, goalScorers[goalScorer].name), end = '\r')
                    goalScorers[goalScorer].goals += 1
                    ansi.doCursorUp(totalScore)
                else:
                    ansi.doCursorDown(totalScore)
                    print('{} Goal'.format(goalTime), end = '\r')
                    ansi.doCursorUp(totalScore)

            if goalTime in awayGoalsTimes:
                awayScore += 1
                ansi.doCursorUp(1)
                print('{}{:>17}{} {} - {} {}'.format(self.teams[homeTeam].colour, self.teams[homeTeam].name, ansi.RESET_ALL, homeScore, awayScore, self.teams[awayTeam].getColouredName()))
                totalScore = homeScore + awayScore
                if awayTeam == self.teamIndex:
                    ansi.doCursorDown(totalScore)
                    goalScorer = random.randint(0, len(goalScorers)-1)
                    print('{}{} {}'.format(' ' * 22, goalTime, goalScorers[goalScorer].name), end = '\r')
                    goalScorers[goalScorer].goals += 1
                    ansi.doCursorUp(totalScore)
                else:
                    ansi.doCursorDown(totalScore)
                    print('{}{} Goal'.format(' ' * 22, goalTime), end = '\r')
                    ansi.doCursorUp(totalScore)


            print('{}Time {}   '.format(' ' * 17, goalTime), end = '\r')
            sys.stdout.flush()
            time.sleep(realTime + 0.3 - time.time())

            if goalTime == 45:
                print('{}Half Time.'.format(' ' * 16, goalTime), end = '\r')
                sys.stdout.flush()
                # Did the fixture calculations here in the BBC Basic version.
                time.sleep(4)

        # Move down.
        ansi.doCursorDown(homeGoals + awayGoals + 1)
        print('Final Score')
        print('{}{:>17}{} {} - {} {}'.format(self.teams[homeTeam].colour, self.teams[homeTeam].name, ansi.RESET_ALL, homeGoals, awayGoals, self.teams[awayTeam].getColouredName()))
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



    def match(self, homeTeam, awayTeam, homeBonus, awayBonus):
        ''' Replacement for DEFPROCMATCH (Line 6920) in the BBC Basic version. '''
        home = self.teams[homeTeam]
        away = self.teams[awayTeam]
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

        # Show league results summary.
        print(' [--- Home ---] [--- Away ---]')
        print('  W  D  L  F  A  W  D  L  F  A Pts')

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

        # Wait for the user.
        self.wait()
