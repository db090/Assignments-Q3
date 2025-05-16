import streamlit as st
import random

class Word:
    def __init__(self, word):
        """Initialize Word object with the chosen word"""
        self.word = word.lower()
        self.letters_guessed = set()
    
    def guess_letter(self, letter):
        """Process a letter guess and return if it's in the word"""
        letter = letter.lower()
        self.letters_guessed.add(letter)
        return letter in self.word
    
    def word_guessed(self):
        """Check if all letters in the word have been guessed"""
        return all(letter in self.letters_guessed for letter in self.word)
    
    def get_current_state(self):
        """Return the current state of the word with underscores for unguessed letters"""
        return ''.join([letter if letter in self.letters_guessed else '_' for letter in self.word])
    
    def get_remaining_letters(self):
        """Return the set of letters that haven't been guessed yet"""
        alphabet = set('abcdefghijklmnopqrstuvwxyz')
        return alphabet - self.letters_guessed

class Game:
    def __init__(self, word_list=None):
        """Initialize the game with a word list"""
        if word_list is None:
            # Default word list if none provided
            self.word_list = ['python', 'streamlit', 'hangman', 'programming', 
                             'developer', 'algorithm', 'function', 'variable', 
                             'object', 'class']
        else:
            self.word_list = word_list
        
        self.max_attempts = 6
        self.reset_game()
    
    def reset_game(self):
        """Reset the game state with a new random word"""
        random_word = random.choice(self.word_list)
        self.current_word = Word(random_word)
        self.attempts_left = self.max_attempts
        self.game_over = False
        self.won = False
    
    def guess(self, letter):
        """Process a letter guess and update game state"""
        if self.game_over:
            return None
        
        is_correct = self.current_word.guess_letter(letter)
        
        if not is_correct:
            self.attempts_left -= 1
        
        # Check if game is over
        if self.attempts_left <= 0:
            self.game_over = True
        
        # Check if word is guessed
        if self.current_word.word_guessed():
            self.game_over = True
            self.won = True
        
        return is_correct

class HangmanApp:
    def __init__(self):
        """Initialize the Streamlit application"""
        self.hangman_pics = [
            """
              +---+
              |   |
                  |
                  |
                  |
                  |
            =========""",
            """
              +---+
              |   |
              O   |
                  |
                  |
                  |
            =========""",
            """
              +---+
              |   |
              O   |
              |   |
                  |
                  |
            =========""",
            """
              +---+
              |   |
              O   |
             /|   |
                  |
                  |
            =========""",
            """
              +---+
              |   |
              O   |
             /|\\  |
                  |
                  |
            =========""",
            """
              +---+
              |   |
              O   |
             /|\\  |
             /    |
                  |
            =========""",
            """
              +---+
              |   |
              O   |
             /|\\  |
             / \\  |
                  |
            ========="""
        ]
    
    def display_hangman(self, attempts_left):
        """Display the hangman figure based on attempts left"""
        st.text(self.hangman_pics[6 - attempts_left])
    
    def run(self):
        """Run the Streamlit app"""
        st.title("🎮 Hangman Game")
        st.write("Guess the hidden word one letter at a time!")
        
        # Initialize session state for the game
        if 'game' not in st.session_state:
            st.session_state.game = Game()
        
        game = st.session_state.game
        
        # Display current word state
        st.subheader("Word to Guess:")
        word_display = " ".join(game.current_word.get_current_state())
        st.markdown(f"## `{word_display}`")
        
        # Display attempts left
        st.markdown(f"Attempts left: **{game.attempts_left}**")
        
        # Display hangman figure
        self.display_hangman(game.attempts_left)
        
        # Letter buttons
        if not game.game_over:
            st.write("Select a letter:")
            
            # Create a grid of letter buttons using columns
            cols = st.columns(7)
            alphabet = 'abcdefghijklmnopqrstuvwxyz'
            
            for i, letter in enumerate(alphabet):
                col_index = i % 7
                disabled = letter not in game.current_word.get_remaining_letters()
                
                if cols[col_index].button(letter.upper(), key=letter, disabled=disabled):
                    game.guess(letter)
                    st.rerun()
        
        # Game over message
        if game.game_over:
            if game.won:
                st.success(f"🎉 Congratulations! You guessed the word: {game.current_word.word}")
            else:
                st.error(f"😔 Game Over! The word was: {game.current_word.word}")
            
            if st.button("Play Again"):
                st.session_state.game = Game()
                st.rerun()


# Main entry point
if __name__ == "__main__":
    app = HangmanApp()
    app.run()