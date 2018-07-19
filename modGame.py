#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to implement the CGame class for the the BBC Football Manager program.
'''

# System libraries.
import random

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
        else:
            print('No')
            self.NewGame()

        # Play the game.
        self.match = 0
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
                # PROCSELL
                pass
            elif sKey == '2':
                # PROCLEND
                pass
            elif sKey == '3':
                # PROCRENAME
                pass
            elif sKey == '4':
                # Continue.
                self.PlayWeek()
            elif sKey == '5':
                # PROCSAVE
                pass
            elif sKey == '6':
                # PROCRESTART
                pass
            elif sKey == '7':
                self.ShowLeague()
                self.Wait()
            elif sKey == '8':
                # Confirm with the user.
                print('Are you sure you want to exit the program (Y/N) ?')
                if self.YesNo():
                    return

        # Season has finished.
        print('Season has finished.')



    def PlayWeek(self):
        ''' This is the block of code that was after the menu in the week loop of the BBC Basic version. Line 740 onward.'''
        self.match = self.match+1

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

        if bHome:
            self.teams[nOpponent].pts = self.teams[nOpponent].pts + 1
        else:
            self.teams[nOpponent].pts = self.teams[nOpponent].pts + 2
        self.teams[nOpponent].difference = self.teams[nOpponent].difference + random.randint(0, 5) - random.randint(0, 5)

        self.SortDivison()
        self.ShowLeague()
        self.Wait()



    def DisplaySquad(self):
        ''' Replacement for PROCPTEAM (line 2130) in the BBC Basic version. '''
        print('   Player Skill Energy')
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
                nNumber = nNumber - 1
                if self.players[nNumber].in_squad:
                    self.AddPlayer(nNumber)
            else:
                nNumber = self.EnterNumber('Enter Player to Drop ')
                if nNumber >= 1 and nNumber <= 26:
                    self.DropPlayer(nNumber - 1)



    def DropPlayer(self, nIndex):
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
        modANSI.CLS()
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
        self.SetTeamsForDivision()
        self.SortDivison()



    def SetTeamsForDivision(self):
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

        nNewTeam = 1
        for oTeam in self.teams:
            if oTeam.name == '':
                oTeam.GetTeam(nDivision, nNewTeam)
                # Check that this team is unique.
                nNewTeam = nNewTeam+1
            if oTeam.name == self.team_name:
                # Initialise the players team.
                oTeam.Zero()
            else:
                # Initialise the opponent team.
                oTeam.Initialise(self.division)



    def MultiRandomInt(self, nRange, nNumber):
        ''' Replacement for FNRND() (Line 6640) in the BBC Basic version. '''
        nTotal = 0
        for nCount in range(nNumber):
            nTotal = nTotal + random.randint(1, nRange)
        return nTotal



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


