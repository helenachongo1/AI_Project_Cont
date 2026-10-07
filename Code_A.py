import pygame
import random
import sys

# --- Game Constants ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10 # Frames per second - controls game speed

# --- Colors (RGB) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (0, 150, 0) # For snake body

# --- Directions ---
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# --- Snake Class ---
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)] # Initial position in the middle
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT]) # Random starting direction
        self.grow_segments = 0 # How many segments to add next
        self.score = 0
        self.speed = FPS # Initial speed, will increase with score

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        self.body.insert(0, new_head) # Add new head

        if self.grow_segments > 0:
            self.grow_segments -= 1
        else:
            self.body.pop() # Remove tail if not growing

    def change_direction(self, new_dir):
        # Prevent immediate U-turn
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def grow(self):
        self.grow_segments += 1
        self.score += 1
        self.speed = FPS + (self.score // 5) # Increase speed every 5 points

    def check_collision(self):
        head = self.body[0]
        # Wall collision
        if not (0 <= head[0] < GRID_WIDTH and 0 <= head[1] < GRID_HEIGHT):
            return True
        # Self-collision
        if head in self.body[1:]:
            return True
        return False

    def draw(self, surface):
        for i, segment in enumerate(self.body):
            x, y = segment
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if i == 0: # Head of the snake
                pygame.draw.rect(surface, BLUE, rect)
            else:
                pygame.draw.rect(surface, DARK_GREEN, rect)

    def reset(self):
        self.__init__() # Re-initialize the snake

# --- Food Class ---
class Food:
    def __init__(self, snake_body):
        self.position = (0, 0)
        self.spawn(snake_body)

    def spawn(self, snake_body):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_body: # Ensure food doesn't spawn on snake
                self.position = (x, y)
                break

    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)

# --- Game Functions ---
def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, WHITE, (0, y), (SCREEN_WIDTH, y))

def display_message(surface, message, color=WHITE, size=50, center_x=SCREEN_WIDTH // 2, center_y=SCREEN_HEIGHT // 2):
    font = pygame.font.Font(None, size)
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    surface.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food(snake.body)

    game_over = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)
                else: # If game over
                    if event.key == pygame.K_r: # Press 'R' to restart
                        snake.reset()
                        food.spawn(snake.body)
                        game_over = False

        if not game_over:
            snake.move()

            if snake.body[0] == food.position:
                snake.grow()
                food.spawn(snake.body)

            if snake.check_collision():
                game_over = True

        # --- Drawing ---
        screen.fill(BLACK)
        # draw_grid(screen) # Uncomment this line to see the grid

        snake.draw(screen)
        food.draw(screen)

        # Display Score
        display_message(screen, f"Score: {snake.score}", WHITE, 30, SCREEN_WIDTH - 80, 20)

        if game_over:
            display_message(screen, "GAME OVER!", RED, 70, center_y=SCREEN_HEIGHT // 2 - 50)
            display_message(screen, f"Final Score: {snake.score}", WHITE, 40, center_y=SCREEN_HEIGHT // 2 + 10)
            display_message(screen, "Press 'R' to Restart", GREEN, 30, center_y=SCREEN_HEIGHT // 2 + 60)

        pygame.display.flip()
        clock.tick(snake.speed) # Use snake's current speed for FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
