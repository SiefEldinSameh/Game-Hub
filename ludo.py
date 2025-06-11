import pygame
from pygame import mixer
import random
import time
from collections import deque


# Initialize pygame
pygame.init()
pygame.display.set_caption("Ludo")
screen = pygame.display.set_mode((680, 600))

# Loading Images
try:
    board = pygame.image.load(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\Board_2.png")
    star = pygame.image.load(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\star.png")
    dice_images = [
        pygame.image.load(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\1.png"),
        pygame.image.load(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\2.png"),
        pygame.image.load(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\3.png"),
        pygame.image.load(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\4.png"),
        pygame.image.load(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\5.png"),
        pygame.image.load(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\6.png")
    ]
    colors = [
        pygame.image.load(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\red.png"),
        pygame.image.load(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\green.png"),
        pygame.image.load(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\yellow.png"),
        pygame.image.load(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\blue.png")
    ]
except Exception as e:
    print(f"Error loading images: {e}")
    # Create placeholder surfaces if images not found
    board = pygame.Surface((680, 600))
    board.fill((200, 200, 200))
    star = pygame.Surface((20, 20))
    star.fill((255, 255, 0))
    dice_images = [pygame.Surface((50, 50)) for _ in range(6)]
    for i, img in enumerate(dice_images):
        img.fill((255, 255, 255))
        text = pygame.font.SysFont(None, 30).render(str(i+1), True, (0, 0, 0))
        img.blit(text, (20, 15))
    colors = [pygame.Surface((30, 30)) for _ in range(4)]
    colors[0].fill((255, 0, 0))    # Red
    colors[1].fill((0, 255, 0))    # Green
    colors[2].fill((255, 255, 0))  # Yellow
    colors[3].fill((0, 0, 255))    # Blue

color_names = ["Red", "Green", "Yellow", "Blue"]
color_rgb = [(255, 50, 50), (50, 255, 50), (255, 255, 50), (50, 50, 255)]

# Loading Sounds
try:
    mixer.init()
    killSound = mixer.Sound(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\sounds\kill.mp3")
    tokenSound = mixer.Sound(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\sounds\token_movment.mp3")
    diceSound = mixer.Sound(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\sounds\Dice Roll.wav")
    winnerSound = mixer.Sound(r"C:\Users\hp\OneDrive\Desktop\LudoGame\Game-Hub\assets\ludo_assets\sounds\win.mp3")
except:
    # Dummy sound objects if audio fails
    class DummySound:
        def play(self): pass
    killSound = tokenSound = diceSound = winnerSound = DummySound()

# Enhanced Player Selection Screen
def player_selection():
    players = []
    num_players = 0
    input_text = ""
    current_name = ""
    available_colors = [0, 1, 2, 3]
    selected_color = None
    error_message = ""
    
    # Fonts
    title_font = pygame.font.Font('freesansbold.ttf', 48)
    subtitle_font = pygame.font.Font('freesansbold.ttf', 32)
    prompt_font = pygame.font.Font('freesansbold.ttf', 28)
    name_font = pygame.font.Font('freesansbold.ttf', 24)
    button_font = pygame.font.Font('freesansbold.ttf', 30)
    error_font = pygame.font.Font('freesansbold.ttf', 20)
    
    # Colors
    bg_color = (240, 240, 250)
    card_color = (255, 255, 255)
    shadow_color = (200, 200, 210)
    input_color = (245, 245, 245)
    button_color = (100, 200, 100)
    button_hover = (120, 220, 120)
    error_color = (200, 50, 50)
    
    # Input box rectangles
    num_input_rect = pygame.Rect(680//2 - 100, 220, 200, 50)
    name_input_rect = pygame.Rect(680//2 - 150, 300, 300, 50)
    start_button_rect = pygame.Rect(220, 450, 240, 60)
    
    active = True
    while active:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(bg_color)
        
        # Decorative header
        pygame.draw.rect(screen, (230, 230, 240), (0, 0, 680, 100))
        
        # Main card
        pygame.draw.rect(screen, shadow_color, (50, 120, 580, 400), border_radius=15)
        pygame.draw.rect(screen, card_color, (45, 115, 580, 400), border_radius=15)
        
        # Title with shadow
        title = title_font.render("LUDO GAME", True, (50, 50, 80))
        subtitle = subtitle_font.render("Player Setup", True, (100, 100, 130))
        screen.blit(title, (680//2 - title.get_width()//2 + 2, 32))
        screen.blit(title, (680//2 - title.get_width()//2, 30))
        screen.blit(subtitle, (680//2 - subtitle.get_width()//2, 80))
        
        if num_players == 0:
            # Number of players selection
            prompt = prompt_font.render("How many players? (2-4)", True, (80, 80, 100))
            screen.blit(prompt, (680//2 - prompt.get_width()//2, 170))
            
            # Input box
            pygame.draw.rect(screen, input_color, num_input_rect, border_radius=5)
            pygame.draw.rect(screen, (200, 200, 220), num_input_rect, 2, border_radius=5)
            num_text = prompt_font.render(input_text if input_text else " ", True, (50, 50, 80))
            screen.blit(num_text, (num_input_rect.x + 10, num_input_rect.y + 10))
            
            # Error message
            if error_message:
                error = error_font.render(error_message, True, error_color)
                screen.blit(error, (680//2 - error.get_width()//2, 280))
        else:
            # Show selected players
            prompt = prompt_font.render(f"Players: {len(players)}/{num_players}", True, (80, 80, 100))
            screen.blit(prompt, (680//2 - prompt.get_width()//2, 170))
            
            # Player cards
            for i, player in enumerate(players):
                pygame.draw.rect(screen, shadow_color, (100, 220 + i*70, 480, 60), border_radius=10)
                pygame.draw.rect(screen, card_color, (100, 220 + i*70, 480, 60), border_radius=10)
                
                # Color indicator
                pygame.draw.rect(screen, color_rgb[player['color']], (110, 230 + i*70, 40, 40), border_radius=5)
                
                # Player name
                name_text = name_font.render(player['name'], True, (60, 60, 80))
                screen.blit(name_text, (170, 240 + i*70))
                
                # Color name
                color_text = name_font.render(color_names[player['color']], True, color_rgb[player['color']])
                screen.blit(color_text, (480, 240 + i*70))
            
            # Current player input
            if len(players) < num_players:
                # Input card
                pygame.draw.rect(screen, shadow_color, (100, 220 + len(players)*70, 480, 60), border_radius=10)
                pygame.draw.rect(screen, card_color, (100, 220 + len(players)*70, 480, 60), border_radius=10)
                
                # Prompt
                input_prompt = name_font.render(f"Player {len(players)+1} name:", True, (100, 100, 120))
                screen.blit(input_prompt, (110, 240 + len(players)*70))
                
                # Name input
                name_input = name_font.render(current_name, True, (50, 50, 80))
                screen.blit(name_input, (250, 240 + len(players)*70))
                
                # Available colors
                color_prompt = name_font.render("Choose color:", True, (100, 100, 120))
                screen.blit(color_prompt, (340 - 200, 320 + num_players*50))
                
                for i, col in enumerate(available_colors):
                    color_rect = pygame.Rect(240 + i*70, 350 + num_players*50, 60, 60)
                    hover = color_rect.collidepoint(mouse_pos)
                    
                    pygame.draw.rect(screen, shadow_color, color_rect, border_radius=10)
                    pygame.draw.rect(screen, (255, 255, 255) if not hover else (230, 230, 255), color_rect, border_radius=10)
                    pygame.draw.rect(screen, color_rgb[col], (250 + i*70, 360 + num_players*50, 40, 40), border_radius=5)
        
        # Start game button when ready
        if len(players) == num_players and num_players > 0:
            hover = start_button_rect.collidepoint(mouse_pos)
            pygame.draw.rect(screen, button_hover if hover else button_color, start_button_rect, border_radius=15)
            pygame.draw.rect(screen, (60, 140, 60), start_button_rect, 3, border_radius=15)
            
            start_text = button_font.render("START GAME", True, (255, 255, 255))
            screen.blit(start_text, (start_button_rect.x + start_button_rect.width//2 - start_text.get_width()//2, 
                                   start_button_rect.y + start_button_rect.height//2 - start_text.get_height()//2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if start game button is clicked
                if len(players) == num_players and num_players > 0:
                    if start_button_rect.collidepoint(event.pos):
                        active = False
                
                # Check if color is selected for current player
                if len(players) < num_players and current_name.strip():
                    for i, col in enumerate(available_colors):
                        color_rect = pygame.Rect(240 + i*70, 350 + num_players*50, 60, 60)
                        if color_rect.collidepoint(event.pos):
                            selected_color = col
                            players.append({"name": current_name.strip(), "color": col})
                            available_colors.remove(col)
                            current_name = ""
                            selected_color = None
                            break
            
            if event.type == pygame.KEYDOWN:
                if num_players == 0:
                    if event.key == pygame.K_RETURN:
                        if input_text.isdigit() and 2 <= int(input_text) <= 4:
                            num_players = int(input_text)
                            error_message = ""
                        else:
                            error_message = "Please enter 2, 3, or 4"
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                        error_message = ""
                    elif event.unicode.isdigit() and len(input_text) < 1:
                        input_text += event.unicode
                        error_message = ""
                elif len(players) < num_players:
                    if event.key == pygame.K_RETURN and current_name.strip() and available_colors:
                        # Auto-select first available color if none selected
                        players.append({"name": current_name.strip(), "color": available_colors[0]})
                        available_colors.pop(0)
                        current_name = ""
                    elif event.key == pygame.K_BACKSPACE:
                        current_name = current_name[:-1]
                    elif event.unicode.isprintable() and len(current_name) < 12:
                        current_name += event.unicode
    
    return players

# Get player information
players = player_selection()
if not players:
    pygame.quit()
    exit()

# Initialize game variables based on player selection
number = 1
playerKilled = False
diceRolled = False
winnerRank = []

# Create turn queue based on player colors (order: Red, Green, Yellow, Blue)
turn_queue = deque()
for i in range(4):
    for player in players:
        if player['color'] == i:
            turn_queue.append(player['color'])
currentPlayer = turn_queue[0]

# Rendering Text
font = pygame.font.Font('freesansbold.ttf', 11)
FONT = pygame.font.Font('freesansbold.ttf', 16)
currentPlayerText = font.render('Current Player', True, (0, 0, 0))
line = font.render('------------------------------------', True, (0, 0, 0))

# Defining Important Coordinates
HOME = [[(110, 58), (61, 107), (152, 107), (110, 152)],  # Red
        [(466, 58), (418, 107), (509, 107), (466, 153)],  # Green
        [(466, 415), (418, 464), (509, 464), (466, 510)],  # Yellow
        [(110, 415), (61, 464), (152, 464), (110, 510)]]  # Blue

# Red      # Green    # Yellow    # Blue
SAFE = [(50, 240), (328, 50), (520, 328), (240, 520),
        (88, 328), (240, 88), (482, 240), (328, 482)]

position = [[[110, 58], [61, 107], [152, 107], [110, 152]],  # Red
            [[466, 58], [418, 107], [509, 107], [466, 153]],  # Green
            [[466, 415], [418, 464], [509, 464], [466, 510]],  # Yellow
            [[110, 415], [61, 464], [152, 464], [110, 510]]]  # Blue

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
            screen.blit(colors[i], j)

    screen.blit(dice_images[number-1], (605, 270))

    if position[x][y] in WINNER:
        winnerSound.play()

    # Show current player info with name
    player_name = next((p['name'] for p in players if p['color'] == currentPlayer), "")
    player_text = FONT.render(f"{player_name}'s turn", True, (0, 0, 0))
    
    screen.blit(colors[currentPlayer], (620, 28))
    screen.blit(player_text, (600 - player_text.get_width()//2, 10))
    screen.blit(line, (592, 59))

    for i in range(len(winnerRank)):
        player_name = next((p['name'] for p in players if p['color'] == winnerRank[i]), "")
        rank = FONT.render(f'{i+1}. {player_name}', True, (0, 0, 0))
        screen.blit(rank, (600, 85 + (40*i)))
        screen.blit(colors[winnerRank[i]], (570, 75 + (40*i)))

    pygame.display.update()
    time.sleep(0.5)

# Bliting in while loop
def blit_all():
    for i in SAFE[4:]:
        screen.blit(star, i)

    for i in range(len(position)):
        for j in position[i]:
            screen.blit(colors[i], j)

    screen.blit(dice_images[number-1], (605, 270))

    # Show current player info with name
    player_name = next((p['name'] for p in players if p['color'] == currentPlayer), "")
    player_text = FONT.render(f"{player_name}'s turn", True, (0, 0, 0))
    
    screen.blit(colors[currentPlayer], (620, 28))
    screen.blit(player_text, (600 - player_text.get_width()//2, 10))
    screen.blit(line, (592, 59))

    for i in range(len(winnerRank)):
        player_name = next((p['name'] for p in players if p['color'] == winnerRank[i]), "")
        rank = FONT.render(f'{i+1}. {player_name}', True, (0, 0, 0))
        screen.blit(rank, (600, 85 + (40*i)))
        screen.blit(colors[winnerRank[i]], (570, 75 + (40*i)))

# check if the token move to enter the final path 
def to_win(x, y):
    # Red
    if (position[x][y][1] == 284 and position[x][y][0] <= 202 and x == 0) \
            and (position[x][y][0] + 38*number > WINNER[x][0]):
        return False

    # Yellow
    elif (position[x][y][1] == 284 and 368 < position[x][y][0] and x == 2) \
            and (position[x][y][0] - 38*number < WINNER[x][0]):
        return False
    # Green
    elif (position[x][y][0] == 284 and position[x][y][1] <= 202 and x == 1) \
            and (position[x][y][1] + 38*number > WINNER[x][1]):
        return False
    # Blue
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

        # R
        if (position[x][y][1] == 284 and position[x][y][0] <= 202 and x == 0) \
                and (position[x][y][0] + 38*number <= WINNER[x][0]):
            for i in range(number):
                position[x][y][0] += 38
                show_token(x, y)

        # Y
        elif (position[x][y][1] == 284 and 368 < position[x][y][0] and x == 2) \
                and (position[x][y][0] - 38*number >= WINNER[x][0]):
            for i in range(number):
                position[x][y][0] -= 38
                show_token(x,y)

        # G
        elif (position[x][y][0] == 284 and position[x][y][1] <= 202 and x == 1) \
                and (position[x][y][1] + 38*number <= WINNER[x][1]):
            for i in range(number):
                position[x][y][1] += 38
                show_token(x,y)
        # B
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
while running:
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
                number = random.randint(1,6)
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

pygame.quit()