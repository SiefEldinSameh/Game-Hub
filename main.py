import tkinter as tk
import os
from collections import deque
from utils import selection_sort, sort_by_length, search_game

game_list = ["Connect4", "Chess", "Snake & Ladder", "Ludo"]

recent_queue = deque(maxlen=10)  # Recently Played Queue

def launch_game(game):
    if game == "Connect4":
        os.system("python connect4.py")
    elif game == "Chess":
        os.system("python chess.py")
    elif game == "Snake & Ladder":
        os.system("python snake_ladder.py")
    elif game == "Ludo":
        os.system("python ludo.py")
    else:
        result_label.config(text="Game not found!")
        return
    
    if game in recent_queue:
        recent_queue.remove(game)
    recent_queue.append(game)
    update_recent_list()

def search_and_launch():
    query = search_entry.get()
    result = search_game(game_list, query)
    if result:
        launch_game(result)
    else:
        result_label.config(text="Game not found!")

def sort_az():
    global game_list
    game_list = selection_sort(game_list.copy(), reverse=False)
    update_game_list(game_list)

def sort_za():
    global game_list
    game_list = selection_sort(game_list.copy(), reverse=True)
    update_game_list(game_list)

def sort_by_name_length():
    global game_list
    game_list = sort_by_length(game_list.copy())
    update_game_list(game_list)

def sort_by_recent():
    recent_sorted_list = list(recent_queue) + [game for game in game_list if game not in recent_queue]
    update_game_list(recent_sorted_list)

def update_game_list(display_list):
    game_listbox.delete(0, tk.END)
    for game in display_list:
        game_listbox.insert(tk.END, game)

def update_recent_list():
    recent_listbox.delete(0, tk.END)
    for game in list(recent_queue):
        recent_listbox.insert(tk.END, game)

def on_game_select(event):
    selected = game_listbox.curselection()
    if selected:
        game = game_listbox.get(selected[0])
        launch_game(game)

# ---------------- GUI Setup --------------------
root = tk.Tk()
root.title("🎮 Dark Game Launcher")
root.geometry("450x650")
root.config(bg="#222831")  # Dark background

title = tk.Label(root, text="🎮 Game Launcher", font=("Arial", 18, "bold"), bg="#222831", fg="#00FFF5")
title.pack(pady=10)

# Game List
game_listbox = tk.Listbox(root, height=6, width=25, font=("Arial", 14), bg="#393E46", fg="#EEEEEE", selectbackground="#00FFF5")
game_listbox.pack(pady=5)
update_game_list(game_list)

game_listbox.bind('<<ListboxSelect>>', on_game_select)

# Search Section
tk.Label(root, text="🔍 Search Game:", font=("Arial", 12), bg="#222831", fg="#EEEEEE").pack()
search_entry = tk.Entry(root, width=25, bg="#393E46", fg="#EEEEEE", insertbackground='white')
search_entry.pack(pady=5)
tk.Button(root, text="Search & Play", command=search_and_launch, bg="#00ADB5", fg="white").pack(pady=5)

result_label = tk.Label(root, text="", fg="red", bg="#222831")
result_label.pack()

# Sort Buttons
tk.Label(root, text="🔃 Sort Options:", font=("Arial", 12), bg="#222831", fg="#EEEEEE").pack(pady=5)
tk.Button(root, text="Sort A-Z", command=sort_az, bg="#00ADB5", fg="white").pack(pady=2)
tk.Button(root, text="Sort Z-A", command=sort_za, bg="#00ADB5", fg="white").pack(pady=2)
tk.Button(root, text="Sort by Name Length", command=sort_by_name_length, bg="#00ADB5", fg="white").pack(pady=2)
tk.Button(root, text="Sort by Recently Used", command=sort_by_recent, bg="#00ADB5", fg="white").pack(pady=2)

# Recently Played
tk.Label(root, text="🕒 Recently Played:", font=("Arial", 12), bg="#222831", fg="#EEEEEE").pack(pady=5)
recent_listbox = tk.Listbox(root, height=4, width=25, font=("Arial", 12), bg="#393E46", fg="#EEEEEE", selectbackground="#00FFF5")
recent_listbox.pack(pady=5)

root.mainloop()
