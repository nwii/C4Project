import random as rand
import c4game
import keras
import copy
import tensorflow as tf
import numpy as np

rand.seed() # generate random seed


class RP: # RANDOM PLAYER W/ logic for winning and blocking its opponent from winning
    """
    Checks 1 move ahead for a game-ending move, if none found, uses random number
    """
    def __init__(self, game):
        self.game = game
        self.board = copy.deepcopy(game.board)

    def lookforend(self, move): # checks to see if it can win / block opponent from winning
        for testplayer in [2, 1]: # check player 2, then player 1
            for i in range(0,7): 
                testboard = copy.deepcopy(self.game.board) # generate copy of board for move testing
                if c4game.checkvalid(testboard, i): # for each move, if valid...
                    row = c4game.getrow(testboard, i)
                    testboard[row][i] = testplayer # make that move
                    if c4game.checkwin(testboard, testplayer): # and see if it results in a win
                        testboard[row][i] = 0
                        return i # if so, make that move
                    testboard[row][i] = 0
        return move

    def move(self): # generate a move to make
        move = rand.randint(0,6) # first generate a random move
        move = self.lookforend(move) # then check to see if that can be overriden with a logical move
        attemptedMoves = [0,0,0,0,0,0,0] # tracks all attempted moves (failsafe to check for tie)
        while(c4game.checkvalid(copy.deepcopy(self.game.board),move) == False): # keep generating moves until a valid one is found
            move = rand.randint(0,6)
            move = self.lookforend(move)
            attemptedMoves[move] = 1
            if 0 not in attemptedMoves: # tie game, all moves have been tried and none are valid
                return move # returning a move will force the gamecontrol to register the tie
        return move

    
class RPdumb: # RANDOM PLAYER WITHOUT LOGIC
    """
    Checks 1 move ahead for a game-ending move, if none found, uses random number
    """

    def __init__(self, game):
        self.game = game
        self.board = copy.deepcopy(game.board)
        self.type = 'RPdumb'


    def move(self): # generates a move number
        move = rand.randint(0, 6) # generate random int move
        while (c4game.checkvalid(copy.deepcopy(self.game.board), move) == False):  # keep generating moves until a valid one is found
            move = rand.randint(0, 6)
        return move

class manual: # MANUAL PLAYER - controlled by user input from 0-6
    def __init__(self, game):
        self.game = game

    def move(self):
        self.game.show()
        move = int(input("make move: ")) # input move
        return move

class CNN: # CNN MODEL PLAYER
    def __init__(self, custom=None):
        if custom == None: # custom argument is used to load a pre-trained CNN from a file
            self.model = keras.Sequential(
                [
                    keras.layers.Conv2D(64, (4,4), activation="relu", input_shape=(6,7,1)), # 64 filters, kernel_size = filter_size = 4x4, 6x7 grid with 1 dimension
                    keras.layers.Flatten(), # flatten into vector for dense layers
                    keras.layers.Dense(42, activation="relu"), # 42 densely connected neurons
                    keras.layers.Dense(42, activation="relu"), # 42 densely connected neurons
                    keras.layers.Dense(3, activation="softmax") # 3 outputs. Softmax makes it so the outputs are
                                                                # a probability that sums to 1.
                ])                                              # [0] = p(tie), [1] = p(P2 win), [2] = p(P1 win)
        else:
            self.model = custom # load the custom model
        
        # Compile. Categorical crossentropy = good for classification, Adam = versatile loss optimizer
        # Metric = accuracy, strive for accurate classification of winning and losing board configurations.
        self.model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=['accuracy'])

    def train(self, X_train, y_train): # train with pre-set parameters
        self.model.fit(X_train, y_train, epochs=3, validation_split=0.2)

class CNNagent: # Controls the CNN model for usage in C4 game
    def __init__(self, model, game):
        self.model = model
        self.game = game

    def move(self): # generates move based on max probability of winning board configuration
        bestprob = 0
        move = 0
        possibleMoves = self.game.getnextmoves()
        illegalMoves = []
        #print(possibleMoves)

        for i in range(0, 7):
            if np.array_equal(possibleMoves[i],self.game.board): # if move is invalid
                illegalMoves.append(i) # register that move as illegal
                
            possibleMoves[i] = tf.expand_dims(possibleMoves[i], axis=-1)
            possibleMoves[i] = tf.expand_dims(possibleMoves[i], axis=0)
            
            if i not in illegalMoves: # if the move is legal...
                prediction = self.model.model.predict(possibleMoves[i]) # predict its probabilities
            
                if prediction[0][2] > bestprob: # choose the move that maximizes the probability
                    move = i
                    bestprob = prediction[0][2]
        return move

