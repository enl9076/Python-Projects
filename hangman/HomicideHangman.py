import random, string, pygame, pyautogui
from pygame import mixer
from pygame.locals import *
from hints import *

pygame.init()
DIS_WIDTH = 900
DIS_HEIGHT = 700
display_win = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Hangman')
clock = pygame.time.Clock()


# Game variables
word_list = word_list
possible_letters = list(string.ascii_letters)
remaining_letters = []
correct_guesses = []
incorrect_guesses = []
global music 
global get_hints
global menu 

POS_X, POS_Y = (600, 300)
hangman_status = 0
restart = True

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (10, 10, 180)
CYAN = (160, 240, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

# Fonts
LETTERFONT = pygame.font.SysFont("timesnewroman", 30)
WORDFONT = pygame.font.SysFont("timesnewroman", 40)
MSGFONT = pygame.font.SysFont("franklingothic", 60)
TITLEFONT = pygame.font.SysFont("comicsans", 70)

# Images
bg = pygame.image.load("bgPNG_new.png")

images = []
for i in range(6):
  image = pygame.image.load("img" + str(i) + ".png")
  images.append(image)
  
# Sound 
def music_playback(is_on=True):
    if is_on==True:
        mixer.init()
        mixer.music.load('bg_music.wav')
        lose_sound = mixer.Sound('lose_sound.wav')
        mixer.music.play(-1)
        return lose_sound 
    elif is_on==False:
        mixer.music.stop()

def start_menu(restart=True):
    menu = True
    while menu:
        
        display_win.fill(BLACK)
        display_win.blit(bg, (0,0))
        pygame.draw.rect(display_win, BLACK, (340,300,200,65))
        pygame.draw.rect(display_win, BLACK, (340,400,200,65))
        title = TITLEFONT.render("Homicide Hangman", 1, RED)
        start = WORDFONT.render("Start Game", 1, GREEN)
        settings = WORDFONT.render("Settings", 1, GREEN)
        display_win.blit(title, (180, 80))
        display_win.blit(start, (350, 310))
        display_win.blit(settings, (380, 410))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                if clickPos[0] >= 340 and clickPos[0] <= 540 and clickPos[1] >= 300 and clickPos[1] <= 365:
                    menu = False
                elif clickPos[0] >= 340 and clickPos[0] <= 540 and clickPos[1] >= 400 and clickPos[1] <= 465:
                    get_settings()


def get_settings():
    settings = True
    while settings:
        display_win.fill(BLACK)
        title = TITLEFONT.render("Homicide Hangman", 1, RED)
        settings = WORDFONT.render("Settings", 1, GREEN)
        music = LETTERFONT.render("Music", 1, RED)
        hints_on = LETTERFONT.render("Hints", 1, RED)
        ok_btn = LETTERFONT.render("OK", 1, PURPLE)
        on1 = LETTERFONT.render("On", 1, WHITE)
        off1 = LETTERFONT.render("Off", 1, WHITE)
        on2 = LETTERFONT.render("On", 1, WHITE)
        off2 = LETTERFONT.render("Off", 1, WHITE)
        display_win.blit(title, (180, 10))
        display_win.blit(settings, (350, 200))
        display_win.blit(music, (200, 350))
        display_win.blit(on1, (400, 350))
        display_win.blit(off1, (500, 350))
        display_win.blit(hints_on, (200, 440))
        display_win.blit(on2, (400, 440))
        display_win.blit(off2, (500, 440))
        display_win.blit(ok_btn, (800, 600))
        pygame.draw.circle(display_win, WHITE, (380, 370), 8, width=2)
        pygame.draw.circle(display_win, WHITE, (480, 370), 8, width=2)
        pygame.draw.circle(display_win, WHITE, (380, 460), 8, width=2)
        pygame.draw.circle(display_win, WHITE, (480, 460), 8, width=2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                if clickPos[0] >= 800 and clickPos[0] <= 900 and clickPos[1] >= 600 and clickPos[1] <= 650:
                    settings = False
                    menu = True
                elif clickPos[0] >= 375 and clickPos[0] <= 385 and clickPos[1] >= 365 and clickPos[1] <= 375:
                    music_playback()
                elif clickPos[0] >= 475 and clickPos[0] <= 485 and clickPos[1] >= 365 and clickPos[1] <= 375:
                    music_playback(False)

def choose_word():
    target_word = random.choice(word_list)
    remaining_letters = list(string.ascii_uppercase)
    return target_word, remaining_letters

def show_word():
    display_word = ""
    for i in target_word:
        if i in correct_guesses:
            display_word += i + " "
        else:
            display_word += "_ "
    text = WORDFONT.render(display_word, 1, GREEN)
    display_win.blit(text, (POS_X, POS_Y))


def show_choices():
    choices = ""
    for i in remaining_letters:
        choices += i + "  "
    options_text_row1 = LETTERFONT.render(choices[0:len(choices)//2], 1, WHITE)
    options_text_row2 = LETTERFONT.render(choices[len(choices)//2:len(choices)], 1, WHITE)
    display_win.blit(options_text_row1, (50, 500))
    display_win.blit(options_text_row2, (50, 530))

def display_message(message, color):
    display_win.fill(WHITE)
    msg = MSGFONT.render(message, 1, color)
    display_win.blit(msg, (100, 300))
    pygame.display.update()
    pygame.time.delay(3000)

def ask_hint():
    hint = True
    while hint:
        pygame.draw.rect(display_win, CYAN, (100,150,750,120))
        hint_msg = LETTERFONT.render("You've made 5 incorrect guesses, would you like a hint? (y/n)", 1, BLACK)
        display_win.blit(hint_msg, (100, 170))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.TEXTINPUT:
                if event.text.lower() == 'y':
                    show_hint()
                    hint = False
                elif event.text.lower() == 'n':
                    hint = False
        
def show_hint():
    pygame.draw.rect(display_win, CYAN, (100,150,750,120))
    hint = LETTERFONT.render(hints[target_word], 1, BLACK)
    display_win.blit(hint, (100, 170))
    pygame.display.update()
    pygame.time.delay(5000)
    
def play_again():
    ask = True
    while ask:
        display_win.fill(WHITE)
        text = MSGFONT.render("Play again? (y/n)", 1, PURPLE)
        display_win.blit(text, (300, 300))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.TEXTINPUT:
                if event.text.lower() == 'y':
                    correct_guesses.clear()
                    incorrect_guesses.clear()
                    possible_letters = list(string.ascii_letters)
                    remaining_letters = possible_letters
                    restart==True
                    ask=False
                elif event.text.lower() == 'n':
                    pygame.quit()
                    quit()

    
# Main game loop
def game():
    hangman_status = 0
    game_play = True
    
    while game_play:
        clock.tick(60)
        
        display_win.fill(BLACK)
        title = TITLEFONT.render("Homicide Hangman", 1, RED)
        start_return = LETTERFONT.render("Return to Start", 1, RED)
        pygame.draw.rect(display_win, BLACK, (690,640,60,100))
        display_win.blit(title, (180, 10))
        display_win.blit(start_return, (700, 650))
        display_win.blit(images[hangman_status], (150, 170))
        show_word()
        show_choices()
        pygame.display.update()
        pygame.key.start_text_input()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickPos = pygame.mouse.get_pos()
                if clickPos[0] >= 710 and clickPos[0] <= 800 and clickPos[1] >= 660 and clickPos[1] <= 860:
                    game_play = False
                    restart = True
                    start_menu()
                    
            if event.type == pygame.TEXTINPUT:
                guess = event.text
                
                if guess in target_word and guess not in correct_guesses:
                    correct_guesses.append(guess)
                    remaining_letters.remove(guess.upper())
                    
                elif guess in incorrect_guesses or guess in correct_guesses:
                    pyautogui.alert("You already guessed that letter! Guess again!")
                
                elif guess not in possible_letters:
                    pyautogui.alert("Try a letter!")
                    
                elif guess not in target_word:
                    if hangman_status < 5 and len(incorrect_guesses) < 4:
                        hangman_status += 1
                        display_win.blit(images[hangman_status], (180, 200))
                        pygame.display.update()
                        remaining_letters.remove(guess.upper())
                        incorrect_guesses.append(guess)
                        
                    elif hangman_status < 5 and len(incorrect_guesses) == 4:
                        ask_hint()
                        hangman_status += 1
                        display_win.blit(images[hangman_status], (180, 200))
                        remaining_letters.remove(guess.upper())
                        incorrect_guesses.append(guess)     
                        
                    elif hangman_status == 5:
                        pygame.mixer.Sound.play(lose_sound)
                        display_message("You lose! "+f"It was {full_names[target_word]}", RED)
                        game_play=False

                    
                if len(set(target_word)) == len(set(correct_guesses)):
                    display_message("You win! "+f"It was {full_names[target_word]}", DARK_BLUE)
                    game_play= False


music_playback(True)
start_menu()
                   
while restart:        
    
    target_word, remaining_letters = choose_word()
    
    game()
    
    play_again()

