# Import Modules
import pygame
from pygame.locals import *
from math import sqrt
from random import randint

# Initialize Pygame Modules
pygame.font.init()

# Assign Constants
WIDTH = 1200
HEIGHT = 800
MID_WIDTH = WIDTH // 2
MID_HEIGHT = HEIGHT // 2

RED = (230, 60, 80)
YELLOW = (230, 210, 60)
GREEN = (60, 230, 110)
BLUE = (60, 80, 230)

# Setup Variables
last_click = ()
stage = "menu"
countdown = 3
team = ""
player_number = randint(1, 6)

# Define Functions


def button_clicked(rect_object, circle=False):
    if circle:
        distance = sqrt((event.pos[0] - rect_object.centerx) ** 2 + (event.pos[1] - rect_object.centery) ** 2)
        return distance <= rect_object.width / 2
    else:
        return event.pos[0] in range(rect_object.left, rect_object.right+1) and \
               event.pos[1] in range(rect_object.top, rect_object.bottom+1)


def draw_bases():
    pygame.draw.rect(screen, RED, (0, 0, WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, YELLOW, (MID_WIDTH, 0, WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, GREEN, (MID_WIDTH, MID_HEIGHT, WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, BLUE, (0, MID_HEIGHT, WIDTH // 2, HEIGHT // 2))


def display_text(text, x, y, color, size, center=False):
    font_object = pygame.font.Font("/System/Library/Fonts/Avenir Next.ttc", size)
    text_object = font_object.render(text, False, color)
    if center:
        screen.blit(text_object, (x - text_object.get_width() // 2, y - text_object.get_height() // 2))
    else:
        screen.blit(text_object, (x, y))


def display_menu():
    padding = 15

    display_text("Base Wars", WIDTH // 2, HEIGHT // 5, "white", 60, True)
    start_button = pygame.draw.rect(screen, (35, 171, 84), (WIDTH // 2 - 25, HEIGHT // 2 - 25, 50, 50))
    pygame.draw.polygon(screen, "white",
                        ((start_button.left + padding, start_button.top + padding),
                         (start_button.left + padding, start_button.bottom - padding),
                         (start_button.right - padding, start_button.centery)))
    return start_button


def display_selection():
    # Buttons
    red_choice = pygame.draw.circle(screen, RED, (WIDTH // 5, HEIGHT // 2), 50, True)  # Red
    yellow_choice = pygame.draw.circle(screen, YELLOW, (WIDTH // 5 * 2, HEIGHT // 2), 50, True)  # Yellow
    green_choice = pygame.draw.circle(screen, GREEN, (WIDTH // 5 * 3, HEIGHT // 2), 50, True)  # Green
    blue_choice = pygame.draw.circle(screen, BLUE, (WIDTH // 5 * 4, HEIGHT // 2), 50, True)  # Blue

    # Text
    display_text("Choose Your Team", WIDTH // 2, HEIGHT // 10, "white", 60, True)
    display_text("Team Red", WIDTH // 5, HEIGHT // 3 * 2, RED, 30, True)  # Red
    display_text("Team Yellow", WIDTH // 5 * 2, HEIGHT // 3 * 2, YELLOW, 30, True)  # Yellow
    display_text("Team Green", WIDTH // 5 * 3, HEIGHT // 3 * 2, GREEN, 30, True)  # Green
    display_text("Team Blue", WIDTH // 5 * 4, HEIGHT // 3 * 2, BLUE, 30, True)  # Blue
    return red_choice, yellow_choice, green_choice, blue_choice


def display_countdown():
    global countdown, stage

    display_text(str(countdown), MID_WIDTH, MID_HEIGHT, "white", 100, True)
    countdown -= 1

    if countdown == -1:
        stage = "main"


def display_main():
    draw_bases()


# Classes


class Team:
    def __init__(self, name, size=6):
        self.name = name.title()
        self.size = size
        self.data = {player_id: Rect(0, 0, 0, 0) for player_id in range(1, size+1)}

    def __repr__(self):
        return f"Team {self.name}\n" + \
               "\n".join(f"{player_id}: {rect_object}" for player_id, rect_object in self.data.items())

    def add_player(self, rect_object=Rect(0, 0, 0, 0)):
        self.size += 1
        self.data[self.size] = rect_object

    def remove_player(self, player):
        self.size -= 1
        self.data.pop(player)
        self.data = {player_id - (player_id > player): rect_object for player_id, rect_object in self.data.items()}

    def reset_position(self):
        pass


# Setup Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Base Wars")

# Create a Clock
clock = pygame.time.Clock()

# Game Loop
while True:

    # Event Loop
    for event in pygame.event.get():

        # Quit Button
        if event.type == QUIT:
            quit()

        # Mouse Clicked
        elif event.type == MOUSEBUTTONDOWN:
            last_click = event.pos

        # Mouse Released
        elif event.type == MOUSEBUTTONUP:
            if event.pos == last_click:
                if stage == "menu":
                    if button_clicked(play_button):
                        stage = "selection"
                elif stage == "selection":
                    if button_clicked(red_button):
                        team = "red"
                        stage = "countdown"
                    elif button_clicked(yellow_button):
                        team = "yellow"
                        stage = "countdown"
                    elif button_clicked(green_button):
                        team = "green"
                        stage = "countdown"
                    elif button_clicked(blue_button):
                        team = "blue"
                        stage = "countdown"

        # Key Released
        elif event.type == KEYUP:
            if event.key in [K_UP, K_w]:
                pass
            elif event.key in [K_DOWN, K_s]:
                pass
            if event.key in [K_LEFT, K_a]:
                pass
            elif event.key in [K_RIGHT, K_d]:
                pass

    # Fills Screen
    screen.fill("gray")

    # Creates a screen based on the stage
    if stage == "main":
        display_main()
    elif stage == "countdown":
        draw_bases()
        display_countdown()
    elif stage == "selection":
        red_button, yellow_button, green_button, blue_button = display_selection()
    elif stage == "menu":
        play_button = display_menu()

    # Updates Screen
    pygame.display.update()

    if stage == "countdown":
        clock.tick(1)
    else:
        clock.tick()
