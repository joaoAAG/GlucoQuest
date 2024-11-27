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
pygame.display.set_caption("Badges")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)
label_font = pygame.font.Font(None, 24)

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

# Blank and full badge images
badge_blank_images = {
    'star_0': pygame.image.load('images/star_blank.png'),
    'star_1': pygame.image.load('images/star_blank.png'),
    'star_2': pygame.image.load('images/star_blank.png'),
    'star_3': pygame.image.load('images/star_blank.png'),
    'star_4': pygame.image.load('images/star_blank.png'),
    'star_5': pygame.image.load('images/star_blank.png'),
    'star_6': pygame.image.load('images/star_blank.png'),
    'star_7': pygame.image.load('images/star_blank.png')
}

badge_sticker_images = {
    'star_0': pygame.image.load('images/star_sticker.png'),
    'star_1': pygame.image.load('images/star1_sticker.png'),
    'star_2': pygame.image.load('images/star2_sticker.png')
}

# Names for badges
badge_names = {
    'star_0': 'Look at you!',
    'star_1': 'First Value',
    'star_2': 'What a nice day',
    'star_3': '???',
    'star_4': '???',
    'star_5': '???',
    'star_6': '???',
    'star_7': '???'
}

# Resize images
for key in badge_blank_images:
    badge_blank_images[key] = pygame.transform.scale(badge_blank_images[key], (100, 100))

for key in badge_sticker_images:
    badge_sticker_images[key] = pygame.transform.scale(badge_sticker_images[key], (100, 100))

# List to keep track of collected badges
collected_badges = ['star_0', 'star_1', 'star_2']

# Pagination variable
current_page = 0
pages = ['Badges']


def save_new_badge(badge_key):
    global collected_badges
    if badge_key not in collected_badges:
        collected_badges.append(badge_key)


def draw_text(screen, text, position, font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


def show_badge_info(screen, key):
    message = f"Badge: {key.capitalize()}"
    lines = message.split('\n')
    y_offset = 0
    for line in lines:
        draw_text(screen, line, (SCREEN_WIDTH // 2 + 100, 200 + y_offset), font, BLACK)
        y_offset += 40


def main_badges(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar):
    global current_page
    running = True
    selected_badge = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check if leave icon is clicked
                if leave_icon_pos[0] <= mouse_pos[0] <= leave_icon_pos[0] + 50 and leave_icon_pos[1] <= mouse_pos[1] <= \
                        leave_icon_pos[1] + 50:
                    running = False
                    run_game()
                # Check if left arrow is clicked
                if left_arrow_pos[0] <= mouse_pos[0] <= left_arrow_pos[0] + 50 and left_arrow_pos[1] <= mouse_pos[1] <= \
                        left_arrow_pos[1] + 50:
                    current_page = (current_page - 1) % len(pages)
                # Check if right arrow is clicked
                if right_arrow_pos[0] <= mouse_pos[0] <= right_arrow_pos[0] + 50 and right_arrow_pos[1] <= mouse_pos[
                    1] <= right_arrow_pos[1] + 50:
                    current_page = (current_page + 1) % len(pages)

                # Check if a badge is clicked
                for i, key in enumerate(badge_blank_images):
                    badge_rect = pygame.Rect(50 + (i % 3) * 230, 100 + (i // 3) * 150, 100, 100)
                    if badge_rect.collidepoint(mouse_pos) and key in collected_badges:
                        selected_badge = key

        # Draw everything
        draw_background(screen)
        screen.blit(leave_icon, leave_icon_pos)
        screen.blit(left_arrow, left_arrow_pos)
        screen.blit(right_arrow, right_arrow_pos)

        # Display badges based on the current page
        for i, key in enumerate(badge_blank_images):
            badge_rect = pygame.Rect(50 + (i % 3) * 230, 100 + (i // 3) * 150, 100, 100)
            if key in collected_badges:
                badge_image = badge_sticker_images.get(key, badge_blank_images[key])
                label = badge_names.get(key, '???')
            else:
                badge_image = badge_blank_images[key]
                label = '???'
            screen.blit(badge_image, badge_rect)

            # Draw label below the badge
            label_position = (badge_rect.centerx - label_font.size(label)[0] // 2, badge_rect.bottom + 10)
            draw_text(screen, label, label_position, label_font)

        # Draw page title
        draw_text(screen, pages[current_page], (SCREEN_WIDTH // 2 - 40, 50), font)

        # Display badge info if a badge is selected
        if selected_badge:
            show_badge_info(screen, selected_badge)

        pygame.display.flip()


if __name__ == "__main__":
    from main_controller import run_game, run_stickers, run_leaderboard, run_challenges, run_avatar

    main_badges(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar)
