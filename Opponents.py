import random as rand
import c4game
import keras
import copy
import tensorflow as tf
import numpy as np

rand.seed()


class RP:
    """
    Checks 1 move ahead for a game-ending move, if none found, uses random number
    """
    def __init__(self, game):
        self.game = game
        self.board = copy.deepcopy(game.board)

    def lookforend(self, move):
        for testplayer in [2, 1]:
            for i in range(0,7):
                testboard = copy.deepcopy(self.game.board)
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
        attemptedMoves = [0,0,0,0,0,0,0]
        while(c4game.checkvalid(copy.deepcopy(self.game.board),move) == False): # keep generating moves until a valid one is found
            move = rand.randint(0,6)
            move = self.lookforend(move)
            attemptedMoves[move] = 1
            if 0 not in attemptedMoves: # tie game
                print("\nERROR: RP cannot find move")
                return move
        return move


class manual:
    def __init__(self, game):
        self.game = game

    def move(self):
        self.game.show()
        move = int(input("make move: "))
        return move

class CNN:
    def __init__(self, custom=None):
        if custom == None:
            self.model = keras.Sequential(
                [
                    keras.layers.Conv2D(64, (4,4), activation="relu", input_shape=(6,7,1)), # 64 nodes, kernel_size = filter_size = 4x4, 6x7 grid with 1 dimension
                    keras.layers.Flatten(),
                    keras.layers.Dense(42, activation="relu"),
                    keras.layers.Dense(42, activation="relu"),
                    keras.layers.Dense(3, activation="softmax") # 7 ~ num. outputs (each possible column). Each will have its own probability due to the softmax activation.

                    # Quote from CNN 0-9 digit classifier:
                    # "We will have 10 nodes in our output layer, one for each possible outcome (0-9). The activation is "softmax". Softmax makes the output sum up to 1 so the output can be interpreted as probabilities. The model will then make its prediction based on which option has the highest probability".
                ])
        else:
            self.model = custom
            
        self.model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=['accuracy'])
        
        # Could also compile with optimizer="rmsprop". We'll need to experiment and find the best parameters. 
        # Categorical Crossentropy is popular for classification, so it might be worthwhile to experiment with other loss functions too. A low categorical crossentropy value means it's performing well.

    def train(self, X_train, y_train):
        #X_train = X_train.reshape(-1, 6, 7, 1)
        self.model.fit(X_train, y_train, epochs=3, validation_split=0.2)

class CNNagent:
    def __init__(self, model, game):
        self.model = model
        self.game = game

    def move(self):
        bestprob = 0
        move = 0
        possibleMoves = self.game.getnextmoves()
        illegalMoves = []
        #print(possibleMoves)

        for i in range(0, 7):
            if np.array_equal(possibleMoves[i],self.game.board): # if move is invalid
                illegalMoves.append(i)
            possibleMoves[i] = tf.expand_dims(possibleMoves[i], axis=-1)
            possibleMoves[i] = tf.expand_dims(possibleMoves[i], axis=0)
            
            if i not in illegalMoves:
                prediction = self.model.model.predict(possibleMoves[i])
            
                if prediction[0][2] > bestprob: # 1 SHOULD BE REPLACED BY CNN's PLAYER NUMBER
                    move = i
                    bestprob = prediction[0][2]
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