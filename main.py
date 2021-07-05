# Imports the Pygame module.
import pygame
# Imports the constants of Pygame to improve readability.
from pygame.locals import *
# Imports the random module to generate random numbers
from random import randint

# Initialize the Pygame font module.
pygame.font.init()
# Initialize the Pygame music module.
pygame.mixer.init()

# Set the information for the screen.
WIDTH = 1200
HEIGHT = 800
MID_WIDTH = WIDTH // 2
MID_HEIGHT = HEIGHT // 2

# Assigns custom RGB values for each color used.
RED = (230, 60, 80)
YELLOW = (230, 210, 60)
GREEN = (60, 230, 110)
BLUE = (60, 80, 230)

# Setup Variables
stage = "menu"

last_click = ()
countdown = 3

# Loads and resizes the menu images.
play = pygame.image.load("Images/Menu/play.png")
play = pygame.transform.scale(play, (75, 75))

settings = pygame.image.load("Images/Menu/settings.png")
settings = pygame.transform.scale(settings, (75, 75))

# Loads and resizes the player images.
red_player = pygame.image.load("Images/Players/red_player.png")
red_player = pygame.transform.scale(red_player, (50, 50))

yellow_player = pygame.image.load("Images/Players/yellow_player.png")
yellow_player = pygame.transform.scale(yellow_player, (50, 50))

green_player = pygame.image.load("Images/Players/green_player.png")
green_player = pygame.transform.scale(green_player, (50, 50))

blue_player = pygame.image.load("Images/Players/blue_player.png")
blue_player = pygame.transform.scale(blue_player, (50, 50))

# Loads and resizes the selection images.
red_logo = pygame.image.load("Images/Selection/red_logo.png")
# yellow_logo = pygame.image.load("Images/Selection/yellow_logo.png")

green_logo = pygame.image.load("Images/Selection/green_logo.png")
green_logo = pygame.transform.scale(green_logo, (100, 100))

# blue_logo = pygame.image.load("Images/Selection/blue_logo.png")

# Loads all of the sounds.
click = pygame.mixer.Sound("Sounds/click.mp3")
countdown_sound = pygame.mixer.Sound("Sounds/countdown.wav")


def button_clicked(rect_object, circle=False):
    return event.pos[0] in range(rect_object.left, rect_object.right + 1) and \
           event.pos[1] in range(rect_object.top, rect_object.bottom + 1)


