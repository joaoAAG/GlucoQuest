import pygame
import sys
import csv
import random
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from menu import main as menu_main
from stickers import save_new_sticker

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
FONT_SIZE = 32
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
ZOOM_DURATION = 1  # Duration of the zoom effect in seconds
POPUP_DURATION = 3  # Duration of the pop-up in seconds
ROULETTE_DURATION = 5  # Duration of the roulette animation in seconds
GLU_APPEAR_DURATION = 5  # Duration for Hyperglu and Hipoglu to appear

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GlucoQuest")

# Fonts
font = pygame.font.Font(None, FONT_SIZE)
zoom_font = pygame.font.Font(None, 100)  # Larger font for zoom effect

# Load images
left_icon = pygame.image.load('images/left_arrow.png')
right_icon = pygame.image.load('images/right_arrow.png')
leave_icon = pygame.image.load('images/leave_icon.png')
save_button_normal = pygame.image.load('images/button_normal.png')
save_button_hover = pygame.image.load('images/button_hover.png')
save_button_click = pygame.image.load('images/button_click.png')
chart_icon = pygame.image.load('images/chart_icon.png')
background_normal = pygame.image.load('images/background.jpg')
background_high = pygame.image.load('images/background_high.jpg')
cloud_image_normal = pygame.image.load('images/cloud.png')
cloud_image_high = pygame.image.load('images/cloud_high.png')
hyperglu_image = pygame.image.load('images/hyperglu.png')
hipoglu_image = pygame.image.load('images/hipoglu.png')  # Add hipoglu image
roulette_border_normal = pygame.image.load('images/border.png')
roulette_border_high = pygame.image.load('images/border_high.png')

# Blank images for roulette
blank_images = {
    'carrot': pygame.image.load('images/carrot_blank.png'),
    'potato': pygame.image.load('images/potato_blank.png'),
    'broccoli': pygame.image.load('images/broccoli_blank.png'),
    'cheese': pygame.image.load('images/cheese_blank.png'),
    'milk': pygame.image.load('images/milk_blank.png'),
    'spaghetti': pygame.image.load('images/spaghetti_blank.png'),
    'tomato': pygame.image.load('images/tomato_blank.png'),
    'banana': pygame.image.load('images/banana_blank.png'),
    'bread': pygame.image.load('images/bread_blank.png'),
    'yogurt': pygame.image.load('images/yogurt_blank.png'),
    'pea': pygame.image.load('images/pea_blank.png')
}

# Full sticker images
sticker_images = {
    'carrot': pygame.image.load('images/carrot_sticker.png'),
    'potato': pygame.image.load('images/potato_sticker.png'),
    'broccoli': pygame.image.load('images/broccoli_sticker.png'),
    'cheese': pygame.image.load('images/cheese_sticker.png'),
    'milk': pygame.image.load('images/milk_sticker.png'),
    'spaghetti': pygame.image.load('images/spaghetti_sticker.png'),
    'tomato': pygame.image.load('images/tomato_sticker.png'),
    'banana': pygame.image.load('images/banana_sticker.png'),
    'bread': pygame.image.load('images/bread_sticker.png'),
    'yogurt': pygame.image.load('images/yogurt_sticker.png'),
    'pea': pygame.image.load('images/pea_sticker.png')
}

# Resize icons
left_icon = pygame.transform.scale(left_icon, (30, 30))
right_icon = pygame.transform.scale(right_icon, (30, 30))
leave_icon = pygame.transform.scale(leave_icon, (50, 50))
save_button_normal = pygame.transform.scale(save_button_normal, (BUTTON_WIDTH, BUTTON_HEIGHT))
save_button_hover = pygame.transform.scale(save_button_hover, (BUTTON_WIDTH, BUTTON_HEIGHT))
save_button_click = pygame.transform.scale(save_button_click, (BUTTON_WIDTH, BUTTON_HEIGHT))
chart_icon = pygame.transform.scale(chart_icon, (50, 50))

# Resize blank and sticker images
for key in blank_images:
    blank_images[key] = pygame.transform.scale(blank_images[key], (100, 100))
    sticker_images[key] = pygame.transform.scale(sticker_images[key], (100, 100))

# Resize hyperglu and hipoglu images
hyperglu_image = pygame.transform.scale(hyperglu_image, (150, 150))
hipoglu_image = pygame.transform.scale(hipoglu_image, (150, 150))  # Resize hipoglu image
roulette_border_normal = pygame.transform.scale(roulette_border_normal, (200, 200))
roulette_border_high = pygame.transform.scale(roulette_border_high, (200, 200))

