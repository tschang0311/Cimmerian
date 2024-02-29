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
DistantMonster = pygame.mixer.SoundType("sounds/Monsters/DistantMonster.wav")
NearbyMonster = pygame.mixer.SoundType("sounds/Monsters/NearbyMonster.wav")
AttackMonster = pygame.mixer.SoundType("sounds/Monsters/MonsterAttack.wav")
DoorTry = pygame.mixer.SoundType("Sounds/KeysAndDoors/DoorUnlockFail.wav")
DoorUnlockFail = pygame.mixer.SoundType(
    "sounds/KeysAndDoors/DoorUnlockFail.wav")
DoorUnlockSuccess = pygame.mixer.SoundType(
    "sounds/KeysAndDoors/DoorUnlockSuccess.wav")
KeyInspect = pygame.mixer.SoundType("sounds/KeysAndDoors/KeyInspect.wav")
KeyPickup = pygame.mixer.SoundType("sounds/KeysAndDoors/KeyPickup.wav")
Trapwire = pygame.mixer.SoundType("sounds/Traps/TrapTripwireNoVoice.wav")
TrapFall = pygame.mixer.SoundType("sounds/Traps/TrapCollisionWithVoice.wav")
wall = pygame.mixer.SoundType("sounds/Wall.wav")
ladderUp = pygame.mixer.SoundType("sounds/LadderUp.wav")
ladderDown = pygame.mixer.SoundType("sounds/LadderDown.wav")
flies = pygame.mixer.SoundType("sounds/Soundscape/SoundscapeFlies.wav")
rats = pygame.mixer.SoundType("sounds/Soundscape/SoundscapeRats.wav")


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
    [
        #Level 0 - No Monster
        {"position": None, "path":[None], "path_index": 0, "speed": 0, "move_counter": 0},
        ],
    [
        #Level 01 - No Monster
        {"position": None, "path":[None], "path_index": 0, "speed": 0, "move_counter": 0},
        ],
    [
        #Level 02 - No Monster
        {"position": None, "path":[None], "path_index": 0, "speed": 0, "move_counter": 0},
        ],
    [
        #Level 03 - Static Monster on G
        {"position": 'g', "path":['g'], "path_index": 0, "speed": 0, "move_counter": 0},
        ],
    [  
        # Level 1
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


def move_monsters(player_position):
    global current_level, monsters_data
    for monster in monsters_data[current_level]:
        # Check if it's time for this monster to move
        if monster['move_counter'] >= monster['speed']:
            check_monster_proximity(player_position)
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
            NearbyMonster.play()
            return  # Assuming only need to warn once per check

        # Check if the monster is 2 spaces away
        for adjacent in keyboard_map[player_position]:
            if monster['position'] in keyboard_map[adjacent]:
                DistantMonster.play()
                # print("Monster is 2 spaces away!")
                return  # Assuming only need to warn once per check
    # If no monster is 1 or 2 spaces away, do nothing


def check_collision(player_position):
    global current_level, monsters_data
    # Loop through all monsters on the current level
    for monster in monsters_data[current_level]:
        if player_position == monster['position']:
            AttackMonster.play()
            pygame.time.delay(11000)
            print("Caught by the monster! Game Over.")
            pygame.quit()
            sys.exit()
            break  # Exit the loop after finding a collision


# Play Maps with walls ('w') and traps ('t')
play_maps = [
    {   # Level 0
        'm': 'wall', 'o': 'wall', '0': 'wall',
        'k': 'door', 'f': 'key',
        'l': 'ladder_down',
        },
    {   # Level 01
        '2': 'wall', 'w': 'wall', 'x': 'wall',
        's': 'door', '6': 'key',
        'y': 'trap', 'h': 'trap', 'n': 'trap',
        'a': 'ladder_down',
        },
    {   # Level 02
        'm': 'wall', 'o': 'wall', '0': 'wall',
        's': 'wall', 'w': 'trap', 'v': 'wall', 'g': 'wall', '6': 'wall',
        'u': 'wall', 'h': 'trap',
        'k': 'door', 'f': 'key',
        'l': 'ladder_down',
        },
    {   # Level 03
        '2': 'wall', 'w': 'wall', 'x': 'wall',
        's': 'door', 'h': 'key',
        'a': 'ladder_down',
        },
    {  # Level 1
        'f': 'wall', 'b': 'wall', 'p': 'wall', '3': 'wall',
        'e': 'trap', 'h': 'trap',
        'w': 'key',
        'd': 'door',
        'p': 'ladder_down',  # Ladder going down to the next level
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
        'z': 'ladder_up',
        'g': 'goal'  # Assuming a way back up
        # Continue defining level 4...
    }
]


def is_wall(position):
    global current_level
    return play_maps[current_level].get(position, '') == 'wall'

def is_trap(position):
    global current_level
    return play_maps[current_level].get(position, '') == 'trap'

def is_key(position):
    global current_level
    return play_maps[current_level].get(position, '') == 'key'

def is_door(position):
    global current_level
    return play_maps[current_level].get(position, '') == 'door'


def handle_win_condition():
    print("You win!")
    # Play a victory sound
    # victorySound.play()  # Assume you have a victory sound loaded similarly to other sounds
    # Display a win message or screen
    # You might want to implement a simple pygame screen display here
    pygame.quit()
    sys.exit()

# Function to move the player on the keyboard game field


def move_player(current_position, move, shift_pressed=False):
    global player_keys, current_level
    play_map = play_maps[current_level]  # Use the current level's play map
    if shift_pressed:
        print(f"Shift + Move attempted to '{move}'.")
        # what is this
    else:
        # Check if the move is to a key location
        if play_map.get(move) == 'key':
            print("You've picked up a key!")
            KeyPickup.play()
            player_keys += 1  # Increment the key counter
            del play_map[move]  # Remove the key from the map
            current_position = move
        elif play_map.get(move) == 'ladder_down' and move in keyboard_map[current_position]:
            print("Descending to the next level...")
            ladderDown.play()
            current_level += 1  # Move down a level
            current_position = move
            if current_level == 2:
                rats.play()
            elif current_level == 3:
                flies.play()
        elif play_map.get(move) == 'ladder_up':
            ladderUp.play()
            print("Climbing back up to the previous level...")
            current_level -= 1  # Move up a level
            current_position = move
        elif play_map.get(move) == 'door':
            DoorUnlockFail.play()
            print("The door is locked. You need a key and to 'Shift+hold' to open it.")
            return current_position  # Prevent moving through the door without Shift+hold
        elif play_map.get(move) in ['wall']:
            if play_map.get(move) == 'wall':
                wall.play()
                print(f"Wall at '{move}'. Move not allowed.")
                return current_position
        elif move in keyboard_map[current_position]:
            current_position = move
            print(f"Moved to '{current_position}'.")
            if current_level == 0:
                normal_step.play()
            elif current_level == 1:
                normal_step.play()
            elif current_level == 2:
                puddle_step.play()
            elif current_level == 3:
                mud_step.play()
            else:
                mud_step.play()
            if is_trap(current_position):
                TrapFall.play()
                pygame.time.delay(9000)
                print("Stepped on a trap! Game Over.")
                pygame.quit()
                sys.exit()
            if play_map.get(move) == 'goal':
                print("Congratulations! You've reached the goal and won the game!")
                # Here, you could either exit the game or trigger a win sequence
                handle_win_condition()
                running = False  # This stops the game loop
                return current_position  # Optionally return early
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
            if is_door(char):
                DoorTry.play()
            if is_wall(char):
                wall.play()
                print(f"Sounds like there's a wall at '{char}'!")
            if is_key(char):
                KeyInspect.play()
                print(f"Sounds like there's a key at '{char}'!")
            if is_trap(char):
                Trapwire.play()
                print(f"Trap inspected at '{char}'. Dangerous!")
            else:
                # need sound here
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
                    DoorUnlockSuccess.play()
                    print(
                        "You've opened the door with one of your keys. The door remains open.")
                    player_keys -= 1
                    play_map[char] = 'open_door'  # Mark the door as open
                else:
                    DoorUnlockFail.play()
                    print("The door is locked. You need a key to open it.")
            else:
                wall.play()
                print("There's no door in the direction you're trying to open.")
    except ValueError:
        pass  # Key pressed does not correspond to a character


def shift_tap_action(key):
    # Convert pygame key name to a single character (if applicable)
    try:
        char = chr(key)
        if char in keyboard_map:
            # need sound here
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
                    # check_monster_proximity(current_position)
    if monster_move_counter >= monster_move_threshold:
        move_monsters(current_position)
        # check_monster_proximity(current_position)
        monster_move_counter = 0
    else:
        monster_move_counter += 1

    # Check for collision with the monster after player and monster have moved
    check_collision(current_position)
    clock.tick(60)

pygame.quit()
sys.exit()
