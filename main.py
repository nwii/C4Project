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

    numIntervals = 3 # how many training intervals to run through

    g1 = c4g.game()
    player1 = op.CNNagent(op.CNN(), g1)
    player2 = op.RP(g1)
    
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
        
        # First, run 100 games to collect data

        control =c4g.gamecontrol(g1, player1, player2)
        xdata, ydata, wins = control.playmultiple(10)
            
        # Now, after the 100 games, select next interval's players based on winners
        print("Wins: {}".format(wins))
        
        

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
