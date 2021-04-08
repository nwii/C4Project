import numpy as np
import copy
from scipy.signal import convolve2d
import Opponents as op

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
    :param col:
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
    winhorizontal = np.array([[1, 1, 1, 1]])
    winvert = np.transpose(winhorizontal)
    windiag1 = np.eye(4, dtype=int)
    windiag2 = np.fliplr(windiag1)
    wincons = [winhorizontal, winvert, windiag1, windiag2]
    for wincon in wincons:
        if (convolve2d(board == player, wincon, mode="valid") == 4).any():
            return True
    return False

class game:
    def __init__(self):
        self.board = np.zeros((6,7))
        self.turn = 0 # player is (turn % 2)+1
        self.gameover = False
        self.winner = None
        self.history = []

    def reset(self):
        self.board = np.zeros((6, 7))
        self.turn = 0
        self.gameover = False
        self.winner = None
        self.history = []

    def show(self):
        print("")
        print(self.board)
        pass

    def showhis(self):
        for i in self.history:
            print(i)

    def makemove(self, col):
        """
        checks if move is "overflowing",
        puts player's "token" on the lowest free space
        checks for win condition
        :param col: int (0-6), Column on board
        :return:
        """
        player = (self.turn % 2) + 1

        if checkvalid(self.board, col):
            row = getrow(self.board, col)
            self.board[row][col] = player
            self.history.append(copy.deepcopy(self.board))

            if checkwin(self.board, player):
                self.winner = player
                self.gameover = True

            self.turn += 1
        else:
            checktie = True
            for i in range(0, 7):
                if checkvalid(self.board, i):
                    checktie = False
            if checktie:
                self.winner = 0
                self.gameover = True


class gamecontrol:
    """
    game is a game object
    Player 1 should have a .move (0-6)
    """
    def __init__(self, game, Player1, Player2):
        self.game = game
        self.player1 = Player1
        self.player2 = Player2

    def playgame(self):
        player = self.player1
        while not self.game.gameover:
            move = player.move()
            self.game.makemove(move)
            if player == self.player1:
                player = self.player2
            else:
                player = self.player1
        winner = copy.deepcopy(self.game.winner)
        hist = copy.deepcopy(self.game.history)
        #print(self.game.board)
        self.game.reset()
        return winner, hist

    def playmultiple(self, iterations):
        """
        plays i games,
        For each game: (takes the history from each game, assigns winner label to all boards on that game)
        :param iterations: int
        :return: [[winner, boardstate], [winner, boardstate] ...]
        """
        hist = []
        for i in range(0,iterations+1):
            localwinner, localhis = self.playgame()
            for i in localhis:
                hist.append([i, localwinner])
        return hist


if __name__ == '__main__':
    g1 = game()
    player1 = op.RP(g1)
    player2 = op.RP(g1)
    control = gamecontrol(g1, player1, player2)
    xdata = control.playmultiple(600)
    print(len(xdata))
    # winner, history = control.playgame()
    # print("winner: {}".format(winner))
    # for i in history:
    #     print(i)