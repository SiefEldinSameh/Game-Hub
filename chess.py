import pygame as py 
from collections import deque

py.init() 

width ,height = py.display.Info().current_w,py.display.Info().current_h

is_fullscreen = False
screen = py.display.set_mode((width*0.6,height*0.85))
undo_queue = deque()

py.display.set_caption("CHESS")
icon = py.image.load("assets//images//icon.png")
py.display.set_icon(icon)
timer = py.time.Clock()
fps = 60
font = py.font.Font("freesansbold.ttf",30)
small_font = py.font.Font("freesansbold.ttf",15)
big_font = py.font.Font("freesansbold.ttf",45)
size = 0
moves = []
steps = 0


white_pieces = ["rook","knight","bishop","king","queen","bishop","knight","rook",
                "pawn","pawn","pawn","pawn", "pawn","pawn", "pawn",  "pawn"  ]

white_locations = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
                  (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1) ]


black_pieces = ["rook","knight","bishop","king","queen","bishop","knight","rook",
                "pawn","pawn","pawn","pawn", "pawn","pawn", "pawn",  "pawn"  ]


black_locations =[(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),
                  (0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6) ]
piece_list = ["pawn", 'queen', 'king', 'knight', 'rook', 'bishop']

captured_pieces_white = []
captured_pieces_black = []

# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []
winner = "" 
game_over = False 






def draw_board1():
    width,height = screen.get_size()
    global size
    side_margin = width *0.3
    buttom_margin = height *0.1
    max_width = width-side_margin
    max_height = height - buttom_margin
    size = min(max_width//8,max_height//8)
    for row in range(8):
        for column in range(8):
                if (column+row) % 2 == 0:
                    py.draw.rect(screen, (101, 67, 33), (column*size, row*size, size,size))
                else:
                     py.draw.rect(screen, (240, 217, 181), (column*size,row *size,size,size))
    for i in range(8):   
        py.draw.rect(screen,"black",(0,i*size,8*size,size),1)
        py.draw.rect(screen,"black",(i*size,0,size,8*size),1)

    py.draw.rect(screen,"gold",(0,8*size,width,height-8*size),4)
    py.draw.rect(screen,"gold",(8*size,0,width-8*size,8*size),4)
    status_text = ["White: Select a Piece To Move!" , "White: Select a Distination !"
                   ,"Black: Select a Piece To Move!" , "Black: Select a Distination !"]
    screen.blit(big_font.render(status_text[turn_step],True,"black"),(10,8*size+10))
    screen.blit(font.render("SURRENDER",True,"black"),(8.75*size,8.25*size))
    for i in range(8):
         screen.blit(small_font.render(f"{i+1}",True,"black"),(8*size-0.15*size,(i)*size+0.1*size))
         screen.blit(small_font.render(f"{chr(ord('a')+i)}",True,"black"),((i)*size+0.08*size,8*size-0.2*size))
    for i,j in enumerate(moves):
         screen.blit(font.render(f"{j}",True,"black"),((i) *size,8*size+55))
         


def draw_pieces():
    black_queen = py.image.load('assets/images/black queen.png')
    black_queen = py.transform.scale(black_queen, (0.8*size, 0.8*size))
    black_king = py.image.load('assets/images/black king.png')
    black_king = py.transform.scale(black_king, (0.8*size, 0.8*size))
    black_rook = py.image.load('assets/images/black rook.png')
    black_rook = py.transform.scale(black_rook, (0.8*size, 0.8*size))
    black_bishop = py.image.load('assets/images/black bishop.png')
    black_bishop = py.transform.scale(black_bishop, (0.8*size, 0.8*size))
    black_knight = py.image.load('assets/images/black knight.png')
    black_knight = py.transform.scale(black_knight, (0.8*size, 0.8*size))
    black_pawn = py.image.load('assets/images/black pawn.png')
    black_pawn = py.transform.scale(black_pawn, (0.65*size, 0.65*size))
    white_queen = py.image.load('assets/images/white queen.png')
    white_queen = py.transform.scale(white_queen, (0.8*size, 0.8*size))
    white_king = py.image.load('assets/images/white king.png')
    white_king = py.transform.scale(white_king, (0.8*size, 0.8*size))
    white_rook = py.image.load('assets/images/white rook.png')
    white_rook = py.transform.scale(white_rook, (0.8*size, 0.8*size))
    white_bishop = py.image.load('assets/images/white bishop.png')
    white_bishop = py.transform.scale(white_bishop, (0.8*size, 0.8*size))
    white_knight = py.image.load('assets/images/white knight.png')
    white_knight = py.transform.scale(white_knight, (0.8*size, 0.8*size))
    white_pawn = py.image.load('assets/images/white pawn.png')
    white_pawn = py.transform.scale(white_pawn, (0.65*size, 0.65*size))
    white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]

    black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
   

    for i in range(len(white_pieces)):
          index = piece_list.index(white_pieces[i])
          if white_pieces[i] == "pawn":
               screen.blit(white_pawn,(white_locations[i][0]*size+15,white_locations[i][1]*size+22))
          else:
               screen.blit(white_images[index],(white_locations[i][0]*size+10,white_locations[i][1]*size+10))

          if turn_step <2 :
               if selection == i :
                    py.draw.rect(screen,"red",(white_locations[i][0]*size,white_locations[i][1]*size,size,size),2)
               

    for i in range(len(black_pieces)):
          index = piece_list.index(black_pieces[i])
          if black_pieces[i] == "pawn":
               screen.blit(black_pawn,(black_locations[i][0]*size+15,black_locations[i][1]*size+22))
          else:
               screen.blit(black_images[index],(black_locations[i][0]*size+10,black_locations[i][1]*size+10))
          if turn_step >= 2 :
             if selection == i :
                 py.draw.rect(screen,"blue",(black_locations[i][0]*size,black_locations[i][1]*size,size,size),2)

