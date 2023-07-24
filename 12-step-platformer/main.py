# pygame 

# 1 - Import packages
import pygame
import sys
import random
import pygwidgets

# from pygame.locals import *
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import Explosion

# 2 - Define Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
FRAMES_PER_SECOND = 30

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the WINDOW is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # self.surf = pygame.Surface((75, 25)) # user a picture instead
        self.surf = pygame.image.load("images/jet.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            print("up")
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the WINDOW
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the WINDOW is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        # self.surf = pygame.Surface((20, 10))
        self.surf = pygame.image.load("images/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(WINDOW_WIDTH + 20, WINDOW_WIDTH + 100),
                random.randint(0, WINDOW_HEIGHT),
            )
        )
        self.speed = random.randint(5, 30)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the WINDOW
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the cloud object by extending pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("images/cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(WINDOW_WIDTH + 20, WINDOW_WIDTH + 100),
                random.randint(0, WINDOW_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

#3 Initialize the world
# Setup for sounds. Defaults are good.
pygame.mixer.init()

pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# 4 - Load Assets: image(s), sound(s), etc.
# Load and play our background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("sounds/Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# 5 - Initialize variables
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load all our sound files
# Sound sources: Jon Fincher
move_up_sound = pygame.mixer.Sound("sounds/Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("sounds/Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("sounds/Collision.ogg")

# Set the base volume for all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

#variable to control the loop 
running = True

# 6 - Loop forever
while running:

    # 7 - Check for and handle events
    for event in pygame.event.get():
        #Clicked the close button? Quit pygame and end the program
        if event.type == pygame.QUIT:
            running = False
        
        # Check for keydown event
        elif event.type == KEYDOWN:
            # Was it the escape key? Exit the main loop.
            if event.key == K_ESCAPE:
                running = False
        
        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite group
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Add a new cloud/meteor
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to the sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)
    
    
    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # 8 - Do any "per frame actions"
    
    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Update enemy positions
    enemies.update()
    clouds.update()


    # 9 - Clear the window
    # window.fill(BLACK)
    window.fill((135, 206, 250))  # fill the window with sky-blue

    # 10 - Draw all elements
    window.blit(player.surf, player.rect)

    # Draw all sprites
    for entity in all_sprites:
        window.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player and stop the loop
        player.kill()
        running = False

    # 11 - Update the winodw
    # pygame.display.update()
    pygame.display.flip()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)