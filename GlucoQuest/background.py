import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Load images
background_normal = pygame.image.load('images/background.jpg')
cloud_image_normal = pygame.image.load('images/cloud.png')

# Resize images
background_normal = pygame.transform.scale(background_normal, (SCREEN_WIDTH, SCREEN_HEIGHT))
cloud_image_normal = pygame.transform.scale(cloud_image_normal, (150, 100))

# Cloud settings
clouds = [{'pos': [-150, random.randint(50, 150)], 'speed': random.uniform(0.2, 0.5), 'image': cloud_image_normal} for _ in range(3)]

def draw_background(screen):
    screen.blit(background_normal, (0, 0))

    # Move clouds
    for cloud in clouds:
        cloud['pos'][0] += cloud['speed']
        if cloud['pos'][0] > SCREEN_WIDTH:
            cloud['pos'][0] = -150
            cloud['pos'][1] = random.randint(50, 150)
        screen.blit(cloud['image'], cloud['pos'])