def check_options(pieces,loctions,turn):
     moves_list = []
     all_moves_list = []
     for i in range(len(pieces)):
          loction = loctions[i]
          piece = pieces[i]
          if piece == "pawn":
               moves_list = check_pawn(loction,turn)
          elif piece == "bishop" :
               moves_list = check_bishop(loction,turn)
          elif piece == "queen" :
               moves_list = check_queen(loction,turn)
          elif piece == "king" :
               moves_list = check_king(loction,turn)
          elif piece == "knight" :
                moves_list = check_knight(loction,turn)  
          elif piece == "rook" :
               moves_list = check_rook(loction,turn) 
          all_moves_list.append(moves_list)
     return all_moves_list
               
def check_pawn(position,color):
     x = position[0]
     y = position[1]
     move_list = []
     if color =="white":
        if  (x,y+1) not in white_locations and (x,y+1) not in black_locations and y+1 <8:
            move_list.append((x,y+1))
        if (x,y+2) not in white_locations and (x,y+2) not in black_locations and y ==1:
            move_list.append((x,y+2))
        if (x+1,y+1) in black_locations:
            move_list.append((x+1,y+1))
        if (x-1,y+1) in black_locations:
            move_list.append((x-1,y+1))

     else :
          if  (x,y-1) not in white_locations and (x,y-1) not in black_locations and y > 0:
            move_list.append((x,y-1))
          if (x,y-2) not in white_locations and (x,y-2) not in black_locations and y ==6:
            move_list.append((x,y-2))
          if (x-1,y-1) in white_locations:
            move_list.append((x-1,y-1))
          if (x+1,y-1) in white_locations:
            move_list.append((x+1,y-1))

     return move_list
          
def check_valid_moves():
     if turn_step <2:
          options_list = white_options[selection]
     else:
          options_list = black_options[selection]

     return options_list 

def draw_valid_moves(moves):
     if turn_step<2:
          color = "red"
     else:
          color = "blue"
     for i in range(len(moves)):
          py.draw.circle(screen,color,(moves[i][0]*size+size/2,moves[i][1]*size+size/2),5)

