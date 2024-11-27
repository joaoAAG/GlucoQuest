import pygame
import sys
from menu import main as menu_main
from background import draw_background  # Import the draw_background function

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 32
CHAR_WIDTH = 79
CHAR_HEIGHT_BOYS = 120
CHAR_HEIGHT_GIRLS = 113
CHAR_SPACING = 52

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Avatar Selection")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Load images
boys_image = pygame.image.load('images/boys.png')
girls_image = pygame.image.load('images/girls.png')
leave_icon = pygame.image.load('images/leave_icon.png')

# Resize icons
leave_icon = pygame.transform.scale(leave_icon, (50, 50))

# Leave icon position
leave_icon_pos = (SCREEN_WIDTH - 60, 10)

# Function to cut the sprite sheet into individual characters
def get_characters(image, rows, char_width, char_height, char_spacing):
    characters = []
    image_width, image_height = image.get_size()
    for row in range(rows):
        for col in range(image_width // (char_width + char_spacing)):
            x = col * (char_width + char_spacing)
            y = row * (char_height + char_spacing)
            if x + char_width <= image_width and y + char_height <= image_height:
                rect = pygame.Rect(x, y, char_width, char_height)
                character = image.subsurface(rect)
                characters.append(character)
            else:
                print(f"Skipping character at {x},{y} due to out-of-bounds")
    return characters

# Get characters from sprite sheets
boys_characters = get_characters(boys_image, 1, CHAR_WIDTH, CHAR_HEIGHT_BOYS, CHAR_SPACING)
girls_characters = get_characters(girls_image, 1, CHAR_WIDTH, CHAR_HEIGHT_GIRLS, CHAR_SPACING)

# Function to draw text
def draw_text(screen, text, position, font, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Draw the avatars
def draw_avatars(screen, boys, girls):
    draw_background(screen)  # Draw the background
    title = font.render("Select Your Avatar", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

    y_pos = 100
    for i, character in enumerate(boys):
        x_pos = 50 + i * (CHAR_WIDTH + 10)
        screen.blit(character, (x_pos, y_pos))

    y_pos = 300
    for i, character in enumerate(girls):
        x_pos = 50 + i * (CHAR_WIDTH + 10)
        screen.blit(character, (x_pos, y_pos))

    # Draw leave icon
    screen.blit(leave_icon, leave_icon_pos)

# Main function for avatar selection
def main_avatar(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check if leave icon is clicked
                if leave_icon_pos[0] <= mouse_pos[0] <= leave_icon_pos[0] + 50 and leave_icon_pos[1] <= mouse_pos[1] <= leave_icon_pos[1] + 50:
                    running = False
                    menu_main(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar)
                # Check if an avatar is clicked
                # Add your logic here for avatar selection

        draw_avatars(screen, boys_characters, girls_characters)
        pygame.display.flip()

if __name__ == "__main__":
    from main_controller import run_game, run_stickers, run_leaderboard, run_challenges, run_avatar
    main_avatar(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar)
