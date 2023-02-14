import tkinter as tk
from tkinter import *
from bs4 import BeautifulSoup
import requests
import random
import math

# Create a view with Tkinter
BACKGROUND_COLOR = "white"
window = tk.Tk()
window.title("Type Speed Test")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)

# variable initialize
## timer variables
timer = None
TIME_LENGTH = 60
## score variables
score_num = 0
game_continue= False
## type variables
words_list = []
entered_text = ""
letter_loc = 0
q_word = ""


# Create words library
URL = r"https://en.wiktionary.org/wiki/Appendix:1000_basic_English_words"
response = requests.get(url=URL)
soup = BeautifulSoup(response.text, "html.parser")
words_list_init = soup.find_all(name=["dd","a"])
for words_list_a_tag in words_list_init:
    words = words_list_a_tag.find_all(name="a")
    [words_list.append(word.text) for word in words]


# Set timer
def start_timer():
    global game_continue
    global q_word
    game_continue = True
    count_down(TIME_LENGTH)
    start_button.grid_remove()
    q_word = random.choice(words_list)
    update_view()

def count_down(count):
    global game_continue
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}" #remaining seconds
    remaining_time.config(text=f"{count_min}:{count_sec}") #change to label
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        game_continue = False
        problem.config(text=f"Final score is {score_num}")
        restart_button.grid(sticky = "n", row=6, column=0, columnspan=2)
            
def restart_game():
    global score_num
    # reset view
    window.after_cancel(timer)
    remaining_time.config(text="00:00")
    score_num = 0
    score.config(text=f"Score: {score_num}")
    # restart functions
    start_timer()
    reset_setting()
    restart_button.grid_remove()

#reset variables for new game
def reset_setting():
    global q_word
    global entered_text
    global letter_loc
    q_word = random.choice(words_list)
    entered_text = ""
    letter_loc = 0
    update_view()

def update_view():
    global q_word
    global score_num
    #show new word
    problem.config(text=q_word)
    #clear user entry
    user_entry.config(text=entered_text)
    #update score
    score.config(text=f"Score: {score_num}", background=BACKGROUND_COLOR, font=("Arial", "12"))

def add_score_num():
    global score_num
    score_num += 1

# enter word and check answer
def type_event(event):
    global entered_text
    global letter_loc
    global game_continue
    if game_continue:
        letters = list(q_word)
        letter_count = len(letters)
        if letter_loc == letter_count:
            add_score_num()
            reset_setting()
            update_view()
        else:
            if letters[letter_loc] == event.keysym:
                letter_loc += 1
                # show letter on view
                entered_text = entered_text + event.keysym
                user_entry.config(text=entered_text)
                


# User view
q_word = "Problem Here"
title = tk.Label(text=f"Type Speed Test", background=BACKGROUND_COLOR, font=("Arial", "20", "bold"))
title.grid(sticky = "w", row=0, column=0, columnspan=2)
score = tk.Label(text=f"Score: {score_num}", background=BACKGROUND_COLOR, font=("Arial", "12"))
score.grid(sticky = "n", row=1, column=0, columnspan=2)
remaining_time = tk.Label(text=f"01:00", background=BACKGROUND_COLOR, font=("Arial", "12"))
remaining_time.grid(sticky = "n", row=2, column=0, columnspan=2)
problem_label = tk.Label(text="Enter: ", background=BACKGROUND_COLOR, font=("Arial", "12"))
problem_label.grid(sticky = "n", row=3, column=0, columnspan=2)
problem = tk.Label(text=q_word, background=BACKGROUND_COLOR, font=("Arial", "20"))
problem.grid(sticky = "n", row=4, column=0, columnspan=2)
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)
user_entry = tk.Label(text="", background=BACKGROUND_COLOR, font=("Arial", "12", "bold"))
user_entry.grid(sticky = "n", row=5, column=0, columnspan=2)
restart_button = Button(text="Re-start", highlightthickness=0, command=restart_game)
restart_button.grid(sticky = "n", row=6, column=0, columnspan=2)
restart_button.grid_remove()

# catch user keyboard entry
event_sequence = '<KeyPress>'
window.bind(event_sequence, type_event)

window.mainloop()