def check_rook(position,color):
     move_list = []
     if color == "white":
          friend = white_locations
          enemy=black_locations
     else:
          friend = black_locations
          enemy = white_locations

     for i in range(4):
          chain =1
          path = True
          if i ==0 :
               x=0
               y=1
          elif i ==1:
               x=0
               y=-1
          elif i==2:
               x=-1
               y=0
          elif i ==3:
               x=1
               y=0
          while path:
            if (position[0] +(chain * x),position[1] +(chain*y)) not in friend and 0<= position[0] +(chain*x) <=7 and 0<= position[1] + (chain*y) <=7:
                 move_list.append((position[0]+(chain*x),position[1]+chain*y))
                 if (position[0] +(chain * x),position[1] +(chain*y)) in enemy:
                      path = False
                 chain +=1
            else:
                 path = False
     return move_list 
          
def check_knight(position,color ):
     move_list = []
     if color == "white":
          friend = white_locations
          enemy=black_locations
     else:
          friend = black_locations
          enemy = white_locations
     targets = [(1,2),(1,-2),(2,1),(2,-1),(-1,-2),(-1,2),(-2,1),(-2,-1)]
     for i in range(8):
          target = (position[0]+targets[i][0],position[1]+targets[i][1])
          if target not in friend and 0<= target[0] <=7 and 0<= target[1] <=7:
               move_list.append(target)
     return move_list

def check_bishop(position,color):
     move_list = []
     if color == "white":
          friend = white_locations
          enemy=black_locations
     else:
          friend = black_locations
          enemy = white_locations
     for i in range(4):
          chain =1
          path = True
          if i ==0 :
               x=1
               y=-1
          elif i ==1:
               x=1
               y=1
          elif i==2:
               x=-1
               y=-1
          elif i ==3:
               x=-1
               y=1
          while path:
            if (position[0] +(chain * x),position[1] +(chain*y)) not in friend and 0<= position[0] +(chain*x) <=7 and 0<= position[1] + (chain*y) <=7:
                 move_list.append((position[0]+(chain*x),position[1]+chain*y))
                 if (position[0] +(chain * x),position[1] +(chain*y)) in enemy:
                      path = False
                 chain +=1
            else:
                 path = False
     return move_list 

def check_queen(position,color):
     return check_bishop(position,color) +check_rook(position,color)

def check_king(position,color):
     move_list = []
     if color == "white":
          friend = white_locations
          enemy=black_locations
     else:
          friend = black_locations
          enemy = white_locations
     targets = [(1,1),(1,-1),(0,1),(0,-1),(-1,0),(1,0),(-1,1),(-1,-1)]
     for i in range(8):
          target = (position[0]+targets[i][0],position[1]+targets[i][1])
          if target not in friend and 0<= target[0] <=7 and 0<= target[1] <=7:
               move_list.append(target)
     return move_list

