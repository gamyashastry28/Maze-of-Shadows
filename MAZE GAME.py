import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 24
MAZE_WIDTH, MAZE_HEIGHT = 25, 25  # Dimensions in number of tiles
WIDTH, HEIGHT = MAZE_WIDTH * TILE_SIZE, MAZE_HEIGHT * TILE_SIZE
HEAD_START_TIME = 2  # Head start time for the player

# Colors
BG_COLOR = (0, 0, 0)  # Background color (black)
WALL_COLOR = (255, 255, 255)  # Wall color (white)
PLAYER_COLOR = (0, 255, 0)  # Player color (green)
EXIT_COLOR = (255, 0, 0)  # Exit color (red)

# Create the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze of Shadows")

# Maze layout with exit represented by 'E'
levels = [
    [
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "X  XXXXXXX          XXXXX",
        "X  XXXXXXX  XXXXXX  XXXXX",
        "X       XX  XXXXXX  XXXXX",
        "X       XX  XXX        XX",
        "XXXXXX  XX  XXX        XX",
        "XXXXXX  XX  XXXXXX  XXXXX",
        "XXXXXX  XX    XXXX  XXXXX",
        "X  XXX        XXXX  XXXXX",
        "X  XXX  XXXXXXXXXXXXXXXXX",
        "X         XXXXXXXXXXXXXXX",
        "X                XXXXXXXX",
        "XXXXXXXXXXXX     XXXXX  X",
        "XXXXXXXXXXXXXXX  XXXXX  X",
        "XXX  XXXXXXXXXX         X",
        "XXX                     X",
        "XXX         XXXXXXXXXXXXX",
        "XXXXXXXXXX  XXXXXXXXXXXXX",
        "XXXXXXXXXX              X",
        "XX  XXXXX               X",
        "XX  XXXXXXXXXXXXX       X",  
        "XXXX                  E X", # Exit here
        "XXXXXXXXXXXXXXXXXXXXXXXXX"
    ],
    [
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "X                      XX",
        "X  XXXXXXXXXXXXXXXXX    X",
        "X  XXXXXXXXXXXXXXXXX    X",
        "X       XXXXXXXXXX      X",
        "X       XX             XX",
        "XXXXXX    XXXXXXXXXXXXXXX",
        "XXXXXX  XX             XX",
        "X      XX  XXXXXX       X",
        "X      XX  XXXXXX       X",
        "X  XXXX      XXXXXX     X",
        "X   XXXXXXXXXXXXXXXXXXXXX",
        "X                       X",
        "XXXXXXXXXXXXXX  XXXX    X",
        "X           E  XXXXXX",
        "XXXXXXX  XXXXXXX      XXX",
        "XXXXXXXXXXX   XXXXXXXXXXX",
        "XXXXXXXXXXXXXXXXX   XXXXX",
        "XXXXXXXXXXXXXXXXX   XXXXX",
        "XXXXXXXXXXXXXXXXXX   XXXX",
        "XXXXXXXXXXXXXXXXXX   XXXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX"
    ],
    [
        "XXXXXXXXXXXXXXXXXXXXXXXXX",
        "X       E               X",
        "X  XXXX  XXXXXXXXXXX   XX",
        "X  XXXX  XXXXXXXXXXX   XX",
        "X       XX             XX",
        "X  XXXX  XXXXXXXX      XX",
        "X  XXXX  XXXXXXXX      XX",
        "X       XXXXXXXXXX     XX",
        "X                       X",
        "XXXXXXXXXXXXXX  XXXX    X",
        "X                 X     X",
        "X  XXXXXXXXXXXXXXXX     X",
        "X                 XX    X",
        "X  XXXXXXXXXXXXXXXX     X",
        "XX                     XX",
        "XX  XXXXXXXXXXXXXXXX    X",
        "XXXXXXXXXXXXXXXXXXXX   XX",
        "XXXXXXXXXXXXXXXXXXXX   XX",
        "XXXXXXXXXXXXXXXXXXXX   XX",
        "XXXXXXXXXXXXXXXXXXXX   XX",
        "XXXXXXXXXXXXXXXXXXXXXXXXX"
    ]
]

# Set up the maze walls and exit
def setup_maze(level):
    walls = []
    exit_pos = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "X":
                wall_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                walls.append(wall_rect)
            elif level[y][x] == "E":
                exit_pos = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)  # Set exit position
    return walls, exit_pos

# Load the maze walls and exit for the current level
current_level_index = 0
walls, exit_rect = setup_maze(levels[current_level_index])

# Player settings
player_pos = [1 * TILE_SIZE, 1 * TILE_SIZE]  # Starting position for the player
player_rect = pygame.Rect(player_pos[0], player_pos[1], TILE_SIZE, TILE_SIZE)
player_speed = TILE_SIZE  # Movement by one tile at a time

# Timer settings
head_start_ticks = pygame.time.get_ticks()  # Get the head start initial time
level_completed = False  # To track if the level is completed

# Check if the player is colliding with any walls
def is_colliding_with_wall(new_rect):
    for wall in walls:
        if new_rect.colliderect(wall):
            return True
    return False

# Main Game Loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement handling
    keys = pygame.key.get_pressed()
    new_rect = player_rect.copy()  # Temporary rect for collision checking
    
    if keys[pygame.K_LEFT]:
        new_rect.x -= player_speed
        if not is_colliding_with_wall(new_rect):
            player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        new_rect.x += player_speed
        if not is_colliding_with_wall(new_rect):
            player_rect.x += player_speed
    if keys[pygame.K_UP]:
        new_rect.y -= player_speed
        if not is_colliding_with_wall(new_rect):
            player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        new_rect.y += player_speed
        if not is_colliding_with_wall(new_rect):
            player_rect.y += player_speed

    # Check for level completion
    if player_rect.colliderect(exit_rect) and not level_completed:
        level_completed = True

    # Draw background (black)
    screen.fill(BG_COLOR)

    # Draw walls
    for wall in walls:
        pygame.draw.rect(screen, WALL_COLOR, wall)

    # Draw the player
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    # Draw the exit
    if not level_completed:
        pygame.draw.rect(screen, EXIT_COLOR, exit_rect)

    # Display game status
    if level_completed:
        font = pygame.font.Font(None, 74)
        text = font.render("Level Completed!", True, (255, 255, 255))  # White text
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        # Move to the next level after a delay
        pygame.time.delay(2000)  # Delay for 2 seconds before moving to the next level
        current_level_index += 1
        if current_level_index < len(levels):
            walls, exit_rect = setup_maze(levels[current_level_index])  # Load the next level
            player_rect.topleft = (1 * TILE_SIZE, 1 * TILE_SIZE)  # Reset player position
            level_completed = False  # Reset level completion status
        else:
            # Game completed, quit or reset
            running = False

    # Create a surface for the dark overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Create an overlay with alpha

    # Fill the overlay with black color
    overlay.fill((0, 0, 0, 255))  # Completely opaque black

    # Create a circle cut-out in the overlay where the light will shine
    light_radius = 100  # Adjust the radius of the light area
    pygame.draw.circle(overlay, (0, 0, 0, 0), (player_rect.centerx, player_rect.centery), light_radius)

    # Blit the overlay onto the screen
    screen.blit(overlay, (0, 0))

    # Refresh the screen
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
