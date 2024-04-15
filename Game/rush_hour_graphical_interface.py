import pygame
import sys
from rush_hour import easy_load, medium_load, hard_load

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 720, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rush Hour")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
LIGHT_BLUE = (173, 216, 230)
DARK_GREEN = (0, 100, 0)

# Fonts
font = pygame.font.Font("upheavtt.ttf", 25)
font_overline = pygame.font.Font("upheavtt.ttf", 27)
title_font = pygame.font.Font("SwipeRaceDemo.ttf", 45)
title_overline = pygame.font.Font("SwipeRaceDemo.ttf", 45)

background = pygame.image.load("park.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Button class
class Button:
    def __init__(self, x, y, width, height, color, text, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        
         # Draw overline
        pygame.draw.line(surface, WHITE, (self.rect.left, self.rect.top), (self.rect.right, self.rect.top), 3)
        pygame.draw.line(surface, WHITE, (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.bottom), 3)
        pygame.draw.line(surface, WHITE, (self.rect.left, self.rect.top), (self.rect.left, self.rect.bottom), 3)
        pygame.draw.line(surface, WHITE, (self.rect.right, self.rect.top), (self.rect.right, self.rect.bottom), 3)
        
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


    def clicked(self):
        if self.action:
            self.action()


# Function to display rules
def display_rules():
    screen.blit(background, (0, 0))
    
    title_text = title_font.render("RUSH HOUR", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_text, title_rect)
    title_text_overline = title_overline.render("RUSH HOUR", True, WHITE)
    title_rect_overline = title_text_overline.get_rect(center=((WIDTH // 2)-5, 100))
    screen.blit(title_text_overline, title_rect_overline)
    
    screen.blit(title_text, title_rect)
    
    rules_text = [
        "1. Move vehicles horizontally or vertically",  "to clear a path for the red car to exit.",
        "2. Vehicles can only move in their", "allowed directions (up/down or left/right).",
        "3. You win the game when the red car (XX)",  "can exit through the rightmost exit.",
        "4. Use the arrows to move the vehicles.", "Click 'Play' to start the game.",
    ]

    rules_text_overline = [
        "1. Move vehicles horizontally or vertically",  "to clear a path for the red car to exit.",
        "2. Vehicles can only move in their", "allowed directions (up/down or left/right).",
        "3. You win the game when the red car (XX)",  "can exit through the rightmost exit.",
        "4. Use the arrows to move the vehicles.", "Click 'Play' to start the game.",
    ]

    y_offset = 200  # Adjusted vertical offset for rules text
    for text in rules_text_overline:
        text_surf = font.render(text, True, WHITE)
        screen.blit(text_surf, (50, y_offset))
        y_offset += 40
    back_button.draw(screen)

    y_offset = 200  # Adjusted vertical offset for rules text
    for text in rules_text:
        text_surf = font.render(text, True, BLACK)
        screen.blit(text_surf, (50, y_offset))
        y_offset += 40
    back_button.draw(screen)

    pygame.display.update()

# Function to display the levels menu
def display_levels():
    screen.blit(background, (0, 0))
    
    title_text = title_font.render("RUSH HOUR", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_text, title_rect)
    title_text_overline = title_overline.render("RUSH HOUR", True, WHITE)
    title_rect_overline = title_text_overline.get_rect(center=((WIDTH // 2)-5, 100))
    screen.blit(title_text_overline, title_rect_overline)
    
    screen.blit(title_text, title_rect)

    for button in levels_buttons:
        button.draw(screen)
    
    back_button.draw(screen)
    pygame.display.flip()

# Function to display the main menu
def display_main_menu():
    screen.blit(background, (0, 0))
    # Title text
    title_text = title_font.render("RUSH HOUR", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_text, title_rect)
    title_text_overline = title_overline.render("RUSH HOUR", True, WHITE)
    title_rect_overline = title_text_overline.get_rect(center=((WIDTH // 2)-5, 100))
    screen.blit(title_text_overline, title_rect_overline)
    
    screen.blit(title_text, title_rect)
    # Draw buttons
    for button in buttons:
        button.draw(screen)
    pygame.display.flip()

# Function to close the program
def close_game():
    pygame.quit()
    sys.exit()

def start_game():
    global levels_displayed
    levels_displayed = True  # Set levels_displayed to True to display the levels menu
    display_levels()

# Function to go back to the main menu
def back_to_menu():
    global rules_displayed, levels_displayed, mode_displayed
    if rules_displayed:
        rules_displayed = False
        display_main_menu()
    elif levels_displayed:
        levels_displayed = False
        display_main_menu()
    elif mode_displayed:
        mode_displayed = False
        display_levels()


# Buttons
rules_button = Button(260, 250, 200, 50, ORANGE, "Rules", WHITE, display_rules)
play_button = Button(260, 350, 200, 50, ORANGE, "Play", WHITE, start_game)
exit_button = Button(260, 450, 200, 50, ORANGE, "Exit", WHITE, close_game)
back_button = Button(260, 580, 200, 50, BLUE, "Back to Menu", WHITE, back_to_menu)
easy_button = Button(260, 200, 200, 50, ORANGE, "Easy", WHITE, easy_load)
medium_button = Button(260, 300, 200, 50, ORANGE, "Medium", WHITE, medium_load)
hard_button = Button(260, 400, 200, 50, ORANGE, "Hard", WHITE, hard_load)
return_button = Button(260, 400, 200, 50, BLUE, "Return", WHITE, back_to_menu)

buttons = [rules_button, play_button, exit_button]
levels_buttons = [easy_button, medium_button, hard_button]

# Main loop
running = True
rules_displayed = False  # Variable to track if rules are displayed
levels_displayed = False 
mode_displayed = False

while running:
    screen.blit(background, (0, 0))
    
    # Title text
    title_text = title_font.render("RUSH HOUR", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(title_text, title_rect)
    title_text_overline = title_overline.render("RUSH HOUR", True, WHITE)
    title_rect_overline = title_text_overline.get_rect(center=((WIDTH // 2)-5, 100))
    screen.blit(title_text_overline, title_rect_overline)
    
    screen.blit(title_text, title_rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit the loop when the X button is clicked
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not rules_displayed:  # Only handle button clicks if rules are not displayed
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            button.clicked()
                            if button == rules_button:
                                rules_displayed = True
                                break  # Exit the loop after handling the click
                elif not levels_displayed:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            button.clicked()
                            if button == play_button:
                                levels_displayed = True
                                break 
    
    if rules_displayed:
        display_rules()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_button.rect.collidepoint(event.pos):
                        back_button.clicked()
                        rules_displayed = False  # Set rules_displayed to False after returning to main menu
                        pygame.display.update()

    elif levels_displayed:
        display_levels()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if easy_button.rect.collidepoint(event.pos):
                        easy_button.clicked()
                        levels_displayed = False
                        easy_load()

                    elif medium_button.rect.collidepoint(event.pos):
                        medium_button.clicked()
                        levels_displayed = False
                        medium_load()
                
                    if hard_button.rect.collidepoint(event.pos):
                        hard_button.clicked()
                        levels_displayed = False
                        hard_load()

                    if back_button.rect.collidepoint(event.pos):
                        back_button.clicked()
                        levels_displayed = False 
                        pygame.display.update()



    else:
        for button in buttons:
            button.draw(screen)
        pygame.display.update()

pygame.quit()
sys.exit()
