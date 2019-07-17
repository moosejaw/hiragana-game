import csv
import pprint
import random
import colorama

class Color:
    """Class containing some common methods used for colorama."""
    def __init__(self):
        colorama.init()

    def reset(self):
        print(colorama.Style.RESET_ALL)

    def setRedText(self):
        print(colorama.Fore.RED)

    def setGreenText(self):
        print(colorama.Fore.GREEN)


class Game:
    """Class containing all the game methods and the letters dictionary."""
    letters = {}
    color = Color()

    def __init__(self):
        # Load the letters
        try:
            with open('hiragana.csv', 'r') as lettersFile:
                reader = csv.DictReader(lettersFile)
                for line in reader:
                    self.letters[line['letter']] = line['sound']
        except FileNotFoundError as e:
            print('The letters file could not be loaded.')
            raise FileNotFoundError

        # Sanity check!
        if not self.letters:
            print('The letters dictionary is empty. Check the file \
            and try again.')
            raise Error

    def getAppraisal(self, score):
        if score == 0:
            return 'That\'s too bad!'
        elif score < 5:
            return 'There\'s room for improvement!'
        elif 5 < score < 8:
            return 'Nice!'
        else:
            return 'Amazing job! Well done!'

    def printMainMenu(self):
        print(
        '''Welcome to the Japanese Hiragana game!

        Please select an option:
            1. Play the game
            2. View the letters
            3. Exit
        ''')

    def printLetters(self):
        print('The letters and their sounds are as follows:')
        for k, v in self.letters.items():
            print(f'{k} : {v}')
        self.printEmptyLines(1)

    def printEmptyLines(self, numberOfLines):
        for i in range(numberOfLines):
            print('\n')

    def playGame(self):
        correctAnswers = 0
        for i in range(10):
            # Quickly cast the keys to subscriptable list
            selectedLetter = random.choice(list(self.letters.keys()))

            # Ask the question
            print(f'What is the sound of the letter: {selectedLetter}?')
            playerAnswer = input('Your answer: ')

            # Get the answer and determine if it's right or wrong
            if playerAnswer.lower() == self.letters[selectedLetter]:
                self.color.setGreenText()
                print('Correct answer! Well done!')
                self.color.reset()
                correctAnswers += 1
            else:
                self.color.setRedText()
                print(f'That\'s incorrect. It\'s actually pronounced: \
                \'{self.letters[selectedLetter]}\'.')
                self.color.reset()
            self.printEmptyLines(1)

        # Appraise the player's score!
        appraisal = self.getAppraisal(correctAnswers)
        print(f'You scored {correctAnswers} out of 10. {appraisal}')


# Main code
if __name__ == '__main__':
    gameIsActive = True
    while gameIsActive:
        game = Game()
        game.printMainMenu()
        selection = input('Please select an option: ')

        if selection == '1':
            game.playGame()
        elif selection == '2':
            game.printLetters()
        elif selection == '3':
            # Quit the game
            gameIsActive = False
