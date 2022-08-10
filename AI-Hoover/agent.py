from random import random
from matplotlib import collections
import torch
import random
import os
import numpy as np
from collections import deque
from simulation import BLOCK_SIZE, RobotState, Hoover_Environement, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot
import argparse as ap
import pygame


MAX_MEMORY = 100_000
BATCH_SIZE = 1000
EXP_TRADE = 80
LR = 0.001

class Agent:

    def __init__(self):
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')
            
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.85 # discount rate 0 -> 1
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(20, 256, 4).to(self.device) # taken Suction out of the equation
        #self.model = Linear_QNet(21, 256, 5).to(self.device)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma, device=self.device)

    def get_state(self, game):
        robot = game.Robot.get_state()
        dir_l = robot.Direction == Direction.LEFT
        dir_r = robot.Direction == Direction.RIGHT
        dir_u = robot.Direction == Direction.UP
        dir_d = robot.Direction == Direction.DOWN

        state = [
            # Move direction
            dir_l,
            dir_r,
            dir_u, 
            dir_d,

            # Robot State
            robot.Power,
            robot.Recharge,
            #robot.Suction,
            robot.Motor,
            robot.Load,

            # Environement Locations
            game.Bin.x <  robot.Position.x,
            game.Bin.x >  robot.Position.x,
            game.Bin.y <  robot.Position.y,
            game.Bin.y >  robot.Position.y,
            game.Recharge.x < robot.Position.x,
            game.Recharge.x > robot.Position.x,
            game.Recharge.y < robot.Position.y,
            game.Recharge.y > robot.Position.y,
            game.dirt.x < robot.Position.x,
            game.dirt.x > robot.Position.x,
            game.dirt.y < robot.Position.y,
            game.dirt.y > robot.Position.y,
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # pop left if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state, trade=EXP_TRADE):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = trade - self.n_games
        final_move = [0,0,0,0]#,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3) #4)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float).to(self.device)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move

def train(file):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    agent.model.load(file)
    game = Hoover_Environement()
    game.Robot.command(pygame.K_SPACE) #switch on suction

    # Training loop
    while True:
        # Get Old State
        state_old = agent.get_state(game)

        # Get Move
        final_move = agent.get_action(state_old)

        # Perform move and get new state
        reward, done, score = game.play_step_ai(final_move)
        state_new = agent.get_state(game)

        # Train Short Memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # Remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Train long memory, plot results
            game.reset()
            game.Robot.command(pygame.K_SPACE) #switch on suction
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save(score=record)
            
            print('Game:', agent.n_games, 'Score:', score, 'Record:', record)

            # Plot
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores, str(agent.model))

def play(file):
    agent = Agent()
    agent.model.load(file)
    game = Hoover_Environement()
    game.Robot.command(pygame.K_SPACE) #switch on suction

    # Training loop
    while True:
        # Get Old State
        state_old = agent.get_state(game)

        # Get Move
        final_move = agent.get_action(state_old, 0) # No random
        print('Moves:', game.frame_iteration)
        # Perform move and get new state
        reward, done, score = game.play_step_ai(final_move)
        state_new = agent.get_state(game)

        if done:
            # Train long memory, plot results
            game.reset()            
            game.Robot.command(pygame.K_SPACE) #switch on suction
            agent.n_games += 1            
            print('Game:', agent.n_games, 'Score:', score)

def main(args):
    if args.load is None:
        file = None
    else:
        file = args.load[0]

    if args.train:
        train(file)
    else:
        play(file)

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='An AI Hoover Training Agent')
    parser.add_argument('-t', '--train', action='store_true', help='Train the AI')
    parser.add_argument('-l','--load', required=False, nargs=1, type=str, help='Load the specified AI state dictionary')
    args = parser.parse_args()
    main(args)
