import pygame
import sys
import csv
import os
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Traffic Flow Simulation System")

# Colors
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 36)

# Traffic signal
signal_green = True
signal_timer = 0

# Vehicle spawning
spawn_timer = 0
spawn_delay = 90

# Create CSV file
if not os.path.exists("traffic_data.csv"):

    with open("traffic_data.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "vehicle_count",
            "signal_status",
            "signal_timer"
        ])

# Car class
class Car:

    def __init__(self, x, y, color, speed):

        self.x = x
        self.y = y
        self.width = 50
        self.height = 25
        self.color = color
        self.speed = speed

    def move(self, vehicles):

        global signal_green

        safe_distance = 70

        # Collision avoidance
        for vehicle in vehicles:

            if vehicle == self:
                continue

            if abs(vehicle.y - self.y) < 10:

                if vehicle.x > self.x and vehicle.x - self.x < safe_distance:
                    return

        # Stop line
        stop_line = 500

        # Stop at red signal
        if self.x + self.width < stop_line or signal_green:
            self.x += self.speed

    def draw(self):

        pygame.draw.rect(
            screen,
            self.color,
            (self.x, self.y, self.width, self.height)
        )

# Ambulance class
class Ambulance(Car):

    def __init__(self, x, y):

        super().__init__(x, y, PURPLE, 6)

        self.width = 65
        self.height = 30

# Vehicle lists
cars = []
ambulances = []

# Road lanes
lanes = [320, 360]

# Main loop
while True:

    # Background
    screen.fill(WHITE)

    # Draw roads
    pygame.draw.rect(screen, GRAY, (0, 280, WIDTH, 140))
    pygame.draw.rect(screen, GRAY, (530, 0, 140, HEIGHT))

    # Horizontal lane markings
    for i in range(0, WIDTH, 50):

        pygame.draw.rect(
            screen,
            WHITE,
            (i, 348, 25, 4)
        )

    # Vertical lane markings
    for i in range(0, HEIGHT, 50):

        pygame.draw.rect(
            screen,
            WHITE,
            (598, i, 4, 25)
        )

    # Spawn normal vehicles
    spawn_timer += 1

    if spawn_timer > spawn_delay and len(cars) < 20:

        colors = [BLUE, RED, GREEN, ORANGE, BLACK, YELLOW]

        lane = random.choice(lanes)

        speed = random.randint(2, 5)

        new_car = Car(
            -100,
            lane,
            random.choice(colors),
            speed
        )

        cars.append(new_car)

        spawn_timer = 0

    # Spawn ambulance randomly
    if random.randint(1, 900) == 1:

        ambulance = Ambulance(
            -150,
            320
        )

        ambulances.append(ambulance)

    # Vehicle count
    vehicle_count = len(cars) + len(ambulances)

    # Emergency vehicle detection
    emergency_active = False

    for ambulance in ambulances:

        if 250 < ambulance.x < 550:

            emergency_active = True

    # AI Dynamic Signal Timing
    if vehicle_count > 12:
        green_duration = 600

    elif vehicle_count > 6:
        green_duration = 400

    else:
        green_duration = 250

    # Signal timer
    signal_timer += 1

    # Emergency priority
    if emergency_active:

        signal_green = True
        signal_timer = 0

    elif signal_timer > green_duration:

        signal_green = not signal_green
        signal_timer = 0

    # Draw traffic signal
    if signal_green:

        pygame.draw.circle(
            screen,
            GREEN,
            (500, 250),
            18
        )

    else:

        pygame.draw.circle(
            screen,
            RED,
            (500, 250),
            18
        )

    # Move normal vehicles
    for car in cars[:]:

        car.move(cars)
        car.draw()

        # Remove off-screen vehicles
        if car.x > WIDTH + 100:

            cars.remove(car)

    # Move ambulances
    for ambulance in ambulances[:]:

        ambulance.move(ambulances)
        ambulance.draw()

        # Remove off-screen ambulance
        if ambulance.x > WIDTH + 100:

            ambulances.remove(ambulance)

    # Save traffic data
    with open("traffic_data.csv", "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            vehicle_count,
            int(signal_green),
            signal_timer
        ])

    # Dashboard text
    vehicle_text = font.render(
        f"Vehicles: {vehicle_count}",
        True,
        BLACK
    )

    screen.blit(vehicle_text, (20, 20))

    signal_text = font.render(
        f"Signal: {'GREEN' if signal_green else 'RED'}",
        True,
        BLACK
    )

    screen.blit(signal_text, (20, 60))

    ai_text = font.render(
        "AI Smart Traffic Control Active",
        True,
        BLACK
    )

    screen.blit(ai_text, (20, 100))

    # Emergency alert
    if emergency_active:

        emergency_text = font.render(
            "Emergency Vehicle Priority ACTIVE",
            True,
            RED
        )

        screen.blit(emergency_text, (20, 140))

    # Instructions
    instruction_text = font.render(
        "Traffic Simulation Running",
        True,
        BLACK
    )

    screen.blit(instruction_text, (20, 180))

    # Handle events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

    # Update display
    pygame.display.update()

    # FPS
    clock.tick(60)