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
normal_step = pygame.mixer.SoundType("sounds/Footsteps/NormalFootsteps.wav")
mud_step = pygame.mixer.SoundType("sounds/Footsteps/MuddyFootsteps.wav")
puddle_step = pygame.mixer.SoundType("sounds/Footsteps/PuddleFootsteps.wav")


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

monsters_data = [
    [  # Level 1
        {"position": "m", "path": ["m", "n", "b", "v", "c", "x", "c", "v",
                                   "b", "n"], "path_index": 0, "speed": 5, "move_counter": 0},
        # More monsters for level 1
    ],
    [  # Level 2
        {"position": "g", "path": ["g", "f", "e", "d", "c"],
            "path_index": 0, "speed": 3, "move_counter": 0},
        # More monsters for level 2
    ],
    [  # Level 3
        {"position": "g", "path": ["g", "f", "e", "d", "c"],
            "path_index": 0, "speed": 3, "move_counter": 0},
        # More monsters for level 3
    ],
    [  # Level 4
        {"position": "g", "path": ["g", "f", "e", "d", "c"],
            "path_index": 0, "speed": 3, "move_counter": 0},
        # More monsters for level 4
    ]
]

player_keys = 0  # Initialize the counter for keys in the player's inventory
current_level = 0  # Start on level 1


def move_monsters():
    global current_level, monsters_data
    for monster in monsters_data[current_level]:
        # Check if it's time for this monster to move
        if monster['move_counter'] >= monster['speed']:
            # Move the monster along its path
            monster['path_index'] = (
                monster['path_index'] + 1) % len(monster['path'])
            monster['position'] = monster['path'][monster['path_index']]
            # Reset the move counter for this monster
            monster['move_counter'] = 0
        else:
            # Increment the move counter
            monster['move_counter'] += 1
    # print(f"Monster moves to '{monster_position}'.")


def check_monster_proximity(player_position):
    global current_level, monsters_data
    for monster in monsters_data[current_level]:
        # Directly adjacent check (1 space away)
        if monster['position'] in keyboard_map[player_position]:
            print("Monster is 1 space away!")
            return  # Assuming only need to warn once per check

        # Check if the monster is 2 spaces away
        for adjacent in keyboard_map[player_position]:
            if monster['position'] in keyboard_map[adjacent]:
                # print("Monster is 2 spaces away!")
                return  # Assuming only need to warn once per check
    # If no monster is 1 or 2 spaces away, do nothing


def check_collision(player_position):
    global current_level, monsters_data
    # Loop through all monsters on the current level
    for monster in monsters_data[current_level]:
        if player_position == monster['position']:
            print("Caught by the monster! Game Over.")
            pygame.quit()
            sys.exit()
            break  # Exit the loop after finding a collision


# Play Maps with walls ('w') and traps ('t')
play_maps = [
    {  # Level 1
        'f': 'wall', 'b': 'wall', 'p': 'wall', '3': 'wall',
        'e': 'trap', 'h': 'trap',
        'w': 'key',
        'd': 'door',
        'p': 'ladder_down'  # Ladder going down to the next level
    },
    {  # Level 2
        # Define the layout for level 2 with its own set of walls, traps, etc.
        'f': 'wall',  # Example entries
        'n': 'trap',
        'm': 'key',
        'o': 'door',
        'p': 'ladder_up',
        'q': 'ladder_down',  # Assuming a way back up
        # Continue defining level 2...
    },
    {  # Level 3
        # Define the layout for level 3 with its own set of walls, traps, etc.
        'f': 'wall',  # Example entries
        'n': 'trap',
        'm': 'key',
        'o': 'door',
        'q': 'ladder_up',
        'z': 'ladder_down',  # Assuming a way back up
        # Continue defining level 3...
    },
    {  # Level 4
        # Define the layout for level 4 with its own set of walls, traps, etc.
        'f': 'wall',  # Example entries
        'n': 'trap',
        'm': 'key',
        'o': 'door',
        'z': 'ladder_up',  # Assuming a way back up
        # Continue defining level 4...
    }
]


def is_wall(position):
    global current_level
    return play_maps[current_level].get(position, '') == 'wall'


def is_trap(position):
    global current_level
    return play_maps[current_level].get(position, '') == 'trap'

# Function to move the player on the keyboard game field


