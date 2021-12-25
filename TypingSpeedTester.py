import curses   #inbuilt py module for styling / designing terminal 
from curses import wrapper  #It initialises the module & gains control over your terminal/ screen
import time #standard python module which gives the current time once called.


def start_screen(stdscr): #func1: It shows some messages before starting the game. we pass stdscr coz we use .addstr, .refresh etc...
    stdscr.clear() #It clears the junk present in the buffer
    stdscr.addstr("Welcome to the Speed Typing Test! You'll be given a block of text and need to type as fast as possible.")
    stdscr.addstr("\nPress any key to start!")  #It adds the string to the standard screen[here terminal].Works same as printf in C lang
    stdscr.refresh() #It refreshes the screen after clearing and adding text to the screen.
    stdscr.getkey() #It waits for user to input any key.Works same as getch() in C lang, it holds the screen.

def display_text(stdscr, target_text, current_text, wpm=0): #func2 here wpm=0 means if we do not give any value it will have the value of zero {0}.
    stdscr.addstr(target_text) #it prints the sentence present in the target_text variable.
    stdscr.addstr(1, 0, f"WPM:{wpm}") #it adds two strings directly "WPM:", by putting the curly braces it behaves as a variable(here wpm) directly to the screen where (1 , 0) signifies rows n column 

    

    for i, char in enumerate(current_text): #Overlaying the target text.
        #here enumerate will give the index no. and the the corresponding element in a string. i starts from 0 and increases by one 
        correct_char = target_text[i] #it stores the i^th element of the target text.
        color =curses.color_pair(1)
        if char != correct_char: # it constantly compares i^th element of the current text with the corresponding element of the target text
            color = curses.color_pair(2)# if the character does not match its color is changed to the pair with ID 2.
        stdscr.addstr(0 ,i, char,color)#overlaying the current text over the target text.


def wpm_test(stdscr):

    target_text = "Hello this is a typing test line for testing your speed!"# variable that stores the target text.
    current_text = [] #It is a list which stores multiple items in a single variable.Currently it stores our user keys
    wpm = 0 #variable whose current value is 0
    start_time = time.time() # It stores the current time that is the starting time 
    stdscr.nodelay(True)# it is a method which says here do not delay for the user to enter any key.

    
    while True:
        time_elapsed = max(time.time() - start_time, 1) # it takes the maximum of the current time and the starting time. If the starting time is zero it will take as max as 1. 
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5) #rounding off the whole formula where 5 denotes avg. character per word.
        stdscr.clear() 

        display_text(stdscr, target_text, current_text, wpm)#Calling the function 

        stdscr.refresh()

        if "".join(current_text) == target_text: #When the user have typed all the strings correctly then we will compare the user input to the target text but their nature is different so to convert list into string we use .join(arg)
            stdscr.nodelay(False)
            break

        try:
            key =stdscr.getkey() # this acting as a blocker here so to ignore this exception we use try and except steatement
        except:
            continue

        if ord(key) == 27:# if the user presses the Esc key ,the game stops as the ASSCI code of Esc is 27.
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):#if the user presses backspace key. 
            if len(current_text) > 0:
                current_text.pop()#instead of sliding the cursor backwards it just deletes the last character
        elif len(current_text) < len(target_text): # this condition is when we are at the very end character of the target_text.So, stops you from writing furthur.
            current_text.append(key)   #it stores the the character to the end(append) of the current_text  
        

        

def main(stdscr):
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)# Adds color to the string in foreground and background.
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)# ( ID of the pair ,color of the text, background)
    curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_BLACK)
    
    start_screen(stdscr) #calling the start_screen function
    while True:   
        wpm_test(stdscr)
    
        stdscr.addstr(2, 0, "You completed the test! Press any key to continue...")
        stdscr.addstr(3, 0, "Press Esc to exit the game!!!")
        key = stdscr.getkey()
        if ord(key) == 27:#It waits for user to input any key.Works same as getch() in C lang, it holds the screen.
            break

 
wrapper(main)