def draw_captured_pieces():
    black_queen = py.image.load('assets/images/black queen.png')
    black_queen_small = py.transform.scale(black_queen, (0.45*size, 0.45*size))
    black_king = py.image.load('assets/images/black king.png')
    black_king_small = py.transform.scale(black_king, (0.45*size, 0.45*size))
    black_rook = py.image.load('assets/images/black rook.png')
    black_rook_small = py.transform.scale(black_rook, (0.45*size, 0.45*size))
    black_bishop = py.image.load('assets/images/black bishop.png')
    black_bishop_small = py.transform.scale(black_bishop, (0.45*size, 0.45*size))
    black_knight = py.image.load('assets/images/black knight.png')
    black_knight_small = py.transform.scale(black_knight, (0.45*size, 0.45*size))
    black_pawn = py.image.load('assets/images/black pawn.png')
    black_pawn_small = py.transform.scale(black_pawn, (0.45*size, 0.45*size))
    white_queen = py.image.load('assets/images/white queen.png')
    white_queen_small = py.transform.scale(white_queen, (0.45*size, 0.45*size))
    white_king = py.image.load('assets/images/white king.png')
    white_king_small = py.transform.scale(white_king, (0.45*size, 0.45*size))
    white_rook = py.image.load('assets/images/white rook.png')
    white_rook_small = py.transform.scale(white_rook, (0.45*size, 0.45*size))
    white_bishop = py.image.load('assets/images/white bishop.png')
    white_bishop_small = py.transform.scale(white_bishop, (0.45*size, 0.45*size))
    white_knight = py.image.load('assets/images/white knight.png')
    white_knight_small = py.transform.scale(white_knight, (0.45*size, 0.45*size))
    white_pawn = py.image.load('assets/images/white pawn.png')
    white_pawn_small = py.transform.scale(white_pawn, (0.45*size, 0.45*size))
    small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                        white_rook_small, white_bishop_small]
    small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                        black_rook_small, black_bishop_small]
    for i in range(len(captured_pieces_black)):
          captured_piece = captured_pieces_black[i]
          index = piece_list.index(captured_piece)
          screen.blit(small_white_images[index],(8*size,10+i*size*0.5))
    for i in range(len(captured_pieces_white)):
          captured_piece = captured_pieces_white[i]
          index = piece_list.index(captured_piece)
          screen.blit(small_black_images[index],((8+1)*size,10+i*size*0.5))
                     
def draw_checked():
     if turn_step <2 :
          if "king" in white_pieces:
               king_index = white_pieces.index("king")
               king_location = white_locations[king_index]
               for i in range(len(black_options)):
                    if king_location in black_options[i]:
                         if counter <3:
                              py.draw.rect(screen,"dark red",(king_location[0]*size,king_location[1]*size,size,size),5)
     else:
          if "king" in black_pieces:
               king_index = black_pieces.index("king")
               king_location = black_locations[king_index]
               for i in range(len(white_locations)):
                    if king_location in white_options[i]:
                         if counter <3:
                              py.draw.rect(screen,"dark blue",(king_location[0]*size,king_location[1]*size,size,size),5)

def draw_game_over(player):
     if game_over:
          py.draw.rect(screen,"black",(4*size,4*size,5*size,2*size))
          screen.blit(big_font.render(f"{player} has won !",True,"white"),(4*size,4*size))
          screen.blit(big_font.render("press R to restart",True,"white"),(4*size,5*size))

def restart():
     global white_locations,white_options,white_pieces,black_locations,black_options,black_pieces,captured_pieces_black,captured_pieces_white,turn_step,selection,valid_moves,winner,game_over
     white_pieces = ["rook","knight","bishop","king","queen","bishop","knight","rook",
                "pawn","pawn","pawn","pawn", "pawn","pawn", "pawn",  "pawn"  ]

     white_locations = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
                    (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1) ]


     black_pieces = ["rook","knight","bishop","king","queen","bishop","knight","rook",
                    "pawn","pawn","pawn","pawn", "pawn","pawn", "pawn",  "pawn"  ]


     black_locations =[(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),
                    (0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6) ]

     captured_pieces_white = []
     captured_pieces_black = []

     # 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
     turn_step = 0
     selection = 100
     valid_moves = []
     winner = "" 
     game_over = False 
     black_options = check_options(black_pieces,black_locations,"black")
     white_options = check_options(white_pieces,white_locations,"white")

def undo(queue):
    global white_locations, black_locations, captured_pieces_black, captured_pieces_white
    global white_pieces, black_pieces, turn_step, selection, valid_moves
    global black_options, white_options
    if not queue:
        return
    data = queue.pop()
    
    white_locations = data["wl"].copy()  
    black_locations = data["bl"].copy()
    captured_pieces_black = data["bc"].copy()
    captured_pieces_white = data["wc"].copy()
    white_pieces = data["wp"].copy()
    black_pieces = data["bp"].copy()
    turn_step = data["ts"]
    
    selection = 100
    valid_moves = []
    
    black_options = check_options(black_pieces, black_locations, "black")
    white_options = check_options(white_pieces, white_locations, "white")
    

