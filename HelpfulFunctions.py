# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 17:26:20 2024

@author: Arnaud
"""
from itertools import permutations
import time
from random import randint
from itertools import combinations
from random import randrange
from collections import Counter
import cv2


##### Create the game so that agent can play it
colors=['corazon','trebol','pica','rombo']
values=[1,2,3,4,5,6,7,8,9,10,11,12,13]
perm=permutations(values,len(colors))
positions_6p={0:"small blind",1:"big blind",2:"utg",3:"utg+1",4:"utg+2",5:"MP"}
playerStates=["Playing","All In","Fold","Out","Check","Raise","Call"]
actions_allowed=["Fold","Check","Call","2Raise","3Raise","AllInCall","AllInRaise","33Raise","50Raise"]
board_states={'Nothing':0,'Preflop':1,'Flop':2,'River':3,'Turn':4}
state_indexes={"board_state":[],"board1_val":[],"board2_val":[],
                "board3_val":[],"board4_val":[],"board5_val":[],
                "board1_col":[],"board2_col":[],"board3_col":[],
                "board4_col":[],"board5_col":[],"hand1_val":[],
                "hand2_val":[],"hand1_col":[],"hand2_col":[],"big_blindsP":[],
                "big_blinds1":[],"big_blinds2":[],"big_blinds3":[],
                "big_blinds4":[],"big_blinds5":[],"player_stateP":[],
                "player_state1":[],"player_state2":[],"player_state3":[],
                "player_state4":[],"player_state5":[],"betP":[],"bet1":[],
                "bet2":[],"bet3":[],"bet4":[],"bet5":[],
                "pot":[],"total_amountP":[],"total_amount1":[],
                "total_amount2":[],"total_amount3":[],"total_amount4":[],
                "total_amount5":[],"position":[]
                }

class Card: 
    
    def __init__(self,value=0,color=""):
        self.value=value
        self.color=color
        

    
class Board:
    def __init__(self,hand1=Card(0),hand2=Card(1),board1=Card(2),board2=Card(3),board3=Card(4),board4=Card(5),board5=Card(6),num_players=6):
        # self.player=Player(0)
        self.board1=board1
        self.board2=board2
        self.board3=board3
        self.board4=board4
        self.board5=board5
        self.board=[self.board1,self.board2,self.board3,self.board4,self.board5]
        self.bets=[0]*num_players
        self.total_bet=[0]*num_players
        self.bigBlinds=[0]*num_players
        self.states=[""]*num_players
        # self.cards=[self.player.hand0,self.player.hand1]+self.board
        self.state=None
        self.pot=0
        self.highestBet=0
        self.last_position_to_raise=None
        
    
    def get_state(self):
        if self.hand1.value is None:
            self.state=0
        if self.board1.value is None:
            self.state=1
        if self.board4.value is None:
            self.state=2
        if self.board5.value is None:
            self.state=3
        self.state=4
    

    
        



def createDeck() :   
    deck=[]
    for num in values:   
        zipped=[(num,col) for col in colors]
        deck+=zipped
    return deck


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
    
def compare5Cards(fiveCards1,fiveCards2): #1 if first wins, -1 if second wins, 0 if draw
    value_1=value_5cards(fiveCards1)
    value_2=value_5cards(fiveCards2)
    for i in range(len(value_1)):
        if value_1[i]>value_2[i]:
            return -1
        if value_1[i]<value_2[i]:
            return 1
    return 0

def best_possible_hand(Cards): #Doesn't return best hand, return value of best hand and best hand

    hands=possible_hands(Cards)
    best_hand=hands[0]
    for hand in hands:
        if compare5Cards(best_hand, hand)==1:
            best_hand=hand
    val=value_5cards(best_hand)
    return val,best_hand


def possible_hands(Cards):
    return list(combinations(Cards,5))

    
def possible_actions(obs):
    actions=[]
    highestBet=max([obs['bet0'],obs['bet1'],obs['bet2'],obs['bet3'],obs['bet4'],obs['bet5']])
    bet=obs['bet0']
    bigBlinds=obs['big_blinds0']
    if bet==highestBet:
        actions.append("Check")
        if bet!=0:
            if bigBlinds+bet<highestBet*(2.5):
                actions.append("AllInRaise")
                return actions
            if bigBlinds+bet<highestBet*3:
                actions.append("AllInRaise")
                actions.append("2Raise")
                return actions
            if bigBlinds+bet<highestBet*4:
                actions.append("AllInRaise")
                actions.append("2Raise")
                actions.append("3Raise")
                return actions
            actions.append("AllInRaise")
            actions.append("2Raise")
            actions.append("3Raise")
            actions.append("4Raise")
            return actions
        if bet==0:
            if bigBlinds+bet<obs['pot']/3:
                actions.append("AllInRaise")
                return actions
            if bigBlinds+bet<obs['pot']/2:
                actions.append("33Raise")
                actions.append("AllInRaise")
                return actions
            if bigBlinds+bet<obs['pot']*0.75:
                actions.append("33Raise")
                actions.append("50Raise")
                actions.append("AllInRaise")
                return actions
            if bigBlinds+bet<obs['pot']:
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
    if bet<highestBet:
        actions.append('Fold')
        if bigBlinds+bet<=highestBet:
            actions.append("AllInCall")
            return actions
        actions.append("Call")
        if bigBlinds+bet<=highestBet*(2.5):
            actions.append("AllInRaise")
            return actions
        if bigBlinds+bet<=highestBet*3:
            actions.append("AllInRaise")
            actions.append("2Raise")
            return actions
        if bigBlinds+bet<=highestBet*4:
            actions.append("AllInRaise")
            actions.append("2Raise")
            actions.append("3Raise")
            return actions
        actions.append("AllInRaise")
        actions.append("2Raise")
        actions.append("3Raise")
        actions.append("4Raise")
        return actions

def real_value(num):
    if num==1:
        return 14
    else:
        return num