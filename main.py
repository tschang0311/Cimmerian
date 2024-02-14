import pygame
import sys

# CONFIG section (can be moved to a .config file for full game)
START_POS = "A"

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Sound on Key Press')

# Load the sounds
sound = pygame.mixer.Sound('sounds/step.wav')  # Replace 'sound.wav' with your sound file

# Walkable Map 1-0 and qwerty
keyboard_map = {
    '1': ['2', 'q'],
    '2': ['1', '3', 'q', 'w'],
    '3': ['2', '4', 'w', 'e'],
    '4': ['3', '5', 'e', 'r'],
    '5': ['4', '6', 'r', 't'],
    '6': ['5', '7', 't', 'y'],
    '7': ['6', '8', 'y', 'u'],
    '8': ['7', '9', 'u', 'i'],
    '9': ['8', '0', 'i', 'o'],
    '0': ['9', 'o', 'p'],

    'q': ['1', '2', 'w', 'a'],
    'w': ['q', '2', '3', 'e', 's', 'a'],
    'e': ['w', '3', '4', 'r', 'd', 's'],
    'r': ['e', '4', '5', 't', 'f', 'd'],
    't': ['r', '5', '6', 'y', 'g', 'f'],
    'y': ['t', '6', '7', 'u', 'h', 'g'],
    'u': ['y', '7', '8', 'i', 'j', 'h'],
    'i': ['u', '8', '9', 'o', 'k', 'j'],
    'o': ['i', '9', '0', 'p', 'l', 'k'],
    'p': ['o', '0', 'l'],

    'a': ['q', 'w', 's', 'z'],
    's': ['a', 'w', 'e', 'd', 'x', 'z'],
    'd': ['s', 'e', 'r', 'f', 'c', 'x'],
    'f': ['d', 'r', 't', 'g', 'v', 'c'],
    'g': ['f', 't', 'y', 'h', 'b', 'v'],
    'h': ['g', 'y', 'u', 'j', 'n', 'b'],
    'j': ['h', 'u', 'i', 'k', 'm', 'n'],
    'k': ['j', 'i', 'o', 'l', 'm'],
    'l': ['k', 'o', 'p'],

    'z': ['a', 's', 'x'],
    'x': ['z', 's', 'd', 'c'],
    'c': ['x', 'd', 'f', 'v'],
    'v': ['c', 'f', 'g', 'b'],
    'b': ['v', 'g', 'h', 'n'],
    'n': ['b', 'h', 'j', 'm'],
    'm': ['n', 'j', 'k']
}

# Nice little helper guys

# Assuming keyboard_map is defined as before

def move_player(current_position, move):
    if move in keyboard_map[current_position]:
        # Move is valid, update the position
        current_position = move
        print(f"Moved to '{current_position}'.")
    else:
        # Move is invalid, position remains unchanged
        print(f"Cannot move to '{move}' from '{current_position}'. Move is not valid.")
    
    return current_position






# Main game loop
running = True
current_position = START_POS
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Play sound on spacebar press
            if event.key == pygame.K_SPACE:
                sound.play()
            character = event.unicode
            if character:
                current_position = move_player(current_position.lower(), character)
                print(current_position)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
