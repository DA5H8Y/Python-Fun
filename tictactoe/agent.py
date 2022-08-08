import random
import sys
import time
import numpy as np
import torch
from collections import deque
from game import TicTacToe
from pygame.locals import *
import pygame as pg
from helper import plot
from model import Linear_QNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
EXP_TRADE = 80
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.85
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(10, 256, 9)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    
    def get_state(self, game):
        player = ord(game.XO)
        board = np.array(game.board).flatten()
        board = [' ' if v is None else v for v in board]   
        state = np.array([ord(x) for x in board])
        state = np.insert(state, 0, player)
        return np.array(state, dtype=int)

    def valid_move(self, game, move):
        board = np.array(game.board).flatten()
        board = [0 if v is None else 1 for v in board]
        for x in range(9):
            if move[x] == 1:
                if board[x] == 1:
                    return False
        return True

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = EXP_TRADE - self.n_games
        final_move = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 8)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move

def train():
    plot_scores1 = []
    plot_mean_scores1 = []
    total_score1 = 0
    record1 = 0
    plot_scores2 = []
    plot_mean_scores2 = []
    total_score2 = 0
    record2 = 0
    score1 = 0
    score2 = 0

    agent1 = Agent()    
    agent2 = Agent()
    game = TicTacToe()

    # Training loop
    while True:
        # Get Old State
        state_old = agent1.get_state(game)

        if chr(state_old[0]) == 'x':
            # Get Move
            final_move = agent1.get_action(state_old)
        else:
            # Get Move
            final_move = agent2.get_action(state_old)
        
        if agent1.valid_move(game, final_move):            
            # Perform move and get new state        
            reward = 0
            winner, draw = game.play_step(final_move)
            if draw is True:
                reward = -5
                score1 = 0
                score2 = 0

            if winner is not None:
                if winner == 'x':
                    if chr(state_old[0]) == 'x':
                        reward = 10
                    else:
                        reward = -10
                    score1 += 1
                    score2 = 0
                else:
                    if chr(state_old[0]) == 'x':
                        reward = -10
                    else:
                        reward = 10
                    score1 = 0
                    score2 += 1
        else:
            reward = -5
        
        state_new = agent1.get_state(game)

        done = (winner is not None or draw is True)        

        if chr(state_old[0]) == 'x':
            # Train Short Memory
            agent1.train_short_memory(state_old, final_move, reward, state_new, done)

            # Remember
            agent1.remember(state_old, final_move, reward, state_new, done)
        else:            
            # Train Short Memory
            agent2.train_short_memory(state_old, final_move, reward, state_new, done)

            # Remember
            agent2.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Train long memory, plot results
            game.reset_game()
            agent1.n_games += 1
            agent2.n_games += 1
            agent1.train_long_memory()
            agent2.train_long_memory()

            if score1 > record1:
                record1 = score1
                agent1.model.save(score=record1)

            if score2 > record2:
                record2 = score2
                agent2.model.save(score=record2)

            print('Game:', agent1.n_games, 'P1 Wins:', score1, 'P1 Record:', record1, 'P2 Wins:', score2, 'P2 Record:', record2)

            """
            # Plot1
            plot_scores1.append(score1)
            total_score1 += score1
            mean_score1 = total_score1 / agent1.n_games
            plot_mean_scores1.append(mean_score1)
            plot(plot_scores1, plot_mean_scores1, str(agent1.model))

            # Plot2
            plot_scores2.append(score1)
            total_score2 += score2
            mean_score2 = total_score2 / agent2.n_games
            plot_mean_scores2.append(mean_score2)
            plot(plot_scores2, plot_mean_scores2, str(agent2.model))
            """

def play(FileName=''):
    agent = Agent()   
    agent.model.load(FileName)
    game = TicTacToe()

    while True:
        # Get Old State
        state_old = agent.get_state(game)

        if chr(state_old[0]) == 'x':
            # Get Move
            final_move = agent.get_action(state_old)
            if agent.valid_move(game, final_move):            
                # Perform move and get new state        
                winner, draw = game.play_step(final_move)
        else:
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    game.user_click()
                    winner = game.winner
                    draw = game.draw

        done = (winner is not None or draw is True) 

        if done:
            game.reset_game()

if __name__ == '__main__':
    if len(sys.argv) == 2:
            if sys.argv[1].endswith('.pth'):
                play(sys.argv[1])
            else:
                print('Expect path to state dictionary to end with <.pth>')
    else:
        train()
