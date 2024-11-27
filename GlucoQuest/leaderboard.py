import pygame
import sys
import random
from menu import main as menu_main
from background import draw_background

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 32
CHAR_SIZE = 32
SEPARATION = 8
ROWS = 8
COLUMNS = 10
SCROLL_SPEED = 20
TAB_HEIGHT = 50

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Leaderboard")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Load the sprite sheet
sprite_sheet = pygame.image.load('images/list_characters.png')
leave_icon = pygame.image.load('images/leave_icon.png')

# Resize icons
leave_icon = pygame.transform.scale(leave_icon, (50, 50))

# Leave icon position
leave_icon_pos = (SCREEN_WIDTH - 60, 10)

# Function to cut the sprite sheet into individual characters
def get_characters(sprite_sheet):
    characters = []
    sheet_width, sheet_height = sprite_sheet.get_size()
    for row in range(ROWS):
        for col in range(COLUMNS):
            x = col * (CHAR_SIZE + SEPARATION)
            y = row * (CHAR_SIZE + SEPARATION)
            if x + CHAR_SIZE <= sheet_width and y + CHAR_SIZE <= sheet_height:
                rect = pygame.Rect(x, y, CHAR_SIZE, CHAR_SIZE)
                character = sprite_sheet.subsurface(rect)
                characters.append(character)
            else:
                print(f"Skipping character at row {row}, column {col} due to out-of-bounds")
    return characters

# Generate random points for each character between 540 and 8900
def generate_points(num_characters):
    return [random.randint(540, 8900) for _ in range(num_characters)]

# Draw the leaderboard
def draw_leaderboard(screen, characters, points, offset):
    draw_background(screen)
    title = font.render("Leaderboard", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

    # Combine characters with points and sort by points
    leaderboard = sorted(zip(characters, points), key=lambda x: x[1], reverse=True)

    for i, (character, point) in enumerate(leaderboard):
        y_pos = 80 + i * (CHAR_SIZE + 10) + offset
        if 80 <= y_pos <= SCREEN_HEIGHT - CHAR_SIZE:
            screen.blit(character, (50, y_pos))
            point_text = font.render(f"{point} points", True, BLACK)
            screen.blit(point_text, (100, y_pos + (CHAR_SIZE // 4)))

    # Draw leave icon
    screen.blit(leave_icon, leave_icon_pos)

# Main function
def main_leaderboard(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar):
    characters = get_characters(sprite_sheet)
    points = generate_points(len(characters))

    offset = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    offset -= SCROLL_SPEED
                elif event.key == pygame.K_UP:
                    offset += SCROLL_SPEED
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check if leave icon is clicked
                if leave_icon_pos[0] <= mouse_pos[0] <= leave_icon_pos[0] + 50 and leave_icon_pos[1] <= mouse_pos[1] <= leave_icon_pos[1] + 50:
                    running = False
                    menu_main(run_game, run_stickers, run_leaderboard, run_challenges)

        draw_leaderboard(screen, characters, points, offset)
        pygame.display.flip()

if __name__ == "__main__":
    from main_controller import run_game, run_stickers, run_leaderboard, run_challenges, run_avatar
    main_leaderboard(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar)
