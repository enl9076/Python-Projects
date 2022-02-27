import random, string, pygame, pyautogui
from hints import *

pygame.init()
display_win = pygame.display.set_mode((900,700))
pygame.display.set_caption('Hangman')
clock = pygame.time.Clock()


# Game variables
word_list = word_list
possible_letters = list(string.ascii_uppercase)
remaining_letters = []
correct_guesses = []
incorrect_guesses = []

POS_X, POS_Y = (600, 300)
hangman_status = 0
restart = True

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (10, 10, 180)
CYAN = (160, 240, 255)
GREEN = (0, 255, 0)
RED = (250, 0, 0)
PURPLE = (255, 0, 255)

# Fonts
LETTERFONT = pygame.font.SysFont("timesnewroman", 30)
WORDFONT = pygame.font.SysFont("timesnewroman", 40)
MSGFONT = pygame.font.SysFont("franklingothic", 60)
TITLEFONT = pygame.font.SysFont("comicsans", 70)

# Images
images = []
for i in range(6):
  image = pygame.image.load("img" + str(i) + ".png")
  images.append(image)


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
        display_win.blit(hint_msg, (105, 170))
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
    hint = LETTERFONT.render(hints[target_word.lower()], 1, BLACK)
    display_win.blit(hint, (110, 170))
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
                    possible_letters = list(string.ascii_uppercase)
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
    print(target_word)
    while game_play:
        clock.tick(60)
        
        display_win.fill(BLACK)
        title = TITLEFONT.render("Homicide Hangman", 1, RED)
        display_win.blit(title, (180, 10))
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
                    
            if event.type == pygame.TEXTINPUT:
                guess = event.text
                
                if guess in target_word and guess not in correct_guesses:
                    correct_guesses.append(guess)
                    remaining_letters.remove(guess.upper())
                    
                elif guess in incorrect_guesses.upper() or guess in correct_guesses.upper():
                    pyautogui.alert("You already guessed that letter! Guess again!")
                
                elif guess not in possible_letters:
                    pyautogui.alert("Try a letter!")
                    
                elif guess not in target_word:
                    if len(incorrect_guesses) == 4:
                        ask_hint()
                    elif hangman_status < 5:
                        hangman_status += 1
                        display_win.blit(images[hangman_status], (180, 200))
                        pygame.display.update()
                        remaining_letters.remove(guess.upper())
                        incorrect_guesses.append(guess)
                        
                    elif hangman_status == 5:
                        display_message("You lose! "+f"It was {full_names[target_word]}", RED)
                        game_play=False

                    
                if len(set(target_word)) == len(set(correct_guesses)):
                    display_message("You win! "+f"It was {full_names[target_word]}", DARK_BLUE)
                    game_play= False

                    
while restart:        
    target_word, remaining_letters = choose_word()
    
    game()
    
    play_again()

