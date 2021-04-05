import random as rand
import c4game


class RP:
    """
    Checks 1 move ahead for a game-ending move, if none found, uses random number
    """
    def __init__(self, game):
        self.board = game.board

    def lookforend(self, move):
        for testplayer in [1, 2]:
            for i in range(0,7):
                testboard = self.board
                if c4game.checkvalid(testboard, i):
                    row = c4game.getrow(testboard, i)
                    testboard[row][i] = testplayer
                    if c4game.checkwin(testboard, testplayer):
                        testboard[row][i] = 0
                        return i
                    testboard[row][i] = 0
        return move

    def move(self):
        move = rand.randint(0,6)
        move = self.lookforend(move)

        return move


class manual:
    def move(self):
        move = int(input("make move: "))
        return move

if __name__ == '__main__':
    g1 = c4game.game()
    comp1 = RP(g1, 2)
    comp2 = RP(g1, 1)
    while not g1.gameover:
        if (g1.turn % 2)+1 == 1:
            g1.makemove(comp1.makemove())
        else:
            g1.makemove(comp2.makemove())
        g1.show()
    print("Winner: {}".format(g1.winner))