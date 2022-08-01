import pygame

BACKGROUND = "#b0b0b0"
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CELL_COLOR = (176, 176, 176)
HOSPITAL_COLOR = (191, 209, 255)
LINE_WIDTH = 5

image_assets = [
    "person_normal.png",
    "person_vax.png",
    "person_zombie.png",
    "person_half_zombie.png",
    "kill_background.png",
]

# Initialize pygame
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Outbreak!")
pygame.font.init()
my_font = pygame.font.SysFont("Impact", 30)
game_window_dimensions = (1400, 800)
person_dimensions = (20, 60)
pygame.display.set_caption("Outbreak!")
screen.fill(BACKGROUND)

def get_action(GameBoard, pixel_x, pixel_y):
    """
    Get the action that the click represents.
    If the click was on the heal button, returns "heal"
    Else, returns the board coordinates of the click (board_x, board_y) if valid
    Return None otherwise
    """
    # Check if the user clicked on the "heal" icon, return "heal" if so

    # Get the grid (x,y) where the user clicked
    if pixel_x > GameBoard.display_border and pixel_y > GameBoard.display_border:   # Clicking to the top or left of the border will result in a grid value of 0, which is valid
        board_x = int((pixel_x - GameBoard.display_border) / GameBoard.display_cell_dimensions[0])
        board_y = int((pixel_y - GameBoard.display_border) / GameBoard.display_cell_dimensions[1])
        # Return the grid position if it is a valid position on the board
        if (board_x >= 0 and board_x < GameBoard.columns and board_y >= 0 and board_y < GameBoard.rows):
            return (board_x, board_y)
    return None

def run(GameBoard, hasHospital, heal_button, kill_button):
    """
    Draw the screen and return any events.
    """
    screen.fill(BACKGROUND)
    build_grid(GameBoard, hasHospital) # Draw the grid
    #display_buttons(heal_button, kill_button)
    display_people(GameBoard)
    return pygame.event.get()

def display_buttons(heal_button, kill_button):
    display_image(screen, "Assets/kill_" + kill_button + ".png", (), (800, 50))         # draws specified kill button asset
    display_image(screen, "Assets/heal_" + heal_button + ".png", (), (800, 200))        # draws specified heal button asset

def get_events():
    return pygame.event.get()

def display_image(screen, itemStr, dimensions, position):
    """
    Draw an image on the screen at the indicated position.
    """
    v = pygame.image.load(itemStr).convert_alpha()    
    if len(dimensions) != 0:
        v = pygame.transform.scale(v, dimensions)
    screen.blit(v, position)

def build_grid(GameBoard, hasHospital):
    """
    Draw the grid on the screen.
    """
    grid_width = GameBoard.columns * GameBoard.display_cell_dimensions[0]
    grid_height = GameBoard.rows * GameBoard.display_cell_dimensions[1]
    pygame.draw.rect(screen, BLACK, [GameBoard.display_border - LINE_WIDTH, GameBoard.display_border - LINE_WIDTH, LINE_WIDTH, grid_height + (2 * LINE_WIDTH)])  # left
    pygame.draw.rect(screen, BLACK, [GameBoard.display_border + grid_width, GameBoard.display_border - LINE_WIDTH, LINE_WIDTH, grid_height + (2 * LINE_WIDTH)])  # right
    pygame.draw.rect(screen, BLACK, [GameBoard.display_border - LINE_WIDTH, GameBoard.display_border + grid_height, grid_width + (2 * LINE_WIDTH), LINE_WIDTH])  # bottom
    pygame.draw.rect(screen, BLACK, [GameBoard.display_border - LINE_WIDTH, GameBoard.display_border - LINE_WIDTH, grid_width + (2 * LINE_WIDTH), LINE_WIDTH])   # top
    pygame.draw.rect(screen, CELL_COLOR, [GameBoard.display_border, GameBoard.display_border, grid_width, grid_height]) # Fill the inside wioth the cell color
    
    if hasHospital == True:
        pygame.draw.rect(screen, HOSPITAL_COLOR, [150, 150, 300, 300])

    # Draw the vertical lines
    i = GameBoard.display_border + GameBoard.display_cell_dimensions[0]
    while i < GameBoard.display_border + grid_width:
        pygame.draw.rect(screen, BLACK, [i, GameBoard.display_border, LINE_WIDTH, grid_height])
        i += GameBoard.display_cell_dimensions[0]
    # Draw the horizontal lines
    i = GameBoard.display_border + GameBoard.display_cell_dimensions[1]
    while i < GameBoard.display_border + grid_height:
        pygame.draw.rect(screen, BLACK, [GameBoard.display_border, i, grid_width, LINE_WIDTH])
        i += GameBoard.display_cell_dimensions[1]

