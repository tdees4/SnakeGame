import pygame
import random
from Snake import Snake

pygame.init()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# GRID PROPERTIES
BOX_OUTLINE_WIDTH = 2
BOX_SIZE = 60
GRID_SIZE = 9
START_X = 0
START_Y = 0

# WINDOW PROPERTIES
WIDTH, HEIGHT = GRID_SIZE * BOX_SIZE, GRID_SIZE * BOX_SIZE
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# APPLE
APPLE_SIZE = (BOX_SIZE / 1.2)

# GAME OVER TEXT
game_over_font = pygame.font.Font(pygame.font.get_default_font(), 32)
game_over_text = game_over_font.render('GAME OVER', True, RED)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WIDTH // 2, HEIGHT // 2)

# GAME WON TEXT
game_won_font = pygame.font.Font(pygame.font.get_default_font(), 32)
game_won_text = game_won_font.render('GAME WON', True, RED)
game_won_rect = game_won_text.get_rect()
game_won_rect.center = (WIDTH // 2, HEIGHT // 2)

# SNAKE SPRITE SHEET
sprite_sheet_image = pygame.image.load('assets/snake.png').convert_alpha()
SPRITE_SIZE = 64

GAME_OVER = False
GAME_WON = False

# FRAMES PER SECOND
FPS = 60

START_SPEED = 250  # IN MS
FINAL_SPEED = 125  # IN MS
TIME_BETWEEN_MOVEMENTS = START_SPEED

grid_dict = {
    0: "EMPTY",
    1: "SNAKE",
    2: "APPLE"
}

directions = {
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
    "UP": (0, -1),
    "DOWN": (0, 1)
}

# SPRITE LOCATIONS
sprites = {
    "BOTTOM_TO_RIGHT": (0, 0),
    "HORIZONTAL_STRAIGHT": (64, 0),
    "BOTTOM_TO_LEFT": (128, 0),
    "HEAD_UP": (192, 0),
    "HEAD_RIGHT": (256, 0),
    "TOP_TO_RIGHT": (0, 64),
    "VERTICAL_STRAIGHT": (128, 64),
    "HEAD_LEFT": (192, 64),
    "HEAD_DOWN": (256, 64),
    "TOP_TO_LEFT": (128, 128),
    "TAIL_DOWN": (192, 128),
    "TAIL_LEFT": (256, 128),
    "APPLE": (0, 192),
    "TAIL_RIGHT": (192, 192),
    "TAIL_UP": (256, 192)
}


def get_sprite(sprite_location, scale):
    """
    Get a sprite as an image
    :param sprite_location: The location of the sprite on the sprite sheet
    :param scale: The scale of the outputted sprite
    :return: The sprite as an image
    """

    image = pygame.Surface((SPRITE_SIZE, SPRITE_SIZE)).convert_alpha()
    image.blit(sprite_sheet_image, (0, 0), (sprite_location[0], sprite_location[1], SPRITE_SIZE, SPRITE_SIZE))
    image = pygame.transform.smoothscale(image, (scale, scale))
    image.set_colorkey(BLACK)

    return image


def draw_grid(grid_array, snake):  # DRAW THE SNAKE GRID
    """
    Draws the grid onto the screen
    :param grid_array: The game grid object
    :param snake: The snake object
    """

    for i in range((GRID_SIZE + 1) // 2):  # HORIZONTAL LINES
        rect = pygame.Surface((GRID_SIZE * BOX_SIZE, BOX_SIZE))
        rect.set_alpha(128)
        rect.fill(GREEN)
        WIN.blit(rect, (START_X, START_Y + BOX_SIZE * (i * 2)))

    for i in range((GRID_SIZE + 1) // 2):  # VERTICAL LINES
        rect = pygame.Surface((BOX_SIZE, GRID_SIZE * BOX_SIZE))
        rect.set_alpha(128)
        rect.fill(GREEN)
        WIN.blit(rect, (START_X + BOX_SIZE * (i * 2), START_Y))

    for row in range(len(grid_array)):  # ANYTHING IN GRID BOXES
        for col in range(len(grid_array[row])):
            current = grid_dict[grid_array[row][col]]
            if current == "APPLE":
                x = START_X + (col * BOX_SIZE) + BOX_OUTLINE_WIDTH // 2 + (BOX_SIZE // 2 - APPLE_SIZE // 2)
                y = START_Y + (row * BOX_SIZE) + BOX_OUTLINE_WIDTH // 2 + (BOX_SIZE // 2 - APPLE_SIZE // 2)
                WIN.blit(
                    get_sprite(sprites["APPLE"], APPLE_SIZE),
                    (x, y)
                )

    for i in range(snake.size()):
        current_body = snake.get_location(i)
        x = START_X + (current_body[0] * BOX_SIZE)
        y = START_Y + (current_body[1] * BOX_SIZE)

        if i == 0:  # DISPLAY HEAD OF SNAKE
            if snake.direction == directions["LEFT"]:
                WIN.blit(get_sprite(sprites["HEAD_LEFT"], BOX_SIZE), (x, y))
            elif snake.direction == directions["RIGHT"]:
                WIN.blit(get_sprite(sprites["HEAD_RIGHT"], BOX_SIZE), (x, y))
            elif snake.direction == directions["UP"]:
                WIN.blit(get_sprite(sprites["HEAD_UP"], BOX_SIZE), (x, y))
            elif snake.direction == directions["DOWN"]:
                WIN.blit(get_sprite(sprites["HEAD_DOWN"], BOX_SIZE), (x, y))

        elif i < snake.size() - 1:  # DISPLAY BODY PARTS OF SNAKE
            last_dir = snake.get_direction(i + 1)
            current_dir = snake.get_direction(i)
            if current_dir == last_dir:
                if current_dir == directions["RIGHT"] or current_dir == directions["LEFT"]:
                    WIN.blit(get_sprite(sprites["HORIZONTAL_STRAIGHT"], BOX_SIZE), (x, y))
                else:
                    WIN.blit(get_sprite(sprites["VERTICAL_STRAIGHT"], BOX_SIZE), (x, y))
            else:
                if current_dir == directions["RIGHT"] and last_dir == directions["UP"]:
                    WIN.blit(get_sprite(sprites["BOTTOM_TO_RIGHT"], BOX_SIZE), (x, y))
                elif current_dir == directions["RIGHT"] and last_dir == directions["DOWN"]:
                    WIN.blit(get_sprite(sprites["TOP_TO_RIGHT"], BOX_SIZE), (x, y))
                elif current_dir == directions["LEFT"] and last_dir == directions["UP"]:
                    WIN.blit(get_sprite(sprites["BOTTOM_TO_LEFT"], BOX_SIZE), (x, y))
                elif current_dir == directions["LEFT"] and last_dir == directions["DOWN"]:
                    WIN.blit(get_sprite(sprites["TOP_TO_LEFT"], BOX_SIZE), (x, y))
                elif current_dir == directions["UP"] and last_dir == directions["RIGHT"]:
                    WIN.blit(get_sprite(sprites["TOP_TO_LEFT"], BOX_SIZE), (x, y))
                elif current_dir == directions["UP"] and last_dir == directions["LEFT"]:
                    WIN.blit(get_sprite(sprites["TOP_TO_RIGHT"], BOX_SIZE), (x, y))
                elif current_dir == directions["DOWN"] and last_dir == directions["RIGHT"]:
                    WIN.blit(get_sprite(sprites["BOTTOM_TO_LEFT"], BOX_SIZE), (x, y))
                elif current_dir == directions["DOWN"] and last_dir == directions["LEFT"]:
                    WIN.blit(get_sprite(sprites["BOTTOM_TO_RIGHT"], BOX_SIZE), (x, y))

        else:  # DISPLAY TAIL OF SNAKE
            next_loc = snake.get_location(i - 1)
            current_loc = snake.get_location(i)
            diff_x = current_loc[0] - next_loc[0]
            diff_y = current_loc[1] - next_loc[1]
            if diff_x == 0 and diff_y > 0:
                WIN.blit(get_sprite(sprites["TAIL_DOWN"], BOX_SIZE), (x, y))
            elif diff_x == 0 and diff_y < 0:
                WIN.blit(get_sprite(sprites["TAIL_UP"], BOX_SIZE), (x, y))
            elif diff_x > 0 and diff_y == 0:
                WIN.blit(get_sprite(sprites["TAIL_RIGHT"], BOX_SIZE), (x, y))
            else:
                WIN.blit(get_sprite(sprites["TAIL_LEFT"], BOX_SIZE), (x, y))


def random_apple(grid):
    """
    Places a random apple on the grid
    :param grid: The game grid
    """

    location_list = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 0:
                location_list.append((row, col))
    if len(location_list) > 0:
        location = random.choice(location_list)
        grid[location[0]][location[1]] = 2


def check_won(grid):
    """
    :param grid: The game grid
    :return: True if the player has won, false if they have not
    """

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] != 1:
                return False
    return True


def handle_movement(keys, direction, snake):
    """
    Determine the direction the snake is going
    :param keys: The keys the player is pressing
    :param direction: The current direction of the snake
    :param snake: The snake object
    :return: The direction the snake will be facing
    """

    if keys[pygame.K_d] and snake.direction != directions["LEFT"]:  # RIGHT
        return directions["RIGHT"]
    if keys[pygame.K_a] and snake.direction != directions["RIGHT"]:  # LEFT
        return directions["LEFT"]
    if keys[pygame.K_s] and snake.direction != directions["UP"]:  # DOWN
        return directions["DOWN"]
    if keys[pygame.K_w] and snake.direction != directions["DOWN"]:  # UP
        return directions["UP"]
    else:
        return direction


def draw_window(grid_array, snake):
    """
    Draws the grid as well as the snake on top of it
    :param grid_array: Displays the grid as the game background
    :param snake: The snake to be drawn onto the grid
    """

    WIN.fill(WHITE)
    draw_grid(grid_array, snake)
    if GAME_OVER:
        WIN.blit(game_over_text, game_over_rect)
    elif GAME_WON:
        WIN.blit(game_won_text, game_won_rect)
    pygame.display.update()


def main():
    global GAME_OVER, GAME_WON, TIME_BETWEEN_MOVEMENTS, START_SPEED, FINAL_SPEED

    clock = pygame.time.Clock()

    direction = (0, 1)

    grid_array = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    snake = Snake((0, 0), direction)
    snake.draw(grid_array)

    random_apple(grid_array)

    start_time = pygame.time.get_ticks()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        direction = handle_movement(keys_pressed, direction, snake)

        if start_time and not GAME_OVER and not GAME_WON:
            time_elapsed = pygame.time.get_ticks() - start_time
            if time_elapsed >= TIME_BETWEEN_MOVEMENTS:
                snake.set_direction(direction)
                start_time = pygame.time.get_ticks()
                row, col = snake.get_location(0)[1] + direction[1], snake.get_location(0)[0] + direction[0]

                if row >= GRID_SIZE or row < 0 or col >= GRID_SIZE or col < 0:
                    if check_won(grid_array):
                        GAME_WON = True
                    else:
                        GAME_OVER = True
                elif grid_array[row][col] == 2:
                    snake.grow()
                    random_apple(grid_array)
                    TIME_BETWEEN_MOVEMENTS = \
                        START_SPEED - (START_SPEED - FINAL_SPEED) * (snake.size() / (GRID_SIZE * GRID_SIZE))
                elif grid_array[row][col] == 1:
                    if check_won(grid_array):
                        GAME_WON = True
                    else:
                        GAME_OVER = True

                if not GAME_OVER and not GAME_WON:
                    snake.move()
                    snake.draw(grid_array)

        draw_window(grid_array, snake)

    pygame.quit()


if __name__ == "__main__":
    main()