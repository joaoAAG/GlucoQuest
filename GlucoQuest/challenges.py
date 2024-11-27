import pygame
import sys
from menu import main as menu_main

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
FONT_SIZE = 32
PROGRESS_BAR_WIDTH = 200
PROGRESS_BAR_HEIGHT = 20
ZOOM_DURATION = 1  # Duration of the zoom effect in seconds

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Challenges")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)
zoom_font = pygame.font.Font(None, 100)  # Larger font for zoom effect

# Load icons
star_icon = pygame.image.load('images/star_icon.png')
global_icon = pygame.image.load('images/global_icon.png')
leave_icon = pygame.image.load('images/leave_icon.png')
collect_button_normal = pygame.image.load('images/button_normal.png')
collect_button_hover = pygame.image.load('images/button_hover.png')
collect_button_click = pygame.image.load('images/button_click.png')

# Resize icons
star_icon = pygame.transform.scale(star_icon, (50, 50))
global_icon = pygame.transform.scale(global_icon, (50, 50))
leave_icon = pygame.transform.scale(leave_icon, (50, 50))
collect_button_normal = pygame.transform.scale(collect_button_normal, (150, 50))
collect_button_hover = pygame.transform.scale(collect_button_hover, (150, 50))
collect_button_click = pygame.transform.scale(collect_button_click, (150, 50))

# Icon positions
leave_icon_pos = (SCREEN_WIDTH - 60, 10)
individual_challenge_pos = (50, 100)
global_challenge_pos = (50, 300)
collect_button_pos = (SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT - 100)
collect_button_rect = collect_button_normal.get_rect(topleft=collect_button_pos)

# Example challenges
individual_challenges = [
    "Record glucose level 3 times a day for a week.",
    "Keep glucose levels within normal range for 3 days."
]

global_challenges = [
    "Collectively record 10,000 glucose entries.",
    "Achieve 1,000 points as a community."
]

# Fake progress for challenges (values between 0 and 1)
individual_progress = [0.6, 0.4]
global_progress = [0.3, 1.0]  # Full progress for demonstration

# Game variables
zoom_effect_active = False
zoom_effect_start_time = None
zoom_effect_text = ""
zoom_effect_color = BLACK
points = 0
collected_points = False  # Track if points have been collected


def draw_progress_bar(screen, x, y, progress, full=False):
    pygame.draw.rect(screen, BLACK, (x, y, PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT), 2)
    if full:
        pygame.draw.rect(screen, GREEN, (x, y, PROGRESS_BAR_WIDTH * progress, PROGRESS_BAR_HEIGHT))
    else:
        pygame.draw.rect(screen, BLACK, (x, y, PROGRESS_BAR_WIDTH * progress, PROGRESS_BAR_HEIGHT))


def draw_challenges(screen):
    screen.fill(WHITE)
    title = font.render("Challenges", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

    # Draw individual challenges
    screen.blit(star_icon, individual_challenge_pos)
    individual_title = font.render("Individual Challenges", True, BLACK)
    screen.blit(individual_title, (individual_challenge_pos[0] + 60, individual_challenge_pos[1]))

    for i, challenge in enumerate(individual_challenges):
        challenge_text = font.render(challenge, True, BLACK)
        y_pos = individual_challenge_pos[1] + 60 + i * 60
        screen.blit(challenge_text, (individual_challenge_pos[0] + 60, y_pos))
        draw_progress_bar(screen, individual_challenge_pos[0] + 60, y_pos + 30, individual_progress[i])

    # Draw global challenges
    screen.blit(global_icon, global_challenge_pos)
    global_title = font.render("Global Challenges", True, BLACK)
    screen.blit(global_title, (global_challenge_pos[0] + 60, global_challenge_pos[1]))

    for i, challenge in enumerate(global_challenges):
        challenge_text = font.render(challenge, True, BLACK)
        y_pos = global_challenge_pos[1] + 60 + i * 60
        screen.blit(challenge_text, (global_challenge_pos[0] + 60, y_pos))
        draw_progress_bar(screen, global_challenge_pos[0] + 60, y_pos + 30, global_progress[i], full=(i == 1))

    # Draw leave icon
    screen.blit(leave_icon, leave_icon_pos)

    # Draw collect button
    if global_progress[1] == 1.0 and not collected_points:  # Only show if the challenge is fully completed and not collected
        screen.blit(collect_button_normal, collect_button_pos)
        draw_text(screen, "Collect", (collect_button_pos[0] + 40, collect_button_pos[1] + 10), font)


def draw_text(screen, text, position, font, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


def main_challenges(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar):
    global zoom_effect_active, zoom_effect_start_time, zoom_effect_text, points, collected_points
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
                    menu_main(run_game, run_stickers, run_leaderboard, run_challenges)
                # Check if collect button is clicked
                if collect_button_rect.collidepoint(mouse_pos) and global_progress[1] == 1.0 and not collected_points:
                    zoom_effect_text = "+50"
                    zoom_effect_start_time = pygame.time.get_ticks()
                    zoom_effect_active = True
                    points += 50
                    collected_points = True
                    global_progress[1] = 0.0  # Reset the progress bar

        draw_challenges(screen)

        # Handle zoom effect
        if zoom_effect_active:
            elapsed_time = (pygame.time.get_ticks() - zoom_effect_start_time) / 1000
            if elapsed_time < ZOOM_DURATION:
                scale = 1 + 2 * elapsed_time / ZOOM_DURATION  # Scale from 1 to 3
                zoom_text_surface = zoom_font.render(zoom_effect_text, True, GREEN)
                zoom_text_surface = pygame.transform.scale(zoom_text_surface, (int(zoom_text_surface.get_width() * scale), int(zoom_text_surface.get_height() * scale)))
                zoom_rect = zoom_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(zoom_text_surface, zoom_rect)
            else:
                zoom_effect_active = False

        pygame.display.flip()


if __name__ == "__main__":
    from main_controller import run_game, run_stickers, run_leaderboard, run_challenges, run_avatar

    main_challenges(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar)
