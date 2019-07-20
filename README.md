# Hiragana Game
## Introduction
A very simple terminal-based Python game for testing your hiragana knowledge. It is currently unfinished.

This project was written in Python 3.7.3.

### Important Note
```hiragana.csv``` contains the mapping of each hiragana letter to its given pronunciation, but it does not yet contain the complete alphabet. You can populate it further manually if you want to.

## Principle
The ```game.py``` script loads the ```hiragana.csv``` file and populates a ```dict``` object with the letters and their sounds, as specified in the CSV file.

When you play the game, a random hiragana letter from the dictionary will be chosen and presented to you, to which you must answer with the corresponding pronounciation.

For example, か is pronounced 'ka', so you would answer with 'ka'.

The game will tell you whether you're correct or incorrect.

## Playing the game in a virtual environment
As with most Python apps, you can also use the game with ```virtualenv```.

Just initialise the virtual environment somewhere and activate it.

Then, in the context of the project folder you can run:
```bash
pip install -r requirements.txt
```
as normal to install the dependencies.

## Future improvements
I'm writing the code for this as I explore my learning of the Japanese language further. Therefore, I'll probably add katakana once I start trying to learn it.
