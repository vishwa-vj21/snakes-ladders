import tkinter as tk
from tkinter import messagebox
import random
import pygame
from PIL import Image, ImageTk  # For transparent player images

# Initialize pygame for sound
pygame.mixer.init()

# Load background music
pygame.mixer.music.load("background_music.wav")  # Ensure this file exists
pygame.mixer.music.set_volume(0.3)  # Adjust volume
pygame.mixer.music.play(-1)  # Loop forever

# Load sound effects
dice_sound = pygame.mixer.Sound("dice_roll.wav")
snake_sound = pygame.mixer.Sound("snake_bite.wav")
ladder_sound = pygame.mixer.Sound("ladder_climb.wav")
step_sound = pygame.mixer.Sound("step.wav")

# Define Snakes and Ladders
snakes = {39: 3, 46: 11, 52: 31, 73: 58, 80: 40, 87: 32, 93: 70, 96: 79, 98: 6}
ladders = {5: 18, 14: 29, 25: 47, 43: 62, 71: 91, 74: 95}

# Initialize Game Window
root = tk.Tk()
root.title("Snakes and Ladders")

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size
window_width = 600
window_height = 750  # Increased to fit dice area

# Calculate position to center the window
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set window position and background
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.configure(bg="black")

# Create a frame for centering
frame = tk.Frame(root, bg="black")
frame.pack(pady=10)  # Add some spacing

# Set Black Background for the Canvas (Game Board)
canvas = tk.Canvas(frame, width=600, height=600, bg="black", highlightthickness=0)
canvas.pack()

# Load board image
board_img = tk.PhotoImage(file="board.png")  # Ensure this file exists
canvas.create_image(300, 300, image=board_img)

# Load and Process Transparent Player Images
def load_transparent_image(path, size=(60, 60)):
    """Loads an image with transparency and resizes it."""
    img = Image.open(path).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

player1_img = load_transparent_image("player1.png")
player2_img = load_transparent_image("player2.png")

# Player Positions
players = {"Player 1": 1, "Player 2": 1}
player_turn = "Player 1"

# Draw Player Tokens (Images)
player_icons = {
    "Player 1": canvas.create_image(15, 540, anchor=tk.NW, image=player1_img),
    "Player 2": canvas.create_image(25, 540, anchor=tk.NW, image=player2_img)
}

# Function to Move Players Step-by-Step
def move_step_by_step(player, target_pos):
    """Moves the player one step at a time until reaching the target position."""
    current_pos = players[player]

    if current_pos == target_pos:
        # Check for Snakes or Ladders after finishing dice movement
        if target_pos in snakes:
            root.after(500, move_step_by_step, player, snakes[target_pos])  # Delay movement for realism
            pygame.mixer.Sound.play(snake_sound)
        elif target_pos in ladders:
            root.after(500, move_step_by_step, player, ladders[target_pos])
            pygame.mixer.Sound.play(ladder_sound)
        else:
            check_winner(player)
        return

    next_pos = current_pos + 1 if current_pos < target_pos else current_pos - 1
    x1, y1 = get_coordinates(current_pos)
    x2, y2 = get_coordinates(next_pos)

    dx, dy = x2 - x1, y2 - y1
    canvas.move(player_icons[player], dx, dy)
    pygame.mixer.Sound.play(step_sound)

    players[player] = next_pos
    root.after(200, move_step_by_step, player, target_pos)  # Continue movement step-by-step

# Function to Check Winner
def check_winner(player):
    if players[player] == 100:
        pygame.mixer.music.stop()  # Stop background music when game ends
        messagebox.showinfo("Game Over", f"{player} Wins!")
        root.quit()

# Function to Roll Dice
def roll_dice():
    global player_turn
    pygame.mixer.Sound.play(dice_sound)  # Play dice sound
    
    dice_value = random.randint(1, 6)  # Generate random dice roll
    
    # Update the dice display label
    dice_label.config(text=f"{player_turn} rolled: {dice_value}")
    
    new_pos = players[player_turn] + dice_value
    if new_pos > 100:
        new_pos = players[player_turn]  # Stay in the same place if roll exceeds 100

    move_step_by_step(player_turn, new_pos)  # Step-by-step movement

    # Switch Turn after movement completes
    def switch_turn():
        global player_turn
        player_turn = "Player 2" if player_turn == "Player 1" else "Player 1"

    root.after(1500, switch_turn)  # Delay switch for smooth gameplay

# Function to Get Board Coordinates with Correct Snakes & Ladders Layout
def get_coordinates(position):
    """Returns x, y coordinates for a given board position where:
       - Odd rows (1st, 3rd, 5th, ...) move left-to-right.
       - Even rows (2nd, 4th, 6th, ...) move right-to-left.
    """
    row = (position - 1) // 10  # Calculate the row index (0-based)
    col = (position - 1) % 10  # Default column index

    if row % 2 == 1:  # Even rows go right-to-left
        col = 9 - col

    x = col * 60 + 15
    y = 540 - row * 60
    return x, y

# Create a frame below the board for the dice display & button
dice_frame = tk.Frame(root, bg="black")
dice_frame.pack(pady=20)

# Dice label to show the rolled number
dice_label = tk.Label(dice_frame, text="Roll the Dice!", font=("Arial", 16, "bold"), fg="white", bg="black")
dice_label.pack()

# Roll Dice Button
roll_button = tk.Button(dice_frame, text="Roll Dice 🎲", font=("Arial", 14), command=roll_dice, bg="white")
roll_button.pack()

# Start Game
root.mainloop()
