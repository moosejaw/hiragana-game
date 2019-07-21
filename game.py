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
    letters      = {}
    rows         = {}
    selectedRows = []
    color        = Color()

    def __init__(self):
        # Load the letters
        try:
            with open('hiragana.csv', 'r') as lettersFile:
                reader = csv.reader(lettersFile)
                for line in reader:
                    self.letters[line[0]] = line[1]
                    self.rows[line[0]] = line[2]
        except FileNotFoundError as e:
            print('The letters file could not be loaded.')
            raise FileNotFoundError

        # Sanity check!
        if not self.letters:
            print('The letters dictionary is empty. Check the file \
            and try again.')
            raise Exception # Raise a generic exception for now
        elif not self.rows:
            print('The sounds (rows) dictionary is empty. Check the file \
            and try again.')
            raise Exception

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

    def letterIsValid(self, letter):
        # Check to see if the letter is in the selected rows
        return self.rows[letter] in self.selectedRows

    def getSoundAnswerChoices(self, letter):
        """Gets the correct answer plus a couple others
        and puts them into a list."""
        answers = [letter]
        while len(answers) < 4:
            rand = self.getRandomLetter()
            if rand not in answers:
                answers.append(rand)
        random.shuffle(answers)
        return answers

    def getRowsToInclude(self):
        """Asks the player for the 'rows' of letters
        they want to use in the game."""
        # Set return object
        rowsSelected = []

        # Quickly get the row choices
        options = [v for k, v in self.rows.items()]
        options = list(set(options))

        self.printEmptyLines(1)
        print('What sounds of the letters do you want to include in questions?')
        print('\t0: All sounds')
        for sound in range(len(options)):
            print(f'\t{sound+1}: -{options[sound]} sounds')
        print('Seperate your choices with a space.')
        self.printEmptyLines(1)
        selection = input('Your choices: ')

        # Quick input validation
        if selection.replace(' ', '').isnumeric():
            if selection == '0':
                rowsSelected = list(options)
            else:
                selection = selection.split(' ')
                for sound in selection:
                    if int(sound)-1 < len(options):
                        rowsSelected.append(options[int(sound)-1])
        return rowsSelected

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
        # Get which rows the player wants to use
        self.selectedRows = []
        while not self.selectedRows:
            rowsToInclude = self.getRowsToInclude()
            if rowsToInclude:
                self.selectedRows = rowsToInclude

        # Start the game, ask the questions
        correctAnswers = 0
        for i in range(10):
            validLetter = False
            while not validLetter:
                selectedLetter = self.getRandomLetter()
                validLetter = self.letterIsValid(selectedLetter)

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
        # Ask the players what rows they want to include
        self.selectedRows = []
        while not self.selectedRows:
            rowsToInclude = self.getRowsToInclude()
            if rowsToInclude:
                self.selectedRows = rowsToInclude

        # Start the game
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
            answerIsCorrect = False
            if playerAnswer.isnumeric():
                if int(playerAnswer) > 0:
                    if choices[int(playerAnswer) - 1] == selectedLetter:
                        answerIsCorrect = True

            # Tell the player
            if answerIsCorrect:
                self.color.setGreenText()
                print('That\'s correct! Well done!')
                self.color.reset()
                correctAnswers += 1
            else:
                self.printWrongSoundAnswer(selectedLetter)

        # Appraise the player's score!
        appraisal = self.getAppraisal(correctAnswers)
        print(f'You scored {correctAnswers} out of 10! {appraisal}')


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
