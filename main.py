# Imports the Pygame module
import pygame
# Imports the constants of Pygame to improve readability.
from pygame.locals import *
# Imports the random module to generate random numbers
from random import randint

# Initialize the Pygame font module.
pygame.font.init()
# Initialize the Pygame mixer module.
pygame.mixer.init()

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
stage = "menu"

last_click = ()
countdown = 3

team = ""
player_number = randint(1, 6)

# Load all of the images.
play = pygame.image.load("Images/play.png")
play = pygame.transform.scale(play, (75, 75))

# Load all of the sounds.
click = pygame.mixer.Sound("Sounds/click.mp3")
countdown_sound = pygame.mixer.Sound("Sounds/countdown.wav")

# Define Functions


def button_clicked(rect_object, circle=False):
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


# This is the function to display the menu.
def display_menu():
    # Displays the title
    display_text("Base Wars", WIDTH // 2, HEIGHT // 5, "white", 60, True)
    # Displays the play button
    start_button = screen.blit(play, (WIDTH // 2 - play.get_width() // 2, HEIGHT // 2 - play.get_height() // 2))
    return start_button


def display_selection():
    # Buttons
    red_choice = pygame.draw.circle(screen, RED, (WIDTH // 5, HEIGHT // 2), 50)  # Red
    yellow_choice = pygame.draw.circle(screen, YELLOW, (WIDTH // 5 * 2, HEIGHT // 2), 50)  # Yellow
    green_choice = pygame.draw.circle(screen, GREEN, (WIDTH // 5 * 3, HEIGHT // 2), 50)  # Green
    blue_choice = pygame.draw.circle(screen, BLUE, (WIDTH // 5 * 4, HEIGHT // 2), 50)  # Blue

    # Text
    display_text("Choose Your Team", WIDTH // 2, HEIGHT // 10, "white", 60, True)
    display_text("Team Red", WIDTH // 5, HEIGHT // 3 * 2, RED, 30, True)
    display_text("Team Yellow", WIDTH // 5 * 2, HEIGHT // 3 * 2, YELLOW, 30, True)
    display_text("Team Green", WIDTH // 5 * 3, HEIGHT // 3 * 2, GREEN, 30, True)
    display_text("Team Blue", WIDTH // 5 * 4, HEIGHT // 3 * 2, BLUE, 30, True)
    return red_choice, yellow_choice, green_choice, blue_choice


def display_countdown():
    global countdown, stage

    if countdown == 3:
        countdown_sound.play()

    display_text(str(countdown), MID_WIDTH, MID_HEIGHT, "white", 100, True)

    countdown -= 1

    if countdown == -1:
        stage = "main"


def display_main():
    draw_bases()
    red_team.reset_team()


# Classes


class Team:
    def __init__(self, name, size=6):
        self.name = name.title()
        self.size = size

        self.data = {player_id + 1: Rect(randint(0, WIDTH//2-50), randint(0, HEIGHT//2-50), 50, 50) for player_id in
                     range(self.size)}

    def __repr__(self):
        return f"{list(self.data.items())}"

    def add_player(self, rect_object=Rect(0, 0, 0, 0)):
        self.size += 1
        self.data[self.size] = rect_object

    def remove_player(self, player):
        self.size -= 1
        self.data.pop(player)
        self.data = {player_id - (player_id > player): rect_object for player_id, rect_object in self.data.items()}

    def reset_team(self, reset_pos=False):
        if reset_pos:
            self.data = {player_id + 1: Rect(randint(0, WIDTH//2 - 50), randint(0, HEIGHT//2 - 50), 50, 50) for player_id in
                         range(self.size)}
        for rect_object in self.data.values():
            pygame.draw.rect(screen, self.name, rect_object)


# Setup all four teams.
red_team = Team("red")
yellow_team = Team("yellow")
green_team = Team("green")
blue_team = Team("blue")

print(red_team)

# Setups the Pygame window with a width of 1200 pixels and a height of 800 pixels.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Sets an appropriate caption for the game.
pygame.display.set_caption("Base Wars")

# Creates a clock to control the framerate
clock = pygame.time.Clock()

# Starts the game loop which controls all of the game logic.
while True:
    # Iterate through each Pygame event.
    for event in pygame.event.get():
        # If the quit button is clicked.
        if event.type == QUIT:
            quit()
        # If the mouse is pressed.
        elif event.type == MOUSEBUTTONDOWN:
            last_click = event.pos
        # If the mouse is released.
        elif event.type == MOUSEBUTTONUP:
            # If the mouse was pressed and released at the same coordinate.
            if event.pos == last_click:
                if stage == "menu":
                    if button_clicked(play_button):
                        stage = "selection"
                        click.play()
                    elif True:
                        pass
                elif stage == "selection":
                    if button_clicked(red_button):
                        team = red_team
                        stage = "countdown"
                        # click.play()
                    elif button_clicked(yellow_button):
                        team = yellow_team
                        stage = "countdown"
                        click.play()
                    elif button_clicked(green_button):
                        team = green_team
                        stage = "countdown"
                        click.play()
                    elif button_clicked(blue_button):
                        team = blue_team
                        stage = "countdown"
                        click.play()
        # If the key is released.
        elif event.type == KEYUP:
            if event.key in [K_UP, K_w]:
                pass
            elif event.key in [K_DOWN, K_s]:
                pass
            if event.key in [K_LEFT, K_a]:
                pass
            elif event.key in [K_RIGHT, K_d]:
                pass

    # Fills the screen with a solid, gray color
    screen.fill("gray65")

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

    # Sets the frame rate
    if stage == "countdown":
        clock.tick(1)
    else:
        clock.tick()
# Imports the Pygame module
import pygame
# Imports the constants of Pygame to improve readability.
from pygame.locals import *
# Imports the random module to generate random numbers
from random import randint

# Initialize the Pygame font module.
pygame.font.init()
# Initialize the Pygame mixer module.
pygame.mixer.init()

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
stage = "menu"

last_click = ()
countdown = 3

team = ""
player_number = randint(1, 6)

# Load all of the images.
play = pygame.image.load("Images/play.png")
play = pygame.transform.scale(play, (75, 75))

# Load all of the sounds.
click = pygame.mixer.Sound("Sounds/click.mp3")
countdown_sound = pygame.mixer.Sound("Sounds/countdown.wav")

# Define Functions


def button_clicked(rect_object, circle=False):
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


# This is the function to display the menu.
def display_menu():
    # Displays the title
    display_text("Base Wars", WIDTH // 2, HEIGHT // 5, "white", 60, True)
    # Displays the play button
    start_button = screen.blit(play, (WIDTH // 2 - play.get_width() // 2, HEIGHT // 2 - play.get_height() // 2))
    return start_button


def display_selection():
    # Buttons
    red_choice = pygame.draw.circle(screen, RED, (WIDTH // 5, HEIGHT // 2), 50)  # Red
    yellow_choice = pygame.draw.circle(screen, YELLOW, (WIDTH // 5 * 2, HEIGHT // 2), 50)  # Yellow
    green_choice = pygame.draw.circle(screen, GREEN, (WIDTH // 5 * 3, HEIGHT // 2), 50)  # Green
    blue_choice = pygame.draw.circle(screen, BLUE, (WIDTH // 5 * 4, HEIGHT // 2), 50)  # Blue

    # Text
    display_text("Choose Your Team", WIDTH // 2, HEIGHT // 10, "white", 60, True)
    display_text("Team Red", WIDTH // 5, HEIGHT // 3 * 2, RED, 30, True)
    display_text("Team Yellow", WIDTH // 5 * 2, HEIGHT // 3 * 2, YELLOW, 30, True)
    display_text("Team Green", WIDTH // 5 * 3, HEIGHT // 3 * 2, GREEN, 30, True)
    display_text("Team Blue", WIDTH // 5 * 4, HEIGHT // 3 * 2, BLUE, 30, True)
    return red_choice, yellow_choice, green_choice, blue_choice


def display_countdown():
    global countdown, stage

    if countdown == 3:
        countdown_sound.play()

    display_text(str(countdown), MID_WIDTH, MID_HEIGHT, "white", 100, True)

    countdown -= 1

    if countdown == -1:
        stage = "main"


def display_main():
    draw_bases()
    red_team.reset_team()


# Classes


class Team:
    def __init__(self, name, size=6):
        self.name = name.title()
        self.size = size

        self.data = {player_id + 1: Rect(randint(0, WIDTH//2-50), randint(0, HEIGHT//2-50), 50, 50) for player_id in
                     range(self.size)}

    def __repr__(self):
        return f"{list(self.data.items())}"

    def add_player(self, rect_object=Rect(0, 0, 0, 0)):
        self.size += 1
        self.data[self.size] = rect_object

    def remove_player(self, player):
        self.size -= 1
        self.data.pop(player)
        self.data = {player_id - (player_id > player): rect_object for player_id, rect_object in self.data.items()}

    def reset_team(self, reset_pos=False):
        if reset_pos:
            self.data = {player_id + 1: Rect(randint(0, WIDTH//2 - 50), randint(0, HEIGHT//2 - 50), 50, 50) for player_id in
                         range(self.size)}
        for rect_object in self.data.values():
            pygame.draw.rect(screen, self.name, rect_object)


# Setup all four teams.
red_team = Team("red")
yellow_team = Team("yellow")
green_team = Team("green")
blue_team = Team("blue")

print(red_team)

# Setups the Pygame window with a width of 1200 pixels and a height of 800 pixels.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Sets an appropriate caption for the game.
pygame.display.set_caption("Base Wars")

# Creates a clock to control the framerate
clock = pygame.time.Clock()

# Starts the game loop which controls all of the game logic.
while True:
    # Iterate through each Pygame event.
    for event in pygame.event.get():
        # If the quit button is clicked.
        if event.type == QUIT:
            quit()
        # If the mouse is pressed.
        elif event.type == MOUSEBUTTONDOWN:
            last_click = event.pos
        # If the mouse is released.
        elif event.type == MOUSEBUTTONUP:
            # If the mouse was pressed and released at the same coordinate.
            if event.pos == last_click:
                if stage == "menu":
                    if button_clicked(play_button):
                        stage = "selection"
                        click.play()
                    elif True:
                        pass
                elif stage == "selection":
                    if button_clicked(red_button):
                        team = red_team
                        stage = "countdown"
                        # click.play()
                    elif button_clicked(yellow_button):
                        team = yellow_team
                        stage = "countdown"
                        click.play()
                    elif button_clicked(green_button):
                        team = green_team
                        stage = "countdown"
                        click.play()
                    elif button_clicked(blue_button):
                        team = blue_team
                        stage = "countdown"
                        click.play()
        # If the key is released.
        elif event.type == KEYUP:
            if event.key in [K_UP, K_w]:
                pass
            elif event.key in [K_DOWN, K_s]:
                pass
            if event.key in [K_LEFT, K_a]:
                pass
            elif event.key in [K_RIGHT, K_d]:
                pass

    # Fills the screen with a solid, gray color
    screen.fill("gray65")

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

    # Sets the frame rate
    if stage == "countdown":
        clock.tick(1)
    else:
        clock.tick()
