# pygame template

# 1 - Import packages
import pygame
from pygame.locals import *
import sys
import SpriteSheet
# import Explosion

# 2 - Define constants
BLACK = (0, 0, 0)
LT_BLACK = (50, 50, 50)
WHITE = (255, 255, 255)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FRAMES_PER_SECOND = 30


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"images/exp{num}.png")
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        # update explosion animation
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) -1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        
        # if the animation is complete reset the animation index
        if self.index >= len(self.images) -1 and self.counter >= explosion_speed:
            self.kill()
            
def get_image(sheet, frame, width, height, scale, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)
    return image
    

# 3 - Initialize the world
pygame.mixer.init()
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Explosion Demo')
clock = pygame.time.Clock()

# 4 - Load assets: image(s), sound(s), etc.
explosion_group = pygame.sprite.Group()
explosion_sound = pygame.mixer.Sound("sounds/explosion.ogg")
explosion_sound.set_volume(1)
sprite_sheet_image = pygame.image.load("images/doux.png").convert_alpha()
sprite_sheet = SpriteSheet.SpriteSheet(sprite_sheet_image)

# 5 - Initialize variables
# Create animation list
animation_list = []
animation_steps = [4, 6, 3, 4]
action = 1
last_update = pygame.time.get_ticks()
animation_cooldown = 100
frame = 0
step_counter = 0

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 24, 24, 3, BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)


running = True
# 6 - Loop forever
while running:

    # 7 - Check for and handle events
    for event in pygame.event.get():
        # Clicked the close button? Quit pygame, end the program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            explosion = Explosion(pos[0], pos[1])
            explosion_group.add(explosion)
            explosion_sound.play()

        if event.type == pygame.KEYDOWN:
            if event.key == K_DOWN and action > 0:
                action -= 1
                frame = 0
            if event.key == K_UP and action < len(animation_list) -1:
                action += 1
                frame =0



    # 8 - Do any "per frame" actions
    explosion_group.update()
    
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0

    # 9 - Clear the window
    window.fill(LT_BLACK)

    # 10 - Draw all elements
    window.blit(animation_list[action][frame], (100,100))
    explosion_group.draw(window)

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)

