import random as rand
import c4game
import keras


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
    def __init__(self, game):
        self.game = game

    def move(self):
        self.game.show()
        move = int(input("make move: "))
        return move

class CNN:
    def __init__(self):
        self.model = keras.Sequential(
            [
                layers.Conv2D(64, kernel_size=4, activation="relu", input_shape=(6,7,1)), # 64 nodes, kernel_size = filter_size = 4x4, 6x7 grid with 1 dimension
                layers.Dense(42, activation="relu"),
                layers.Dense(42, activation="relu"),
                layers.Dense(42, activation="relu"),
                layers.Dense(1, activation="softmax") # 7 ~ num. outputs (each possible column). Each will have its own probability due to the softmax activation.
                
                # Quote from CNN 0-9 digit classifier:
                # "We will have 10 nodes in our output layer, one for each possible outcome (0-9). The activation is "softmax". Softmax makes the output sum up to 1 so the output can be interpreted as probabilities. The model will then make its prediction based on which option has the highest probability".
            ])
            
        self.model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=['accuracy'])
        
        # Could also compile with optimizer="rmsprop". We'll need to experiment and find the best parameters. 
        # Categorical Crossentropy is popular for classification, so it might be worthwhile to experiment with other loss functions too. A low categorical crossentropy value means it's performing well.

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train, epochs=3)

class CNNagent:
    def __init__(self, model):
        self.model = CNN
        pass
    def move(self):
        bestprob = 0
        move = 0
        for i in range(0, 8):
            probability = self.model.predict
            if probability > bestprob:
                move = i
        return move


if __name__ == '__main__':
    g1 = c4game.game()
    comp1 = RP(g1)
    comp2 = RP(g1)
    while not g1.gameover:
        if (g1.turn % 2)+1 == 1:
            g1.makemove(comp1.move())
        else:
            g1.makemove(comp2.move())
        g1.show()
    print("Winner: {}".format(g1.winner))