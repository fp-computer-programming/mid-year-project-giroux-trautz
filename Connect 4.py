# Authors: MOG SCT 2/22/22

# Import sys and pygame
import sys
import pygame
from pygame.locals import *

# Initiate Pygame
pygame.init()

# Set variables such as screen size, the pygame clock to keep things at a certain framerate, and instruction text
width, height = 840, 840
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
smallfont = pygame.font.SysFont('Corbel', 40)
instructions1 = smallfont.render('Connect four of your checkers in a row', True, (0,0,0))
instructions2 = smallfont.render('while preventing your opponent from doing', True, (0,0,0))
instructions3 = smallfont.render('the same. But, look out - your opponent', True, (0,0,0))
instructions4 = smallfont.render('can sneak up on you and win the game!', True, (0,0,0))

# Make other text variables
smallfont = pygame.font.SysFont('Corbel', 70)
start_text = smallfont.render('Which Color Starts?', True, (0,0,0))

smallfont = pygame.font.SysFont('Corbel', 120)
yellow_wins = smallfont.render('Yellow Wins!', True, (255,220,0))
red_wins = smallfont.render('Red Wins!', True, (220,0,0))
tie = smallfont.render('Tie!', True, (0,0,0))

smallfont = pygame.font.SysFont('Corbel', 30)
again1y = smallfont.render('Play', True, (0,0,0))
again2y = smallfont.render('again?', True, (0,0,0))
again1r = smallfont.render('Play', True, (255,255,255))
again2r = smallfont.render('again?', True, (255,255,255))

# Load and scale images to correct size
logo = pygame.image.load('connect4logo.png')
logo = pygame.transform.scale(logo, (840, 258))
yellow = pygame.image.load('connect4yellow.png')
yellow = pygame.transform.scale(yellow, (350, 200))
red = pygame.image.load('connect4red.png')
red = pygame.transform.scale(red, (350, 200))
shadow = pygame.image.load('connect4shadow.png')
shadow = pygame.transform.scale(shadow, (360, 210))

# Set "global" variables that can be updated as game progresses
state = [0]
team = [1]
pos = [4]
score_y = [0]
score_r = [0]
first_game = [1]

# Make 7x6 board using a python comprehension to save space
board = [[0 for _ in range(7)] for _ in range(6)]

# Iterate through every "slot" and return it back to 0
def clear_board():
    for x in range(6):
        for y in range(7):
            board[x][y] = 0
    first_game[0] = 0

# If the slot is not full, set the lowest empty slot in the row to either 1 or -1 depending on which team is dropping
def play(slot, team):
    for x in range(6):
        if board[5 - x][slot - 1] == 0:
            board[5 - x][slot - 1] = team[0]
            team[0] *= -1
            pos[0] = 4
            break

# Draw a yellow or red chip at (x,y) depending on team color
def draw_chip(x,y,team):
    if team == 1:
        color1 = (255,220,0)
        color2 = (220,190,0)
    else:
        color1 = (220,0,0)
        color2 = (190,0,0)

# Many concentric circles to give the chip its appearance
    pygame.draw.circle(screen, color1, (x, y), 50)

    pygame.draw.circle(screen, color2, (x - 45, y), 2)
    pygame.draw.circle(screen, color2, (x - 42, y - 18), 2)
    pygame.draw.circle(screen, color2, (x - 32, y - 32), 2)
    pygame.draw.circle(screen, color2, (x - 18, y - 42), 2)
    pygame.draw.circle(screen, color2, (x, y - 45), 2)
    pygame.draw.circle(screen, color2, (x + 18, y - 42), 2)
    pygame.draw.circle(screen, color2, (x + 32, y - 32), 2)
    pygame.draw.circle(screen, color2, (x + 42, y - 18), 2)
    pygame.draw.circle(screen, color2, (x + 45, y), 2)
    pygame.draw.circle(screen, color2, (x + 42, y + 18), 2)
    pygame.draw.circle(screen, color2, (x + 32, y + 32), 2)
    pygame.draw.circle(screen, color2, (x + 18, y + 42), 2)
    pygame.draw.circle(screen, color2, (x, y + 45), 2)
    pygame.draw.circle(screen, color2, (x - 42, y + 18), 2)
    pygame.draw.circle(screen, color2, (x - 32, y + 32), 2)
    pygame.draw.circle(screen, color2, (x - 18, y + 42), 2)

    pygame.draw.circle(screen, color2, (x, y), 40)
    pygame.draw.circle(screen, color1, (x, y), 38)
    pygame.draw.circle(screen, color2, (x, y), 34)
    pygame.draw.circle(screen, color1, (x, y), 31)
    pygame.draw.circle(screen, color2, (x, y), 27)
    pygame.draw.circle(screen, color1, (x, y), 25)

