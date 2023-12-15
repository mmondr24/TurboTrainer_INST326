"""Name: Madelyn Mondragon

This script is for a car mod themed flashcard practice game named TurboTrainer. This game allows 
users to create and study multiple flashcard sets with their own terms and definitions while earning 
parts to build a car. The amount of parts the user earns is dependent upon the percentage of questions 
answered correctly.  

Instructions for running from the terminal:
1) In the command line input 'python3 turbotrainer.py'
2) To begin, input '1' to create and name a new flashcard set
3) After naming set, press enter
4) Input '3' to add a flashcard term and defintion to the set you just created
5) Repeat until you have entered all desired terms and definitions
6) Input '4' to study the set you created 
7) Terminal will show term, input definition and press enter
8) If correct, terminal will print 'correct!'
9)If incorrect, terminal will print 'Incorrect. The correct answer is ..." and you will be prompted to retry at the end
10) The percentage of the "car completed" corresponds to the percentage of definitions answered correctly
11) To study a previously created set input '2'
12) Input the name of the set you wish to study
13) Input '4' to study the set you just input or '3' to add a new flashcard to the set
14)To finish and exit game menu input '5' 

Bibliography:
https://www.w3schools.com/python/python_json.asp - Guidance on using json
https://www.w3schools.com/python/module_os.asp - Guidance on using os module
https://www.w3schools.com/python/ref_dictionary_keys.asp - Guidance on using keys() method for term/definition retrieval
https://www.w3schools.com/python/ref_random_shuffle.asp - Guidance on using shuffle() method for term/definition flashcard reordering

"""

import random
import json
import os

class CarFlashcardGame:
    """ A class for a car mod themed flashcard game
    
    Attributes:
        flashcard_sets(dict): Dictionary where keys are flashcard set names and values are dictionaries of other attributes.
        current_flashcard_set(str): Stores the name of the currently selected flashcard set
        user_progress(int): tracks percentage of questions user answers correctly 
    """
    def __init__(self):
        """ 
        Initializes the flashcard set and progress saver 

        Attributes:
        flashcard_sets(dict): See class documentation
        current_flashcard_set(): See class documentation
        user_progress(): See class documentation
        """
        self.flashcard_sets = {}
        self.current_flashcard_set = None
        self.user_progress = self.load_user_progress()

    def create_flashcard_set(self, set_name):
        """ This function initializes the flashcard set progress, terms/definitions, and the name input by the user 

        Attributes:
            set_name(str): Name of flashcard set
            flashcards(dict): stores flashcards where keys are terms and values are definitions
            progress(dict): stores user progress information
            percentage(float): percentage of correct answers
            incorrect_flashcards(List): Tuples containing terms and definitions.
        """
        self.flashcard_sets[set_name] = {'flashcards': {}, 'progress': {'percentage': 0, 'incorrect_flashcards': []}}
        self.current_flashcard_set = set_name

    def add_flashcard(self, term, definition):
        """ This function ensures a flashcard set is selected and adds a flashcard to it

        Attributes:
            term(str): The term input by user
            definition(str): The definition input by the user
        """
        if not self.current_flashcard_set:
            print("No flashcard set selected. Please create or choose a flashcard set.")
            return

        self.flashcard_sets[self.current_flashcard_set]['flashcards'][term] = definition
        print(f"Flashcard added to the set: {self.current_flashcard_set}")

    def choose_flashcard_set(self, set_name):
        """ This function allows the user to choose a previous flashcard set to study

        Attributes: 
            set_name (str): The name of the flashcard set to be chosen.
        """
        if set_name in self.flashcard_sets:
            self.current_flashcard_set = set_name
            print(f"Selected flashcard set: {self.current_flashcard_set}")
        else:
            print(f"The flashcard set '{set_name}' does not exist.")

    def study_flashcards(self):
        """ Allows the user to study the flashcards in the current set

        Attributes:
        correct_answers(int): counter for correct answers
        incorrect_answers(int): counter for incorrect answers
        """
        if not self.current_flashcard_set: #Checks if a current flashcard set is selected
            print("No flashcard set selected. Please create or choose a flashcard set.")
            return

        flashcards = self.flashcard_sets[self.current_flashcard_set]['flashcards'] #Retrieves the flashcards for the current flashcard set.
        progress = self.flashcard_sets[self.current_flashcard_set]['progress'] #Retrieves the progress for the current flashcard set.
        correct_answers = 0
        incorrect_answers = 0

        terms = list(flashcards.keys()) #returns flashcard term keys in a list 
        random.shuffle(terms) #Shuffles the terms to randomize the order in which they are presented.

        for term in terms: #Iterates through each term, prompting the user for the definition.
            user_answer = input(f"What is the definition of '{term}'? ")
            correct_answer = flashcards[term]

            if user_answer.lower() == correct_answer.lower():
                print("Correct! You just earned a part for your car!")
                correct_answers += 1
            else:
                print(f"Incorrect. No car parts for you. The correct answer is: {correct_answer}")
                incorrect_answers += 1
                progress['incorrect_flashcards'].append((term, correct_answer))

        total_questions = len(flashcards)
        if total_questions > 0:
            current_percentage = (correct_answers / total_questions) * 100
            progress['percentage'] = current_percentage

            if current_percentage == 100:
                print("\nCongratulations! You answered all questions correctly.")
                print("You've earned all new parts for your car!")
            else:
                print(f"\nYou only built {current_percentage}% of your car")
                self.retry_incorrect_flashcards()

            self.save_user_progress()

    def retry_incorrect_flashcards(self):
        progress = self.flashcard_sets[self.current_flashcard_set]['progress']
        incorrect_flashcards = progress['incorrect_flashcards']

        if incorrect_flashcards:
            print("\nLet's try again!:")
            for term, correct_answer in incorrect_flashcards:
                user_answer = input(f"What is the definition of '{term}'? ")
                if user_answer.lower() == correct_answer.lower():
                    print("Correct! You just earned a part for your car!")
                else:
                    print(f"Incorrect. No car parts for you. The correct answer is: {correct_answer}")

    def load_user_progress(self):
        progress_file = 'flashcard_game_progress.json'
        try:
            with open(progress_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_user_progress(self):
        progress_file = 'flashcard_game_progress.json'
        with open(progress_file, 'w') as file:
            json.dump(self.flashcard_sets, file)

def main():
    car_flashcard_game = CarFlashcardGame()

    while True:
        print("\n Game Menu:")
        print("1. Create New Flashcard Set")
        print("2. Choose Flashcard Set")
        print("3. Add Flashcard")
        print("4. Study Flashcards")
        print("5. Quit")

        choice = input("Enter your choice (1, 2, 3, 4, or 5): ")

        if choice == '1':
            set_name = input("Enter the name for the new flashcard set: ")
            car_flashcard_game.create_flashcard_set(set_name)
        elif choice == '2':
            set_name = input("Enter the name of the flashcard set you want to choose: ")
            car_flashcard_game.choose_flashcard_set(set_name)
        elif choice == '3':
            term = input("Enter the term: ")
            definition = input("Enter the definition: ")
            car_flashcard_game.add_flashcard(term, definition)
        elif choice == '4':
            car_flashcard_game.study_flashcards()
        elif choice == '5':
            car_flashcard_game.save_user_progress()
            print("Exiting TurboTrainer. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()