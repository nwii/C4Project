import numpy as np
import copy
from scipy.signal import convolve2d
import Opponents as op
import tensorflow as tf
import time
import sys

def checkvalid(board, col):
    """
    Checks to see if top row is filled
    :param col: int (0-6)
    :return:
    """
    return board[0][col] == 0


def getrow(board, col):
    """
    gets lowest unused row in column
    :param col: int (0-6)
    :return:
    """
    for r in range(5, -1, -1):
        if board[r][col] == 0:
            return r


def checkwin(board, player):
    """
    Convolves true/false matrix with win conditions, checks if any are connected by 4
    :param player:
    :return:
    """
    winhorizontal = np.array([[1, 1, 1, 1]]) # shape of a horizontal win
    winvert = np.transpose(winhorizontal) # shape of a vertical win
    windiag1 = np.eye(4, dtype=int) # shape of one diagonal win
    windiag2 = np.fliplr(windiag1) # shape of the other diagonal win
    
    wincons = [winhorizontal, winvert, windiag1, windiag2]
    
    for wincon in wincons: # check for each win across the entire board using convolve2d
        if (convolve2d(board == player, wincon, mode="valid") == 4).any():
            return True
    return False

class game:
    def __init__(self):
        self.board = np.zeros((6,7)) # board initialized to zeros
        self.turn = 0 # player is (turn % 2)+1
        self.gameover = False
        self.winner = None
        self.history = [np.zeros((6,7)), np.zeros((6,7))] # history contains only two boards (final and prefinal)

    def reset(self): # reset game to starting state
        self.board = np.zeros((6, 7))
        self.turn = 0
        self.gameover = False
        self.winner = None
        self.history = [np.zeros((6,7)), np.zeros((6,7))]

    def show(self): # display current board
        print("")
        print(self.board)
        pass

    def showhis(self): # display history
        for i in self.history:
            print(i)
            
    def getnextmoves(self): # retuens array of possible next moves
        nextMoves = []
        boardBackup = copy.deepcopy(self.board)
        for i in range(0,7):
            self.makemove(i, True) # make a temporary move
            nextMoves.append(self.board) # append the board configuration resulting from that move
            self.board = copy.deepcopy(boardBackup) # restore the board backup
            self.turn = 0
        return nextMoves

    def makemove(self, col, test=False):
        """
        checks if move is "overflowing",
        puts player's "token" on the lowest free space
        checks for win condition
        :param col: int (0-6), Column on board
        :param test: boolean, true -> just simulating the move, false -> actually making the move
        :return:
        """
        player = (self.turn % 2) + 1 # alternate player making the move

        if checkvalid(self.board, col): # if the move is valid...
            row = getrow(self.board, col) # get the lowest unused row of the board for the selected column
            self.board[row][col] = player # place that player's piece on that position
            

            if checkwin(self.board, player): # if a win is detected...
                if test == False: # and the move isn't being simulated, it's actually being made
                    self.history[1] = copy.deepcopy(self.board) # put the board array into the final history slot
                    self.winner = player
                    self.gameover = True
                    self.turn += 1
                    return

            self.turn += 1
            
        else:
            checktie = True # temp, assume it's a tie until proven not
            for i in range(0, 7): # for each possible column...
                if checkvalid(self.board, i): # check to see if any moves can be made
                    checktie = False # if so, we're not at a tie yet
            if checktie: # if no legal moves are left...
                if test == False: # and the move isn't being simulated, it's actually being made
                    self.history[1] = copy.deepcopy(self.board)
                    self.winner = 0
                    self.gameover = True
                    return
                
        self.history[0] = copy.deepcopy(self.board) # for every move that isn't a game-ender, append the board
                                                    # to history slot 0 (the prefinal slot)
            
class gamecontrol:
    """
    controls the game object and associated players
    """
    def __init__(self, game, Player1, Player2):
        self.game = game
        self.player1 = Player1
        self.player2 = Player2

    def playgame(self, show=True):
        player = self.player1
        while not self.game.gameover: # until the end of the game...
            move = player.move()      # prompt whichever player's turn it is to generate a move
            self.game.makemove(move, False) # make that move for the game
            if player == self.player1: # update which player is next
                player = self.player2
            else:
                player = self.player1
            if show: 
                self.game.show()
        winner = copy.deepcopy(self.game.winner)
        hist = copy.deepcopy(self.game.history)
        self.game.reset()
        return winner, hist

    def playmultiple(self, iterations):
        """
        plays i games,
        For each game: (takes the history from each game, assigns winner label to all boards on that game)
        :param iterations: int
        :return: [[winner, boardstate], [winner, boardstate] ...]
        """
        x = []
        y = []
        p1wins = 0
        p2wins = 0
        tstart = time.time()
        for i in range(0,iterations+1): # for each iteration...
            localwinner, localhis = self.playgame(show=False) # play a game
            if localwinner == 1: # log the winner
                p1wins += 1
            elif localwinner == 2:
                p2wins += 1
            for j in localhis: # for all board configs saved...
                y.append(localwinner) # append the winner (label) to y
                x.append(j) # append the board configuration array (input) to x
            tcur = time.time() - tstart
            sys.stdout.write("\r" + "{:.2f}%   time: {:.0f} secs".format(100 * i / iterations, tcur))
            sys.stdout.flush()
        X = np.dstack(x)
        X = np.rollaxis(X, -1)
        # X = np.array(x)
        Y = np.array(y)
        return X, Y, p1wins, p2wins
    
    