from cgitb import reset

import pygame
import math
import random
from datetime import datetime

# configuration
draw_circle = False
colorchange_on_hour = True
halftime_text = False
dj_text = True

dj_dict = {
    20: "Open Decks",
    21: "J. Unge",
    22: "techno_cio",
    23: "hinueber",
    0: "Onkel Jonas",
    1: "Nelesan",
    2: "MASHA",
    3: "Tympani",
    4: "Petermaksi",
    5: "Open Decks",
    6: "Open Decks",
    7: "Open Decks",
    8: "Open Decks",
    9: "Open Decks",
    10: "Open Decks",
    11: "Open Decks",
    12: "Open Decks",
    13: "Open Decks",
    14: "Open Decks",
    15: "Open Decks",
    16: "Open Decks",
    17: "Open Decks",
    18: "Open Decks",
    19: "Open Decks"
}

pygame.init()
info = pygame.display.Info()

# Set up the display in fullscreen mode
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()


def scale_image_to_fit(image, target_width, target_height):
    image_width, image_height = image.get_size()
    scale_width = target_width / image_width
    scale_height = target_height / image_height
    scale = min(scale_width, scale_height)

    new_width = int(image_width * scale)
    new_height = int(image_height * scale)

    scaled_image = pygame.transform.scale(image, (new_width, new_height))
    return scaled_image

# Clock settings
clock_radius = 400
clock_center = (info.current_w // 2, info.current_h // 2)

def draw_clock_face():
    # Draw the clock face
    pygame.draw.circle(screen, (255, 255, 255), clock_center, clock_radius, 2)

def draw_hand(angle, length, color, width=3):
    x = clock_center[0] + length * math.cos(angle)
    y = clock_center[1] + length * math.sin(angle)
    pygame.draw.line(screen, color, clock_center, (x, y), width)

def update_clock():
    now = datetime.now()
    # Calculate angles for each hand
    second_angle = math.radians((now.second / 60) * 360 - 90)
    minute_angle = math.radians((now.minute / 60) * 360 - 90)
    hour_angle = math.radians(((now.hour % 12) / 12) * 360 + (now.minute / 60) * 30 - 90)

    # Draw hands
    draw_hand(hour_angle, clock_radius * 0.5, (255, 255, 255), 15)
    draw_hand(minute_angle, clock_radius * 0.75, (200, 200, 200), 7)
    draw_hand(second_angle, clock_radius * 0.9, (150, 150, 150))

# Load the background image
background = pygame.image.load("clock-dj-faces.png")

# Scale the background image
scaled_background = scale_image_to_fit(background, screen_width, screen_height)

# Calculate position to center the scaled image
x_offset = (screen_width - scaled_background.get_width()) // 2
y_offset = (screen_height - scaled_background.get_height()) // 2

# Create clock object
clock = pygame.time.Clock()

current_bg_r = 0
current_bg_g = 0
current_bg_b = 0

halftime_font = pygame.font.Font(None, 100)
dj_font = pygame.font.Font(None, 100)
next_dj_font = pygame.font.Font(None, 50)

def calc_bg_color():
    global current_bg_r, current_bg_g, current_bg_b
    current_bg_r = random.randint(0, 255)
    current_bg_g = random.randint(0, 255)
    current_bg_b = random.randint(0, 255)

def reset_bg_color():
    global current_bg_r, current_bg_g, current_bg_b
    current_bg_r = 0
    current_bg_g = 0
    current_bg_b = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Fill the screen background
    now = datetime.now()
    if colorchange_on_hour:
        if now.minute == 0 and now.second < 5:
            calc_bg_color()
        elif now.minute == 0 and now.second == 5:
            reset_bg_color()
    screen.fill((current_bg_r, current_bg_g, current_bg_b))

    # Draw the scaled background image
    screen.blit(scaled_background, (x_offset, y_offset))

    if dj_text:
        # Draw the DJ text
        current_hour = now.hour
        if current_hour in dj_dict.keys():
            dj_name = dj_dict[current_hour]
            text = next_dj_font.render("now playing: ", True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 200))
            text2 = dj_font.render(dj_name, True, (255, 255, 255))
            text_rect2 = text2.get_rect(center=(screen_width // 2, screen_height // 2 - 120))

            screen.blit(text, text_rect)
            screen.blit(text2, text_rect2)

            if now.minute > 55 and current_hour+1 in dj_dict.keys():
                next_dj = dj_dict[(current_hour + 1) % 24]
                text = next_dj_font.render(f"next up: {next_dj}", True, (255, 255, 255))
                text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

                screen.blit(text, text_rect)

    # Draw the clock face and hands here
    if draw_circle:
        draw_clock_face()
    update_clock()

    # Draw the halftime text
    if halftime_text:
        if True:
            text = halftime_font.render("HALFTIME", True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
            screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(5)  # Limit to 60 FPS

pygame.quit()