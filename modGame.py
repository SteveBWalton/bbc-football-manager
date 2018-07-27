#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to implement the CGame class for the the BBC Football Manager program.
'''

# System libraries.
import random
import math
import json
import time
import sys

# Application Libraries.
import modANSI
import modInkey
import modTeam
import modPlayer



class CGame:
    ''' Class to represent the BBC Football Manager game. '''



    def __init__(self):
        ''' Class constructor for the BBC Football manager game. '''
        self.player_name = ''
        self.level = 1
        self.team_name = ''
        self.team_colour = modANSI.WHITE
        self.team_index = None
        self.num_squad = 0
        self.num_team = 0
        self.num_injured = 0
        self.formation = [0, 0, 0]



    def Run(self):
        ''' Execute the football manager game. '''
        self.keyboard = modInkey.CInkey()
        random.seed()

        modANSI.CLS()
        self.Football()

        # Get the player settings.
        print()
        self.player_name = input('Please enter your name: ')

        # Select the level.
        print('Enter level [1-4]')
        self.level = int(self.GetKeyboardCharacter(['1', '2', '3', '4']))
        print('Level {} was selected'.format(self.level))

        # Load a game.
        print('Do you want to load a game?')
        if self.YesNo():
            print('Yes')
            self.Load()
            self.SortDivison()
        else:
            print('No')
            self.NewGame()

        # Play the game.
        nYear = 0
        while True:
            # Play a season.

            while self.match < 30:
                modANSI.CLS()
                print('{} MANAGER: {}'.format(self.team.GetColouredName(), self.player_name))
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
                sKey = self.GetKeyboardCharacter(['1', '2', '3', '4', '5', '6', '7', '8'])
                if sKey == '1':
                    self.SellPlayer()
                elif sKey == '2':
                    self.Bank()
                elif sKey == '3':
                    # PROCRENAME
                    pass
                elif sKey == '4':
                    # Continue.
                    self.PlayWeek()
                elif sKey == '5':
                    self.Save(True)
                elif sKey == '6':
                    # PROCRESTART
                    pass
                elif sKey == '7':
                    modANSI.CLS()
                    self.ShowLeague()
                    self.Wait()
                elif sKey == '8':
                    # Confirm with the user.
                    print('Are you sure you want to exit the program (Y/N) ?')
                    if self.YesNo():
                        return

            # Season has finished.
            modANSI.CLS()
            print('Season has finished.')
            self.ShowLeague()
            self.Wait()

            if self.division == 1:
                print('Qualify for Europe')
            else:
                print('Promotion')
            for nIndex in range(0, 3):
                print(self.teams[nIndex].GetColouredName())
            if self.division != 4:
                print('Relegation')
                for nIndex in range(13, 16):
                    print(self.teams[nIndex].GetColouredName())

            # Rebuild the new league.
            sExclued = []
            if self.division != 1 and self.team_index <= 2:
                # Promotion.
                self.division = self.division - 1
                print('{} are promoted to division {}'.format(self.teams[self.team_index].GetColouredName(), self.division))
                for nIndex in range(3, 13):
                    sExclued.append(self.teams[nIndex].name)
                    self.teams[nIndex].name = ''
            elif self.division != 4 and self.team_index >= 13:
                # Relegation.
                self.division = self.division + 1
                print('{} are relegated to division {}'.format(self.teams[self.team_index].GetColouredName(), self.division))
                for nIndex in range(0, 13):
                    sExclued.append(self.teams[nIndex].name)
                    self.teams[nIndex].name = ''
            else:
                # Same division.
                print('{} stay in division {}'.format(self.teams[self.team_index].GetColouredName(), self.division))
                if self.division != 1:
                    for nIndex in range(0, 3):
                        sExclued.append(self.teams[nIndex].name)
                        self.teams[nIndex].name = ''
                if self.division != 4:
                    for nIndex in range(13, 16):
                        sExclued.append(self.teams[nIndex].name)
                        self.teams[nIndex].name = ''
            self.SetTeamsForDivision(sExclued)

            # Reskill the players.
            self.num_team = 0
            self.num_injured = 0
            self.formation = [0, 0, 0]
            nSkillBonus = 1 if self.division <= 2 else 0
            for oPlayer in self.players:
                oPlayer.skill = random.randint(1, 5) + nSkillBonus
                oPlayer.energy = random.randint(1, 20)
                oPlayer.in_team = False
                oPlayer.injured = False
                oPlayer.caps = 0
                oPlayer.goals = 0
            for nIndex in range(4):
                nPlayer = random.randint(0, 25)
                self.players[nPlayer].skill = 5 + nSkillBonus

            self.match = 0

            self.Wait()



    def PlayWeek(self):
        ''' This is the block of code that was after the menu in the week loop of the BBC Basic version. Line 740 onward.'''
        self.match = self.match + 1

        # Decide and play any cup matches.

        # Choose an opponent for the league match.
        self.team.played_home = True
        self.team.played_away = True
        while True:
            nOpponent = random.randint(0, 15)
            bHome = (self.match & 1) == 1
            if bHome:
                if self.teams[nOpponent].played_home == False:
                    self.teams[nOpponent].played_home = True
                    break;
            else:
                if self.teams[nOpponent].played_away == False:
                    self.teams[nOpponent].played_away = True
                    break;

        # Let the player select the players for the team.
        while True:
            modANSI.CLS()
            if bHome:
                self.DisplayMatch(self.team_index, nOpponent)
            else:
                self.DisplayMatch(nOpponent, self.team_index)
            sKey = self.GetKeyboardCharacter(['c', '\t'])
            if sKey == '\t':
                break;
            # Pick the player.
            self.PickPlayers()

        # Play the match.
        if bHome:
            nPlayerGoals, nOpponentGoals = self.PlayMatch(self.team_index, nOpponent, 0.5, 0)
            self.ApplyPoints(self.team_index, nOpponent, nPlayerGoals, nOpponentGoals)
        else:
            nOpponentGoals, nPlayerGoals = self.PlayMatch(nOpponent, self.team_index, 0.5, 0)
            self.ApplyPoints(nOpponent, self.team_index, nOpponentGoals, nPlayerGoals)

        # PROCPLAYERS
        self.PlayerEngergy()
        self.PlayerInjured()
        # Decided the fixtures for the league was at half time of the playmatch.
        self.Fixtures(nOpponent)

        self.Wait()

        self.Rest()
        self.SortDivison()
        self.Wait()

        modANSI.CLS()
        self.ShowLeague()
        self.Wait()

        self.Market()
        # PROCREPORT
        # PROCPROGRESS
        modANSI.CLS()
        self.PlayerCaps()
        self.PlayerFit()
        self.Wait()



    def ApplyPoints(self, nHome, nAway, nHomeGoals, nAwayGoals):
        ''' Apply the points to the league. '''
        if nHomeGoals == nAwayGoals:
            self.teams[nHome].pts = self.teams[nHome].pts + 1
            self.teams[nAway].pts = self.teams[nAway].pts + 1
            self.teams[nHome].draw = self.teams[nHome].draw + 1
            self.teams[nAway].draw = self.teams[nAway].draw + 1
        else:
            if nHomeGoals > nAwayGoals:
                self.teams[nHome].pts = self.teams[nHome].pts + 3
                self.teams[nHome].win  = self.teams[nHome].win  + 1
                self.teams[nAway].lost = self.teams[nAway].lost + 1
            else:
                self.teams[nAway].pts = self.teams[nAway].pts + 3
                self.teams[nHome].lost = self.teams[nHome].lost + 1
                self.teams[nAway].win  = self.teams[nAway].win + 1
            self.teams[nHome].difference = self.teams[nHome].difference + nHomeGoals - nAwayGoals
            self.teams[nAway].difference = self.teams[nAway].difference + nAwayGoals - nHomeGoals



    def PlayerEngergy(self):
        ''' Replacement for PROCRESET (line 3200) in the BBC Basic version. '''
        self.teams[self.team_index].energy = 0
        for oPlayer in self.players:
            if oPlayer.in_squad:
                if oPlayer.in_team:
                    oPlayer.energy = oPlayer.energy - random.randint(1, 2)
                    if oPlayer.energy < 1:
                        oPlayer.energy = 1
                    self.teams[self.team_index].energy = self.teams[self.team_index].energy + oPlayer.energy
                    oPlayer.caps = oPlayer.caps + 1
                else:
                    oPlayer.energy = oPlayer.energy + 9
                    if oPlayer.energy > 20:
                        oPlayer.energy = 20



    def PlayerInjured(self):
        '''
        Replacement for PROCINJ (line 5100) in the BBC Basic version.
        This gives players an injury.
        '''
        nPlayer = random.randint(0, 25)
        if self.players[nPlayer].injured:
            return
        self.DropPlayer(nPlayer)
        self.players[nPlayer].injured = True
        if self.players[nPlayer].in_squad:
            print('{}{} has been injured.{}'.format(modANSI.RED, self.players[nPlayer].name, modANSI.RESET_ALL))
            self.num_injured = self.num_injured + 1



    def PlayerFit(self):
        ''' This was part of PROCPROGRESS in the BBC Basic version. '''
        for oPlayer in self.players:
            if oPlayer.injured:
                if random.randint(1, 3) == 1:
                    oPlayer.injured = False
                    if oPlayer.in_squad:
                        print('{}{} is fit.{}'.format(modANSI.GREEN, oPlayer.name, modANSI.RESET_ALL))
                        self.num_injured = self.num_injured - 1



    def DisplaySquad(self):
        ''' Replacement for PROCPTEAM (line 2130) in the BBC Basic version. '''
        print('   Player        Skill Energy')
        for oPlayer in self.players:
            if oPlayer.in_squad:
                oPlayer.WriteRow()



    def PickPlayers(self):
        ''' Replacement for PROCPICK (line 2260) in the BBC Basic version. '''
        while True:
            modANSI.CLS()
            self.DisplaySquad()
            if self.num_team <= 11:
                nNumber = self.EnterNumber('>')
                if nNumber == 0:
                    break;
                if nNumber >= 1 and nNumber <= 26:
                    nNumber = nNumber - 1
                    if self.players[nNumber].in_squad:
                        self.AddPlayer(nNumber)
            else:
                nNumber = self.EnterNumber('Enter Player to Drop ')
                if nNumber >= 1 and nNumber <= 26:
                    self.DropPlayer(nNumber - 1)



    def DropPlayer(self, nIndex):
        ''' Replacement for PROCDROP (line ????) in the BBC Basic version. '''
        oPlayer = self.players[nIndex]
        if oPlayer.in_team == False:
            return
        oPlayer.in_team = False
        if oPlayer.position == modPlayer.DEFENSE:
            self.team.defence = self.team.defence - oPlayer.skill
        elif oPlayer.position == modPlayer.MIDFIELD:
            self.team.midfield = self.team.midfield - oPlayer.skill
        else:
            self.team.attack = self.team.attack - oPlayer.skill
        self.team.energy = self.team.energy - oPlayer.energy
        self.num_team = self.num_team - 1
        self.formation[oPlayer.position] = self.formation[oPlayer.position] - 1
        self.team.formation = '{}-{}-{}'.format(self.formation[modPlayer.DEFENSE]-1, self.formation[modPlayer.MIDFIELD], self.formation[modPlayer.ATTACK])



    def AddPlayer(self, nIndex):
        ''' Replacement for PROCIN (line 1580) in the BBC Basic version. '''
        oPlayer = self.players[nIndex]
        if oPlayer.in_team:
            return
        oPlayer.in_team = True
        if oPlayer.position == modPlayer.DEFENSE:
            self.team.defence = self.team.defence + oPlayer.skill
        elif oPlayer.position == modPlayer.MIDFIELD:
            self.team.midfield = self.team.midfield + oPlayer.skill
        else:
            self.team.attack = self.team.attack + oPlayer.skill
        self.team.energy = self.team.energy + oPlayer.energy
        self.num_team = self.num_team + 1
        self.formation[oPlayer.position] = self.formation[oPlayer.position] + 1
        self.team.formation = '{}-{}-{}'.format(self.formation[modPlayer.DEFENSE]-1, self.formation[modPlayer.MIDFIELD], self.formation[modPlayer.ATTACK])



    def SellPlayer(self):
        ''' Replacement for PROCSELL (line 1950) in the BBC Basic version. '''
        modANSI.CLS()
        self.DisplaySquad()
        print('Enter <RETURN> to return to menu.')
        print('Else enter player number to be sold')
        nPlayerNumber = self.EnterNumber('>')
        if nPlayerNumber >= 1 and nPlayerNumber <= 26:
            nPlayerNumber = nPlayerNumber - 1
            if self.players[nPlayerNumber].in_squad:
                nPrice = int((self.players[nPlayerNumber].skill + random.uniform(0, 1)) * 5000 * (5 - self.division))
                print('You are offered £{:,.2f}'.format(nPrice))
                print('Do you accept (Y/N)?')
                if self.YesNo():
                    self.num_squad = self.num_squad - 1
                    self.DropPlayer(nPlayerNumber)
                    self.players[nPlayerNumber].in_squad = False
                    self.money = self.money + nPrice
            else:
                print('On range')
            self.Wait()




    def Market(self):
        ''' Replacement for PROCMARKET (line 3330) in the BBC Basic version. '''
        if self.num_squad >= 18:
            # modANSI.CLS()
            print('{}F.A. rules state that one team may not have more that 18 players. You already have 18 players therefore you may not buy another.{}'.format(modANSI.RED, modANSI.RESET_ALL))
        else:
            while True:
                nPlayer = random.randint(0, 25)
                if self.players[nPlayer].in_squad == False:
                    break;
            # modANSI.CLS()
            self.players[nPlayer].skill = max(self.players[nPlayer].skill, random.randint(1, 5) + (1 if self.division <= 2 else 0))
            if self.players[nPlayer].position == modPlayer.DEFENSE:
                print('Defence')
            elif self.players[nPlayer].position == modPlayer.MIDFIELD:
                print('Mid-field')
            else:
                print('Attack')
            self.players[nPlayer].WriteRow(5000 * (5 - self.division))
            print('You have £{:,.2f}'.format(self.money))
            nBid = self.EnterNumber('Enter your bid: ')
            if nBid <= 0:
                return
            nPrice = self.players[nPlayer].skill * (5000 * (5 - self.division)) + random.randint(1, 10000) - 5000
            if nBid > self.money:
                print('{}You do not have enough money{}'.format(modANSI.RED, modANSI.RESET_ALL))
            elif nBid > nPrice:
                print('{}{} is added to your squad.{}'.format(modANSI.GREEN, self.players[nPlayer].name, modANSI.RESET_ALL))
                self.num_squad = self.num_squad + 1
                self.players[nPlayer].in_squad = True
                self.money = self.money - nBid
            else:
                if nBid > 0:
                    print('{}Your bid is turned down.{}'.format(modANSI.RED, modANSI.RESET_ALL))
        self.Wait()



    def Bank(self):
        ''' Replacement for PROCLEND (line 4170) in the BBC Basic version. '''
        modANSI.CLS()
        print('Bank')
        print('You have £{:,.2f}'.format(self.money))
        if self.debt > 0:
            print('You owe £{:,.2f}'.format(self.debt))
        else:
            print('In Bank £{:,.2f}'.format(-self.debt))
        print('Do you want to Deposit, Withdraw or Exit (D/W/E)?')
        sKey = self.GetKeyboardCharacter(['d', 'w', 'e'])
        if sKey == 'e':
            return
        if sKey == 'd':
            print('Deposit')
        else:
            print('Withdraw')
        nAmount = self.EnterNumber('Enter the amount >')
        if sKey == 'd':
            nAmount = -nAmount
        self.money = self.money + nAmount
        self.debt = self.debt + nAmount
        MAX_DEBT = 2e6 # 1e6
        if self.debt > MAX_DEBT:
            print('You can not have that much')
            self.money = self.money - (self.debt - MAX_DEBT)
            self.debt = MAX_DEBT
        if self.money < 0:
             self.debt = self.debt - self.money
             self.money = 0
        print('You have £{:,.2f}'.format(self.money))
        if self.debt > 0:
            print('You owe £{:,.2f}'.format(self.debt))
        else:
            print('In Bank £{:,.2f}'.format(-self.debt))
        self.Wait()



    def PlayerCaps(self):
        ''' This was part of PROCPROGRESS in the BBC Basic version. '''
        oPlayersByCaps = sorted(self.players, key=lambda CPlayer: CPlayer.caps, reverse=True)
        print('┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓')
        print('┃   Player         Position   Caps Goals ┃')
        for nIndex in range(11):
            oPlayer = oPlayersByCaps[nIndex]
            if oPlayer.injured:
                sPlayerColour = modANSI.RED
            elif oPlayer.in_team:
                sPlayerColour = modANSI.GREEN
            else:
                sPlayerColour = ''
            print('┃{}{:>2} {:<15}{:<10}{:>5}{:>6}{} ┃'.format(sPlayerColour, nIndex + 1, oPlayer.name, oPlayer.GetPosition(), oPlayer.caps, oPlayer.goals, modANSI.RESET_ALL))

        # Top Scorers.
        oPlayersByGoals = sorted(self.players, key=lambda CPlayer: CPlayer.goals, reverse=True)
        print('┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫')
        print('┃   Player         Position   Caps Goals ┃')
        for nIndex in range(5):
            oPlayer = oPlayersByGoals[nIndex]
            if oPlayer.injured:
                sPlayerColour = modANSI.RED
            elif oPlayer.in_team:
                sPlayerColour = modANSI.GREEN
            else:
                sPlayerColour = ''
            if oPlayer.goals > 0:
                print('┃{}{:>2} {:<15}{:<10}{:>5}{:>6}{} ┃'.format(sPlayerColour, nIndex + 1, oPlayer.name, oPlayer.GetPosition(), oPlayer.caps, oPlayer.goals, modANSI.RESET_ALL))
        print('┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')



    def DisplayMatch(self, nHome, nAway):
        ''' Replacement for PROCDISPLAY in the BBC Basic version. '''
        print('   {}{:^18}{}{:^18}{}'.format(self.teams[nHome].colour, self.teams[nHome].name, self.teams[nAway].colour, self.teams[nAway].name, modANSI.RESET_ALL))
        if True:
            print('Pos{:^18}{:^18}'.format(self.teams[nHome].position, self.teams[nAway].position))
        print('Eng{:^18}{:^18}'.format(self.teams[nHome].energy, self.teams[nAway].energy))
        print('Mor{:^18}{:^18}'.format(self.teams[nHome].moral, self.teams[nAway].moral))
        print('For{:^18}{:^18}'.format(self.teams[nHome].formation, self.teams[nAway].formation))
        print('Def{:^18}{:^18}'.format(self.teams[nHome].defence, self.teams[nAway].defence))
        print('Mid{:^18}{:^18}'.format(self.teams[nHome].midfield, self.teams[nAway].midfield))
        print('Att{:^18}{:^18}'.format(self.teams[nHome].attack, self.teams[nAway].attack))
        print()
        print('{} Picked, {} Squad, {} Injured.'.format(self.num_team, self.num_squad, self.num_injured))
        print('Press C to change team')
        print('Press TAB to play match.')



    def Wait(self):
        ''' Replacement for PROCWAIT in the BBC Basic version. '''
        print('----- Press SPACE to continue -----')
        self.GetKeyboardCharacter([' '])



    def ShowLeague(self):
        ''' Replacement for PROCLEAGUE in the BBC Basic version. '''
        print('Division {}'.format(self.division))
        print('   Team             W  D  L Pts Dif')
        for oTeam in self.teams:
            oTeam.WriteTableRow()
        print('Matches Played: {}'.format(self.match))
        print('{} position: {}'.format(self.team.GetColouredName(), self.team_index+1))



    def SortDivison(self):
        ''' Replacement for PROCSORT in the BBC Basic version. '''
        self.teams = sorted(self.teams, key=lambda CTeam: (CTeam.pts, CTeam.difference), reverse=True)
        nPosition = 1
        for oTeam in self.teams:
            oTeam.position = nPosition
            if oTeam.name == self.team_name:
                self.team_index = nPosition-1
                self.team = oTeam
            nPosition = nPosition + 1



    def NewGame(self):
        ''' Initialise a new game. '''
        self.PickTeam()

        # Initialise variables
        self.match = 0
        self.money = 50000
        self.debt = 200000

        # Initialise the players.
        self.players = []
        for nIndex in range(1, 27):
            oPlayer = modPlayer.CPlayer()
            oPlayer.GetPlayer(nIndex)
            oPlayer.skill = random.randint(1, 5)
            oPlayer.energy = random.randint(1, 20)
            self.players.append(oPlayer)
        for nIndex in range(4):
            nPlayer = random.randint(0, 25)
            self.players[nPlayer].skill = 5

        # Pick 12 players.
        self.num_squad = 12
        for nIndex in range(self.num_squad):
            nPlayer = random.randint(0, 25)
            while self.players[nPlayer].in_squad:
                nPlayer = random.randint(0, 25)
            self.players[nPlayer].in_squad = True

        # Initialise the teams.
        self.teams = None
        self.division = 4
        self.SetTeamsForDivision([])
        self.SortDivison()

        # Pick a default selection of players.
        self.num_team = 0
        self.num_injured = 0
        for nIndex in range(26):
            if self.players[nIndex].in_squad:
                if self.num_team < 11:
                    self.AddPlayer(nIndex)



    def SetTeamsForDivision(self, sExistingNames):
        ''' Replacement for PROCDIVISON (line 3520) in the BBC Basic version. '''
        if self.teams == None:
            self.teams = []
            for nTeam in range(16):
                oTeam = modTeam.CTeam()
                oTeam.name = ''
                self.teams.append(oTeam)
            self.teams[0].name = self.team_name
            self.teams[0].colour = self.team_colour
            self.teams[0].position = 1
        nDivision = self.division

        # Record the existing team names.
        for oTeam in self.teams:
            if oTeam.name != '':
                sExistingNames.append(oTeam.name)

        nNewTeam = 1
        for oTeam in self.teams:
            if oTeam.name == '':
                oTeam.GetTeam(nDivision, nNewTeam)
                # Check that this team is unique.
                while oTeam.name in sExistingNames:
                    nNewTeam = nNewTeam + 1
                    oTeam.GetTeam(nDivision, nNewTeam)

                sExistingNames.append(oTeam.name)
                nNewTeam = nNewTeam + 1

            if oTeam.name == self.team_name:
                # Initialise the players team.
                oTeam.Zero()
            else:
                # Initialise the opponent team.
                oTeam.Initialise(self.division)



    def MultiRandomInt(self, nRange, nNumber):
        ''' Replacement for FNRND() (Line 6640) in the BBC Basic version. This gives an integer result. '''
        nTotal = 0
        for nCount in range(nNumber):
            nTotal = nTotal + random.randint(1, nRange)
        return nTotal



    def MultiRandom(self, dRange, nNumber):
        ''' Replacement of FNRND (Line 6640) in the BBC Basic version. This gives a floating point result.  It is usually expected that dRange will be 1.'''
        dTotal = 0
        for nCount in range(nNumber):
            dTotal = dTotal + random.uniform(0, dRange)
        return dTotal



    def PickTeam(self):
        ''' Replacement for PROCPICKTEAM in the BBC Basic version. '''
        nDivision = 1
        while True:
            modANSI.CLS()
            print(' 0 More Teams')
            print(' 1 Own Team')
            for nIndex in range(2, 17):
                oTeam = modTeam.CTeam()
                oTeam.GetTeam(nDivision, nIndex - 1)
                print('{:2} {}'.format(nIndex, oTeam.GetColouredName()))
            nNumber = self.EnterNumber('Enter Team Number ')
            if nNumber >= 2 and nNumber <= 17:
                oTeam.GetTeam(nDivision, nNumber - 1)
                self.team_name = oTeam.name
                self.team_colour = oTeam.colour
                break;
            if nNumber == 1:
                self.team_name = input('Enter Team name ')
                self.team_colour = modANSI.CYAN
                break;
            nDivision = 1 + (nDivision & 3)
        print('You manage {}{}{}'.format(self.team_colour, self.team_name, modANSI.RESET_ALL))



    def EnterNumber(self, sMessage):
        ''' Enter a number at the keyboard. '''
        nNumber = 0
        try:
            nNumber = int(input(sMessage))
        except:
            nNumber = 0
        return nNumber



    def YesNo(self):
        ''' Replacement for FNYES in the BBC Basic version.  Returns True if 'Y' is pressed or False if 'N' is pressed. '''
        sCharacter = self.GetKeyboardCharacter(['y', 'n'])
        if sCharacter == 'y':
            return True
        return False



    def GetKeyboardCharacter(self, allowed):
        ''' Return a keyboard character from the allowed characters. '''
        # No Repeat Until in Python.
        sCharacter = modInkey.getwch()
        while not (sCharacter in allowed):
            sCharacter = modInkey.getwch()
        self.keyboard.Stop()
        return sCharacter



    def Football(self):
        ''' Implementation of DEFPROCfootball().  Display a title. '''
        print('┏━━             ┃       ┃ ┃   ┏━┳━┓')
        print('┃            ┃  ┃       ┃ ┃   ┃ ┃ ┃' )
        print('┣━━ ┏━┓ ┏━┓ ━#━ ┣━┓ ━━┓ ┃ ┃   ┃   ┃ ━━┓ ━┳━┓ ━━┓ ┏━┓ ┏━┓ ┏━')
        print('┃   ┃ ┃ ┃ ┃  ┃  ┃ ┃ ┏━┫ ┃ ┃   ┃   ┃ ┏━┃  ┃ ┃ ┏━┫ ┃ ┃ ┣━┛ ┃')
        print('┃   ┗━┛ ┗━┛  ┃  ┗#┛ ┗━┛ ┃ ┃   ┃   ┃ ┗━┛  ┃ ┃ ┗━┛ ┗━┫ ┗━━ ┃')
        print('                                                   ┃')
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')
        print('By Steve Walton BBC BASIC 1982-1989, 2000, Python 2018.')



    def Save(self, bInteractive):
        ''' Implementation of DEFPROCSAVE (5420) from the BBC Basic version. '''
        oFile = open('save.game', 'w')

        json.dump(self.match, oFile)
        oFile.write('\n')
        json.dump(self.money, oFile)
        oFile.write('\n')
        json.dump(self.debt, oFile)
        oFile.write('\n')
        json.dump(self.num_squad, oFile)
        oFile.write('\n')
        json.dump(self.num_team, oFile)
        oFile.write('\n')
        json.dump(self.num_injured, oFile)
        oFile.write('\n')
        json.dump(self.division, oFile)
        oFile.write('\n')
        json.dump(self.team_name, oFile)
        oFile.write('\n')
        json.dump(self.team_colour, oFile)
        oFile.write('\n')
        json.dump(self.formation, oFile)
        oFile.write('\n')

        # Save the players.
        for oPlayer in self.players:
            oPlayer.Dump(oFile)

        # Save the teams.
        for oTeam in self.teams:
            oTeam.Dump(oFile)

        oFile.close()

        print('Game Saved.')
        time.sleep(5)



    def Load(self):
        ''' Implementation of DEFPROCLOAD (line 5530) from the BBC Basic version. '''
        oFile = open('save.game', 'r')

        sLine = oFile.readline()
        self.match = json.loads(sLine)
        sLine = oFile.readline()
        self.money = json.loads(sLine)
        sLine = oFile.readline()
        self.debt = json.loads(sLine)
        sLine = oFile.readline()
        self.num_squad = json.loads(sLine)
        sLine = oFile.readline()
        self.num_team = json.loads(sLine)
        sLine = oFile.readline()
        self.num_injured = json.loads(sLine)
        sLine = oFile.readline()
        self.division = json.loads(sLine)
        sLine = oFile.readline()
        self.team_name = json.loads(sLine)
        sLine = oFile.readline()
        self.team_colour = json.loads(sLine)
        sLine = oFile.readline()
        self.formation= json.loads(sLine)

        # Load the players.
        self.players = []
        for nIndex in range(26):
            oPlayer = modPlayer.CPlayer()
            oPlayer.Load(oFile)
            self.players.append(oPlayer)

        # Load the teams.
        self.teams = []
        for nIndex in range(16):
            oTeam = modTeam.CTeam()
            oTeam.Load(oFile)
            self.teams.append(oTeam)

        oFile.close()



    def Fixtures(self, nOpponent):
        ''' Replacement for PROCFIXTURES (line 247) in the BBC Basic version. '''
        for oTeam in self.teams:
            oTeam.fixture = 0

        self.teams[self.team_index].fixture = -1
        self.teams[nOpponent].fixture = -1
        for nMatch in range(1, 8):
            while True:
                nHome = random.randint(0, 15)
                if self.teams[nHome].fixture == 0:
                    break;
            self.teams[nHome].fixture = nMatch * 2 - 1
            while True:
                nAway = random.randint(0, 15)
                if self.teams[nAway].fixture == 0:
                    break;
            self.teams[nAway].fixture = nMatch * 2

            # Swap if the away team has fewer month matches.



    def Rest(self):
        '''
        Replacement for DEFPROCREST (line 2710) in the BBC Basic version.
        This is play and display the rest of the matches in the league.
        '''
        for nMatch in range(1, 8):
            for nIndex in range(16):
                if self.teams[nIndex].fixture == 2 * nMatch -1:
                    nHome = nIndex
                if self.teams[nIndex].fixture == 2 * nMatch:
                    nAway = nIndex

            nHomeGoals, nAwayGoals = self.Match(nHome, nAway, 0.5, 0)
            print('{} {} - {} {}'.format(self.teams[nHome].GetColouredName(), nHomeGoals, nAwayGoals, self.teams[nAway].GetColouredName()))
            self.ApplyPoints(nHome, nAway, nHomeGoals, nAwayGoals)



    def PlayMatch(self, nHomeTeam, nAwayTeam, dHomeBonus, dAwayBonus):
        ''' Replacement for DEFPROCPLAYMATCH (Line 1680) in the BBC Basic version. '''
        nHomeGoals, nAwayGoals = self.Match(nHomeTeam, nAwayTeam, dHomeBonus, dAwayBonus)
        # Not implemented yet.

        # Decide when the goals are scored.
        naHomeGoals = []
        for nGoal in range(nHomeGoals):
            nGoalTime = random.randint(1, 90)
            if not (nGoalTime in naHomeGoals):
                naHomeGoals.append(nGoalTime)
        naAwayGoals = []
        for nGoal in range(nAwayGoals):
            nGoalTime = random.randint(1, 90)
            if not (nGoalTime in naAwayGoals):
                naAwayGoals.append(nGoalTime)

        # Decide who might score.
        naScorers = []
        for oPlayer in self.players:
            if oPlayer.in_team:
                if oPlayer.position == modPlayer.DEFENSE:
                    naScorers.append(oPlayer)
                elif oPlayer.position == modPlayer.MIDFIELD:
                    for nCount in range(oPlayer.skill):
                        naScorers.append(oPlayer)
                else:
                    for nCount in range(oPlayer.skill * 3):
                        naScorers.append(oPlayer)

        nHomeScore = 0
        nAwayScore = 0
        print('{} {} - {} {}'.format(self.teams[nHomeTeam].GetColouredName(), nHomeScore, nAwayScore, self.teams[nAwayTeam].GetColouredName()))
        for nTime in range(91):
            fRealTime = time.time()

            if nTime in naHomeGoals:
                nHomeScore = nHomeScore + 1
                modANSI.CursorUp(1)
                print('{} {} - {} {}'.format(self.teams[nHomeTeam].GetColouredName(), nHomeScore, nAwayScore, self.teams[nAwayTeam].GetColouredName()))
                nTotalScore = nHomeScore + nAwayScore
                if nHomeTeam == self.team_index:
                    modANSI.CursorDown(nTotalScore)
                    nScorer = random.randint(0, len(naScorers)-1)
                    print('{} {}'.format(nTime, naScorers[nScorer].name), end='\r')
                    naScorers[nScorer].goals = naScorers[nScorer].goals + 1
                    modANSI.CursorUp(nTotalScore)
                else:
                    modANSI.CursorDown(nTotalScore)
                    print('{} Goal'.format(nTime), end='\r')
                    modANSI.CursorUp(nTotalScore)

            if nTime in naAwayGoals:
                nAwayScore = nAwayScore + 1
                modANSI.CursorUp(1)
                print('{} {} - {} {}'.format(self.teams[nHomeTeam].GetColouredName(), nHomeScore, nAwayScore, self.teams[nAwayTeam].GetColouredName()))
                nTotalScore = nHomeScore + nAwayScore
                if nAwayTeam == self.team_index:
                    modANSI.CursorDown(nTotalScore)
                    nScorer = random.randint(0, len(naScorers)-1)
                    print('            {} {}'.format(nTime, naScorers[nScorer].name), end='\r')
                    naScorers[nScorer].goals = naScorers[nScorer].goals + 1
                    modANSI.CursorUp(nTotalScore)
                else:
                    modANSI.CursorDown(nTotalScore)
                    print('            {} Goal'.format(nTime), end='\r')
                    modANSI.CursorUp(nTotalScore)


            print('Time {}.  '.format(nTime), end='\r')
            sys.stdout.flush()
            time.sleep(fRealTime + 0.3 - time.time())

            if nTime == 45:
                print('Half Time.'.format(nTime), end='\r')
                sys.stdout.flush()
                # Did the fixture calculations here in the BBC Basic version.
                time.sleep(4)

        # Move down
        modANSI.CursorDown(nHomeGoals + nAwayGoals + 1)
        print('Final Score')
        print('{} {} - {} {}'.format(self.teams[nHomeTeam].GetColouredName(), nHomeGoals, nAwayGoals, self.teams[nAwayTeam].GetColouredName()))

        return nHomeGoals, nAwayGoals



    def Pois(self, U, C):
        ''' Replacement for DEFNPOIS (Line 7040) in the BBC Basic version. '''
        nT = 0
        P = math.exp(-U)
        if C < P:
            return 0
        S = P
        while True:
            nT = nT + 1
            P = P * U / nT
            S = S + P
            if C < S:
                break;
        return nT



    def Match(self, nHomeTeam, nAwayTeam, dHomeBonus, dAwayBonus):
        ''' Replacement for DEFPROCMATCH (Line 6920) in the BBC Basic version. '''
        oHome = self.teams[nHomeTeam]
        oAway = self.teams[nAwayTeam]
        dHomeAverageGoals = dHomeBonus + (4.0 * oHome.attack / oAway.defence) * oHome.midfield / (oHome.midfield + oAway.midfield) + (oHome.moral - 10.0) / 40.0 - (oAway.energy - 100.0) / 400.0
        dAwayAverageGoals = dAwayBonus + (4.0 * oAway.attack / oHome.defence) * oAway.midfield / (oAway.midfield + oHome.midfield) + (oAway.moral - 10.0) / 40.0 - (oHome.energy - 100.0) / 400.0
        nHomeGoals = self.Pois(dHomeAverageGoals, self.MultiRandom(1, 2) / 2)
        nAwayGoals = self.Pois(dAwayAverageGoals, self.MultiRandom(1, 2) / 2)

        # Set the moral for the teams.
        if nHomeGoals == nAwayGoals:
            oHome.moral = 10
            oAway.moral = 10
        else:
            if nHomeGoals > nAwayGoals:
                oHome.moral = max(oHome.moral, 10)
                oAway.moral = min(oAway.moral, 10)
                oHome.moral = min(oHome.moral + nHomeGoals - nAwayGoals, 20)
                oAway.moral = max(oAway.moral + nAwayGoals - nHomeGoals, 1)
            else:
                oHome.moral = min(oHome.moral, 10)
                oAway.moral = max(oAway.moral, 10)
                oHome.moral = max(oHome.moral + nHomeGoals - nAwayGoals, 1)
                oAway.moral = min(oAway.moral + nAwayGoals - nHomeGoals, 20)
        return nHomeGoals, nAwayGoals
