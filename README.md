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
- [Acknowledgments](#acknowledgments)

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
