import pygame
from   pygame import mixer
import random
import time
from collections import deque

# Initializing pygame

pygame.init()
pygame.display.set_caption("Ludo")
screen = pygame.display.set_mode((680, 600))
# Loading Images

board = pygame.image.load(r"D:\prog projects\dsa_task\graphics\Board_2.png")
star  = pygame.image.load(r"D:\prog projects\dsa_task\assets\star.png")
one   = pygame.image.load(r"D:\prog projects\dsa_task\assets\1.png")
two   = pygame.image.load(r"D:\prog projects\dsa_task\assets\2.png")
three = pygame.image.load(r"D:\prog projects\dsa_task\assets\3.png")
four  = pygame.image.load(r"D:\prog projects\dsa_task\assets\4.png")
five  = pygame.image.load(r"D:\prog projects\dsa_task\assets\5.png")
six   = pygame.image.load(r"D:\prog projects\dsa_task\assets\6.png") 

red    = pygame.image.load(r"D:\prog projects\dsa_task\graphics\adel_token\red.png")
blue   = pygame.image.load(r"D:\prog projects\dsa_task\graphics\adel_token\blue.png")
green  = pygame.image.load(r"D:\prog projects\dsa_task\graphics\adel_token\green.png")
yellow = pygame.image.load(r"D:\prog projects\dsa_task\graphics\adel_token\yellow.png")

DICE  = [one, two, three, four, five, six]
color = [red, green, yellow, blue]

# Loading Sounds

killSound   = mixer.Sound(r"D:\prog projects\dsa_task\graphics\adel_token\sounds\kill.mp3")
tokenSound  = mixer.Sound(r"D:\prog projects\dsa_task\graphics\adel_token\sounds\token_movment.mp3")
diceSound   = mixer.Sound(r"D:\prog projects\dsa_task\graphics\adel_token\sounds\Dice Roll.wav")
winnerSound = mixer.Sound(r"D:\prog projects\dsa_task\graphics\adel_token\sounds\win.mp3")

# Initializing Variables

number        = 1
playerKilled  = False
diceRolled    = False
winnerRank    = []

turn_queue = deque([0, 1, 2, 3])
currentPlayer = turn_queue[0]


# Rendering Text

font = pygame.font.Font('freesansbold.ttf', 11)
FONT = pygame.font.Font('freesansbold.ttf', 16)
currentPlayerText = font.render('Current Player', True, (0, 0, 0))
line = font.render('------------------------------------', True, (0, 0, 0))

# Defining Important Coordinates

HOME = [[(110, 58),  (61, 107),  (152, 107), (110, 152)],  # Red
        [(466, 58),  (418, 107), (509, 107), (466, 153)],  # Green
        [(466, 415), (418, 464), (509, 464), (466, 510)],  # Yellow
        [(110, 415), (61, 464),  (152, 464), (110, 510)]]  # Blue

        # Red      # Green    # Yellow    # Blue
SAFE = [(50, 240), (328, 50), (520, 328), (240, 520),
        (88, 328), (240, 88), (482, 240), (328, 482)]

position = [[[110, 58],  [61, 107],  [152, 107], [110, 152]],  # Red
            [[466, 58],  [418, 107], [509, 107], [466, 153]],  # Green
            [[466, 415], [418, 464], [509, 464], [466, 510]],  # Yellow
            [[110, 415], [61, 464],  [152, 464], [110, 510]]]  # Blue

jump = {(202, 240): (240, 202),  # R -> G
        (328, 202): (368, 240),  # G -> Y
        (368, 328): (328, 368),  # Y -> B
        (240, 368): (202, 328)}  # B -> R

         # Red        # Green     # Yellow    # Blue
WINNER = [[240, 284], [284, 240], [330, 284], [284, 330]]

# Blit Tokens

def show_token(x, y):
    screen.fill((255, 255, 255))
    screen.blit(board, (0, 0))

    for i in SAFE[4:]:
        screen.blit(star, i)

    for i in range(len(position)):
        for j in position[i]:
            screen.blit(color[i], j)

    screen.blit(DICE[number-1], (605, 270))

    if position[x][y] in WINNER:
        winnerSound.play()


    screen.blit(color[currentPlayer], (620, 28))
    screen.blit(currentPlayerText, (600, 10))
    screen.blit(line, (592, 59))

    for i in range(len(winnerRank)):
        rank = FONT.render(f'{i+1}.', True, (0, 0, 0))
        screen.blit(rank, (600, 85 + (40*i)))
        screen.blit(color[winnerRank[i]], (620, 75 + (40*i)))

    pygame.display.update()
    time.sleep(0.5)

# Bliting in while loop

def blit_all():

    for i in SAFE[4:]:
        screen.blit(star, i)

    for i in range(len(position)):
        for j in position[i]:
            screen.blit(color[i], j)

    screen.blit(DICE[number-1], (605, 270))

    screen.blit(color[currentPlayer], (620, 28))
    screen.blit(currentPlayerText, (600, 10))
    screen.blit(line, (592, 59))

    for i in range(len(winnerRank)):
        rank = FONT.render(f'{i+1}.', True, (0, 0, 0))
        screen.blit(rank, (600, 85 + (40*i)))
        screen.blit(color[winnerRank[i]], (620, 75 + (40*i)))

# check if the token move to enter the final path 

def to_win(x, y):
    #  Red
    if (position[x][y][1] == 284 and position[x][y][0] <= 202 and x == 0) \
            and (position[x][y][0] + 38*number > WINNER[x][0]):
        return False

    #  Yellow
    elif (position[x][y][1] == 284 and 368 < position[x][y][0] and x == 2) \
            and (position[x][y][0] - 38*number < WINNER[x][0]):
        return False
    #  Green
    elif (position[x][y][0] == 284 and position[x][y][1] <= 202 and x == 1) \
            and (position[x][y][1] + 38*number > WINNER[x][1]):
        return False
    #  Blue
    elif (position[x][y][0] == 284 and position[x][y][1] >= 368 and x == 3) \
            and (position[x][y][1] - 38*number < WINNER[x][1]):
        return False
    return True

