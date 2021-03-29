import numpy as np
from scipy.signal import convolve2d


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

    def show(self):
        print("\n")
        print(self.board)
        pass


    def makemove(self, col):
        """
        checks if move is "overflowing",
        puts player's "token" on the lowest free space
        checks for win condition
        :param col: int (0-6), Column on board
        :return:
        """
        player = (self.turn % 2)+1

        if checkvalid(self.board, col):
            row = getrow(self.board, col)
            self.board[row][col] = player

            if checkwin(self.board, player):
                self.winner = player
                self.gameover = True

            self.turn += 1

if __name__ == '__main__':
    g1 = game()
    while not g1.gameover:
        g1.makemove(int(input("make move: ")))
        g1.show()
    print("winner: {}".format(g1.winner))