import pygame as pg
import random
import os
from pygame import mixer


from collections import deque

pg.init()

screen = pg.display.set_mode((563,640))

WIDTH, HEIGHT = 563, 563
ROWS, COLS = 10, 10
SQUARE_SIZE = WIDTH // COLS

playersTurn = deque()
playersTurn.append("player1")
playersTurn.append("player2")


diceSound = mixer.Sound("assets\snake-ladder-assets\dice.wav")


# Set frame folder and prefix
FRAME_FOLDER = "assets\snake-ladder-assets\ezgif-split"
FRAME_PREFIX = "frame_apngframe"
d = "dice"
f = "assets\snake-ladder-assets\dice"
font = pg.font.Font("assets\snake-ladder-assets\FreeSansBold.ttf" ,32)
fontBig = pg.font.Font("assets\snake-ladder-assets\FreeSansBold.ttf" ,55)



diceFrames = []
for i in range(1, 51):  # 1 to 150
    filename = f"{FRAME_PREFIX}{i:03}.png"  # e.g., frame_apngframe001.png
    path = os.path.join(FRAME_FOLDER, filename)
    try:
        image = pg.image.load(path).convert_alpha()
        diceFrames.append(image)
    except FileNotFoundError:
        print(f"Missing frame: {path}")

diceValue = []
for i in range(0, 6):  # 1 to 150
    filename = f"{d}{i+1}.png"  # e.g., frame_apngframe001.png
    path = os.path.join(f, filename)
    try:
        image = pg.image.load(path).convert_alpha()
        small_image = pg.transform.scale(image, (100, 100))  # e.g., (50, 50)

        diceValue.append(small_image)
    except FileNotFoundError:
        print(f"Missing frame: {path}")
    
jumps = {
    # 🐍 Snakes
    99: 80,
    95: 75,
    92: 88,
    89: 68,
    76: 58,
    62: 19,
    49: 11,
    46: 25,
    16: 6,

    # 🪜 Ladders
    2: 38,
    7: 14,
    8: 31,
    15: 26,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    78: 98,
    87: 94
}


def getPosition(square):
    if square < 1 or square > 100:
        raise ValueError("Square must be between 1 and 100")

    row = (square - 1) // 10         # 0 at bottom, 9 at top
    col = (square - 1) % 10

    if row % 2 == 1:
        col = 9 - col  # Zigzag: reverse direction on odd rows

    # Convert to pixel coordinates
    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
    y = (9 - row) * SQUARE_SIZE + SQUARE_SIZE // 2  # y from top

    return (x, y-9)


pg.display.set_caption("Snake and Ladder")
icon = pg.image.load("assets\snake-ladder-assets\sl.png")
pg.display.set_icon(icon)

bgIMG= pg.image.load("assets\snake-ladder-assets\snakesandladdersboard.jpg")


font = pg.font.Font("assets\snake-ladder-assets\FreeSansBold.ttf" ,15)

player1img = pg.image.load("assets\snake-ladder-assets\pawn.png")
player1pos = getPosition(1)
player1Square = 1


player2img = pg.image.load("assets\snake-ladder-assets\pawn2.png")
player2pos = getPosition(1)
player2Square = 1


def displayPlayers():
    screen.blit(player1img , player1pos )
    screen.blit(player2img , player2pos )


def diceVal():

    return random.randint(1,6)

def showDice():
    diceSound.play()
    for frame in diceFrames:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        screen.blit(frame, (200, 200))  # position of dice
        pg.display.update()
        pg.time.delay(40)  # delay between frames
    diceSound.stop()






