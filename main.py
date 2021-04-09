import c4game as c4g
import Opponents as op
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    
    gamesPerInterval = 10 # how many games to play before re-training
    numIntervals = 3 # how many training intervals to run through

    g1 = c4g.game()
    player1 = op.RP(g1)
    player2 = op.RP(g1)
    
    localWinDict = {
        1: 0,
        2: 0
    }
    
    for interval in range(0, numIntervals):
        # For each training interval...
        
        # First, run 100 games to collect data
        for g in range(0, gamesPerInterval):
            g1 = c4g.game()
            player1.board = g1.board # set new player models' boards
            player2.board = g1.board
            control = c4g.gamecontrol(g1, player1, player2)
            winner = control.playgame()
            print("winner: {}".format(winner))
            localWinDict[winner] += 1
            #p2.train(X_train_from_this_game, y_train_from_this_game)
            
        # Now, after the 100 games, select next interval's players based on winners
        #print("P1 wins: {}".format(localWinDict[1]))
        #print("P2 wins: {}".format(localWinDict[2]))
        
        if (localWinDict[2] > localWinDict[1]): # if p2 won more...
            player1 = player2 # make p2 the new p1
            player2 = player1 # make new p2 a copy of the new p1
        else:
            
            
        
            localWinDict[1] = 0
            localWinDict[2] = 0
        
        

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
