import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Sound on Key Press')

# Load the sound
sound = pygame.mixer.Sound('sounds/step.wav')  # Replace 'sound.wav' with your sound file

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Play sound on spacebar press
            if event.key == pygame.K_SPACE:
                sound.play()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