def show_end_screen(winner):
    font_small = pg.font.SysFont("Arial", 30)
    font_big = pg.font.SysFont("Arial", 50, bold=True)

    # Replay button setup
    replay_button = pg.Rect(180, 260, 200, 60)

    
    # Replay button setup
    main_button = pg.Rect(180, 380, 200, 60)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(event.pos):
                    return True  # Replay requested
                
                if main_button.collidepoint(event.pos):
                    return False  # main requested

        # Step 1: Draw background
        screen.blit(bgIMG, (0, 0))

        # Step 2: Draw semi-transparent overlay
        overlay = pg.Surface((465, 350), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # RGBA for transparent grey
        screen.blit(overlay, (50, 125))  # Centered overlay box

        # Step 3: Draw winner text
        win_text = font_big.render(f"{winner} Wins!", True, (255, 255, 0))
        screen.blit(win_text, (160, 180))

        # Step 4: Draw replay button
        pg.draw.rect(screen, (70, 130, 180), replay_button)
        text = font_small.render("Play Again", True, (255, 255, 255))
        screen.blit(text, (replay_button.x + 35, replay_button.y + 15))


        
        # Step 5: Draw main button
        pg.draw.rect(screen, (70, 130, 180), main_button)
        text = font_small.render("Main Menu", True, (255, 255, 255))
        screen.blit(text, (main_button.x + 35, main_button.y + 15))

        pg.display.update()


def showDiceVal(val):
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    screen.blit(diceValue[val-1], (230, 230))  # position of dice
    pg.display.update()
    pg.time.delay(800)  # delay between frames

def show_details(player, diceVal):
    det = font.render(player + "Turn with "+str(diceVal) , True , (255,255,255))
    screen.blit(det , (20 , 600))

def movePlayer(player,val):
    if player == "player1":
        global player1Square
        oldSquare = player1Square
        player1Square = oldSquare + val
        global player1pos
        if player1Square <= 100:
            player1pos =  getPosition(player1Square)

        return player1Square
    
        
    
    elif player == "player2":
        global player2Square
        oldSquare = player2Square
        player2Square = oldSquare + val
        global player2pos 
        if player2Square <= 100:
            player2pos = getPosition(player2Square)

        return player2Square

def jumping(player,newSquare):
    if player == "player1":
        global player1Square
        player1Square = newSquare
        global player1pos
        player1pos =  getPosition(player1Square)

        return player1Square
    
        
    
    elif player == "player2":
        global player2Square
        player2Square = newSquare 
        global player2pos 
        player2pos = getPosition(player2Square)

        return player2Square
    
def rematch():
    global player1pos, player1Square
    global player2pos, player2Square
    global playersTurn

    player1pos = getPosition(1)
    player1Square = 1

    player2pos = getPosition(1)
    player2Square = 1

    playersTurn.clear()  # Empty the queue
    playersTurn.append("player1")
    playersTurn.append("player2")






running = True
played = False
turn = playersTurn[0]

while running:

    screen.fill((0,0,0))
    screen.blit(bgIMG, (0,0))




    

    for e in pg.event.get():
        if e.type == pg.QUIT:
            running  = False 
        if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
            turn = playersTurn.popleft()

            showDice()
            value = diceVal()
            showDiceVal(value)
            squareCheck = movePlayer(turn , value)
            if squareCheck in jumps:
                squareCheck = jumps[squareCheck]
                jumping(turn,squareCheck)

            print(turn)
            print(value)
            played = True
            dicelastvalue = value
            playersTurn.append(turn)
            
            if squareCheck >= 100:
                replay = show_end_screen(turn)
                if replay:
                    rematch()
                    break
                else:
                    print("main menu")


        
    if played:
        det2 = font.render(playersTurn[1]  + " moved "+str(dicelastvalue) + " Square", True , (255,255,255))
        screen.blit(det2 , ( 15 , 580))
        det = font.render(  playersTurn[0] +" Turn....." , True , (255,255,255))
        screen.blit(det , ( 15 , 600))
    else:
        det3 = font.render(  "Player1 is Blue and Player2 is Red" , True , (255,255,255))
        screen.blit(det3 , ( 15 , 580))
        det = font.render(  playersTurn[0] +" Turn....." , True , (255,255,255))
        screen.blit(det , ( 15 , 600))
        




    screen.blit(player1img , player1pos )
    screen.blit(player2img , player2pos )



    pg.display.update()
