import pygame
import os
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display for a fullscreen window
screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
pygame.display.set_caption("Realistic Solar System")

# Load background music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Loop indefinitely

# Load planet images with transparent background
def load_planet_image(name, scale_factor):
    image_path = os.path.join(name)
    image = pygame.image.load(image_path).convert_alpha()  # Use convert_alpha for transparency
    size = (int(scale_factor * 1200), int(scale_factor * 1200))  # Scale based on window width
    return pygame.transform.scale(image, size)  # Resize the planets

# Scale factors for planets relative to the window size
planet_scale_factors = {
    "sun": 0.10,  # 10% of window width for the sun
    "mercury": 0.02,  # 2% of window width
    "venus": 0.03,
    "earth": 0.035,
    "mars": 0.025,
    "jupiter": 0.06,
    "saturn": 0.05,
    "uranus": 0.045,
    "neptune": 0.045,
}

# Load planet images
planets = {}
for planet, scale in planet_scale_factors.items():
    planets[planet] = load_planet_image(f"{planet}.png", scale)

# Distance factors (as a percentage of the maximum possible radius)
distance_factors = {
    "mercury": 0.15,
    "venus": 0.25,
    "earth": 0.35,
    "mars": 0.45,
    "jupiter": 0.55,
    "saturn": 0.65,
    "uranus": 0.75,
    "neptune": 0.85,
}

# Adjust the speeds to be more realistic (inner planets orbit faster)
speeds = {
    "mercury": 0.03,   # Adjusted speeds for realism
    "venus": 0.025,
    "earth": 0.02,
    "mars": 0.017,
    "jupiter": 0.012,
    "saturn": 0.009,
    "uranus": 0.007,
    "neptune": 0.005,
}

# Function to calculate distances based on current screen size
def calculate_distances():
    max_radius = min(1200, 800) / 2 - 50  # Subtract some padding for visibility
    distances = {}
    for planet, factor in distance_factors.items():
        distances[planet] = max_radius * factor
    return distances

# Initialize distances
distances = calculate_distances()

# Create a list of stars for the background with higher density
def create_stars(num_stars):
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, 1200)
        y = random.randint(0, 800)
        stars.append((x, y))
    return stars

# Draw stars on the background
def draw_stars(stars):
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), star, 1)

# Draw the orbit for each planet
def draw_orbit(distance):
    pygame.draw.circle(screen, (100, 100, 100), (600, 400), int(distance), 1)  # Semi-transparent grey

# Draw labels for each planet
def draw_labels(text, position):
    font = pygame.font.SysFont("Arial", 20)
    label = font.render(text, True, (255, 255, 255))  # White text
    screen.blit(label, position)

# Main loop
def main():
    global screen, distances  # Access the screen and distances globally

    clock = pygame.time.Clock()
    running = True
    angles = {planet: 0 for planet in distance_factors.keys()}  # Initialize angles for rotation
    stars = create_stars(300)  # Increased number of stars for a richer background

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:  # Handle window resizing
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                distances = calculate_distances()  # Recalculate distances for orbits
                stars = create_stars(300)  # Recreate stars with the new screen size

        screen.fill((0, 0, 0))  # Clear the screen

        draw_stars(stars)  # Draw stars

        # Draw the sun
        sun_x = 600 - planets["sun"].get_width() // 2
        sun_y = 400 - planets["sun"].get_height() // 2
        screen.blit(planets["sun"], (sun_x, sun_y))  # Center sun

        # Draw orbits and planets
        for planet in distances.keys():
            # Draw the orbit
            draw_orbit(distances[planet])

            # Calculate the planet's position
            x = 600 + distances[planet] * math.cos(angles[planet]) - planets[planet].get_width() // 2
            y = 400 + distances[planet] * math.sin(angles[planet]) - planets[planet].get_height() // 2

            # Draw the planet
            screen.blit(planets[planet], (x, y))

            # Draw the labels for each planet
            label_pos = (x, y + planets[planet].get_height() + 5)
            draw_labels(planet.capitalize(), label_pos)

            # Update angle for the next frame
            angles[planet] += speeds[planet]

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Control the frame rate

    pygame.quit()

if __name__ == "__main__":
    main()
