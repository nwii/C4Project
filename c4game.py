import numpy as np
import copy
from scipy.signal import convolve2d
import Opponents as op
import tensorflow as tf

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
            
    def getnextmoves(self):
        nextMoves = [] # init. array of possible next moves to return
        boardBackup = copy.deepcopy(self.board)
        #turnBackup
        #print("Board backup: ")
        #print(boardBackup)
        for i in range(0,7):
            #print("Making a temp move: ")
            self.makemove(i, True)
            #print(self.board)
            nextMoves.append(self.board)
            #print("Restoring board backup: ")
            self.board = copy.deepcopy(boardBackup)
            #print(self.board)
            self.turn = 0
        return nextMoves

    def makemove(self, col, test):
        """
        checks if move is "overflowing",
        puts player's "token" on the lowest free space
        checks for win condition
        :param col: int (0-6), Column on board
        :return:
        """
        player = (self.turn % 2) + 1
        #print("HISTORY: ")
        #self.showhis()

        if checkvalid(self.board, col):
            row = getrow(self.board, col)
            self.board[row][col] = player
            if test == False:
                self.history = []
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

    def playgame(self, show=True):
        player = self.player1
        while not self.game.gameover:
            move = player.move()
            self.game.makemove(move, False)
            if player == self.player1:
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
        for i in range(0,iterations+1):
            localwinner, localhis = self.playgame(show=False)
            if localwinner == 1:
                p1wins += 1
            elif localwinner == 2:
                p2wins += 1
            for j in localhis:
                y.append(localwinner)
                x.append(j)
                # x.append(j.flatten())
        X = np.dstack(x)
        X = np.rollaxis(X, -1)
        # X = np.array(x)
        Y = np.array(y)
        return X, Y, p1wins, p2wins


if __name__ == '__main__':
    g1 = game()
    player1 = op.RP(g1)
    player2 = op.RP(g1)
    control = gamecontrol(g1, player1, player2)
    xdata, ydata, wins = control.playmultiple(1000)

    xdata = tf.expand_dims(xdata, axis=-1)
    ydata = tf.keras.utils.to_categorical(ydata, 3)
    print(xdata.shape)
    model = op.CNN()
    model.train(xdata, ydata)




    # winner, history = control.playgame()
    # print("winner: {}".format(winner))
    # for i in history:
    #     print(i)