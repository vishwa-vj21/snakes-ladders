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

# Set window size
window_width = 600
window_height = 750
root.geometry(f"{window_width}x{window_height}")

# Create a frame for centering
frame = tk.Frame(root)
frame.pack(pady=10)

# Set Game Board Canvas
canvas = tk.Canvas(frame, width=600, height=600, highlightthickness=0)
canvas.pack()

# Load board image
board_img = tk.PhotoImage(file="board.png")
canvas.create_image(300, 300, image=board_img)

# Load and Process Transparent Player Images
def load_transparent_image(path, size=(50, 50)):
    img = Image.open(path).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)

player1_img = load_transparent_image("player1.png")
player2_img = load_transparent_image("player2.png")

# Player Positions
players = {"Player 1": 1, "Player 2": 1}
player_turn = "Player 1"
rolling_dice = False

# Function to Get Board Coordinates
def get_coordinates(position):
    row = (position - 1) // 10
    col = (position - 1) % 10
    if row % 2 == 1:
        col = 9 - col
    x = col * 60 + 30
    y = 540 - row * 60 + 30
    return x, y

# Draw Player Tokens
x, y = get_coordinates(1)
player_icons = {
    "Player 1": canvas.create_image(x + 15, y + 15, anchor=tk.CENTER, image=player1_img),
    "Player 2": canvas.create_image(x - 15, y + 15, anchor=tk.CENTER, image=player2_img)
}

# Function to Move Players Step-by-Step
def move_step_by_step(player, target_pos):
    current_pos = players[player]
    
    if current_pos == target_pos:
        if target_pos in snakes:
            canvas.itemconfig(player_icons[player], state="hidden")
            root.after(500, lambda: move_snake(player, snakes[target_pos]))
            pygame.mixer.Sound.play(snake_sound)
        elif target_pos in ladders:
            pygame.mixer.Sound.play(ladder_sound)
            move_directly(player, ladders[target_pos])
        else:
            check_winner(player)
            switch_turn()
        return
    
    next_pos = current_pos + 1 if current_pos < target_pos else current_pos - 1
    x1, y1 = get_coordinates(current_pos)
    x2, y2 = get_coordinates(next_pos)

    dx, dy = x2 - x1, y2 - y1
    canvas.move(player_icons[player], dx, dy)
    pygame.mixer.Sound.play(step_sound)

    players[player] = next_pos
    root.after(200, move_step_by_step, player, target_pos)

# Function to Move Instantly for Ladders
def move_directly(player, target_pos):
    x1, y1 = get_coordinates(players[player])
    x2, y2 = get_coordinates(target_pos)
    dx, dy = x2 - x1, y2 - y1
    canvas.move(player_icons[player], dx, dy)
    players[player] = target_pos
    check_winner(player)
    switch_turn()

# Function to Move Player After Snake Bite
def move_snake(player, target_pos):
    canvas.itemconfig(player_icons[player], state="normal")
    x1, y1 = get_coordinates(players[player])
    x2, y2 = get_coordinates(target_pos)
    dx, dy = x2 - x1, y2 - y1
    canvas.move(player_icons[player], dx, dy)
    players[player] = target_pos
    switch_turn()

# Function to Check Winner
def check_winner(player):
    if players[player] == 100:
        pygame.mixer.music.stop()
        messagebox.showinfo("Game Over", f"{player} Wins!")
        root.quit()

# Function to Switch Turn
def switch_turn():
    global player_turn, rolling_dice
    player_turn = "Player 2" if player_turn == "Player 1" else "Player 1"
    dice_label.config(text=f"{player_turn}'s Turn 🎲")
    roll_button.config(state=tk.NORMAL)
    rolling_dice = False

# Function to Roll Dice
def roll_dice():
    global rolling_dice
    if rolling_dice:
        return
    
    rolling_dice = True
    roll_button.config(state=tk.DISABLED)
    pygame.mixer.Sound.play(dice_sound)
    
    dice_value = random.randint(1, 6)
    dice_label.config(text=f"{player_turn} rolled: {dice_value}")
    
    new_pos = players[player_turn] + dice_value
    if new_pos > 100:
        new_pos = players[player_turn]
    
    move_step_by_step(player_turn, new_pos)



# Create a frame below the board for dice display
dice_frame = tk.Frame(root)
dice_frame.pack(pady=20)

dice_label = tk.Label(dice_frame, text="Roll the Dice!", font=("Arial", 16, "bold"))
dice_label.pack()

roll_button = tk.Button(dice_frame, text="Roll Dice 🎲", font=("Arial", 14), command=roll_dice)
roll_button.pack()

root.mainloop()