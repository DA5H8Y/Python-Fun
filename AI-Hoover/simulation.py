from opcode import stack_effect
from operator import truediv
from pickle import FALSE
import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Point():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other):
        return ((self.x == other.x) & (self.y == other.y))

RobotState = namedtuple('RobotState', 'Position, Direction, Power, Recharge, Suction, Motor, Load')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
GREEN = (0, 200, 0)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 40

class Robot_Hover:
    def __init__(self, w, h) -> None:
        self.Position = Point(w/2, h/2)
        self.Direction = Direction.LEFT
        self.Motor = False
        self.Power = 100
        self.Suction = False
        self.Recharge = False
        self.Capacity = 18 * 18
        self.Load = 0
        self.Width = w
        self.Height = h
    
    def reset(self, w, h):
        self.Position = Point(w, h)
        self.Direction = Direction.LEFT
        self.Motor = False
        self.Power = 100
        self.Suction = False
        self.Recharge = False
        self.Capacity = 18 * 18
        self.Load = 0
        self.Width = w
        self.Height = h

    def update_step(self, recharge, bin, dirt):
        if self.Motor:
            self._move()
        
        if self.Suction:
            dirt = self._suck(dirt)
        
        if ((self.Position == recharge) and (self.Power < 100)):
            self.Motor = False
            self.Suction = False
            self.Recharge = True
        else:
            self.Recharge = False

        if self.Position == bin:
            self.Load = 0

        self._update_power()

        return dirt

    def get_state(self):
        return RobotState(self.Position, self.Direction, self.Power, self.Recharge, self.Suction, self.Motor, self.Load)

    def command(self, event):
        if event.type in (pygame.K_UP, pygame.K_DOWN):
            self._lateral()
        elif event.type == pygame.K_LEFT:
            self._rotation([0, 0, 1])
        elif event.type == pygame.K_RIGHT:
            self._rotation([0, 1, 0])
        elif event.type == (pygame.K_SPACE):
            # 3. Suction On/Off
            self._suction()

    def _rotation(self, action):
        # [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [0,1,0]): #right
            next_idx = (idx + 1) % 4
            self.Direction = clock_wise[next_idx]
        elif np.array_equal(action, [0,0,1]): #left
            next_idx = (idx - 1) % 4
            self.Direction = clock_wise[next_idx]
    
    def _lateral(self):
        self.Motor = not self.Motor

    def _suction(self):
        self.Suction = not self.Suction

    def _move(self):
        x = self.Position.x
        y = self.Position.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        
        if self._is_collision(Point(x, y)): # If it would be a collision stop
            self.Position = self.Position
            self.Motor = False
        else:
            self.Position = Point(x, y)

    def _is_collision(self, pt=None):
        if pt is None:
            pt = self.Position

        # hits boundary
        if pt.x > self.Width - BLOCK_SIZE or pt.x < 0 or pt.y > self.Height - BLOCK_SIZE or pt.y < 0:
            return True

        return False

    def _suck(self, dirt):
        if dirt == self.Position:
            if self.Capacity - self.Load > 0:
                self.Load += 1
                return None
            else:
                return dirt
        else:
            return dirt

    def _update_power(self):
        if self.Suction:
            self.Power -= 1
            self.Suction = False if self.Power == 0 else self.Suction
            self.Motor = False if self.Power == 0 else self.Motor  
        
        if self.Motor:
            self.Power -= 1
            self.Suction = False if self.Power == 0 else self.Suction
            self.Motor = False if self.Power == 0 else self.Motor  
        
        if self.Recharge:
            self.Power += 1
            self.Recharge = True if self.Power < 100 else False


class Hoover_Environement:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h

        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # init game state
        self.Robot = Robot_Hover(self.w, self.h)
        self.Bin = Point(0, 0)
        self.Recharge = Point(0, self.h)
        self.score = 0
        self.food = None
        self._place_dirt()
        self.frame_iteration = 0

    def _place_dirt(self):
        x = random.randint(0, (self.w - 1 ) // 1 )
        y = random.randint(0, (self.h - 1 ) // 1 )
        self.dirt = Point(x, y)

        if self.dirt == self.Robot.get_state().Position:
            self._place_dirt()

    def play_step(self):
        self.frame_iteration += 1

        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE):
                self.Robot.command(event)
        
        # 2. Update Simulation
        self.state_old = self.Robot.get_state()
        self.dirt = self.Robot.update_step(self.Recharge, self.Bin, self.dirt)
        self.state_new = self.Robot.get_state()

        # 3. check if game over
        reward = 0
        game_over = False
        if self.state_new.Power == 0 and not self.state_new.Recharge:
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.dirt is None:
            self.score += 0.5
            reward = 10
            self._place_dirt()
   
        # 5. check for load dump
        if self.state_old.Load > self.state_new.Load:
            for x in range(self.state_old.Load):
                self.score += 0.5
            reward = 10
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. return game over and score
        return reward, game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        # 1. Draw dirt
        pygame.draw.rect(self.display, RED, pygame.Rect(self.dirt.x, self.dirt.y, BLOCK_SIZE, BLOCK_SIZE))

        # 2. Draw Recharge
        pygame.draw.rect(self.display, BLUE2, pygame.Rect(self.Recharge.x, self.Recharge.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, BLACK, pygame.Rect(self.Recharge.x + 2, self.Recharge.y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))

        # 2. Draw Bine
        pygame.draw.rect(self.display, GREEN, pygame.Rect(self.Bin.x, self.Bin.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, BLACK, pygame.Rect(self.Bin.x + 2, self.Bin.y + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))

        # 1. Draw hoover
        pos = self.state_new.Position
        pygame.draw.rect(self.display, BLUE1, pygame.Rect(pos.x, pos.y, BLOCK_SIZE, BLOCK_SIZE))

        # 2. Draw power
        for x in range(self.state_new.Power//20):
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pos.x, pos.y + x, 1, 1))
        
        # 3. Draw state
        if self.state_new.Suction:            
            pygame.draw.rect(self.display, GREEN, pygame.Rect(pos.x + 1, pos.y, BLOCK_SIZE, 2))
        elif self.state_new.Recharge:
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pos.x + 1, pos.y, BLOCK_SIZE, 2))
        else:
            pygame.draw.rect(self.display, WHITE, pygame.Rect(pos.x + 1, pos.y, BLOCK_SIZE, 2))

        # 4. Draw load
        for l in range(self.state_new.Load):
            x = l // 20
            y = l % 20
            pygame.draw.rect(self.display, RED, pygame.Rect(pos.x + x, pos.y + y, 1, 1))



        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

def main():
    sim = Hoover_Environement()
    while True:
        sim.play_step()

if __name__ == '__main__':
    main()