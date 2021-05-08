|--------------|
   C4Project
|--------------|

Download all .py and .txt files

Install packages with:
	pip install -r packages.txt

run main.py

|--------------|

main.py is currently configured to run 40 training intervals of 100 games,
each using 3 epochs (folds) to train, to produce our best results. If desired,
one can change these values by changing the variables 'numIntervals' and
'numGames' in main.py.

main.py is also currently configured with player 1 as the CNN model and
player 2 as the random player with win-detection logic. If desired, these player
presets can be changed by commenting and uncommenting the different player options
in main.py, including an option to load the model that was most recently trained
from the file 'saveModels'.

The model saved in 'saveModels' at the time of downloading this zip file has
completed 40 iterations of 100 games and should have a 70 to 80 percent win rate.
Careful, as this model will be overwritten after each training interval.

Thank you!
