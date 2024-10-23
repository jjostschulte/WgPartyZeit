import pygame
import math
from datetime import datetime

# configuration
draw_circle = False



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
    draw_hand(hour_angle, clock_radius * 0.5, (0, 0, 255), 15)
    draw_hand(minute_angle, clock_radius * 0.75, (0, 255, 0), 10)
    draw_hand(second_angle, clock_radius * 0.9, (255, 0, 0))

# Load the background image
background = pygame.image.load("Dj-names.png")

# Scale the background image
scaled_background = scale_image_to_fit(background, screen_width, screen_height)

# Calculate position to center the scaled image
x_offset = (screen_width - scaled_background.get_width()) // 2
y_offset = (screen_height - scaled_background.get_height()) // 2

# Create clock object
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the scaled background image
    screen.blit(scaled_background, (x_offset, y_offset))

    # Draw the clock face and hands here
    if draw_circle:
        draw_clock_face()
    update_clock()

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()