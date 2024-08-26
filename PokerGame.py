
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 17:16:44 2021

@author: arnaud.darche
"""
from itertools import permutations
import time
from random import randint
from itertools import combinations
from random import randrange
from collections import Counter
import cv2
import csv


#Helpful Functions for the game and the agents

import HelpfulFunctions



##### Create the game so that agent can play it
colors=['corazon','trebol','pica','rombo']
values=[1,2,3,4,5,6,7,8,9,10,11,12,13]
perm=permutations(values,len(colors))
positions_6p={0:"small blind",1:"big blind",2:"utg",3:"utg+1",4:"utg+2",5:"MP"}
playerStates=["Playing","All In","Fold","Out","Check","Raise","Call"]
actions_allowed=["Fold","Check","Call","2Raise","3Raise","AllInCall","AllInRaise","33Raise","50Raise"]
board_states={'Nothing':0,'Preflop':1,'Flop':2,'River':3,'Turn':4}
state_indexes={"board_state":[],"turn":[],"board1_val":[],"board2_val":[],
                "board3_val":[],"board4_val":[],"board5_val":[],
                "board1_col":[],"board2_col":[],"board3_col":[],
                "board4_col":[],"board5_col":[],"hand1_val":[],
                "hand2_val":[],"hand1_col":[],"hand2_col":[],"big_blinds0":[],
                "big_blinds1":[],"big_blinds2":[],"big_blinds3":[],
                "big_blinds4":[],"big_blinds5":[],"player_state0":[],
                "player_state1":[],"player_state2":[],"player_state3":[],
                "player_state4":[],"player_state5":[],"bet0":[],"bet1":[],
                "bet2":[],"bet3":[],"bet4":[],"bet5":[],
                "pot":[],"total_amount0":[],"total_amount1":[],
                "total_amount2":[],"total_amount3":[],"total_amount4":[],
                "total_amount5":[],"position":[]
                }





class Card: 
    
    def __init__(self,value=0,color=""):
        self.value=value
        self.color=color
        col_val={"":-1,"corazon":0,"rombo":1,"trebol":2,"pica":3}
        self.id=value + col_val[color]*100
        

    
class Board:
    def __init__(self,board1=Card(),board2=Card(),board3=Card(),board4=Card(),board5=Card(),num_players=6):
        # self.player=Player(0)

        self.bets=[0]*num_players
        self.bigBlinds=[0]*num_players
        self.states=[""]*num_players
        # self.cards=[self.player.hand0,self.player.hand1]+self.board
        self.state=None
        
    

    

    
        






class Player():
    
    def __init__(self,idPlayer,takeInfo=False,showCards=True):
        self.showCards=showCards
        self.id=idPlayer
        self.hand1=Card()
        self.hand2=Card()
        self.bigBlinds=None
        self.position=None
        self.state=None
        self.amount_played=0
        self.bet=0
        self.takeInfo=takeInfo
        self.states={c:[] for c in state_indexes.keys()}
        self.statesP={c:[] for c in state_indexes.keys()}
        self.moment="Pre"
        self.rewards=[]
        self.actions=[]        
        start=cv2.imread("handTemplate.png")
        self.img=start.copy()

    

    
    def save_observation(self, observation):
        
            if len(self.states["board_state"])<200000:
                if self.moment=="Post":
                    for i in self.statesP.keys():
                        self.statesP[i].append(observation[i])
                    rew=self.statesP["big_blindsP"][-1]-self.states["big_blindsP"][-1]
                    self.rewards.append(rew)
                    print("reward is: ",rew)
                    self.moment="Pre"
                if self.moment=="Done":
                    for i in self.statesP.keys():
                        self.statesP[i].append(observation[i])
                    rew=self.statesP["big_blindsP"][-1]-self.states["big_blindsP"][-1]
                    self.rewards.append(rew)
                if self.moment=="Pre":
                    for i in self.states.keys():
                        self.states[i].append(observation[i])
                    self.moment="Post"
            else:
                pass_to_csv(self.states,self.actions,self.rewards,self.statesP)

    
        
    def possibleActions(self,game):
        actions=[]
        if self.bet==game.highestBet:
            actions.append("Check")
            if self.bet!=0: #you are the Big Blind in preflop
                if self.bigBlinds+self.bet < game.highestBet*(2.5):
                    actions.append("AllInRaise")
                    return actions
                if self.bigBlinds+self.bet < game.highestBet*3:
                    actions.append("AllInRaise")
                    actions.append("2Raise")
                    return actions
                if self.bigBlinds+self.bet<game.highestBet*4:
                    actions.append("AllInRaise")
                    actions.append("2Raise")
                    actions.append("3Raise")
                    return actions
                actions.append("AllInRaise")
                actions.append("2Raise")
                actions.append("3Raise")
                actions.append("4Raise")
                return actions
            if self.bet==0: #the others have checked
                if self.bigBlinds+self.bet<game.pot / 3:
                    actions.append("AllInRaise")
                    return actions
                if self.bigBlinds+self.bet<game.pot / 2:
                    actions.append("33Raise")
                    actions.append("AllInRaise")
                    return actions
                if self.bigBlinds+self.bet<game.pot *0.75:
                    actions.append("33Raise")
                    actions.append("50Raise")
                    actions.append("AllInRaise")
                    return actions
                if self.bigBlinds+self.bet <game.pot:
                    actions.append("33Raise")
                    actions.append("50Raise")
                    actions.append("75Raise")
                    actions.append("AllInRaise")
                    return actions
                actions.append("33Raise")
                actions.append("50Raise")
                actions.append("75Raise")
                actions.append("potRaise")
                actions.append("AllInRaise")
                return actions
        if self.bet<game.highestBet:
            actions.append("Fold")
            if self.bigBlinds+self.bet <= game.highestBet:
                actions.append("AllInCall")
                return actions
            actions.append("Call")
            if self.bigBlinds+self.bet < game.highestBet*(2.5):
                actions.append("AllInRaise")
                return actions
            if self.bigBlinds+self.bet < game.highestBet*3:
                actions.append("AllInRaise")
                actions.append("2Raise")
                return actions
            if self.bigBlinds+self.bet < game.highestBet*4:
                actions.append("AllInRaise")
                actions.append("2Raise")
                actions.append("3Raise")
                return actions
            actions.append("AllInRaise")
            actions.append("2Raise")
            actions.append("3Raise")
            actions.append("4Raise")
            return actions
        
            
class Game():
    
    def __init__(self,draw=True,bBInitial=50,num_players=6,players=[Player(0),Player(1),Player(2),Player(3),Player(4),Player(5)],logs=False):
        self.bBInitial=bBInitial
        self.numPlayers=num_players
        self.players=players
        for player in self.players:
            player.bigBlinds=self.bBInitial
            player.position=player.id
        self.draw=draw
        self.image=cv2.imread("handTemplate.png")
        self.i=0
        self.stop=False
        self.logs=logs
        self.board1=Card()
        self.board2=Card()
        self.board3=Card()
        self.board4=Card()
        self.board5=Card()
        self.total_bet=[0]*num_players
        self.pot=0
        self.highestBet=0
        self.last_position_to_raise=None
        self.deck=None
        self.state=None
        self.reset()

    def get_state(self):
        if self.players[0].hand1.value is None:
            self.state=0
        if self.board1.value is None:
            self.state=1
        if self.board4.value is None:
            self.state=2
        if self.board5.value is None:
            self.state=3
        self.state=4


    def reset(self):
        for player in self.players:
            player.bigBlinds=self.bBInitial
            player.position=player.id
            player.bet=0
            player.amount_played=0
            player.hand1=Card()
            player.hand2=Card()
        self.state=None
        self.pot=0
        self.highestBet=0
        self.last_position_to_raise=None
        self.deck=createDeck()
        self.turn=0
        self.board1=Card()
        self.board2=Card()
        self.board3=Card()
        self.board4=Card()
        self.board5=Card()
        self.stop=False

    def step(self,action):
        if self.logs:
            print("step with action ",action)
        while self.players[self.turn].state in ("Out","Fold"):
            self.turn= (self.turn + 1 )%6
        if action in self.players[self.turn].possibleActions(self):
            print("Player ",self.turn," ",action)
            turn=self.turn
            bb=self.players[turn].bigBlinds
            self.update_game(self.turn,action)
            state=self.get_observation(self.turn)
            self.turn=(self.turn+1)%self.numPlayers
            self.round_of_bets()
            reward=self.players[turn].bigBlinds-bb
            return reward, state
        else:
            print("FAIL: UNVALID ACTION")
        

    def start_game(self):
        if self.logs:
            print("start_game")
        for player in self.players:
            player.state="Playing"
        self.start_preflop()

    def start_preflop(self): #player at position 0 is the small blind
        if self.logs:
            print("start_preflop")
        self.state=1    
        self.deck=createDeck()
        self.put_initial_blinds()
        self.giveCardsPlayers()
        self.turn=(self.BB+1)%self.numPlayers
        self.round_of_bets()
                        
    def round_of_bets(self):
        if self.logs:
            print("round_of_bets")
        self.draw_game("test"+str(self.i))
        playerStates=[player.state for player in self.players]
        if playerStates.count("All In")+playerStates.count("Fold")+playerStates.count("Out")==self.numPlayers: #everybody is allin
            self.trans_to_next_state()

        while self.players[self.turn].state in ("Fold","Out","All In"):    #if players are out skip them
            self.turn=(self.turn+1)%self.numPlayers
        if not (self.should_continue()):  
            self.trans_to_next_state()
            # player=self.players[self.turn]
            # if not(player.state in ("Fold","Out","All In")):
            #     next
                # action=str(player.act(board=self.board))
                # self.update_game(i%self.numPlayers,action)
                # self.draw_game("test"+str(self.i))
       
                
    def start_flop(self):
        if self.logs:
            print("start_flop")
        self.state=2
        r=randrange(len(self.deck))
        self.board1=self.deck[r]
        del self.deck[r]
        r=randrange(len(self.deck))
        self.board2=self.deck[r]
        del self.deck[r]            
        r=randrange(len(self.deck))
        self.board3=self.deck[r]
        del self.deck[r]
        self.turn=(self.BB)%self.numPlayers
        self.round_of_bets()
            
    def start_river(self):
        if self.logs:
            print("start_river")
        self.state=3
        r=randrange(len(self.deck))
        self.board4=self.deck[r]
        del self.deck[r]
        self.turn=(self.BB)%self.numPlayers
        self.round_of_bets()
 
    def start_turn(self):
        if self.logs:
            print("start_turn")
        self.state=4
        r=randrange(len(self.deck))
        self.board5=self.deck[r]
        del self.deck[r]
        self.turn=(self.BB)%self.numPlayers
        self.round_of_bets()       
        
    def put_initial_blinds(self): #at the beggining of the hand, put the blinds on the board
        if self.logs:
            print("put_initial_blinds")
        self.players=sorted(self.players,key=lambda x: x.position)
        SB=0
        BB=0
        for player in self.players: #Small blind is first player who is not Out
            if player.state!="Out" and SB!=0 and BB==0: #Big blind is second player who is not out
                BB=player
            if player.state!="Out" and SB==0:
                SB=player
        for player in self.players:
            player.position=(player.id - SB.id)%self.numPlayers
        self.players=sorted(self.players,key=lambda x: x.position)
        self.BB=self.players.index(BB)
        self.highestBet=max(min(SB.bigBlinds,0.5),min(BB.bigBlinds,1))
        amount=min(0.5,SB.bigBlinds)
        SB.bet+=amount
        SB.bigBlinds-= amount
        amount=min(1,BB.bigBlinds)
        BB.bet += amount
        BB.bigBlinds-= amount
        if SB.bigBlinds==0:
            SB.state="All In"
        if BB.bigBlinds==0:
            BB.state="All In"


    def giveCardsPlayers(self):
        if self.logs:
            print("giveCardsPlayers")
        for player in self.players:
            if not(player.state=="Out"):
                r=randrange(len(self.deck))
                player.hand1=self.deck[r]
                del self.deck[r]
                r=randrange(len(self.deck))
                player.hand2=self.deck[r]
                del self.deck[r]


    def update_game(self,position,action):
        if self.logs:
            print("update_game")
        print(action)
        player=self.players[position]
        if action=="Fold":
            player.state="Fold"
        if action=="Check":
            player.state="Check"
        if action=="Call":
            player.state="Call"
            amount=round(self.highestBet - player.bet,2)
            player.bet += amount
            player.bigBlinds = round(player.bigBlinds - amount,2)
        if action=="2Raise": #put on the board twice the amount of the highest bet
            amount=round(2.5*self.highestBet - player.bet,2)
            player.bet+=amount
            player.bigBlinds = round(player.bigBlinds - amount,2)
            self.highestBet*=2.5
            player.state="Raise"
        if action=="3Raise": #3raise the highest bet
            amount=round(3*self.highestBet - player.bet,2)
            player.bet+=amount
            player.bigBlinds = round(player.bigBlinds - amount,2)
            self.highestBet*=3                
            player.state="Raise"
        if action=="4Raise": #3raise the highest bet
            amount=round(4*self.highestBet - player.bet,2)
            player.bet+=amount
            player.bigBlinds = round(player.bigBlinds - amount,2)
            self.highestBet*=4
            player.state="Raise"
        if action=="AllInCall":
            amount=player.bigBlinds
            player.bet +=amount
            player.bigBlinds=0
            player.state="All In"
        if action=="AllInRaise":
            amount=player.bigBlinds
            player.bet+=amount
            player.bigBlinds=0
            self.highestBet=player.bet
            player.state="All In"
        if action=="33Raise": #raise a 1/3 of the pot (only on flop, turn and river)
            amount=round(1/3*self.pot,2)
            player.bet+=amount
            player.bigBlinds = round(player.bigBlinds - amount,2)
            self.highestBet=amount
            player.state="Raise"
        if action=="50Raise":
            amount=round(1/2*self.pot,2)
            player.bet+=amount
            player.bigBlinds = round(player.bigBlinds - amount,2)
            self.highestBet=amount
            player.state="Raise"
        if action=="75Raise":
            amount=round(0.75 *self.pot,2)
            player.bet+=amount
            player.bigBlinds = round(player.bigBlinds - amount,2)
            self.highestBet=amount
            player.state="Raise"
        if action=="potRaise":
            amount=self.pot
            player.bet+=amount
            player.bigBlinds = round(player.bigBlinds - amount,2)
            self.highestBet=amount
            player.state="Raise"

        
        
            
    def should_continue(self): #if player has checked, called or is all in, 
        fact1=self.players[self.turn].state in ["Check","Call","All In","Raise"]
        fact2=self.highestBet==self.players[self.turn].bet
        playerStates=[player.state for player in self.players]
        fact3=playerStates.count("Fold")+playerStates.count("Out")==self.numPlayers -1
        if self.logs:
            print("should_continue with result : ", not( (fact1 and fact2) or fact3))
        return not( (fact1 and fact2) or fact3)
        
        
    def trans_to_next_state(self): #put all the money on the pot, save the money each player has played and move to next state and if everybody hasfolded then give all the money to the other guy
        if self.logs:
            print("trans_to_next_state")
        for player in self.players:
            self.pot+=round(player.bet,2)
            player.amount_played +=round(player.bet,2)
            player.bet=0
            if player.state in ["Check","Call","Raise"]:
                player.state="Playing"
        self.highestBet=0
        for r in range(self.numPlayers):
            self.total_bet[r]+=self.players[r].bet
        states=[player.state for player in self.players]
        if states.count("All In")+states.count("Playing")==1: #everybody has folded
            Winner=[player for player in self.players if player.state=="All In" or player.state=="Playing"][0]
            Winner.bigBlinds+=self.pot
            self.start_new_hand()
        else: #go to next state
            if self.state==1:
                self.start_flop()
            elif self.state==2:
                self.start_river()        
            elif self.state==3:
                self.start_turn()    
            elif self.state==4:
                self.look_at_hands()

    
    def look_at_hands(self):
        if self.logs:
            print("look_at_hands")
        self.draw_game("test"+str(self.i),showCards=True)
        playerStates=[player.state for player in self.players]
        if playerStates.count("Playing")+playerStates.count("All In")==1: #only 1 left
            Winner=[player for player in self.players if player.state=="All In" or player.state=="Playing"][0]
            Winner.bigBlinds+=self.pot
            self.start_new_hand()
        else:
            inGame=[player for player in self.players if player.state in ['All In','Playing',"Call","Check","Raise"]]
            hands=[best_possible_hand(self,player) for player in inGame]
            best_player=0
            getMoney=[inGame[best_player]]
            for i in range(len(inGame)-1):
                winner=compare5Cards(hands[best_player],hands[i+1])
                if winner==0:
                    getMoney.append(inGame[i+1])
                if winner==1:
                    best_player=i+1
                getMoney=[inGame[best_player]]
                self.give_money(getMoney)
        
        
    def give_money(self,getMoney):
        if self.logs:
            print("give_money")
        states=[player.state for player in getMoney]
        if not("All In") in states:
            for player in getMoney:
                player.bigBlinds += round(self.pot /len(getMoney),2)
            self.start_new_hand()

        elif "All In" in states:
            toSplit=0
            sobrante=0
            minDraw=min(getMoney, key=lambda x: x.amount_played)
            amount=minDraw.amount_played
            for player in self.players:
                toSplit += min(player.amount_played,amount)
                sobrante += max(0,player.amount_played - amount)
                player.amount_played=max(0,player.amount_played - amount)
            for player in getMoney:
                player.bigBlinds += toSplit /len(getMoney)
            self.pot=sobrante
            for player in self.players: #bucle para poner en Fold los que ya no tengan nada que conseguir, no es necesario para el funcionamiento pero visualmente será más facil de entender creo.
                if player.amount_played==0:
                    player.state="Fold"
            if self.pot>0:
                self.look_at_hands()
                next
            else:
                self.start_new_hand()
                next



    def start_new_hand(self):
        if self.logs:
            print("start_new_hand")
        for player in self.players:
            if player.bigBlinds==0:
                player.state="Out"
                player.moment="Done"
                # player.get_observation(self.board)
            else:
                player.state="Playing"
            player.amount_played=0
            player.highestBet=0
            player.bet=0
            
        self.total_bet=[0]*self.numPlayers
        states=[player.state for player in self.players]
        print(states)
        if states.count("Out")==self.numPlayers - 1:
            self.end_game()
        else:
            print("no aqui no es")
            for player in self.players:
                player.position = (player.position - 1)%self.numPlayers
            for card in [self.board1,self.board2,self.board3,self.board4,self.board5]:
                card.value=0
                card.color=""
            self.pot=0
            self.deck=createDeck()
            self.start_preflop()
            
        
    def end_game(self):
        obs=self.get_observation(self.turn)
        print("Game Over")
        self.stop=True
        return obs

    
    def draw_game(self,name="Test",showCards=False):
        if self.logs:
            print("draw_game")
        if self.draw:
            print("States: ",[p.state for p in self.players])
            print("bigblinds:",[p.bigBlinds for p in self.players])
            print("bets:",[p.bet for p in self.players])
            print("Total bet:",self.total_bet)
            img=self.image.copy()
            for player in self.players: #draw cards
                if player.state in ["Playing","Call","Check","All In","Raise"]:
                    if player.showCards:
                        cv2.putText(img,str(player.hand1.value),coordsValueHand1(player.id),font,0.8,color[player.hand1.color])
                        cv2.putText(img,str(player.hand2.value),coordsValueHand2(player.id),font,0.8,color[player.hand2.color])
                        drawColor(img,coordsColorHand1(player.id),player.hand1.color)
                        drawColor(img,coordsColorHand2(player.id),player.hand2.color)
                if player.state=="Fold":
                    cv2.putText(img,"Fold",coordsValueHand1(player.id),font,2,black)  
                if player.state=="Out":
                    cv2.putText(img,"Out",coordsValueHand1(player.id),font,3,red)  
                cv2.putText(img,str(player.bigBlinds),coordsBB[str(player.id)],font,1,yellow,thickness=2)
                cv2.putText(img,str(player.bet),coordsBet[str(player.id)],font,0.8,red,thickness=2)
            board=[self.board1,self.board2,self.board3,self.board4,self.board5]
            for card in range(5):
                if not(board[card].value is None):
                    cv2.putText(img,str(board[card].value),coordsValueBoard(str(card)),font,0.8,black)
                    drawColor(img,coordsColorBoard(card),str(board[card].color))
            cv2.putText(img,str(self.pot),coordsPot,font,1,black,2)
            cv2.imwrite("visualization/test/"+name+".png", img)
            cv2.imshow("NoName",img)
            self.i+=1
            cv2.waitKey(0)
        
    def playGame(self,agents):
        for p in range(len(juego.players)):
            juego.players[p].agent=agents[p]
        self.start_game()
        while not self.stop:
            self.step(self.players[self.turn].agent.takeAction(self.get_observation(self.turn)))
        
        
    def get_observation(self,position):
        p=position
        
        state={"board_state":self.state,
               "board1_val":self.board1.value,"board2_val":self.board2.value,"board3_val":self.board3.value,"board4_val":self.board4.value,"board5_val":self.board5.value,
               "board1_col":self.board1.color,"board2_col":self.board2.color,"board3_col":self.board3.color,"board4_col":self.board4.color,"board5_col":self.board5.color,
               "hand1_val":self.players[p].hand1.value,"hand2_val":self.players[p].hand2.value,"hand1_col":self.players[p].hand1.color,"hand2_col":self.players[p].hand2.color,
               "big_blinds0":self.players[p].bigBlinds,"big_blinds1":self.players[(p+1)%6].bigBlinds,"big_blinds2":self.players[(p+2)%6].bigBlinds,"big_blinds3":self.players[(p+3)%6].bigBlinds,"big_blinds4":self.players[(p+4)%6].bigBlinds,"big_blinds5":self.players[(p+5)%6].bigBlinds,
               "player_state0":self.players[p].state,"player_state1":self.players[(p+1)%6].state,"player_state2":self.players[(p+1)%6].state,"player_state3":self.players[(p+3)%6].state,"player_state4":self.players[(p+4)%6].state,"player_state5":self.players[(p+5)%6].state,
               "bet0":self.players[p].bet,"bet1":self.players[(p+1)%6].bet,"bet2":self.players[(p+2)%6].bet,"bet3":self.players[(p+3)%6].bet,"bet4":self.players[(p+4)%6].bet,"bet5":self.players[(p+5)%6].bet,
               "pot":self.pot,"position":position,"turn":self.turn,"highestbet":self.highestBet,"last_position_to_raise":self.last_position_to_raise, "BB":self.BB,
               "total_amount0":self.total_bet[p],"total_amount1":self.total_bet[(p+1)%6],"total_amount2":self.total_bet[(p+2)%6],"total_amount3":self.total_bet[(p+3)%6],"total_amount4":self.total_bet[(p+4)%6],"total_amount5":self.total_bet[(p+5)%6]
                   }
        return state            

    def setup_obs(self, obs,p=0):
        self.deck=createDeck()

        self.state=obs['board_state']

        self.board1=Card(obs['board1_val'],obs['board1_col'])
        self.board2=Card(obs['board2_val'],obs['board2_col'])
        self.board3=Card(obs['board3_val'],obs['board3_col'])
        self.board4=Card(obs['board4_val'],obs['board4_col'])
        self.board5=Card(obs['board5_val'],obs['board5_col'])
        
        self.players[p].hand1=Card(obs['hand1_val'],obs['hand1_col'])
        self.players[p].hand2=Card(obs['hand2_val'],obs['hand2_col'])

        self.players[p].bigBlinds=obs['big_blinds0']
        self.players[(p+1)%6].bigBlinds=obs['big_blinds1']
        self.players[(p+2)%6].bigBlinds=obs['big_blinds2']
        self.players[(p+3)%6].bigBlinds=obs['big_blinds3']
        self.players[(p+4)%6].bigBlinds=obs['big_blinds4']
        self.players[(p+5)%6].bigBlinds=obs['big_blinds5']
        
        self.players[p].state=obs['player_state0']
        self.players[(p+1)%6].state=obs['player_state1']
        self.players[(p+2)%6].state=obs['player_state2']
        self.players[(p+3)%6].state=obs['player_state3']
        self.players[(p+4)%6].state=obs['player_state4']
        self.players[(p+5)%6].state=obs['player_state5']

        self.players[p].bet=obs['bet0']
        self.players[(p+1)%6].bet=obs['bet1']
        self.players[(p+2)%6].bet=obs['bet2']
        self.players[(p+3)%6].bet=obs['bet3']
        self.players[(p+4)%6].bet=obs['bet4']
        self.players[(p+5)%6].bet=obs['bet5']

        self.pot=obs['pot']
        self.position=obs['position']
        self.turn=obs['turn']
        self.highestBet=obs['highestbet']
        self.last_position_to_raise=obs['last_position_to_raise']
        self.BB=obs['BB']

        self.total_bet[p]=obs['total_amount0']
        self.total_bet[(p+1)%6]=obs['total_amount1']
        self.total_bet[(p+2)%6]=obs['total_amount2']
        self.total_bet[(p+3)%6]=obs['total_amount3']
        self.total_bet[(p+4)%6]=obs['total_amount4']
        self.total_bet[(p+5)%6]=obs['total_amount5']
        c1=[c.id for c in self.deck].index(self.players[p].hand1.id)
        del self.deck[c1]
        c2=[c.id for c in self.deck].index(self.players[p].hand2.id)
        del self.deck[c2]
        #Give random cards to the other players
        for p in range(self.numPlayers):
            player=self.players[(p+1)%6]
            r=randrange(len(self.deck))
            player.hand1=self.deck[r]
            del self.deck[r]
            r=randrange(len(self.deck))
            player.hand2=self.deck[r]
            del self.deck[r]

        


#------------------------------------------------------------------------------
# -----------------------------------------Drawings ---------------------------
#------------------------------------------------------------------------------

font=cv2.FONT_HERSHEY_SIMPLEX
#start=cv2.imread("handTemplate.png")
#img=start.copy()
coordsStartCards={"0":(404,521),"1":(169,346),"2":(368,174),"3":(751,156),"4":(1033,337),"5":(785,493)}
black=(0,0,0)
red=(0,0,255)
yellow=(0,255,242)
color={"pica":black,"trebol":black,"corazon":red,"rombo":red}
def sum_coords(a,x):
    return (a[0]+x[0],a[1]+x[1])

def coordsValueHand1(idplayer):
    return sum_coords(coordsStartCards[str(idplayer)],(12,30))
def coordsValueHand2(idplayer):
    return sum_coords(coordsStartCards[str(idplayer)],(69,30))
def coordsColorHand1(idplayer):
    return sum_coords(coordsStartCards[str(idplayer)],(12,40))
def coordsColorHand2(idplayer):
    return sum_coords(coordsStartCards[str(idplayer)],(69,40))

def drawColor(img,coords,color):
    if color=="corazon":
        drawHeart(img,coords)
    if color=="rombo":
        drawDiamond(img,coords)
    if color=="pica":
        drawSpades(img,coords)
    if color=="trebol":
        drawClover(img,coords)
        
def drawHeart(img,coords):
    cv2.rectangle(img, coords, sum_coords(coords,(15,15)), red,thickness=-1)
def drawDiamond(img,coords):
    cv2.circle(img, sum_coords(coords,(7,7)), 7, red,thickness=-1)
def drawSpades(img,coords):
    cv2.rectangle(img, coords, sum_coords(coords,(15,15)), black,thickness=-1)
def drawClover(img,coords):
    cv2.circle(img, sum_coords(coords,(7,7)), 7, black,thickness=-1)


coordsBB={"0":(600,688),"1":(113,507),"2":(517,41),"3":(908,43),"4":(1202,219),"5":(976,685)}
coordsPot=(531,422)
coordsBoardCard={"0":(473,319),"1":(530,319),"2":(584,319),"3":(641,319),"4":(696,319)}
coordsBet={"0":(413,507),"1":(282,415),"2":(363,277),"3":(741,257),"4":(923,386),"5":(769,478)}
def coordsValueBoard(card):
    return sum_coords(coordsBoardCard[str(card)],(12,30))
def coordsColorBoard(card):
    return sum_coords(coordsBoardCard[str(card)],(12,40))

# -----------------------------------------------------------------------------
#functions to pass to a csv a series of experiences, not sure experiences are 
#usually stored this way
#------------------------------------------------------------------------------


# times_appended=1
# num_excel=0

# def pass_to_csv(states,actions,rewards,statesP):
#     bigDict=states.update(statesP)
#     bigDict["Actions"]=actions
#     bigDict["Rewards"]=rewards
#     if not (len(actions)==len(rewards) and len(actions)==len(states["board_state"]) and len(actions)==len(statesP["board_states"])):
#         raise Exception("Length of states actions and rewards are not the same")
#     else:
#         if times_appended<5:
#             create_csv_from_dict(bigDict,"Plays_Poker_"+str(num_excel)+".csv")
#             times_appended+=1
#         else:
#             num_excel+=1
#             times_appended=1
#             create_csv_from_dict(bigDict,"Plays_Poker_"+str(num_excel)+".csv")

    
# def create_csv_from_dict(data_dict, filename):
#     # Get the keys from the dictionary
#     keys = list(data_dict.keys())

#     # Get the values from the dictionary
#     values = list(data_dict.values())

#     # Determine the maximum length of the values
#     max_length = max(len(val) for val in values)

#     # Prepare the rows for the CSV file
#     rows = []
#     rows.append(keys)  # Header row
#     for i in range(max_length):
#         row = [val[i] if i < len(val) else "" for val in values]
#         rows.append(row)

#     # Write the rows to the CSV file
#     with open(filename, "w", newline="") as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerows(rows)

#     print(f"CSV file '{filename}' created successfully.")

#-----------------------------------------------------------------------------
#------------------ HELPFUL FUNCTIONS ----------------------------------------
#-----------------------------------------------------------------------------




def createDeck() :   
    deck=[]
    deck_cards=[]
    for num in values:   
        zipped=[(num,col) for col in colors]
        deck+=zipped
    
    for d in deck:
        deck_cards+=[Card(d[0],d[1])]
    return deck_cards


#------------------------------ value and comparation of hands --------------------------------------
def add14(values): #As is counted as 1 by the programm, so for each 1 in the values, we add a 14
    if not (1 in values):
        return values
    else:
        num_as=values.count(1)
        for i in range(num_as):
            values.append(14)
        return values

def checkPair(values): #returns 1, the pair, the highest card, and the second highest card
    val=values.copy()    
    count=dict(Counter(val))
    if len(count)==len(val):
        return [False]
    else:
        pairs=[c for c in count if count[c]>1]
        max_pair=max(pairs)
        val=list(set(val))
        val.remove(max_pair)
        val.sort(reverse=True)
        return True, 1,max_pair,val[0],val[1],val[2]
    
def checkDoublePair(values): #returns 2, highest pair, the other pair, and the highest card
    val=values.copy()
    count=dict(Counter(val))
    pairs=[c for c in count if count[c]>1]
    if 1 in pairs:
        pairs.remove(1)
    if len(pairs)<2:
        return [False]
    else:
        val=list(set(val))
        val.remove(pairs[0])
        val.remove(pairs[1])
        return True, 2, max(pairs),min(pairs),max(val)
        
def checkThree(values): #returns 3, three value, highest card, and second highest card
    val=values.copy()
    count=dict(Counter(val))
    three=[c for c in count if count[c]>2]
    if three ==[]:
        return [False]
    else:
        val=list(set(val))
        val.remove(three[0])
        val.sort(reverse=True)
        return True, 3, three[0], val[0],val[1]
    
    
def checkStraight(values): #returns 4, and the highest card in straight
    val=values.copy()
    straights=[]
    for n in val:
        if n<11:
            if n+1 in val and n+2 in val and n+3 in val and n+4 in val:
                straights.append(n)
    if len(straights)>0:
        return True, 4, max(straights)+4
    return [False]
    
def checkFlush(colors,values): #returns 5 and all of the cards
    col=colors.copy()
    col=list(set(col))
    if len(col)==1:
        val=values.copy()
        val.sort(reverse=True)
        return True, 5, val[0],val[1],val[2],val[3], val[4]
    return [False]
    
def checkFull(values): #returns 6, three value and pair value
    val=values.copy()
    count=dict(Counter(val))
    pairs=[c for c in count if count[c]>1]
    three=[c for c in count if count[c]>2]
    if len(pairs)>0 and len(three)>0:
        return True, 6, max(three), max(pairs)      
    return [False]
    
def checkPoker(values): #returns 7, poker value and other value
    val=values.copy()
    count=dict(Counter(val))
    four=[c for c in count if count[c]==4]
    if len(four)>0:
        val=list(set(val))
        val.remove(four[0])
        return True, 7, max(four),max(val)
    return [False]
    
def checkStraightFlush(color,values): #returns 8 and highest value
    if checkFlush(color,values)[0]:
        straight=checkStraight(values)
        if straight[0]:    
            return True, 8, straight[2]
    return [False]

def value_5cards(list5cards):
    colors=[card.color for card in list5cards]
    values=[card.value for card in list5cards]
    add14(values)
    if checkStraightFlush(colors,values)[0]:
        return checkStraightFlush(colors,values)[1:]
    elif checkPoker(values)[0]:
        return checkPoker(values)[1:]
    elif checkFull(values)[0]:
        return checkFull(values)[1:]
    elif checkFlush(colors,values)[0]:
        return checkFlush(colors,values)[1:]
    elif checkStraight(values)[0]:
        return checkStraight(values)[1:]
    elif checkThree(values)[0]:
        return checkThree(values)[1:]
    elif checkDoublePair(values)[0]:
        return checkDoublePair(values)[1:]
    elif checkPair(values)[0]:
        return checkPair(values)[1:]
    else:
        values.sort(reverse=True)
        return 0, values[0], values[1],values[2]
    
#1 if first wins, -1 if second wins, 0 if draw
def compare5Cards(fiveCards1,fiveCards2): 
    value_1=value_5cards(fiveCards1)
    value_2=value_5cards(fiveCards2)
    for i in range(len(value_1)):
        if value_1[i]>value_2[i]:
            return -1
        if value_1[i]<value_2[i]:
            return 1
    return 0

#Doesn't return best hand, return value of best hand
def best_possible_hand(game,player): 

    hands=possible_hands(game,player)
    best_hand=hands[0]
    for hand in hands:
        if compare5Cards(best_hand, hand)==1:
            best_hand=hand
    val=value_5cards(best_hand)
    return best_hand

def possible_hands(game,player):
    board=[game.board1,game.board2,game.board3,game.board4,game.board5]
    if game.state==2:
        return [player.hand+board[:3]]
    if game.state==3:
        return list(combinations([player.hand1,player.hand2]+board[:4],5))
    if game.state==4:
        return list(combinations([player.hand1,player.hand2]+board,5))
    



#------------------------------------------------------------------------------
p=Player(0)
p2=Player(5,takeInfo=True)
# juego=Game()

juego=Game(bBInitial=50,num_players=6,logs=True)
# juego.start_game()
