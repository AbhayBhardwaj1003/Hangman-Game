import tkinter as tk
from tkinter import messagebox

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        
        self.word = ""
        self.guessed_word = ""
        self.guesses = []
        self.incorrect_guesses = 0
        self.max_incorrect_guesses = 6

        self.create_widgets()
    
    def create_widgets(self):
        background_color = "#F0EDE5"
        header_color = "#5C6447" 
        button_color = "#C5DCA0" 
        text_color = "#333333"

        # Header label
        self.header_label = tk.Label(self.root, text="Hangman Game", font=("Helvetica", 24, "bold"), pady=10, fg=header_color)
        self.header_label.pack()

        # Frame for word input
        self.word_frame = tk.Frame(self.root)
        self.word_frame.pack(pady=10)

        self.word_label = tk.Label(self.word_frame, text="Player 1, enter the word to guess:", font=("Helvetica", 14), fg=text_color)
        self.word_label.grid(row=0, column=0, padx=10)

        self.word_entry = tk.Entry(self.word_frame, show='•', font=("Helvetica", 14), bg="white")
        self.word_entry.grid(row=0, column=1, padx=10)

        self.word_submit = tk.Button(self.word_frame, text="Submit Word", command=self.set_word, font=("Helvetica", 12), bg=button_color)
        self.word_submit.grid(row=0, column=2, padx=10)

        # Frame for guess input
        self.guess_frame = tk.Frame(self.root)
        self.guess_frame.pack(pady=10)

        self.guess_label = tk.Label(self.guess_frame, text="Player 2, enter your guess:", font=("Helvetica", 14), fg=text_color)
        self.guess_label.grid(row=0, column=0, padx=10)

        self.guess_entry = tk.Entry(self.guess_frame, font=("Helvetica", 14), bg="white")
        self.guess_entry.grid(row=0, column=1, padx=10)

        self.guess_submit = tk.Button(self.guess_frame, text="Guess", command=self.make_guess, font=("Helvetica", 12), bg=button_color)
        self.guess_submit.grid(row=0, column=2, padx=10)

        # Frame for game display (Hangman and status)
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()

        # Hangman canvas
        self.canvas = tk.Canvas(self.game_frame, width=400, height=400, bg='white', highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=10)

        # Frame for status labels
        self.status_frame = tk.Frame(self.game_frame)
        self.status_frame.grid(row=0, column=1, padx=10)

        self.progress_label = tk.Label(self.status_frame, text="", font=("Helvetica", 18, "bold"), bg=background_color, fg=text_color)
        self.progress_label.pack()

        self.guesses_label = tk.Label(self.status_frame, text="", font=("Helvetica", 14), bg=background_color, fg=text_color)
        self.guesses_label.pack()

        # Reset button
        self.reset_button = tk.Button(self.root, text="Reset Game", command=self.reset_game, font=("Helvetica", 14), bg=button_color)
        self.reset_button.pack(pady=10)

        # Initialize the game
        self.reset_game()

    def set_word(self):
        self.word = self.word_entry.get().upper()
        if not self.word.isalpha():
            messagebox.showwarning("Invalid Word", "Please enter a valid word (only letters).")
            return
        
        self.guessed_word = "_" * len(self.word)
        self.update_display()
        self.word_entry.config(state=tk.DISABLED)
        self.word_submit.config(state=tk.DISABLED)
    
    def make_guess(self):
        if not self.word:
            messagebox.showwarning("No Word Set", "Please enter a word first.")
            return
        
        guess = self.guess_entry.get().upper()
        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter.")
            return
        
        if guess in self.guesses:
            messagebox.showwarning("Already Guessed", "You have already guessed this letter.")
            return
        
        self.guesses.append(guess)
        self.guess_entry.delete(0, tk.END)
        
        if guess in self.word:
            new_guessed_word = ""
            for i in range(len(self.word)):
                if self.word[i] == guess:
                    new_guessed_word += guess
                else:
                    new_guessed_word += self.guessed_word[i]
            self.guessed_word = new_guessed_word
        else:
            self.incorrect_guesses += 1
        
        self.update_display()
        
        if self.guessed_word == self.word:
            messagebox.showinfo("Congratulations", "You have guessed the word!")
            self.reset_game()
        elif self.incorrect_guesses >= self.max_incorrect_guesses:
            messagebox.showinfo("Game Over", "You have been hanged! The word was: " + self.word)
            self.reset_game()

    def update_display(self):
        self.canvas.delete("all")

        self.canvas.create_text(200, 50, text="Hangman", font=("Helvetica", 24, "bold"))
        
        self.canvas.create_text(200, 80, text=self.guessed_word, font=("Helvetica", 18, "bold"))

        self.progress_label.config(text="Incorrect Guesses: " + str(self.incorrect_guesses))
        
        self.guesses_label.config(text="Guessed Letters: " + ", ".join(self.guesses))

        self.draw_hangman()

    def draw_hangman(self):
        if self.incorrect_guesses > 0:
            self.canvas.create_line(100, 350, 300, 350, width=3)  # Base

        if self.incorrect_guesses > 1:
            self.canvas.create_line(150, 350, 150, 100, width=3)  # Pole

        if self.incorrect_guesses > 2:
            self.canvas.create_line(150, 100, 250, 100, width=3)  # Top

        if self.incorrect_guesses > 3:
            self.canvas.create_line(250, 100, 250, 150, width=3)  # Rope

        if self.incorrect_guesses > 4:
            self.canvas.create_oval(225, 150, 275, 200, width=3)  # Head

        if self.incorrect_guesses > 5:
            self.canvas.create_line(250, 200, 250, 300, width=3)  # Body
            self.canvas.create_line(250, 225, 225, 275, width=3)  # Left Arm
            self.canvas.create_line(250, 225, 275, 275, width=3)  # Right Arm
            self.canvas.create_line(250, 300, 225, 350, width=3)  # Left Leg
            self.canvas.create_line(250, 300, 275, 350, width=3)  # Right Leg

    def reset_game(self):
        self.word = ""
        self.guessed_word = ""
        self.guesses = []
        self.incorrect_guesses = 0
        self.word_entry.config(state=tk.NORMAL)
        self.word_entry.delete(0, tk.END)
        self.word_submit.config(state=tk.NORMAL)
        self.progress_label.config(text="")
        self.guesses_label.config(text="")
        self.canvas.delete("all")
        self.draw_hangman()

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