def move_player(current_position, move, shift_pressed=False):
    global player_keys, current_level
    play_map = play_maps[current_level]  # Use the current level's play map
    if shift_pressed:
        print(f"Shift + Move attempted to '{move}'.")
    else:
        # Check if the move is to a key location
        if play_map.get(move) == 'key':
            print("You've picked up a key!")
            player_keys += 1  # Increment the key counter
            del play_map[move]  # Remove the key from the map
            current_position = move
        elif play_map.get(move) == 'ladder_down':
            print("Descending to the next level...")
            current_level += 1  # Move down a level
            current_position = move
        elif play_map.get(move) == 'ladder_up':
            print("Climbing back up to the previous level...")
            current_level -= 1  # Move up a level
            current_position = move
        elif play_map.get(move) == 'door':
            print("The door is locked. You need a key and to 'Shift+hold' to open it.")
            return current_position  # Prevent moving through the door without Shift+hold
        elif play_map.get(move) in ['wall']:
            if play_map.get(move) == 'wall':
                print(f"Wall at '{move}'. Move not allowed.")
                return current_position
        elif move in keyboard_map[current_position]:
            current_position = move
            print(f"Moved to '{current_position}'.")
            puddle_step.play()
            if is_trap(current_position):
                print("Stepped on a trap! Game Over.")
                pygame.quit()
                sys.exit()
        else:
            print(
                f"Cannot move to '{move}' from '{current_position}'. Move is not valid.")
            IWouldNot.play()

    return current_position


# Function to inspect traps


def inspect(key):
    try:
        char = chr(key)
        if char in keyboard_map:
            if is_trap(char):
                print(f"Trap inspected at '{char}'. Dangerous!")
            else:
                print(f"No trap at '{char}'. Safe to proceed.")
    except ValueError:
        pass


def shift_hold_action(key):
    global player_keys, play_maps, current_level
    try:
        char = chr(key)
        # Assume doors are interacted with adjacent tiles; define logic to determine the target tile
        # For simplicity, this example assumes current_position is directly usable to check for a door

        if char in keyboard_map:  # Assuming 'char' is a movement key
            play_map = play_maps[current_level]

            if char in play_map and play_map[char] == 'door':
                if player_keys > 0:
                    print(
                        "You've opened the door with one of your keys. The door remains open.")
                    player_keys -= 1
                    play_map[char] = 'open_door'  # Mark the door as open
                else:
                    print("The door is locked. You need a key to open it.")
            else:
                print("There's no door in the direction you're trying to open.")
    except ValueError:
        pass  # Key pressed does not correspond to a character


def shift_tap_action(key):
    # Convert pygame key name to a single character (if applicable)
    try:
        char = chr(key)
        if char in keyboard_map:
            print(f"Shift + tap action completed with key: {chr(key)}")
    except ValueError:
        pass  # Key pressed does not correspond to a character


def on_key_tap(key, shift_pressed=False):
    if shift_pressed:
        print(f"Shift + Tapped {chr(key)}")
    else:
        inspect(key)  # Use tap to inspect for traps

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
current_position = 'a'  # Starting position of the player on the keyboard

# Monster stuff
monster_move_counter = 0
monster_move_threshold = 50  # Adjust as needed for speed

# Main game loop
running = True
clock = pygame.time.Clock()
# Welcome.play()
while running:
    shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key not in key_press_times:
                key_press_times[event.key] = pygame.time.get_ticks()
        elif event.type == pygame.KEYUP:
            duration = pygame.time.get_ticks() - key_press_times.pop(event.key,
                                                                     pygame.time.get_ticks())
            if duration <= 200:  # Threshold for a tap
                if shift_pressed:
                    shift_tap_action(event.key)
                else:
                    on_key_tap(event.key)
            else:  # Threshold for a hold
                if shift_pressed:
                    shift_hold_action(event.key)
                else:
                    current_position = on_key_hold(event.key, current_position)
                    check_monster_proximity(current_position)
    if monster_move_counter >= monster_move_threshold:
        move_monsters()
        check_monster_proximity(current_position)
        monster_move_counter = 0
    else:
        monster_move_counter += 1

    # Check for collision with the monster after player and monster have moved
    check_collision(current_position)
    clock.tick(60)

pygame.quit()
sys.exit()
