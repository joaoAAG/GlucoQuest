import pygame
import sys
from background import draw_background

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 32

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stickers")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Load images
leave_icon = pygame.image.load('images/leave_icon.png')
leave_icon = pygame.transform.scale(leave_icon, (50, 50))
leave_icon_pos = (10, 10)
left_arrow = pygame.image.load('images/left_arrow.png')
left_arrow = pygame.transform.scale(left_arrow, (50, 50))
left_arrow_pos = (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 60)
right_arrow = pygame.image.load('images/right_arrow.png')
right_arrow = pygame.transform.scale(right_arrow, (50, 50))
right_arrow_pos = (SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT - 60)

# Blank and full sticker images for vegetables
vegetables_blank_images = {
    'carrot': pygame.image.load('images/carrot_blank.png'),
    'potato': pygame.image.load('images/potato_blank.png'),
    'broccoli': pygame.image.load('images/broccoli_blank.png'),
    'pea': pygame.image.load('images/pea_blank.png')
}

vegetables_sticker_images = {
    'carrot': pygame.image.load('images/carrot_sticker.png'),
    'potato': pygame.image.load('images/potato_sticker.png'),
    'broccoli': pygame.image.load('images/broccoli_sticker.png'),
    'pea': pygame.image.load('images/pea_sticker.png')
}

# Blank and full sticker images for foods
foods_blank_images = {
    'cheese': pygame.image.load('images/cheese_blank.png'),
    'milk': pygame.image.load('images/milk_blank.png'),
    'spaghetti': pygame.image.load('images/spaghetti_blank.png'),
    'tomato': pygame.image.load('images/tomato_blank.png'),
    'banana': pygame.image.load('images/banana_blank.png'),
    'bread': pygame.image.load('images/bread_blank.png'),
    'yogurt': pygame.image.load('images/yogurt_blank.png')
}

foods_sticker_images = {
    'cheese': pygame.image.load('images/cheese_sticker.png'),
    'milk': pygame.image.load('images/milk_sticker.png'),
    'spaghetti': pygame.image.load('images/spaghetti_sticker.png'),
    'tomato': pygame.image.load('images/tomato_sticker.png'),
    'banana': pygame.image.load('images/banana_sticker.png'),
    'bread': pygame.image.load('images/bread_sticker.png'),
    'yogurt': pygame.image.load('images/yogurt_sticker.png')
}

# Nutritional information for stickers
nutritional_info = {
    'carrot': {'carbohydrates': 10, 'lipids': 0.1, 'carbohydrates_per_100g': 9.6, 'lipids_per_100g': 0.24},
    'potato': {'carbohydrates': 17, 'lipids': 0.1, 'carbohydrates_per_100g': 17.58, 'lipids_per_100g': 0.1},
    'broccoli': {'carbohydrates': 7, 'lipids': 0.3, 'carbohydrates_per_100g': 6.64, 'lipids_per_100g': 0.37},
    'cheese': {'carbohydrates': 1, 'lipids': 9, 'carbohydrates_per_100g': 1.3, 'lipids_per_100g': 10},
    'milk': {'carbohydrates': 12, 'lipids': 8, 'carbohydrates_per_100g': 12.18, 'lipids_per_100g': 8},
    'spaghetti': {'carbohydrates': 25, 'lipids': 1.5, 'carbohydrates_per_100g': 25.1, 'lipids_per_100g': 1.51},
    'tomato': {'carbohydrates': 4, 'lipids': 0.2, 'carbohydrates_per_100g': 3.89, 'lipids_per_100g': 0.2},
    'banana': {'carbohydrates': 22, 'lipids': 0.3, 'carbohydrates_per_100g': 22.84, 'lipids_per_100g': 0.33},
    'bread': {'carbohydrates': 49, 'lipids': 2.5, 'carbohydrates_per_100g': 49, 'lipids_per_100g': 2.5},
    'yogurt': {'carbohydrates': 6, 'lipids': 3.5, 'carbohydrates_per_100g': 6.66, 'lipids_per_100g': 3.25},
    'pea': {'carbohydrates': 14, 'lipids': 0.4, 'carbohydrates_per_100g': 14.45, 'lipids_per_100g': 0.4}
}

# Resize images
for key in vegetables_blank_images:
    vegetables_blank_images[key] = pygame.transform.scale(vegetables_blank_images[key], (100, 100))
    vegetables_sticker_images[key] = pygame.transform.scale(vegetables_sticker_images[key], (100, 100))