def display_people(GameBoard):
    """
    Draw the people (government, vaccinated, and zombies) on the grid.
    """
    for x in range(len(GameBoard.States)):
        if GameBoard.States[x].person != None:
            p = GameBoard.States[x].person
            char = "Assets/" + image_assets[0]
            if p.isVaccinated:
                char = "Assets/" + image_assets[1]
            elif p.isZombie and p.halfCured == False:
                char = "Assets/" + image_assets[2]
            elif p.isZombie and p.halfCured:
                char = "Assets/" + image_assets[3]
            coords = (
                int(x % GameBoard.rows) * GameBoard.display_cell_dimensions[0] + GameBoard.display_border + 10,
                int(x / GameBoard.columns) * GameBoard.display_cell_dimensions[1] + GameBoard.display_border + 10,
            )
            display_image(screen, char, (80, 80), coords)

def display_win_screen():
    screen.fill(BACKGROUND)
    screen.blit(
        pygame.font.SysFont("Comic Sans", 32).render("You win!", True, WHITE),
        (500, 400),
    )
    pygame.display.update()

    # catch quit event
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

def display_lose_screen():
    screen.fill(BACKGROUND)
    screen.blit(
        pygame.font.SysFont("Comic Sans", 32).render("You lose lol!", True, WHITE),
        (500, 500),
    )
    pygame.display.update()

    # catch quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return

def display_options_screen(self_play, hospital, hover):
    screen.fill(BACKGROUND)

    screen.blit(
        pygame.font.SysFont("Calibri", 40).render("OPTIONS", True, WHITE), (500, 100),
    )
    screen.blit(
        pygame.font.SysFont("Calibri", 32).render("Train AI?", True, WHITE), (325, 200),
    )
    screen.blit(
        pygame.font.SysFont("Calibri", 32).render("Hospital On?", True, WHITE), (675, 200),
    )
    screen.blit(
        pygame.font.SysFont("Calibri", 24).render("Proceed to Game.", True, WHITE), (975, 600),
    )

    if hover == "proceed":
        display_image(screen, "Assets/checked_box.png", (100, 100), (1050, 650))
    else:
        display_image(screen, "Assets/unchecked_box.png", (100, 100), (1050, 650))
    if hover == "hospital":
        display_image(screen, "Assets/checked_box.png", (100, 100), (700, 250))
    else:
        if hospital:
            display_image(screen, "Assets/checked_box.png", (100, 100), (700, 250))
        else:
            display_image(screen, "Assets/unchecked_box.png", (100, 100), (700, 250))
    if hover == "self":
        display_image(screen, "Assets/checked_box.png", (100, 100), (350, 250))
    else:
        if self_play: 
            display_image(screen, "Assets/checked_box.png", (100, 100), (350, 250))
        else:
            display_image(screen, "Assets/unchecked_box.png", (100, 100), (350, 250))
    pygame.display.update()

def select(coord):
    left = coord[0] * 100 + 150
    top = coord[1] * 100 + 150
    color = (232, 232, 232)
    # Drawing Rectangle
    pygame.draw.rect(screen, color, pygame.Rect(left, top, 100 + LINE_WIDTH, 100 + LINE_WIDTH),  LINE_WIDTH+3)
    pygame.display.update()

def kill_animation(frame):
    char = "Assets/" + image_assets[4]
    # Draws background first and then draws the specified frame. The animations have the same number of frames and are already made to be synched up
    display_image(screen, char, (), (0,0))
    display_image(screen, "Assets/zombiedeath/sprite_" + str(frame) + ".png", (200, 200), (400, 350))
    display_image(screen, "Assets/watergun/sprite_" + str(frame) + ".png", (200, 200), (600, 350))

def half_heal_animation(frame):
    image = str(frame)
    if frame < 10:
        image = "0" + str(frame)
    display_image(screen, "Assets/heal1_background.png", (), (0, 200))
    display_image(screen, "Assets/heal1_zombie/sprite_" + image + ".png", (200, 200), (428, 350))    
    display_image(screen, "Assets/heal1_human/sprite_" + image + ".png", (200, 200), (572, 350))

def full_heal_animation(frame):
    image = str(frame)
    if frame < 10:
        image = "0" + str(frame)
    display_image(screen, "Assets/heal2_background.png", (), (0, 200))
    display_image(screen, "Assets/heal2_zombie/sprite_" + image + ".png", (200, 200), (428, 350))    
    display_image(screen, "Assets/heal2_human/sprite_" + image + ".png", (200, 200), (572, 350))

def vaccine_animation(frame):
    display_image(screen, "Assets/heal2_background.png", (), (0, 200))
    display_image(screen, "Assets/vaccine/sprite_" + str(frame) + ".png", (200, 200), (428, 350))    
    display_image(screen, "Assets/heal2_human/sprite_0" + str(frame) + ".png", (200, 200), (572, 350))

def direction(coord1, coord2):
    if coord2[1] > coord1[1]:
        return "moveDown"
    elif coord2[1] < coord1[1]:
        return "moveUp"
    elif coord2[0] > coord1[0]:
        return "moveRight"
    elif coord2[0] < coord1[0]:
        return "moveLeft"