# Background and cloud settings
background_normal = pygame.transform.scale(background_normal, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_high = pygame.transform.scale(background_high, (SCREEN_WIDTH, SCREEN_HEIGHT))
cloud_image_normal = pygame.transform.scale(cloud_image_normal, (150, 100))
cloud_image_high = pygame.transform.scale(cloud_image_high, (150, 100))

# Cloud settings
clouds = [{'pos': [-150, random.randint(50, 150)], 'speed': random.uniform(0.2, 0.5), 'image': cloud_image_normal} for _ in range(3)]

# Icon positions
left_icon_date_pos = (432, 44)
right_icon_date_pos = (560, 44)
left_icon_meal_pos = (171, 44)
right_icon_meal_pos = (285, 44)
leave_icon_pos = (SCREEN_WIDTH - 60, 10)
save_button_pos = (SCREEN_WIDTH - BUTTON_WIDTH - 20, SCREEN_HEIGHT - BUTTON_HEIGHT - 20)
save_button_rect = save_button_normal.get_rect(topleft=save_button_pos)
chart_icon_pos = (SCREEN_WIDTH - 70, 70)
chart_icon_rect = chart_icon.get_rect(topleft=chart_icon_pos)

# Game Variables
points = 520
glucose_records = {}
sticker_awarded_dates = set()
current_date = datetime.now().strftime('%Y-%m-%d')
date_input_active = False
input_text = ""
date_input_text = current_date
meal_type = "Breakfast"
meal_types = ["Breakfast", "Lunch", "Snack", "Dinner"]
zoom_effect_active = False
zoom_effect_start_time = None
zoom_effect_text = ""
zoom_effect_color = BLACK
popup_active = False
popup_start_time = None
popup_image = None
roulette_active = False
roulette_start_time = None
roulette_images = []
roulette_result_key = None
sticker_zoom_effect_active = False
sticker_zoom_effect_start_time = None
hyperglu_active = False
hyperglu_start_time = None
hyperglu_pos = [SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT]
hipoglu_active = False
hipoglu_start_time = None
hipoglu_pos = [SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT]
border_type = 'normal'  # Can be 'normal' or 'high'
background = background_normal

# Table settings
table_x = 50
table_y = 150
cell_width = 150
cell_height = 50


def save_records_to_csv(records, filename="glucose_records.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Meal", "Glucose Level", "Status"])
        for date, daily_records in records.items():
            for record in daily_records:
                writer.writerow([date] + record)


def load_records_from_csv(filename="glucose_records.csv"):
    records = {}
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                date, meal, level, status = row
                if date not in records:
                    records[date] = []
                records[date].append([meal, level, status])
    except FileNotFoundError:
        pass
    return records


