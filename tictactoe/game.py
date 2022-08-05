import sys
from matplotlib.backend_bases import MouseEvent
import numpy as np
import pygame as pg
import sys
import time
from pygame.locals import *

class TicTacToe():
    def __init__(self):
        self.XO = 'x'
        self.winner = None
        self.draw = None
        self.width = 400
        self.height = 400
        self.bg_color = (255, 255, 255)
        self.line_color = (0, 0, 0)
        self.board = [[None]*3, [None]*3, [None]*3]

        # intialize the pygame window
        pg.init()

        # setting the fps manually
        self.fps = 30

        # this is used to track time
        self.CLOCK = pg.time.Clock()

        #this method is used to build the infrastructure of the display
        self.screen = pg.display.set_mode((self.width, self.height + 100), 0, 32)

        # set the nametag for the window
        pg.display.set_caption("My Tic Tac Toe")

        # loading the images as python object
        initiating_window = pg.image.load("modified_cover.png")
        x_img = pg.image.load("X_modified.png")
        o_img = pg.image.load("o_modified.png")
  
        # resizing images
        self.initiating_window = pg.transform.scale(initiating_window, (self.width, self.height + 100))
        self.x_img = pg.transform.scale(x_img, (80, 80))
        self.o_img = pg.transform.scale(o_img, (80, 80))

        self.game_initiating_window()

    def game_initiating_window(self):
        # displaying over the screen
        self.screen.blit(self.initiating_window, (0, 0))
     
        # updating the display
        pg.display.update()
        #time.sleep(0)                   
        self.screen.fill(self.bg_color)
  
        # drawing vertical lines
        pg.draw.line(self.screen, self.line_color, (self.width / 3, 0), (self.width / 3, self.height), 7)
        pg.draw.line(self.screen, self.line_color, (self.width / 3 * 2, 0), (self.width / 3 * 2, self.height), 7)
  
        # drawing horizontal lines
        pg.draw.line(self.screen, self.line_color, (0, self.height / 3), (self.width, self.height / 3), 7)
        pg.draw.line(self.screen, self.line_color, (0, self.height / 3 * 2), (self.width, self.height / 3 * 2), 7)
        self.draw_status()
  
    def draw_status(self):
        if self.winner is None:
            message = self.XO.upper() + "'s Turn"
        else:
            message = self.winner.upper() + " won !"
        
        if self.draw:
            message = "Game Draw !"
  
        # setting a font object
        font = pg.font.Font(None, 30)
     
        # setting the font properties like
        # color and width of the text
        text = font.render(message, 1, (255, 255, 255))
  
        # copy the rendered message onto the board
        # creating a small block at the bottom of the main display
        self.screen.fill ((0, 0, 0), (0, 400, 500, 100))
        text_rect = text.get_rect(center =(self.width / 2, 500-50))
        self.screen.blit(text, text_rect)
        pg.display.update()

    def check_win(self):
        # checking for winning rows
        for row in range(0, 3):
            if((self.board[row][0] == self.board[row][1] == self.board[row][2]) and (self.board [row][0] is not None)):
                self.winner = self.board[row][0]
                pg.draw.line(self.screen, (250, 0, 0),
                     (0, (row + 1) * self.height / 3 - self.height / 6),
                     (self.width, (row + 1) * self.height / 3 - self.height / 6 ), 4)
                break
  
        # checking for winning columns
        for col in range(0, 3):
            if((self.board[0][col] == self.board[1][col] == self.board[2][col]) and (self.board[0][col] is not None)):
                self.winner = self.board[0][col]
                pg.draw.line (self.screen, (250, 0, 0), ((col + 1) * self.width / 3 - self.width / 6, 0), \
                      ((col + 1) * self.width / 3 - self.width / 6, self.height), 4)
                break
  
        # check for diagonal winners
        if (self.board[0][0] == self.board[1][1] == self.board[2][2]) and (self.board[0][0] is not None):
            # game won diagonally left to right
            self.winner = self.board[0][0]
            pg.draw.line (self.screen, (250, 70, 70), (50, 50), (350, 350), 4)
         
        if (self.board[0][2] == self.board[1][1] == self.board[2][0]) and (self.board[0][2] is not None):
            # game won diagonally right to left
            self.winner = self.board[0][2]
            pg.draw.line (self.screen, (250, 70, 70), (350, 50), (50, 350), 4)
  
        if(all([all(row) for row in self.board]) and self.winner is None ):
            self.draw = True
 
        self.draw_status()

    def drawXO(self, row, col):     
        # for the first row, the image should be pasted at a x coordinate of 30 from the left margin
        if row == 1:
            posx = 30
      
        # for the second row, the image should be pasted at a x coordinate of 30 from the game line    
        if row == 2:
            # margin or width / 3 + 30 from the left margin of the window
            posx = self.width / 3 + 30
     
        if row == 3:
            posx = self.width / 3 * 2 + 30
  
        if col == 1:
            posy = 30
            
        if col == 2:
            posy = self.height / 3 + 30
     
        if col == 3:
            posy = self.height / 3 * 2 + 30
         
        # setting up the required board value to display
        self.board[row-1][col-1] = self.XO
     
        if(self.XO == 'x'):
            # pasting x_img over the screen at a coordinate position of (pos_y, posx) defined in the above code
            self.screen.blit(self.x_img, (posy, posx))
            self.XO = 'o'
        else:
            self.screen.blit(self.o_img, (posy, posx))
            self.XO = 'x'
        pg.display.update()
  
    def user_click(self):
        # get coordinates of mouse click
        x, y = pg.mouse.get_pos()
  
        # get column of mouse click (1-3)
        if(x < self.width / 3):
            col = 1
        elif (x < self.width / 3 * 2):
            col = 2
        elif(x < self.width):
            col = 3
        else:
            col = None
  
        # get row of mouse click (1-3)
        if(y < self.height / 3):
            row = 1
        elif (y < self.height / 3 * 2):
            row = 2
        elif(y < self.height):
            row = 3
        else:
            row = None
       
        # after getting the row and col, we need to draw the images at the desired positions
        if(row and col and self.board[row - 1][col - 1] is None):
            self.drawXO(row, col)
            self.check_win()

    def play_step(self, final_move):
        for x in range(9):
            if final_move[x] == 1:
                row = (x // 3) + 1
                col = (x % 3) + 1
                break

        # after getting the row and col, we need to draw the images at the desired positions
        if(row and col and self.board[row - 1][col - 1] is None):
            self.drawXO(row, col)
            self.check_win()
        
        return self.winner, self.draw

    def reset_game(self):
        time.sleep(0.5)
        self.xo = 'x'
        self.draw = False
        self.game_initiating_window()
        self.winner = None        
        self.board = [[None]*3, [None]*3, [None]*3]
    
def main():
    game = TicTacToe()

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                game.user_click()

                if(game.winner or game.draw):
                    game.reset_game()
        
        pg.display.update()
        game.CLOCK.tick(game.fps)

if __name__ == '__main__':
    main()
