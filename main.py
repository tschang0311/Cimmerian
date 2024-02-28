import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Cimmerian')

# Load sounds
step = pygame.mixer.Sound('sounds/step.wav')
Welcome = pygame.mixer.Sound('sounds/WelcomeToMarshiniMansion.wav')
IWouldNot = pygame.mixer.Sound('sounds/IWouldNot.wav')

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

# Function to move the player on the keyboard game field


def move_player(current_position, move):
    if move in keyboard_map[current_position]:
        current_position = move
        print(f"Moved to '{current_position}'.")
        step.play()
    else:
        print(
            f"Cannot move to '{move}' from '{current_position}'. Move is not valid.")
        IWouldNot.play()
        
    return current_position

# Function to handle key tap, triggering a movement if valid

def shift_hold_action(key):
    try:
        char = chr(key)
        if char in keyboard_map:
            print(f"Shift + hold action completed with key: {chr(key)}")
    except ValueError:
        pass 
    

def shift_tap_action(key):
    # Convert pygame key name to a single character (if applicable)
    try:
        char = chr(key)
        if char in keyboard_map:
            print(f"Shift + tap action completed with key: {chr(key)}")
    except ValueError:
        pass  # Key pressed does not correspond to a character


def on_key_tap(key, current_position):
    # Convert pygame key name to a single character (if applicable)
    try:
        char = chr(key)
        if char in keyboard_map:
            print(f"Tapped {char}")
    except ValueError:
        pass  # Key pressed does not correspond to a character

# Function to handle key hold, triggering a movement if valid


def on_key_hold(key, current_position):
    # Convert pygame key name to a single character (if applicable)
    try:
        char = chr(key)
        if char in keyboard_map:
            new_position = move_player(current_position, char)
            return new_position
    except ValueError:
        pass  # Key pressed does not correspond to a character
    return current_position


# Dictionary to track key holds and taps
key_press_times = {}
current_position = 'g'  # Starting position of the player on the keyboard

# Main game loop
running = True
clock = pygame.time.Clock()
Welcome.play()
while running:
    shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key not in key_press_times:
                key_press_times[event.key] = pygame.time.get_ticks()
        elif event.type == pygame.KEYUP:
            duration = pygame.time.get_ticks() - key_press_times.pop(event.key, pygame.time.get_ticks())
            if duration <= 200:  # Threshold for a tap
                if shift_pressed:
                    shift_tap_action(event.key)
                else:
                    on_key_tap(event.key, current_position)
            else:  # Threshold for a hold
                if shift_pressed:
                    shift_hold_action(event.key)
                else:
                    current_position = on_key_hold(event.key, current_position)

    clock.tick(60)

pygame.quit()
sys.exit()