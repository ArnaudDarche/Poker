# -*- coding: utf-8 -*-
"""
Created on Mon May 13 18:38:00 2024

@author: Arnaud
"""

# SO, SOMEIMES THE GAME BREAKS IT SEEMS, HARD TO ESTIMATE WHEN BECAUSE IT 
# DOESNT HAPPEN OFTEN. MUST BE A WEIRD CASE, TRY TO SAVE PICTURES OF EACHMOVE IN A FOLDER AND 
# MAKE IT PLAY 10 TIMES. IT IS SURELY GOING TO BUG AT SOME POINT, THEN YOU CAN LOOK
# AT THE PICTURES. IF THAT DOESNT WORK, TRY TO CREATE A LOG IN NOTEBOOK OF STATES.
# WILL BE HELPFUL IN THE FUTURE BUT REALLY SHITTY TO WORK WITH. WELL NOT THAT SHITTY
# AS MAYBE I CAN REPLICATE SOME SPECIFIC STATE. THAT WOULD BE NICE. CREATE A FUNCTION
# THAT REPLICATE A GAME WITH SOME SPECIFIC OBSERVATION

#NECESITO HACER UNA FUNCION QUE LE DE CARTAS A LOS JUGADORES Y LAS QUITE DE LA BARAJA o ALGO ASi


# OK, logs are done, I would add the last action made maybe



from basicAgents import randomAgent
from basicAgents import basicAgent
from PokerGame import Game

import pandas as pd
import matplotlib.pyplot as plt


agents=[randomAgent()]*5+[basicAgent()]
def play_one_game(agents,juego=Game(),logs=False,nombre_logs="logs_poker.txt"):
    juego.reset()
    juego.start_game()
    for p in juego.players:
        p.agent=agents[p.id]
    timestamp=0
    blind_evol=pd.DataFrame(columns=["timestamp"]+["Player_"+str(i) for i in range(juego.numPlayers)])
    while not juego.stop:
        turn=juego.turn
        # id_turn=juego.players[turn].id
        obs=juego.get_observation(turn)
        if write_logs:
            write_logs(obs,nombre_logs)
        # starter=(6+id_turn)%6
        bigblinds=[juego.players[i%6].bigBlinds for i in range(juego.numPlayers)]
        print(bigblinds)
        add_to_df=[timestamp]+bigblinds
        blind_evol.loc[timestamp]=add_to_df
        juego.step(juego.players[turn].agent.takeAction(obs))
        timestamp+=1
    return blind_evol

def play_a_lot_of_games(n_games,agents,drawing=False,logs=False,nombre_logs="logs_poker.txt"):
    juego_t=Game(draw=drawing)
    blind_evol=pd.DataFrame(columns=["game","timestamp"]+["Player_"+str(i) for i in range(juego_t.numPlayers)])
    for j in range(n_games):
        print("Game number:",j)
        write_logs('new game, number '+ str(j),nombre_logs)
        juego_t.reset()
        game=j
        be=play_one_game(agents,juego_t,drawing,logs,nombre_logs)
        be["game"]=game
        blind_evol.append(be)
    return blind_evol
    
def write_logs(obs,nombre_archivo='logs_poker.txt'):
    with open(nombre_archivo,'a') as archivo:
        archivo.write(str(obs))
        archivo.write('\n')

# for i in range(6):
#     player = 'Player_' + str(i)
#     plt.plot(blind_evol['timestamp'], blind_evol[player], label=player)

# # Configurar etiquetas y título del gráfico
# plt.xlabel('Timestamp')
# plt.ylabel('Fichas')
# plt.title('Fichas de los jugadores a lo largo del tiempo')
# plt.legend()  # Mostrar leyenda con los nombres de los jugadores



# correr simulaciones y replicar una observación
# juego=Game()
# play_a_lot_of_games(10,agents)
# obs={'board_state': 2, 'board1_val': 0, 'board2_val': 3, 'board3_val': 1, 'board4_val': 2, 'board5_val': 5, 'board1_col': '', 'board2_col': 'trebol', 'board3_col': 'corazon', 'board4_col': 'trebol', 'board5_col': 'pica', 'hand1_val': 5, 'hand2_val': 6, 'hand1_col': 'pica', 'hand2_col': 'corazon', 'big_blinds0': 7.46, 'big_blinds1': 0, 'big_blinds2': 0, 'big_blinds3': 0, 'big_blinds4': 0.0, 'big_blinds5': 0, 'player_state0': 'Raise', 'player_state1': 'Out', 'player_state2': 'Out', 'player_state3': 'Out', 'player_state4': 'Out', 'player_state5': 'Out', 'bet0': 8.040000000000001, 'bet1': 0, 'bet2': 281.0, 'bet3': 0, 'bet4': 0, 'bet5': 0, 'pot': 2.0, 'position': 4, 'turn': 4, 'highestbet': 281.0, 'last_position_to_raise': None, 'BB': 4, 'total_amount0': 0, 'total_amount1': 0, 'total_amount2': 0, 'total_amount3': 0, 'total_amount4': 0, 'total_amount5': 0}

# juego.setup_obs(obs_0)
# juego.draw_game()