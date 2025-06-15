# Multiplayer Turn-Based Game Engine

![Game Showcase](assets/showcase.gif)

A versatile game engine supporting three classic board games: **Snake & Ladder**, **Chess**, and **Ludo**, implemented with Python and Pygame.

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Games Overview](#games-overview)
  - [Snake & Ladder](#snake--ladder)
  - [Chess](#chess)
  - [Ludo](#ludo)
- [Data Structures Used](#data-structures-used)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Team Members](#team-members)
- [Submitted to](#submitted-to)

## Project Description
This project demonstrates advanced data structure implementation through three multiplayer turn-based games. Developed as part of our Data Structures course under the supervision of **Eng. Moutair**, it showcases:
- Queue-based turn management
- Complex move validation algorithms
- State preservation for undo/redo functionality
- Graphical user interface with Pygame

Key components include:
- Game state management
- Rule enforcement engines
- Interactive GUI
- Win condition detection

## Features
- **Common Framework** for all three games
- **Turn Management** using queues
- **Undo/Redo** functionality with stack
- **Interactive GUI** with Pygame
- **Special Game Rules** implemented (snakes/ladders, chess moves, ludo captures)
- **Multiplayer Support** (2-4 players depending on game)

## Games Overview

### Snake & Ladder
Classic dice-based race to the top with:
- Random dice rolls
- Snake and ladder jumps
- 2-player turn system

![Snake & Ladder](assets/snake_screenshot.png)

### Chess
Full chess implementation featuring:
- All piece movements
- Check/checkmate detection
- Piece capturing
- Undo functionality

![Chess](assets/chess_screenshot.png)

### Ludo
Traditional Ludo with:
- 2-4 player support
- Token movement logic
- Safe zones and star jumps
- Token capturing

![Ludo](assets/ludo_screenshot.png)

## Data Structures Used
| Data Structure       | Usage in Project                          |
|----------------------|------------------------------------------|
| Queue                | Player turn management                   |
| Stack                | Undo/redo functionality                  |
| 2D Arrays            | Board representations                   |
| Dictionaries         | Snake/ladder mappings, piece positions  |
| Graphs               | Chess move validation                   |
| Object-Oriented      | Game pieces and player management       |

## Installation
1. Clone the repository:
     ```bash
     git clone https://github.com/yourusername/multiplayer-game-engine.git
     ```
2. Install dependencies:
    ```bash
    pip install pygame numpy
    ```
3. Run the desired game:
    ```bash
    python snake_ladder.py
    python chess.py
    python ludo.py
    ```

## How to Play
- Snake & Ladder: Press spacebar to roll dice
- Chess: Click to select pieces and destinations
- Ludo: Click dice to roll, then click your token

## 👥 Team Members

| Member Name | Game Contribution | LinkedIn |
|-------------|------------------|----------|
| [Saif](#) | Chess Engine | [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat&logo=linkedin)](https://linkedin.com) |
| [Ziad](#) | Snake & Ladder GUI | [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/ibrahim-abdelqader-93b9b124b/) |
| [Ibrahim](#) | Snake & Ladder Engine | [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/ziad0nassif/) |
| [Mohamed](#) | Ludo UI/UX | [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/mohamed-elnefary-1246672b0/) |
| [Jana](#) | Ludo Game Logic | [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/jana-nour-1510bb324/) |

## Submitted to:
- Dr. Eman Marzban & Eng. Mutair 
All rights reserved © 2025 to Team 07 - Systems & Biomedical Engineering, Cairo University (Class 2028)
