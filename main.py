import c4game as c4g
import Opponents as op
import tensorflow as tf
import time

import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize) # debug, forces terminal to print full array rather than abbr.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    numIntervals = 100   # how many training intervals to run through
    numGames = 100        # how many games per training interval

    g1 = c4g.game()
    
    player1 = op.CNNagent(op.CNN(), g1)
    #player1 = op.manual(g1)
    player2 = op.RP(g1)
    #player2 = op.manual(g1)
    
    localWinDict = {
        1: 0,
        2: 0
    }
    
    opponentPool = [
        op.RP(g1),
        op.RP(g1),
        op.RP(g1),
        op.RP(g1)
    ]
    
    for interval in range(0, numIntervals):
        # For each training interval...
        print("\nStarting collection interval " + str(interval+1) + "/" + str(numIntervals))
        
        # First, run 100 games to collect data

        control =c4g.gamecontrol(g1, player1, player2)
        startTS = time.time()
        xdata, ydata, p1wins, p2wins = control.playmultiple(numGames)
        endTS = time.time()
        print("Time for " + str(numGames) + " games: " + str(endTS-startTS))
        
        #print("\n\nTRAINING DATA BOARDS: \n")
        #print(xdata)
        #print("\n\n")
        
        xdata = tf.expand_dims(xdata, axis=-1)
        ydata = tf.keras.utils.to_categorical(ydata,3)
        print("xdata shape: " + str(xdata.shape))
        print("ydata shape: " + str(ydata.shape))
        
        
        print("\nP1 Wins: {}".format(p1wins))
        print("P2 Wins: {}".format(p2wins))
        
        player1.model.train(xdata,ydata)
            
        # Now, after the 100 games, select next interval's players based on winners
        #print("Wins: {}".format(wins))
        
        

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
