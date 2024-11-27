import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
FONT_SIZE = 32

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GlucoQuest Menu")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)

# Load images
logo = pygame.image.load('images/logo.png')
button_normal = pygame.image.load('images/button_normal.png')
button_hover = pygame.image.load('images/button_hover.png')
button_click = pygame.image.load('images/button_click.png')
avatar_icon = pygame.image.load('images/avatar_icon.png')
background_image = pygame.image.load('images/background2.jpg')  # Add this line

# Resize images
logo = pygame.transform.scale(logo, (400, 150))
button_normal = pygame.transform.scale(button_normal, (200, 50))
button_hover = pygame.transform.scale(button_hover, (200, 50))
button_click = pygame.transform.scale(button_click, (200, 50))
avatar_icon = pygame.transform.scale(avatar_icon, (50, 50))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize background

# Position images
logo_rect = logo.get_rect(center=(SCREEN_WIDTH // 2 - 20, 150))
button_rects = [
    button_normal.get_rect(center=(SCREEN_WIDTH // 2, 300)),
    button_normal.get_rect(center=(SCREEN_WIDTH // 2, 360)),
    button_normal.get_rect(center=(SCREEN_WIDTH // 2, 420)),
    button_normal.get_rect(center=(SCREEN_WIDTH // 2, 480))
]
avatar_rect = avatar_icon.get_rect(topright=(SCREEN_WIDTH - 60, 20))

# Game Variables
button_state = ["normal"] * 4
button_texts = ["Diary", "Stickers", "Social", "Challenges"]

def draw_text_on_button(screen, text, button_rect, font):
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

def main(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar):
    global button_state
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        button_state[i] = "click"
                if avatar_rect.collidepoint(event.pos):
                    run_avatar()
            elif event.type == pygame.MOUSEBUTTONUP:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos) and button_state[i] == "click":
                        button_state[i] = "hover"
                        # Handle button click event here
                        if button_texts[i] == "Diary":
                            run_game()
                        elif button_texts[i] == "Stickers":
                            run_stickers()
                        elif button_texts[i] == "Social":
                            run_leaderboard()
                        elif button_texts[i] == "Challenges":
                            run_challenges()
                    else:
                        button_state[i] = "normal"
            elif event.type == pygame.MOUSEMOTION:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        if button_state[i] != "click":
                            button_state[i] = "hover"
                    else:
                        button_state[i] = "normal"

        # Draw everything
        screen.blit(background_image, (0, 0))  # Draw the background image
        screen.blit(logo, logo_rect)
        screen.blit(avatar_icon, avatar_rect)

        for i, rect in enumerate(button_rects):
            if button_state[i] == "normal":
                screen.blit(button_normal, rect)
            elif button_state[i] == "hover":
                screen.blit(button_hover, rect)
            elif button_state[i] == "click":
                screen.blit(button_click, rect)
            draw_text_on_button(screen, button_texts[i], rect, font)

        pygame.display.flip()

if __name__ == "__main__":
    main(lambda: print("Run Game"), lambda: print("Run Stickers"), lambda: print("Run Leaderboard"), lambda: print("Run Challenges"), lambda: print("Run Avatar"))