# For every space in our board, if there is a 1 or -1, draw the appropriate color chip in the appropriate slot
def display_chips():
    for y, i in enumerate(board):
        for x, val in enumerate(i):
            if val == 1:
                draw_chip(x * 120 + 60, y * 120 + 180, 1)
            elif val == -1:
                draw_chip(x * 120 + 60, y * 120 + 180, -1)

# draw a chip in the top bar that can move side to side based on the "pos" variable
def moving_chip(slot, team):
    draw_chip(slot * 120 - 60, 60, team)

# Make the chip visually "fall" into its designated position
def drop(slot, team):
    for i in range(6):
        if board[5 - i][slot - 1] == 0:
            y = 5 - i + 1
            break

    for i in range(1, int((y * 120) ** (1 / 2)) + 1):
        pygame.draw.circle(screen, (255,255,255), (slot * 120 - 60, y), 55)
        y = i ** 2 + 60

# Update screen        
        draw_chip(slot * 120 - 60, y, team)
        draw_board()
        clock.tick(60)
        pygame.display.flip()

# Iterate through each possible win position, if a win is found, return 1 or -1 if the board is full, return -2, else 0
def check_for_win():
    win = 0
    # Vertical Checks
    for x in range(6-3):
        for y in range(7):
            if board[x][y] == board[x+1][y] == board[x+2][y] == board[x+3][y] and board[x][y] != 0:
                win = board[x][y]
    # Horizontal Checks
    for x in range(6):
        for y in range(7-3):
            if board[x][y] == board[x][y+1] == board[x][y+2] == board[x][y+3] and board[x][y] != 0:
                win = board[x][y]
    # Diagonal Right Checks
    for x in range(6-3):
        for y in range(7-3):
            if board[x][y] == board[x+1][y+1] == board[x+2][y+2] == board[x+3][y+3] and board[x][y] != 0:
                win = board[x][y]
    # Diagonal Left Checks
    for x in range(2,6):
        for y in range(7-3):
            if board[x][y] == board[x-1][y+1] == board[x-2][y+2] == board[x-3][y+3] and board[x][y] != 0:
                win = board[x][y]
    # Filled Board Check
    empty_spaces = len([x for y in board for x in y if x == 0])
    if empty_spaces == 0:
        return -2
    
    return win

# Draw the literal board onscreen by drawing one section and repeating it over each row, in each column
def draw_board():
    for x in range(8):
        pygame.draw.rect(screen, (0,0,255), (x * 120 - 10, 120, 20, 840))
        for y in range(7):
            pygame.draw.rect(screen, (0,0,255), (0 , x * 120 - 10 + 240, 840, 20))
            if y > 0:
                pygame.draw.polygon(screen, (0,0,255), [(x * 120 + 40, y * 120 + 120), (x * 120, y * 120 + 40 + 120), (x * 120 - 40, y * 120 + 120), (x * 120, y * 120 - 40 + 120)])
            else:
                pygame.draw.polygon(screen, (0,0,255), [(x * 120 + 40, 120), (x * 120, y * 120 + 40 + 120), (x * 120 - 40, y * 120 + 120)])

    pygame.draw.rect(screen, (0,0,255), (0,120,840,10))

    for x in range(7):
        for y in range(6):
            pygame.draw.circle(screen, (0,0,255), (x * 120 + 60, y * 120 + 180), 60, 10)
            pygame.draw.circle(screen, (0,100,255), (x * 120 + 60, y * 120 + 180), 55, 5)

# Displays the start screen, with the title, instructions, buttons, and code to detect whether the mouse is hovering over the button
def start_screen():
    screen.fill((255,255,255))

    if (((mouse[0] - 150) ** 2) + ((mouse[1] - 690) ** 2)) ** .5 <= 100 or (((mouse[0] - 300) ** 2) + ((mouse[1] - 690) ** 2)) ** .5 <= 100 or 150 <= mouse[0] <= 300 and 590 <= mouse[1] <= 790:
        screen.blit(shadow, (45,585))
    if (((mouse[0] - 540) ** 2) + ((mouse[1] - 690) ** 2)) ** .5 <= 100 or (((mouse[0] - 690) ** 2) + ((mouse[1] - 690) ** 2)) ** .5 <= 100 or 540 <= mouse[0] <= 690 and 590 <= mouse[1] <= 790:
        screen.blit(shadow, (435,585))

