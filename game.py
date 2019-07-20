import csv
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

    def setBlueText(self):
        print(colorama.Fore.BLUE)


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
            raise Exception # Raise a generic exception for now

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
        '''Welcome to the hiragana game!

        Please select an option:
            1. Play the game
            2. View the letters
            3. Exit
        ''')

    def getRandomLetter(self):
        # Quickly cast the letters dict into a list and pick a random one
        return random.choice(list(self.letters.keys()))

    def getSoundAnswerChoices(self, letter):
        """Gets the correct answer plus a couple others
        and puts them into a list."""
        answers = [letter]
        for i in range(3):
            rand = self.getRandomLetter()
            if rand not in answers:
                answers.append(rand)
            else:
                i -= 1
                continue
        random.shuffle(answers)
        return answers

    def printGameMenu(self):
        self.printEmptyLines(1)
        print(
        '''What type of game do you want to play?

        Please select an option:
            1. Ask me the letters, and I'll tell you the sound!
            2. Ask me the sound and I'll choose the letter!
            3. Go back
        ''')

    def printLetters(self):
        self.printEmptyLines(1)
        print('The letters and their sounds are as follows:')
        for k, v in self.letters.items():
            print(f'{k} : {v}')
        self.printEmptyLines(1)

    def printWrongSoundAnswer(self, answer):
        self.color.setRedText()
        print(f'That\'s incorrect. The correct answer is: {answer}.')
        self.color.reset()
        self.printEmptyLines(1)

    def printEmptyLines(self, numberOfLines):
        for i in range(numberOfLines):
            print('\n')

    def getGameSelection(self):
        self.printGameMenu()
        selection = input('Please select an option: ')
        menuOptions = {
            '1': self.playLettersGame,
            '2': self.playSoundsGame
        }
        menuOptions.get(selection)() if menuOptions.get(selection) else None

    def playLettersGame(self):
        correctAnswers = 0
        for i in range(10):
            selectedLetter = self.getRandomLetter()

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

    def playSoundsGame(self):
        correctAnswers = 0
        for i in range(10):
            selectedLetter = self.getRandomLetter()
            choices = self.getSoundAnswerChoices(selectedLetter)

            # Ask the question
            print(f'What letter corresponds to the sound: \'{self.letters[selectedLetter]}\'?')
            for a in range(len(choices)):
                print(f'{a+1}: {choices[a]}')
            playerAnswer = input('Your answer: ')

            # Get the answer and determine if it's right or wrong
            if playerAnswer.isnumeric():
                if int(playerAnswer) > 0:
                    if choices[int(playerAnswer) - 1] == selectedLetter:
                        self.color.setGreenText()
                        print('That\'s correct! Well done!')
                        self.color.reset()
                        correctAnswers += 1
                    else:
                        self.printWrongSoundAnswer(selectedLetter)
                else:
                    self.printWrongSoundAnswer(selectedLetter)
            else:
                self.printWrongSoundAnswer(selectedLetter)

        # Appraise the player's score!
        appraisal = self.getAppraisal(correctAnswers)
        print(f'You scored {correctAnswers} out of 10! {appraisal}')

# Main code
if __name__ == '__main__':
    gameIsActive = True
    while gameIsActive:
        game = Game()
        game.printEmptyLines(1)
        game.printMainMenu()
        selection = input('Please select an option: ')

        menuOptions = {
            '1': game.getGameSelection,
            '2': game.printLetters,
        }

        if selection == '3':
            # Quit the game
            gameIsActive = False
        else:
            menuOptions.get(selection)() if menuOptions.get(selection) else None