# Moving the token

def move_token(x, y):
    global currentPlayer, diceRolled

    # Taking Token out of HOME
    if tuple(position[x][y]) in HOME[currentPlayer] and number == 6:
        position[x][y] = list(SAFE[currentPlayer])
        tokenSound.play()
        diceRolled = False

    # Moving token which is not in HOME
    elif tuple(position[x][y]) not in HOME[currentPlayer]:
        tokenSound.play()
        diceRolled = False
        if not number == 6:
            turn_queue.rotate(-1)
            currentPlayer = turn_queue[0]


        # Way to WINNER position

        #  R
        if (position[x][y][1] == 284 and position[x][y][0] <= 202 and x == 0) \
                and (position[x][y][0] + 38*number <= WINNER[x][0]):
            for i in range(number):
                position[x][y][0] += 38
                show_token(x, y)

        #  Y
        elif (position[x][y][1] == 284 and 368 < position[x][y][0] and x == 2) \
                and (position[x][y][0] - 38*number >= WINNER[x][0]):
            for i in range(number):
                position[x][y][0] -= 38
                show_token(x,y)

        #  G
        elif (position[x][y][0] == 284 and position[x][y][1] <= 202 and x == 1) \
                and (position[x][y][1] + 38*number <= WINNER[x][1]):
            for i in range(number):
                position[x][y][1] += 38
                show_token(x,y)
        #  B
        elif (position[x][y][0] == 284 and position[x][y][1] >= 368 and x == 3) \
                and (position[x][y][1] - 38*number >= WINNER[x][1]):
            for i in range(number):
                position[x][y][1] -= 38
                show_token(x,y)

        # Other Paths
        else:
            for _ in range(number):

            
                if (position[x][y][1] == 240 and position[x][y][0] < 202) \
                        or (position[x][y][1] == 240 and 368 <= position[x][y][0] < 558):
                    position[x][y][0] += 38
                
                elif (position[x][y][0] == 12 and position[x][y][1] > 240):
                    position[x][y][1] -= 44

               
                elif (position[x][y][1] == 328 and 12 < position[x][y][0] <= 202) \
                        or (position[x][y][1] == 328 and 368 < position[x][y][0]):
                    position[x][y][0] -= 38
               
                elif (position[x][y][0] == 558 and position[x][y][1] < 328):
                    position[x][y][1] += 44

              
                elif (position[x][y][0] == 240 and 12 < position[x][y][1] <= 202) \
                        or (position[x][y][0] == 240 and 368 < position[x][y][1]):
                    position[x][y][1] -= 38
              
                elif (position[x][y][1] == 12 and 240 <= position[x][y][0] < 328):
                    position[x][y][0] += 44

              
                elif (position[x][y][0] == 328 and position[x][y][1] < 202) \
                        or (position[x][y][0] == 328 and 368 <= position[x][y][1] < 558):
                    position[x][y][1] += 38
                
                elif (position[x][y][1] == 558 and position[x][y][0] > 240):
                    position[x][y][0] -= 44
                
                else:
                    for i in jump:
                        if position[x][y] == list(i):
                            position[x][y] = list(jump[i])
                            break

                show_token(x, y)

        # Killing 
        if tuple(position[x][y]) not in SAFE:
            for i in range(len(position)):
                for j in range(len(position[i])):
                    if position[i][j] == position[x][y] and i != x:
                        position[i][j] = list(HOME[i][j])
                        killSound.play()
                        turn_queue.rotate(3)
                        currentPlayer = turn_queue[0]

# Checking Win
def check_winner():
    global currentPlayer
    if currentPlayer not in winnerRank:
        for i in position[currentPlayer]:
            if i not in WINNER:
                return
        winnerRank.append(currentPlayer)

        # Remove winner from turn queue and update currentPlayer
        turn_queue.remove(currentPlayer)
        if turn_queue:
            currentPlayer = turn_queue[0]
    else:
        turn_queue.rotate(-1)
        currentPlayer = turn_queue[0]


# Main LOOP
running = True
while(running):
    screen.fill((255, 255, 255))
    screen.blit(board, (0, 0)) # Bliting Board

    check_winner()
    
    for event in pygame.event.get():

        # Event QUIT
        if event.type == pygame.QUIT:
            running = False

        # When MOUSEBUTTON is clicked
        if event.type == pygame.MOUSEBUTTONUP:
            coordinate = pygame.mouse.get_pos()

            # Rolling Dice
            if not diceRolled and (605 <= coordinate[0] <= 669) and (270 <= coordinate[1] <= 334):
                number =random.randint(1,6)
                diceSound.play()
                flag = True
                for i in range(len(position[currentPlayer])):
                    if tuple(position[currentPlayer][i]) not in HOME[currentPlayer] and to_win(currentPlayer, i):
                        flag = False
                if (flag and number == 6) or not flag:
                    diceRolled = True

                else:
                    turn_queue.rotate(-1)
                    currentPlayer = turn_queue[0]

            # Moving Player
            elif diceRolled:
                for j in range(len(position[currentPlayer])):
                    if position[currentPlayer][j][0] <= coordinate[0] <= position[currentPlayer][j][0]+31 \
                            and position[currentPlayer][j][1] <= coordinate[1] <= position[currentPlayer][j][1]+31:
                        move_token(currentPlayer, j)
                        break

    blit_all()

    pygame.display.update()