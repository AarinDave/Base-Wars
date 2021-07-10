# Imports the Pygame module.
import pygame
# Imports the constants of Pygame to improve readability.
from pygame.locals import *
# Imports the random module to generate random numbers and values.
from random import choice, randint

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

# Set the values the game will use.
SPEED = 1

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
blue_logo = pygame.image.load("Images/Selection/blue_logo.png")

# Loads all of the sounds.
click = pygame.mixer.Sound("Sounds/click.mp3")
countdown_sound = pygame.mixer.Sound("Sounds/countdown.wav")


def button_clicked(rect_object):
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
    # settings_button = screen.blit(settings, (WIDTH // 2 - settings.get_width() // 2, HEIGHT // 2 - settings.get_height() // 2))
    return start_button


def display_selection():
    pygame.draw.rect(screen, "white", (100, 300, 1000, 300), border_radius=10)

    # Displays the team choices.
    red_choice = screen.blit(red_logo, (WIDTH // 5 - 50, HEIGHT // 2 - 50))
    yellow_choice = pygame.draw.circle(screen, YELLOW, (WIDTH // 5 * 2, HEIGHT // 2), 50)
    green_choice = screen.blit(green_logo, (WIDTH // 5 * 3 - 50, HEIGHT // 2 - 50))
    blue_choice = screen.blit(blue_logo, (WIDTH // 5 * 4 - 50, HEIGHT // 2 - 50))

    # Displays the text of the selection.
    display_text("Choose Your Team", WIDTH // 2, HEIGHT // 10, "white", 60, True)
    display_text("Team Red", WIDTH // 5, HEIGHT // 3 * 2, RED, 30, True)
    display_text("Team Yellow", WIDTH // 5 * 2, HEIGHT // 3 * 2, YELLOW, 30, True)
    display_text("Team Green", WIDTH // 5 * 3, HEIGHT // 3 * 2, GREEN, 30, True)
    display_text("Team Blue", WIDTH // 5 * 4, HEIGHT // 3 * 2, BLUE, 30, True)

    return red_choice, yellow_choice, green_choice, blue_choice


# This is the function to display the main game.
def display_main():
    global player_team, player_number

    # Draws the team members for each team.
    for attacking_team in teams:
        teams[attacking_team].display()
        teams[attacking_team].set_targets()

    # Iterate through each pressed key and move the player accordingly.
    keys = pygame.key.get_pressed()
    # If the up arrow key or w key is pressed.
    if keys[K_w] or keys[K_UP]:
        teams[player_team].move(player_number, 0, SPEED)
    # If the left arrow key or a key is pressed.
    if keys[K_a] or keys[K_LEFT]:
        teams[player_team].move(player_number, -SPEED, 0)
    # If the down arrow key or s key is pressed.
    if keys[K_s] or keys[K_DOWN]:
        teams[player_team].move(player_number, 0, -SPEED)
    # If the right arrow key or d key is pressed.
    if keys[K_d] or keys[K_RIGHT]:
        teams[player_team].move(player_number, SPEED, 0)

    infected_players = {team: [] for team in teams}

    # Iterate through each team.
    for attacking_team in teams.values():
        # Iterate through each player of that team.
        for ai_id, ai_rect in attacking_team.players.items():
            # Checks if the current player is not the user.
            if (attacking_team.name, ai_id) != (player_team, player_number):
                # Identify the target player.
                target_team, target_id = attacking_team.targets[ai_id - 1]
                target_rect = teams[target_team].players[target_id]

                # Moves the player according to the position of the target player.
                attacking_team.move(ai_id,
                                    SPEED if ai_rect.x < target_rect.x else -SPEED,
                                    SPEED if ai_rect.y < target_rect.y else -SPEED)

                for team_to_check_collision in teams.values():
                    if team_to_check_collision.name != attacking_team.name:
                        teammates = team_to_check_collision.players.copy()
                        collided = ai_rect.collidedict(teammates, True)
                        if collided:
                            information = (team_to_check_collision.name, *collided)
                            if information not in infected_players[attacking_team.name]:
                                infected_players[attacking_team.name].append(information)

    for team, targets in infected_players.items():
        for target_team, target_id, target_rect in targets:
            if (target_team, target_id) == (player_team, player_number):
                player_team = target_team
                player_number = target_id
            teams[team].add(target_rect)
            teams[target_team].remove(target_id)


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

        self.players = {player_id + 1: Rect(randint(self.base.left, self.base.right - 50),
                                            randint(self.base.top, self.base.bottom - 50), 50, 50)
                        for player_id in range(self.size)}

        self.other_teams = {}
        self.targets = []

    def __repr__(self):
        return f"{list(self.players.items())}"

    def __str__(self):
        return self.name

    def add(self, rect_object):
        self.size += 1
        self.players[self.size] = rect_object

        #
        random_team = choice(sorted(self.other_teams))
        random_player = randint(1, teams[random_team].size)
        self.targets.append((random_team, random_player))

    def remove(self, player):
        self.size -= 1
        rect_object = self.players.pop(player)
        self.players = {player_id - (player_id > player): rect_object
                        for player_id, rect_object in self.players.items()}
        return rect_object

    def display(self, reset_pos=False):
        if reset_pos:
            self.players = {player_id + 1: Rect(randint(0, WIDTH // 2 - 50), randint(0, HEIGHT // 2 - 50), 50, 50)
                            for player_id in range(self.size)}

        for ai_id, rect_object in self.players.items():
            screen.blit(self.image, rect_object.topleft)
            if (self.name, ai_id) == (player_team, player_number):
                display_text(f"You", *rect_object.midtop, "yellow", 15, True)
            else:
                display_text(f"Player {ai_id}", *rect_object.midtop, "white", 15, True)

    def move(self, player_id, x_change, y_change):
        self.players[player_id].x += x_change
        self.players[player_id].y -= y_change
        # return self.data[player_id]

    def set_targets(self):
        self.other_teams = {team: teams[team].size for team in teams if team != player_team}

        # If there currently are targets.
        if self.targets:
            targets = []
            for target_team, target_id in self.targets:
                if teams[target_team].size < target_id:
                    target_id = randint(1, teams[target_team].size)
                targets.append((target_team, target_id))
            self.targets = targets.copy()

        # If there are no targets.
        else:
            for _ in range(self.size):
                random_team = choice(sorted(self.other_teams))
                random_player = randint(1, teams[random_team].size)
                self.targets.append((random_team, random_player))


# Setups the Pygame window with a width of 1200 pixels and a height of 800 pixels.
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Sets an appropriate caption for the game.
pygame.display.set_caption("Base Wars")

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
                        player_team = "red"
                        stage = "countdown"
                    elif button_clicked(yellow_button):
                        player_team = "yellow"
                        stage = "countdown"
                    elif button_clicked(green_button):
                        player_team = "green"
                        stage = "countdown"
                    elif button_clicked(blue_button):
                        player_team = "blue"
                        stage = "countdown"

    # Draws the four bases.
    draw_bases()

    # Creates a screen based on the stage
    if stage == "main":
        display_main()

    elif stage == "countdown":
        # If we started the countdown.
        if countdown == 3:
            # Start the countdown sound.
            countdown_sound.play()
        # Displays the current countdown time.
        display_text(str(countdown) if countdown > 0 else "GO", MID_WIDTH, MID_HEIGHT, "white", 100, True)
        # If the countdown falls below 0.
        if countdown == -1:
            # Setup each team using the Team class.
            teams = {"red": Team("red"), "yellow": Team("yellow"), "green": Team("green"), "blue": Team("blue")}
            # Chooses a random player in the team.
            player_number = randint(1, teams[player_team].size)
            # Switches to the main game.
            stage = "main"
        # Decreases the countdown by one second.
        countdown -= 1

    elif stage == "selection":
        red_button, yellow_button, green_button, blue_button = display_selection()

    elif stage == "menu":
        play_button = display_menu()

    # Updates the screen to show the current state.
    pygame.display.update()

    # Slows down the game to 90 frames per second.
    if stage == "main":
        clock.tick(90)
    # Slows down the countdown to 1 frame per second.
    elif stage == "countdown":
        clock.tick(1)
    # Sets the frame rate to the maximum at everywhere else.
    else:
        clock.tick()
