# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 12:02:26 2023

@author: Arnaud
"""
# Some basic Agents
from random import randint

import HelpfulFunctions
from HelpfulFunctions import Card
from HelpfulFunctions import createDeck
from HelpfulFunctions import possible_actions
from HelpfulFunctions import real_value
from HelpfulFunctions import best_possible_hand
from HelpfulFunctions import possible_hands
from HelpfulFunctions import value_5cards

from PokerGame import Game

import pandas as pd


class randomAgent():
    
    def __init__(self,takeInfo=False):
        self.human=0
        self.name="Random"

        
    def takeAction(self,obs):
        possibleActions=possible_actions(obs)
        r=randint(0, len(possibleActions)-1)
        return possibleActions[r]
        
            
            
class humanAgent():
    
    def __init__(self,takeInfo=False):
        self.human=1       
        self.takeInfo=takeInfo
        self.name="Human"
        
    def takeAction(self,obs):
        possibleActions=possible_actions(obs)
        what= input(possibleActions)
        return possibleActions[int(what)]        
    
class basicAgent():
    #this agent will check/fold if there are better hands than his hand
    #   and will raise randomly if there are not better hands
    
    def __init__(self,takeInfo=False):
        self.takeInfo=takeInfo
        self.name="Basic"
        
    def takeAction(self,obs):
        hand1_val=real_value(obs['hand1_val'])
        hand2_val=real_value(obs['hand2_val'])
        actions=possible_actions(obs)
        if obs['board_state']==1:
            if hand1_val+hand2_val>=26:
                doables=['3Raise','33Raise','AllInRaise','AllInCall']
                return [a for a in doables if a in actions][0]
            else:
                return [a for a in ("Check","Fold") if a in actions][0]
        elif obs['board_state']>1:
            Cards=[Card(obs['hand1_val'],obs['hand1_col']),Card(obs['hand2_val'],obs['hand2_val'])]+[Card(obs['board'+str(i)+'_val'],obs['board'+str(i)+'_col']) for i in [1,2,3,4,5] if obs['board'+str(i)+'_val']>0]
            if value_5cards(Cards)==best_possible_hand(Cards)[0]:
                doables=['3Raise','33Raise','AllInRaise','AllInCall']
                return [a for a in doables if a in actions][0]
            else:
                doables=['Check','Fold']
                return [a for a in doables if a in actions][0]
                    
        
   
# def better_hands(obs):
#     cards_val=[obs['board1_val'],
#                obs['board2_val'],
#                obs['board3_val'],
#                obs['board4_val'],
#                obs['board5_val'],
#                obs['hand1_val'],
#                obs['hand2_val']]
#     cards_val=[i for i in cards_val if i>0]
#     cards_col=[obs['board1_col'],
#                obs['board2_col'],
#                obs['board3_col'],
#                obs['board4_col'],
#                obs['board5_col'],
#                obs['hand1_col'],
#                obs['hand2_col']]
#     cards_col=[i for i in cards_col if i!=""]
#     cards=[Card(0,cards_val[i],cards_col[i]) for i in range(len(cards_val))]
#     deck=createDeck()
#     next
    
    
#for test
obs_test={'board1_val':1,
          'board2_val':3,
          'board3_val':5,
          'board4_val':7,
          'board5_val':9,
          'hand1_val':1,
          'hand2_val':11,
          'board1_col':'trebol',
          'board2_col':'trebol',
          'board3_col':'trebol',
          'board4_col':'corazon',
          'board5_col':'corazon',
          'hand1_col':'corazon',
          'hand2_col':'corazon'
          }

# juego.playGame([randomAgent()]*5+[basicAgent()])

# juego.playGame([randomAgent()]*6)



            
        