for key in foods_blank_images:
    foods_blank_images[key] = pygame.transform.scale(foods_blank_images[key], (100, 100))
    foods_sticker_images[key] = pygame.transform.scale(foods_sticker_images[key], (100, 100))

# List to keep track of collected stickers
collected_stickers = []

# Pagination variable
current_page = 0
pages = ['Vegetables', 'Foods']

def save_new_sticker(sticker_key):
    global collected_stickers
    if sticker_key not in collected_stickers:
        collected_stickers.append(sticker_key)

def draw_text(screen, text, position, font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def show_nutritional_info(screen, key):
    info = nutritional_info[key]
    message = f"{key.capitalize()}:\nCarbohydrates: {info['carbohydrates']}g\nLipids: {info['lipids']}g\n" \
              f"Carbohydrates per 100g: {info['carbohydrates_per_100g']}g\nLipids per 100g: {info['lipids_per_100g']}g"
    lines = message.split('\n')
    y_offset = 0
    for line in lines:
        draw_text(screen, line, (SCREEN_WIDTH // 2 + 100, 200 + y_offset), font, BLACK)
        y_offset += 40

def main_stickers(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar):
    global current_page
    running = True
    selected_sticker = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check if leave icon is clicked
                if leave_icon_pos[0] <= mouse_pos[0] <= leave_icon_pos[0] + 50 and leave_icon_pos[1] <= mouse_pos[1] <= leave_icon_pos[1] + 50:
                    running = False
                    run_game()
                # Check if left arrow is clicked
                if left_arrow_pos[0] <= mouse_pos[0] <= left_arrow_pos[0] + 50 and left_arrow_pos[1] <= mouse_pos[1] <= left_arrow_pos[1] + 50:
                    current_page = (current_page - 1) % len(pages)
                # Check if right arrow is clicked
                if right_arrow_pos[0] <= mouse_pos[0] <= right_arrow_pos[0] + 50 and right_arrow_pos[1] <= mouse_pos[1] <= right_arrow_pos[1] + 50:
                    current_page = (current_page + 1) % len(pages)

                # Check if a sticker is clicked
                if pages[current_page] == 'Vegetables':
                    for i, key in enumerate(vegetables_blank_images):
                        sticker_rect = pygame.Rect(50 + (i % 3) * 230, 100 + (i // 3) * 150, 100, 100)
                        if sticker_rect.collidepoint(mouse_pos) and key in collected_stickers:
                            selected_sticker = key
                elif pages[current_page] == 'Foods':
                    for i, key in enumerate(foods_blank_images):
                        sticker_rect = pygame.Rect(50 + (i % 3) * 230, 100 + (i // 3) * 150, 100, 100)
                        if sticker_rect.collidepoint(mouse_pos) and key in collected_stickers:
                            selected_sticker = key

        # Draw everything
        draw_background(screen)
        screen.blit(leave_icon, leave_icon_pos)
        screen.blit(left_arrow, left_arrow_pos)
        screen.blit(right_arrow, right_arrow_pos)

        # Display stickers based on the current page
        if pages[current_page] == 'Vegetables':
            for i, key in enumerate(vegetables_blank_images):
                if key in collected_stickers:
                    sticker_image = vegetables_sticker_images[key]
                else:
                    sticker_image = vegetables_blank_images[key]
                sticker_rect = pygame.Rect(50 + (i % 3) * 230, 100 + (i // 3) * 150, 100, 100)
                screen.blit(sticker_image, sticker_rect)
        elif pages[current_page] == 'Foods':
            for i, key in enumerate(foods_blank_images):
                if key in collected_stickers:
                    sticker_image = foods_sticker_images[key]
                else:
                    sticker_image = foods_blank_images[key]
                sticker_rect = pygame.Rect(50 + (i % 3) * 230, 100 + (i // 3) * 150, 100, 100)
                screen.blit(sticker_image, sticker_rect)

        # Draw page title
        draw_text(screen, pages[current_page], (SCREEN_WIDTH // 2 - 40, 50), font)

        # Display nutritional info if a sticker is selected
        if selected_sticker:
            show_nutritional_info(screen, selected_sticker)

        pygame.display.flip()

if __name__ == "__main__":
    from main_controller import run_game, run_stickers, run_leaderboard, run_challenges, run_avatar
    main_stickers(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar)
