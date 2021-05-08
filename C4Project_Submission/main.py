import c4game as c4g
import Opponents as op
import tensorflow as tf
import time
import keras

import sys
import numpy
import matplotlib.pyplot as plt

if __name__ == '__main__':

    numIntervals = 40   # how many training intervals to run through
    numGames = 100        # how many games per training interval

    g1 = c4g.game()
    
    # LOAD MODEL for P1
    model = op.CNN(keras.models.load_model('saveModels'))
    player1 = op.CNNagent(model, g1)
    
    # NEW CNN MODEL for P1
    #player1 = op.CNNagent(op.CNN(), g1)
    
    # MANUAL PLAYER FOR P1
    #player1 = op.manual(g1)
    
    # RANDOM OPPONENT FOR P2
    player2 = op.RP(g1)
    
    # MANUAL PLAYER FOR P2
    #player2 = op.manual(g1)
    
    # RANDOM OPPONENT WITHOUT WIN/BLOCK LOGIC FOR P2
    #player2 = op.RPdumb(g1)
    
    RPperflog1 = [] # Array that tracks p1wins for plotting
    RPperflog2 = [] # Array that tracks p2wins for plotting
    RPperflogT = [] # Array that tracks ties for plotting
    
    for interval in range(0, numIntervals): # For each training interval...
        
        print("\nStarting training interval " + str(interval+1) + "/" + str(numIntervals))

        control =c4g.gamecontrol(g1, player1, player2) # init. gamecontrol with game and players
        
        # First, run 100 games to collect data
        
        startTS = time.time() # start timing
        xdata, ydata, p1wins, p2wins = control.playmultiple(numGames) # play numGames games and report stats
        endTS = time.time() # end timing
        
        print("\nTime for " + str(numGames) + " games: " + str(endTS-startTS)) # report time
        
        # Append stats to their plotting arrays
        RPperflog1.append(p1wins*100/(numGames+1))
        RPperflog2.append(p2wins*100/(numGames+1))
        RPperflogT.append(numGames+1 - p1wins - p2wins)

        # DEBUG: Uncomment to see the training data arrays and their labels
        #print("\n\nTRAINING DATA BOARDS: \n")
        #print(xdata)
        #print(ydata)
        #print("\n\n")
        
        # Format xdata and ydata for training
        xdata = tf.expand_dims(xdata, axis=-1)
        ydata = tf.keras.utils.to_categorical(ydata,3)
        
        # Report wins
        print("\nP1 Wins: {}".format(p1wins))
        print("P2 Wins: {}".format(p2wins))
        
        player1.model.train(xdata,ydata) # Train the model using the data collected from numGames games
        
        player1.model.model.save('saveModels') # Save the most recently trained model
    
    # PLOT 1: CNN vs. RP Wins
    plt.figure(1)
    plt.plot(RPperflog1, label='CNN Model')
    plt.plot(RPperflog2, label='Random Player')
    plt.ylim(0,100)
    plt.title('Figure 1. CNN vs RP Wins')
    plt.ylabel("Model Wins %")
    plt.xlabel("Training Intervals")
    plt.legend()
    plt.show()
    
    # PLOT 2: TIES (unused?)
    plt.figure(2)
    plt.plot(RPperflogT)
    plt.ylim(0,100)
    plt.title('Figure 2. Ties across Intervals')
    plt.ylabel("Ties")
    plt.xlabel("Training Intervals")
    plt.show()
    
    # PLOT 3: Just CNN Wins
    plt.figure(3)
    plt.plot(RPperflog1)
    plt.ylim(0,100)
    plt.title('Figure 3. CNN Wins')
    plt.ylabel("Model Wins %")
    plt.xlabel("Training Intervals")
    plt.show()