def save_current(queue, ts):
    data = {
        "wp": white_pieces.copy(),
        "bp": black_pieces.copy(),
        "wl": white_locations.copy(),
        "bl": black_locations.copy(),
        "wc": captured_pieces_white.copy(),
        "bc": captured_pieces_black.copy(),
        "ts": ts
    }
    queue.append(data)
    if len(queue) > 10:
        queue.popleft()


def main():
    global black_options, white_options, run, counter, is_fullscreen, screen
    global turn_step, selection, valid_moves, game_over, winner,steps
    
    black_options = check_options(black_pieces,black_locations,"black")
    white_options = check_options(white_pieces,white_locations,"white")
    run = True
    counter = 0
    
    while run:
        timer.tick(fps)
        screen.fill("dark grey")
        draw_board1()
        draw_pieces()
        draw_captured_pieces()
        draw_checked()
        draw_game_over(winner)
        
        if selection !=100:
             valid_moves = check_valid_moves()
             draw_valid_moves(valid_moves)
        if counter <5:
             counter +=1
        else:
             counter =0

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
            elif event.type == py.KEYDOWN:
                if event.key ==py.K_F11 :
                     is_fullscreen = not is_fullscreen
                     if is_fullscreen:
                          screen = py.display.set_mode((0,0),py.FULLSCREEN)
                     else:
                          screen = py.display.set_mode((width*0.6,height*0.85))
                elif event.key == py.K_r:
                     restart()
                elif event.key == py.K_u:
                     undo(undo_queue)
            elif event.type == py.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                 x_coor = int(event.pos[0]//size)
                 y_coor = int(event.pos[1]//size)
                 click_coor = (x_coor,y_coor)
                 if turn_step < 2 :
                      if click_coor in [(9,8),(10,8)]:
                           game_over = True
                           winner = "BLACK"
                      if click_coor in white_locations:
                           selection = white_locations.index(click_coor)
                           if turn_step == 0 :
                                turn_step = 1
                                
                      if click_coor in valid_moves and selection != 100 :
                           save_current(undo_queue,0)
                           moves.append((chr(click_coor[0]+ord("a")),click_coor[1]+1))
                           steps+=1
                           print((chr(click_coor[0]+ord("a")),click_coor[1]+1))
                           white_locations[selection] = click_coor
                           if click_coor in black_locations:
                                black_piece = black_locations.index(click_coor)
                                captured_pieces_white.append(black_pieces[black_piece])
                                if black_pieces[black_piece] == "king":
                                      game_over = True
                                      winner = "WHITE"
                                black_pieces.pop(black_piece)
                                black_locations.pop(black_piece)
                           black_options = check_options(black_pieces,black_locations,"black")
                           white_options = check_options(white_pieces,white_locations,"white")
                           turn_step = 2
                           selection =100
                           valid_moves = []
                 if turn_step >= 2 :
                      if click_coor in [(9,8),(10,8)]:
                           game_over = True
                           winner = "WHITE"
                      if click_coor in black_locations:
                           selection = black_locations.index(click_coor)
                           if turn_step == 2 :
                                turn_step = 3
                      if click_coor in valid_moves and selection != 100 :
                           save_current(undo_queue,2)
                           moves.append((chr(click_coor[0]+ord("a")),click_coor[1]+1))
                           steps+=1
                           black_locations[selection] = click_coor
                           if click_coor in white_locations:
                                white_piece = white_locations.index(click_coor)
                                captured_pieces_black.append(white_pieces[white_piece])
                                if white_pieces[white_piece] == "king":
                                      game_over = True
                                      winner = "BLACK"
                                white_pieces.pop(white_piece)
                                white_locations.pop(white_piece)
                           black_options = check_options(black_pieces,black_locations,"black")
                           white_options = check_options(white_pieces,white_locations,"white")
                           turn_step = 0
                           selection =100
                           valid_moves = []

        py.display.flip()



if __name__ == "__main__":
    main()