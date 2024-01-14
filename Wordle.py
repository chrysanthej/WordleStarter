# File: Wordle.py
# Description: This file (linked with WordleDictionary.py and WordleGraphics.py) allows you to play a game of Wordle (NY Times Games)
# Authors: Lorin Costley, Chrysanthe Belgique, Kian Bangerter, Ryan Hafen

# To do:
# 1. Allow users to use the backspace button on keyboard (works on screen)
# 2. If word is not in word list, allow users to type in a new word
# 3. Stop user from making any entries after word is guessed
# 4. Implement get_current_row..?
# 5. Implement N_ROWS and N_COLS
# 6. Milestone 4

import random

from WordleDictionary import FIVE_LETTER_WORDS
from WordleGraphics import WordleGWindow, N_COLS, N_ROWS, CORRECT_COLOR, PRESENT_COLOR, MISSING_COLOR

def wordle():

    # Disaplay the window that contains the graphics from WordleGraphics.py
    gw = WordleGWindow()

    # Choose a random word for the entire game
    word_to_guess = random.choice(FIVE_LETTER_WORDS)

    # Initialize current_row and current_guess (to a list of empty characters the length of the word to guess)
    current_row = 0
    current_guess = [''] * len(word_to_guess)

    # MILESTONE 1
    # Choose a random word from the list
    # random_word = random.choice(FIVE_LETTER_WORDS)

    def enter_action(user_guess):
        nonlocal current_row, current_guess  # Nonlocal allows you to modify the current_row variable

        # Assign current_guess to whatever the user put in
        current_guess = user_guess

        # If the user guess is in the FIVE_LETTER_WORDS list, continue to check each letter
        if current_guess.lower() in FIVE_LETTER_WORDS:
            # Milestone 2 - verify current_guess is a word and show the message
            #gw.show_message("That is a word!")

            # Enummerate iterates over each letter in current_guess and their indices
            # The index is assigned to 'col' and the letter is assigned to 'guess_letter'
            for col, guess_letter in enumerate(current_guess.lower()):
                
                # Associates word_letter with the letter in the correct position within the column corresponding to the current iteration in word_to_guess.      
                word_letter = word_to_guess[col]

                # Checks if the guessed letter is in the right spot
                if guess_letter == word_letter:
                    gw.set_square_color(current_row, col, CORRECT_COLOR)
                # Checks if the guessed letter is in the word_to_guess
                elif guess_letter in word_to_guess:
                    gw.set_square_color(current_row, col, PRESENT_COLOR)
                # Guessed letter is not in the word_to_guess
                else:
                    gw.set_square_color(current_row, col, MISSING_COLOR)

        
            # Check if all letters are correct
            if current_guess.lower() == word_to_guess:
                gw.show_message("Congratulations! You guessed the word.")

            # Move on to the next row
            current_row += 1

            # Reset current guess for the next row
            current_guess = [''] * len(word_to_guess)

            # Set the current row for the next guess
            gw.set_current_row(current_row)

        # Else, display "Not in word list"
        else:
            gw.show_message("Not in word list")

    # MILESTONE 1
    # Display the random word in the first row
    # for col, letter in enumerate(random_word):
    #     # Sets the letter in the specified row and column
    #     gw.set_square_letter(0, col, letter)

    # Respond to user input of "enter" key
    gw.add_enter_listener(enter_action)

# Startup code

if __name__ == "__main__":
    wordle()
