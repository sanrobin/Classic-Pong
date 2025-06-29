# Pong Game

A classic 2D Pong game built with Python and Pygame featuring retro black-and-white styling with multiple difficulty levels and sound effects.

## Features

- **Two Paddles**: Player-controlled paddle and AI opponent
- **Bouncing Ball**: Physics-based ball movement with paddle collision detection
- **Scoring System**: Real-time score tracking displayed at the top
- **Keyboard Controls**: Use arrow keys or WASD for paddle movement
- **Three Difficulty Levels**: Easy (Green), Medium (Yellow), and Hard (Red)
- **Sound Effects**: Paddle hits, wall bounces, and scoring sounds
- **Smart AI Opponent**: Difficulty-adjusted AI with varying reaction times and speeds
- **Retro Styling**: Clean black-and-white design with center court line
- **Object-Oriented Design**: Well-structured code with separate classes for game components

## Requirements

- Python 3.6+
- Pygame 2.0.0+

## Installation

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the game:
   ```bash
   python pong_game.py
   ```

## Controls

- **1, 2, 3**: Select difficulty (Easy, Medium, Hard) in menu
- **UP Arrow** or **W**: Move paddle up
- **DOWN Arrow** or **S**: Move paddle down
- **ESC**: Return to menu or quit game

## Difficulty Levels

- **Easy (Green)**: Slower AI, reduced ball speed, more forgiving gameplay
- **Medium (Yellow)**: Balanced gameplay with moderate AI and ball speed
- **Hard (Red)**: Fast AI, increased ball speed, challenging gameplay

## Game Rules

- First player to score wins the point
- Ball bounces off top and bottom walls
- Ball bounces off paddles with slight angle variation based on hit position
- Game continues indefinitely - compete for the highest score!

## Sound Effects

- **Paddle Hit**: Sound when ball hits either paddle
- **Wall Bounce**: Sound when ball bounces off top/bottom walls
- **Score**: Sound when either player scores

## Code Structure

- `Paddle`: Handles paddle movement and rendering
- `Ball`: Manages ball physics and collision detection
- `AIPlayer`: Controls the computer opponent with difficulty scaling
- `ScoreBoard`: Manages and displays game scores
- `SoundManager`: Handles all sound effects
- `PongGame`: Main game loop and coordination

Enjoy playing this classic arcade game!