# This is the function to draw the bases.
def draw_bases():
    red_base = pygame.draw.rect(screen, RED, (0, 0, WIDTH // 2, HEIGHT // 2))
    yellow_base = pygame.draw.rect(screen, YELLOW, (MID_WIDTH, 0, WIDTH // 2, HEIGHT // 2))
    green_base = pygame.draw.rect(screen, GREEN, (MID_WIDTH, MID_HEIGHT, WIDTH // 2, HEIGHT // 2))
    blue_base = pygame.draw.rect(screen, BLUE, (0, MID_HEIGHT, WIDTH // 2, HEIGHT // 2))
    globals().update(locals())


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
    # settings_button = screen.blit(settings, (WIDTH // 2 - play.get_width() // 2, HEIGHT // 2 - play.get_height() // 2))
    return start_button


def display_selection():
    draw_bases()

    pygame.draw.rect(screen, "white", (100, 300, 1000, 300), border_radius=10)

    # Displays the team choices.
    red_choice = screen.blit(red_logo, (WIDTH // 5 - 50, HEIGHT // 2 - 50))
    yellow_choice = pygame.draw.circle(screen, YELLOW, (WIDTH // 5 * 2, HEIGHT // 2), 50)
    green_choice = screen.blit(green_logo, (WIDTH // 5 * 3 - 50, HEIGHT // 2 - 50))
    blue_choice = pygame.draw.circle(screen, BLUE, (WIDTH // 5 * 4, HEIGHT // 2), 50)

    # Displays the text of the selection.
    display_text("Choose Your Team", WIDTH // 2, HEIGHT // 10, "white", 60, True)
    display_text("Team Red", WIDTH // 5, HEIGHT // 3 * 2, RED, 30, True)
    display_text("Team Yellow", WIDTH // 5 * 2, HEIGHT // 3 * 2, YELLOW, 30, True)
    display_text("Team Green", WIDTH // 5 * 3, HEIGHT // 3 * 2, GREEN, 30, True)
    display_text("Team Blue", WIDTH // 5 * 4, HEIGHT // 3 * 2, BLUE, 30, True)

    return red_choice, yellow_choice, green_choice, blue_choice


def display_countdown():
    global countdown, stage
    # Starts
    if countdown == 3:
        countdown_sound.play()
    # Displays the current countdown time.
    display_text(str(countdown), MID_WIDTH, MID_HEIGHT, "white", 100, True)
    # Decreases the countdown by one second.
    countdown -= 1

    if countdown == -1:
        # Switches to the main game.
        stage = "main"


# This is the function to display the main game.
def display_main():
    # Draws the four bases.
    draw_bases()
    # Draws the team members for each team.
    teams["red"].display_team()
    teams["yellow"].display_team()
    teams["green"].display_team()
    teams["blue"].display_team()

    # Iterate through each pressed key and move the player accordingly.
    keys = pygame.key.get_pressed()
    if keys[K_w] or keys[K_UP]:
        teams[team].move_player(player_number, 0, 1)
    if keys[K_a] or keys[K_LEFT]:
        teams[team].move_player(player_number, -1, 0)
    if keys[K_s] or keys[K_DOWN]:
        teams[team].move_player(player_number, 0, -1)
    if keys[K_d] or keys[K_RIGHT]:
        teams[team].move_player(player_number, 1, 0)

    for teammate in teams.values():
        pass


# Creates a button class to easily create buttons.
class Button:
    def __init__(self, x, y, width, height, color):
        self.button = pygame.draw.rect(screen, color, (x, y, width, height))

    def update(self, position, value):
        if self.button.collidepoint(position):
            return value


# Creates a class to easily create teams.
class Team:
    def __init__(self, name, size=6):
        self.name = name
        self.size = size

        self.base = globals()[self.name + "_base"]
        self.image = globals()[self.name + "_player"]

        self.data = {player_id + 1: Rect(randint(self.base.left, self.base.right - 50),
                                         randint(self.base.top, self.base.bottom - 50), 50, 50)
                     for player_id in range(self.size)}

    def __repr__(self):
        return f"{list(self.data.items())}"

    def add_player(self, rect_object=Rect(0, 0, 50, 50)):
        self.size += 1
        self.data[self.size] = rect_object

    def remove_player(self, player):
        self.size -= 1
        self.data.pop(player)
        self.data = {player_id - (player_id > player): rect_object for player_id, rect_object in self.data.items()}

    def display_team(self, reset_pos=False):
        if reset_pos:
            self.data = {player_id + 1: Rect(randint(0, WIDTH // 2 - 50), randint(0, HEIGHT // 2 - 50), 50, 50)
                         for player_id in range(self.size)}

        for rect_object in self.data.values():
            screen.blit(self.image, rect_object.topleft)

    def move_player(self, player_id, x_change=0, y_change=0):
        self.data[player_id].x += x_change
        self.data[player_id].y -= y_change
        # return self.data[player_id]


# Setups the Pygame window with a width of 1200 pixels and a height of 800 pixels.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Sets an appropriate caption for the game.
pygame.display.set_caption("Base Wars")

# Draws the bases as the background for the menu.
draw_bases()

# Creates a clock to control the frame rate.
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
                # If we are in the menu page.
                if stage == "menu":
                    if button_clicked(play_button):
                        stage = "selection"
                        click.play()
                # If we are in the selection page.
                elif stage == "selection":
                    if button_clicked(red_button):
                        team = "red"
                        stage = "countdown"
                        player_number = randint(1, 6)
                    elif button_clicked(yellow_button):
                        team = "yellow"
                        stage = "countdown"
                        player_number = randint(1, 6)
                    elif button_clicked(green_button):
                        team = "green"
                        stage = "countdown"
                        player_number = randint(1, 6)
                    elif button_clicked(blue_button):
                        team = "blue"
                        stage = "countdown"
                        player_number = randint(1, 6)

    # Creates a screen based on the stage
    if stage == "main":
        display_main()
    elif stage == "countdown":
        draw_bases()
        display_countdown()
        # If the countdown is over.
        if countdown == 0:
            # Setup each team using the Team class.
            teams = {"red": Team("red"), "yellow": Team("yellow"), "green": Team("green"), "blue": Team("blue")}
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
