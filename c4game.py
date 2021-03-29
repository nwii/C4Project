import numpy as np
from scipy.signal import convolve2d


class game:
    def __init__(self):
        self.board = np.zeros((6,7))
        self.turn = 0 # player is (turn % 2)+1
        self.gameover = False
        self.winner = None

        winhorizontal = np.array([[1, 1, 1, 1]])
        winvert = np.transpose(winhorizontal)
        windiag1 = np.eye(4, dtype=int)
        windiag2 = np.fliplr(windiag1)
        self.wincons = [winhorizontal, winvert, windiag1, windiag2]

    def show(self):
        print("\n\n\n\n")
        print(self.board)
        pass

    def checkwin(self, player):
        """
        Convolves true/false matrix with win conditions, checks if any are connected by 4
        :param player:
        :return:
        """
        for wincon in self.wincons:
            if (convolve2d(self.board == player, wincon, mode="valid") == 4).any():
                return True
        return False

    def checkvalid(self, col):
        """
        Checks to see if top row is filled
        :param col: int (0-6)
        :return:
        """
        return self.board[0][col] == 0

    def getrow(self, col):
        for r in range(5, -1, -1):
            if self.board[r][col] == 0:
                return r

    def makemove(self, col):
        """
        checks if move is "overflowing",
        puts player's "token" on the lowest free space
        checks for win condition
        :param col: int (0-6), Column on board
        :return:
        """
        player = (self.turn % 2)+1

        if self.checkvalid(col):
            row = self.getrow(col)
            self.board[row][col] = player

            if self.checkwin(player):
                self.winner = player
                self.gameover = True

            self.turn += 1

if __name__ == '__main__':
    g1 = game()
    while not g1.gameover:
        g1.makemove(int(input("make move: ")))
        g1.show()
    print("winner: {}".format(g1.winner))