def draw_text(screen, text, position, font, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


def generate_charts(records):
    meals = ["Breakfast", "Lunch", "Snack", "Dinner"]
    meal_data = {meal: [] for meal in meals}
    meal_counts = {meal: 0 for meal in meals}

    current_date = datetime.now()
    date_range = [(current_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

    for date in date_range:
        if date in records:
            for record in records[date]:
                meal, level, _ = record
                if meal in meal_data:
                    meal_data[meal].append(int(level))
                    meal_counts[meal] += 1

    meal_averages = {meal: (sum(values) / len(values) if values else 0) for meal, values in meal_data.items()}

    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.bar(meal_averages.keys(), meal_averages.values(), color=['blue', 'green', 'red', 'orange'])
    plt.xlabel('Meals')
    plt.ylabel('Average Glucose Level')
    plt.title('Average Glucose Levels for Each Meal (Last 7 Days)')

    plt.subplot(2, 1, 2)
    plt.bar(meal_counts.keys(), meal_counts.values(), color=['blue', 'green', 'red', 'orange'])
    plt.xlabel('Meals')
    plt.ylabel('Number of Values')
    plt.title('Number of Values for Each Meal (Last 7 Days)')

    plt.tight_layout()
    plt.show()


def show_popup():
    global popup_active, popup_start_time, popup_image
    popup_active = True
    popup_start_time = pygame.time.get_ticks()
    popup_image = random.choice(list(blank_images.values()))


def start_roulette():
    global roulette_active, roulette_start_time, roulette_images, roulette_result_key, border_type
    roulette_active = True
    roulette_start_time = pygame.time.get_ticks()
    roulette_keys = list(blank_images.keys())
    roulette_images = [blank_images[key] for key in random.choices(roulette_keys, k=30)]  # Display 30 images in the roulette
    roulette_result_key = random.choice(roulette_keys)  # Final result key of the roulette
    # Determine the border type based on the last glucose record
    if glucose_records[current_date][-1][2] == "High":
        border_type = 'high'
    else:
        border_type = 'normal'

def main_game(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar):
    global points, glucose_records, sticker_awarded_dates, current_date, date_input_text, meal_type, input_text, date_input_active, zoom_effect_active, zoom_effect_start_time, zoom_effect_text, zoom_effect_color, popup_active, popup_start_time, popup_image, roulette_active, roulette_start_time, roulette_images, roulette_result_key, sticker_zoom_effect_active, sticker_zoom_effect_start_time, hyperglu_active, hyperglu_start_time, hyperglu_pos, border_type, background, hypoglu_active, hypoglu_start_time, hypoglu_pos, warning_text, warning_start_time

    glucose_records = load_records_from_csv()
    if current_date not in glucose_records:
        glucose_records[current_date] = []

    running = True
    save_button_state = "normal"
    previous_date = current_date
    hypoglu_active = False
    hypoglu_start_time = None
    hypoglu_pos = [SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT]
    warning_text = ""
    warning_start_time = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_records_to_csv(glucose_records)
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Check if leave icon is clicked
                if leave_icon_pos[0] <= mouse_pos[0] <= leave_icon_pos[0] + 50 and leave_icon_pos[1] <= mouse_pos[1] <= leave_icon_pos[1] + 50:
                    save_records_to_csv(glucose_records)
                    running = False
                    menu_main(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar)
                # Check if save button is clicked
                if save_button_rect.collidepoint(mouse_pos):
                    save_button_state = "click"
                # Check if chart icon is clicked
                if chart_icon_rect.collidepoint(mouse_pos):
                    generate_charts(glucose_records)
                # Check if left icon (date) is clicked
                if left_icon_date_pos[0] <= mouse_pos[0] <= left_icon_date_pos[0] + 30 and left_icon_date_pos[1] <= mouse_pos[1] <= left_icon_date_pos[1] + 30:
                    current_date = (datetime.strptime(current_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
                    date_input_text = current_date
                    if current_date not in glucose_records:
                        glucose_records[current_date] = []
                # Check if right icon (date) is clicked
                elif right_icon_date_pos[0] <= mouse_pos[0] <= right_icon_date_pos[0] + 30 and right_icon_date_pos[1] <= mouse_pos[1] <= right_icon_date_pos[1] + 30:
                    current_date = (datetime.strptime(current_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                    date_input_text = current_date
                    if current_date not in glucose_records:
                        glucose_records[current_date] = []
                    if current_date != previous_date:
                        show_popup()
                    previous_date = current_date
                # Check if left icon (meal) is clicked
                elif left_icon_meal_pos[0] <= mouse_pos[0] <= left_icon_meal_pos[0] + 30 and left_icon_meal_pos[1] <= mouse_pos[1] <= left_icon_meal_pos[1] + 30:
                    current_index = meal_types.index(meal_type)
                    meal_type = meal_types[(current_index - 1) % len(meal_types)]
                # Check if right icon (meal) is clicked
                elif right_icon_meal_pos[0] <= mouse_pos[0] <= right_icon_meal_pos[0] + 30 and right_icon_meal_pos[1] <= mouse_pos[1] <= right_icon_meal_pos[1] + 30:
                    current_index = meal_types.index(meal_type)
                    meal_type = meal_types[(current_index + 1) % len(meal_types)]
            if event.type == pygame.MOUSEBUTTONUP:
                if save_button_rect.collidepoint(event.pos):
                    if save_button_state == "click":
                        if current_date not in sticker_awarded_dates and len(glucose_records[current_date]) >= 3:
                            save_records_to_csv(glucose_records)
                            save_button_state = "hover"
                            start_roulette()  # Start the roulette after saving
                            sticker_awarded_dates.add(current_date)  # Mark this date as having awarded a sticker
                        else:
                            save_records_to_csv(glucose_records)
                            save_button_state = "hover"
                else:
                    save_button_state = "normal"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if date_input_active:
                        current_date = date_input_text
                        date_input_active = False
                    else:
                        if input_text.isdigit():
                            glucose_record = int(input_text)
                            status = "Normal" if 70 <= glucose_record <= 180 else "Low" if glucose_record < 70 else "High"

                            # Check if the meal type is already recorded for the day
                            duplicate_entry = any(record[0] == meal_type for record in glucose_records[current_date])

                            if not duplicate_entry:
                                glucose_records[current_date].append([meal_type, glucose_record, status])
                                input_text = ""
                                if 70 <= glucose_record <= 180:
                                    points += 20
                                    zoom_effect_text = "+20"
                                    zoom_effect_color = GREEN
                                    zoom_effect_start_time = pygame.time.get_ticks()
                                    zoom_effect_active = True
                                elif glucose_record < 70:
                                    points += 5  # Correcting hypoglycemia
                                    zoom_effect_text = "+10"
                                    zoom_effect_color = RED
                                    zoom_effect_start_time = pygame.time.get_ticks()
                                    zoom_effect_active = True
                                    hypoglu_active = True
                                    hypoglu_start_time = pygame.time.get_ticks()
                                    hypoglu_pos = [SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT]
                                    warning_text = " Hypoglycemia! Administer insulin and remeasure in 2 hours."
                                    warning_start_time = pygame.time.get_ticks()
                                elif glucose_record > 230:
                                    points += 5  # Correcting hyperglycemia
                                    zoom_effect_text = "+5"
                                    zoom_effect_color = BLUE
                                    zoom_effect_start_time = pygame.time.get_ticks()
                                    zoom_effect_active = True
                                    hyperglu_active = True
                                    hyperglu_start_time = pygame.time.get_ticks()
                                    hyperglu_pos = [SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT]
                                    warning_text = "Hyperglycemia detected! Check again in 30 minutes"
                                    warning_start_time = pygame.time.get_ticks()
                            else:
                                glucose_records[current_date].append([meal_type, glucose_record, status])
                                input_text = ""
                                if 70 <= glucose_record <= 180:
                                    points += 10
                elif event.key == pygame.K_BACKSPACE:
                    if date_input_active:
                        date_input_text = date_input_text[:-1]
                    else:
                        input_text = input_text[:-1]
                elif event.key == pygame.K_TAB:
                    date_input_active = not date_input_active
                else:
                    if date_input_active:
                        date_input_text += event.unicode
                    else:
                        input_text += event.unicode

        # Determine background and cloud image based on glucose levels
        if glucose_records[current_date] and glucose_records[current_date][-1][2] == "High":
            background = background_high
            for cloud in clouds:
                cloud['image'] = cloud_image_high
        else:
            background = background_normal
            for cloud in clouds:
                cloud['image'] = cloud_image_normal

        # Draw everything
        screen.blit(background, (0, 0))

        # Move clouds
        for cloud in clouds:
            cloud['pos'][0] += cloud['speed']
            if cloud['pos'][0] > SCREEN_WIDTH:
                cloud['pos'][0] = -150
                cloud['pos'][1] = random.randint(50, 150)
            screen.blit(cloud['image'], cloud['pos'])

        # Draw leave icon
        screen.blit(leave_icon, leave_icon_pos)

        # Draw date input
        draw_text(screen, f"Date:    {date_input_text}", (370, 50), font)
        # Draw left and right icons for date
        screen.blit(left_icon, left_icon_date_pos)
        screen.blit(right_icon, right_icon_date_pos)

        # Draw meal type selection
        draw_text(screen, f"Meal Type:    {meal_type}", (50, 50), font)
        # Draw left and right icons for meal type
        screen.blit(left_icon, left_icon_meal_pos)
        screen.blit(right_icon, right_icon_meal_pos)

        # Determine table row count
        rows = max(len(glucose_records[current_date]), 5)

        # Draw table
        for i in range(rows):  # 5 rows initially, add more if needed
            for j in range(3):  # 3 columns: Meal, Glucose, Status
                rect = pygame.Rect(table_x + j * cell_width, table_y + i * cell_height, cell_width, cell_height)
                pygame.draw.rect(screen, BLACK, rect, 2)
                if i < len(glucose_records[current_date]):
                    record = glucose_records[current_date][i]
                    text_surface = font.render(str(record[j]), True, BLACK)  # Convert values to strings
                    screen.blit(text_surface, (table_x + j * cell_width + 10, table_y + i * cell_height + 10))

        # Adjust input box position and size based on row count
        input_box_height = cell_height if rows <= 5 else cell_height - 10
        input_box_y = table_y + rows * cell_height + 10
        input_box = pygame.Rect(table_x, input_box_y, cell_width * 2, input_box_height)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        draw_text(screen, input_text, (input_box.x + 10, input_box.y + 10), font)

        # Display points
        draw_text(screen, f"Points: {points}", (50, 570), font)

        # Draw save button
        if save_button_state == "normal":
            screen.blit(save_button_normal, save_button_pos)
        elif save_button_state == "hover":
            screen.blit(save_button_hover, save_button_pos)
        elif save_button_state == "click":
            screen.blit(save_button_click, save_button_pos)
        draw_text(screen, "Save", (save_button_pos[0] + 50, save_button_pos[1] + 10), font)

        # Draw chart icon
        screen.blit(chart_icon, chart_icon_pos)

        # Handle zoom effect
        if zoom_effect_active:
            elapsed_time = (pygame.time.get_ticks() - zoom_effect_start_time) / 1000
            if elapsed_time < ZOOM_DURATION:
                scale = 1 + 2 * elapsed_time / ZOOM_DURATION  # Scale from 1 to 3
                zoom_text_surface = zoom_font.render(zoom_effect_text, True, zoom_effect_color)
                zoom_text_surface = pygame.transform.scale(zoom_text_surface, (int(zoom_text_surface.get_width() * scale), int(zoom_text_surface.get_height() * scale)))
                zoom_rect = zoom_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(zoom_text_surface, zoom_rect)
            else:
                zoom_effect_active = False

        # Handle roulette
        if roulette_active:
            elapsed_time = (pygame.time.get_ticks() - roulette_start_time) / 1000
            if elapsed_time < ROULETTE_DURATION:
                current_index = int(len(roulette_images) * elapsed_time / ROULETTE_DURATION)
                roulette_image = roulette_images[current_index]
                screen.blit(roulette_border_normal if border_type == 'normal' else roulette_border_high, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
                roulette_rect = roulette_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(roulette_image, roulette_rect)
            else:
                roulette_active = False
                # Display final roulette result and turn it into a sticker
                sticker_image = sticker_images[roulette_result_key]
                sticker_zoom_effect_active = True
                sticker_zoom_effect_start_time = pygame.time.get_ticks()
                save_new_sticker(roulette_result_key)  # Save the key

        # Handle sticker zoom effect
        if sticker_zoom_effect_active:
            elapsed_time = (pygame.time.get_ticks() - sticker_zoom_effect_start_time) / 1000
            if elapsed_time < ZOOM_DURATION:
                scale = 1 + 2 * elapsed_time / ZOOM_DURATION  # Scale from 1 to 3
                sticker_zoom_surface = pygame.transform.scale(sticker_image, (int(sticker_image.get_width() * scale), int(sticker_image.get_height() * scale)))
                sticker_zoom_rect = sticker_zoom_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(sticker_zoom_surface, sticker_zoom_rect)
            else:
                sticker_zoom_effect_active = False

        # Handle hyperglu appearance
        if hyperglu_active:
            elapsed_time = (pygame.time.get_ticks() - hyperglu_start_time) / 1000
            if elapsed_time < GLU_APPEAR_DURATION:
                hyperglu_pos[1] = SCREEN_HEIGHT - int((130 / GLU_APPEAR_DURATION) * elapsed_time)
                screen.blit(hyperglu_image, hyperglu_pos)
            else:
                hyperglu_active = False

        # Handle hypoglu appearance
        if hypoglu_active:
            elapsed_time = (pygame.time.get_ticks() - hypoglu_start_time) / 1000
            if elapsed_time < GLU_APPEAR_DURATION:
                hypoglu_pos[1] = SCREEN_HEIGHT - int((130 / GLU_APPEAR_DURATION) * elapsed_time)
                screen.blit(hipoglu_image, hypoglu_pos)
            else:
                hypoglu_active = False

        # Display warning text
        if warning_text:
            elapsed_time = (pygame.time.get_ticks() - warning_start_time) / 1000
            if elapsed_time < 5:  # Display for 3 seconds
                warning_surface = font.render(warning_text, True, BLACK)

                warning_rect = warning_surface.get_rect(center=(SCREEN_WIDTH // 2, 140))

                screen.blit(warning_surface, warning_rect)
            else:
                warning_text = ""

        pygame.display.flip()



if __name__ == "__main__":
    from main_controller import run_game, run_stickers, run_leaderboard, run_challenges, run_avatar

    main_game(run_game, run_stickers, run_leaderboard, run_challenges, run_avatar)
