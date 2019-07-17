# Hiragana Game
A very simple Python-based game for testing your hiragana knowledge.

## Principle
The ```game.py``` script loads the ```hiragana.csv``` file and populates a ```dict``` object with the letters and their sounds, as specified in the CSV file.

When you play the game, a random hiragana letter from the dictionary will be chosen and presented to you, to which you must answer with the corresponding pronounciation.

For example, か is pronounced 'ka', so you would answer with 'ka'.

The game will tell you whether you're correct or incorrect.

## Playing the game in a virtual environment
As with most Python apps, you can also use the game with ```virtualenv```.

Just initialise the virtual environment inside the root folder:
```bash
$ virtualenv .
```

Then, activate the environment:
```bash
$ source ./bin/activate
```

Then you can ```pip install requirements.txt``` as normal to install the dependencies.
