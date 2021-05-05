import c4game as c4g
import Opponents as op
import tensorflow as tf
import time
import keras

import sys
import numpy
import matplotlib.pyplot as plt


numpy.set_printoptions(threshold=sys.maxsize) # debug, forces terminal to print full array rather than abbr.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    numIntervals = 3   # how many training intervals to run through
    numGames = 4        # how many games per training interval

    g1 = c4g.game()
    
    # LOAD MODEL for P1
    #model = op.CNN(keras.models.load_model('saveModels'))
    #player1 = op.CNNagent(model, g1)
    
    # NEW CNN MODEL for P1
    player1 = op.CNNagent(op.CNN(), g1)
    
    # MANUAL PLAYER FOR P1
    #player1 = op.manual(g1)
    
    # RANDOM OPPONENT FOR P2
    player2 = op.RP(g1)
    
    # MANUAL PLAYER FOR P2
    #player2 = op.manual(g1)
    
    RPperflog1 = []
    RPperflog2 = []
    
    for interval in range(0, numIntervals):
        # For each training interval...
        print("\nStarting collection interval " + str(interval+1) + "/" + str(numIntervals))
        
        # First, run 100 games to collect data

        control =c4g.gamecontrol(g1, player1, player2)
        
        startTS = time.time()
        
        xdata, ydata, p1wins, p2wins = control.playmultiple(numGames)
        #RPperflog.append(100*(2*p1wins+(100-p1wins-p2wins))/(2*numGames))
        RPperflog1.append(p1wins*100/(numGames+1))
        RPperflog2.append(p2wins*100/(numGames+1))
        
        endTS = time.time()
        
        print("\nTime for " + str(numGames) + " games: " + str(endTS-startTS))
        
        #print("\n\nTRAINING DATA BOARDS: \n")
        #print(xdata)
        #print(ydata)
        #print("\n\n")
        
        xdata = tf.expand_dims(xdata, axis=-1)
        ydata = tf.keras.utils.to_categorical(ydata,3)
        print("xdata shape: " + str(xdata.shape))
        print("ydata shape: " + str(ydata.shape))
        
        
        print("\nP1 Wins: {}".format(p1wins))
        print("P2 Wins: {}".format(p2wins))
        
        player1.model.train(xdata,ydata)
        
        player1.model.model.save('saveModels')
            
        # Now, after the 100 games, select next interval's players based on winners
        #print("Wins: {}".format(wins))
        
    plt.plot(RPperflog1, label='CNN Model')
    plt.plot(RPperflog2, label='Random Player')
    plt.ylim(0,100)
    plt.title('Model vs RP')
    plt.ylabel("Model wins %")
    plt.xlabel("iterations")
    plt.legend()
    plt.show()
        
        

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