# "Blit" the logo and buttons to the screen
    screen.blit(logo, (0,0))
    screen.blit(yellow, (50,590))
    screen.blit(red, (440,590))
    screen.blit(instructions1 , (420 - instructions1.get_rect()[2] // 2, 250))
    screen.blit(instructions2 , (420 - instructions2.get_rect()[2] // 2, 300))
    screen.blit(instructions3 , (420 - instructions3.get_rect()[2] // 2, 350))
    screen.blit(instructions4 , (420 - instructions4.get_rect()[2] // 2, 400))
    screen.blit(start_text, (420 - start_text.get_rect()[2] // 2, 500))

# Start of game loop
while True:
    mouse = pygame.mouse.get_pos()

# If someone has won/the board is full, change to the win/tie screen
    if check_for_win() != 0:
        state[0] = 2

# If the state variable is 0, display the start screen
    if state[0] == 0:
        start_screen()
    
# If the state variable is 1, fill the background with white, display the chip at the top, and display the chips with the board
    if state[0] == 1:
        screen.fill((255,255,255))
        moving_chip(pos[0], team[0])
        display_chips()
        draw_board()

# If the state variable is 2, fill the background with white and display the chips with the board like state 1, but this time, display who won and add in buttons to play again
    if state[0] == 2:
        screen.fill((255,255,255))
        display_chips()
        draw_board()
        if check_for_win() == 1:
            screen.blit(yellow_wins, (420 - yellow_wins.get_rect()[2] // 2, 10))
        if check_for_win() == -1:
            screen.blit(red_wins, (420 - red_wins.get_rect()[2] // 2, 10))
        if check_for_win() == -2:
            screen.blit(tie, (420 - tie.get_rect()[2] // 2, 13))

        if (((mouse[0] - 60) ** 2) + ((mouse[1] - 60) ** 2)) ** .5 <= 50:
            pygame.draw.circle(screen, (0,0,0), (60,60), 52)
        if (((mouse[0] - 780) ** 2) + ((mouse[1] - 60) ** 2)) ** .5 <= 50:
            pygame.draw.circle(screen, (0,0,0), (780,60), 52)
        draw_chip(60, 60, 1)
        draw_chip(780, 60, -1)
# If its not the first game in this "session" display the score instead of "Play again?"
        if first_game[0] == 1:
            screen.blit(again1y, (60 - again1y.get_rect()[2] // 2, 35))
            screen.blit(again2y, (60 - again2y.get_rect()[2] // 2, 55))
            screen.blit(again1r, (780 - again1r.get_rect()[2] // 2, 35))
            screen.blit(again2r, (780 - again2r.get_rect()[2] // 2, 55))
        else:
            smallfont = pygame.font.SysFont('Corbel', 50)
            yellow_score = smallfont.render('{}'.format(score_y[0]), True, (0,0,0))
            red_score = smallfont.render('{}'.format(score_r[0]), True, (255,255,255))
            screen.blit(yellow_score, (60 - yellow_score.get_rect()[2] // 2, 60 - yellow_score.get_rect()[3] // 2))
            screen.blit(red_score, (780 - red_score.get_rect()[2] // 2, 60 - red_score.get_rect()[3] // 2))

# Handles button inputs
    for event in pygame.event.get():
# If the x button is clicked, end the game
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if state[0] == 1:
# If the game is being played and a key is pressed, move the pos of the moving chip left or right
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  
                    if pos[0] < 7:
                        pos[0] += 1
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if pos[0] > 1:
                            pos[0] -= 1
# If s or down is pressed and the game is being played, drop the chip using the drop() and play() functions
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if board[0][pos[0] - 1] == 0:
                            drop(pos[0], team[0])
                            play(pos[0], team)
                            if check_for_win() == 1:
                                score_y[0] += 1
                            if check_for_win() == -1:
                                score_r[0] += 1 
# On click, if the mouse is over a button in the start screen, reload the game to play again.
        if event.type == pygame.MOUSEBUTTONUP:
            if state[0] == 0:
                if (((mouse[0] - 150) ** 2) + ((mouse[1] - 690) ** 2)) ** .5 <= 100 or (((mouse[0] - 300) ** 2) + ((mouse[1] - 690) ** 2)) ** .5 <= 100 or 150 <= mouse[0] <= 300 and 590 <= mouse[1] <= 790:
                    team[0] = 1
                    state[0] = 1
                if (((mouse[0] - 540) ** 2) + ((mouse[1] - 690) ** 2)) ** .5 <= 100 or (((mouse[0] - 690) ** 2) + ((mouse[1] - 690) ** 2)) ** .5 <= 100 or 540 <= mouse[0] <= 690 and 590 <= mouse[1] <= 790:
                    team[0] = -1
                    state[0] = 1
# On click, if the mouse is over a button in the end screen, reload the game to play again.
            if state[0] == 2:
                if (((mouse[0] - 60) ** 2) + ((mouse[1] - 60) ** 2)) ** .5 <= 50:
                    clear_board()
                    team[0] = 1
                    state[0] = 1
                if (((mouse[0] - 780) ** 2) + ((mouse[1] - 60) ** 2)) ** .5 <= 50:
                    clear_board()
                    team[0] = -1
                    state[0] = 1
# Wait enough time to make the game run at 60 fps, and update (flip) the screen
    clock.tick(60)
    pygame.display.flip()
