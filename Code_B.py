import pygame
import random
import sys

# --- Game Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20  # Each segment of the snake and food will be 20x20 pixels
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 150, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# Game Speed
INITIAL_SPEED = 8  # Frames per second
SPEED_INCREMENT = 1 # How much FPS increases per food eaten
MAX_SPEED = 30     # Cap the speed

# --- Pygame Initialization ---
pygame.init()
pygame.display.set_caption("Python Snake Game")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Fonts
font_small = pygame.font.Font(None, 30)
font_medium = pygame.font.Font(None, 50)
font_large = pygame.font.Font(None, 75)

# --- Snake Class ---
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)] # Start in the middle
        self.direction = (GRID_SIZE, 0)  # Start moving right
        self.grow = False # Flag to determine if snake should grow

    def move(self):
        """Moves the snake's head and body."""
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % SCREEN_WIDTH, (head_y + dy) % SCREEN_HEIGHT) # Wrap around screen

        self.body.insert(0, new_head) # Add new head
        if not self.grow:
            self.body.pop() # Remove tail if not growing
        else:
            self.grow = False # Reset grow flag

    def change_direction(self, new_dir):
        """
        Changes the snake's direction. Prevents immediate 180-degree turns.
        """
        current_dx, current_dy = self.direction
        new_dx, new_dy = new_dir

        # Prevent turning directly back on itself
        if (new_dx, new_dy) != (-current_dx, -current_dy):
            self.direction = new_dir

    def check_collision(self):
        """Checks for collisions with itself or walls."""
        head_x, head_y = self.body[0]

        # Self-collision: Check if head collides with any part of its body (excluding the head itself)
        if (head_x, head_y) in self.body[1:]:
            return True

        # Wall collision (if not wrapping around, otherwise this isn't needed)
        # For a game that wraps, collision is only with itself
        # If we wanted hard walls, uncomment this:
        # if not (0 <= head_x < SCREEN_WIDTH and 0 <= head_y < SCREEN_HEIGHT):
        #     return True

        return False

    def draw(self, surface):
        """Draws the snake on the given surface."""
        for i, segment in enumerate(self.body):
            color = GREEN if i == 0 else DARK_GREEN # Head is brighter green
            pygame.draw.rect(surface, color, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))
            # Optional: Add a border for better segment definition
            pygame.draw.rect(surface, BLACK, (segment[0], segment[1], GRID_SIZE, GRID_SIZE), 1)

# --- Food Class ---
class Food:
    def __init__(self, snake_body):
        self.position = self._generate_position(snake_body)

    def _generate_position(self, snake_body):
        """Generates a random position for the food, ensuring it's not on the snake."""
        while True:
            x = random.randrange(0, GRID_WIDTH) * GRID_SIZE
            y = random.randrange(0, GRID_HEIGHT) * GRID_SIZE
            if (x, y) not in snake_body:
                return (x, y)

    def draw(self, surface):
        """Draws the food on the given surface."""
        pygame.draw.rect(surface, RED, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, WHITE, (self.position[0], self.position[1], GRID_SIZE, GRID_SIZE), 1) # Border

# --- Game Functions ---
def display_message(surface, message, font, color, y_offset=0):
    """Helper function to display text messages on screen."""
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset))
    surface.blit(text_surface, text_rect)

def reset_game():
    """Resets all game variables for a new game."""
    global snake, food, score, current_speed, game_over, game_started

    snake = Snake()
    food = Food(snake.body)
    score = 0
    current_speed = INITIAL_SPEED
    game_over = False
    game_started = False # Set to False to show start screen

# --- Main Game Loop ---
def main():
    global snake, food, score, current_speed, game_over, game_started

    reset_game() # Initialize game state

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r: # Restart game
                        reset_game()
                elif not game_started:
                    if event.key == pygame.K_SPACE: # Start game
                        game_started = True
                else: # Game is running
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -GRID_SIZE))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, GRID_SIZE))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-GRID_SIZE, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((GRID_SIZE, 0))

        # --- Game Logic (only if game is started and not over) ---
        if game_started and not game_over:
            snake.move()

            # Check for collisions after moving
            if snake.check_collision():
                game_over = True

            # Check if snake eats food
            if snake.body[0] == food.position:
                snake.grow = True
                score += 1
                food = Food(snake.body) # Generate new food
                
                # Increase speed, up to MAX_SPEED
                current_speed = min(MAX_SPEED, current_speed + SPEED_INCREMENT)
        
        # --- Drawing ---
        screen.fill(BLACK) # Clear screen

        if not game_started:
            display_message(screen, "SNAKE GAME", font_large, GREEN, -100)
            display_message(screen, "Press SPACE to Start", font_medium, WHITE, 0)
            display_message(screen, "Use Arrow Keys to Move", font_small, GRAY, 50)
            display_message(screen, "Created by Expert Python Dev", font_small, GRAY, 250)
        elif game_over:
            display_message(screen, "GAME OVER!", font_large, RED, -50)
            display_message(screen, f"Score: {score}", font_medium, WHITE, 20)
            display_message(screen, "Press 'R' to Restart", font_small, GRAY, 80)
        else:
            snake.draw(screen)
            food.draw(screen)
            
            # Display score in top-left corner
            score_text = font_small.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
            
            # Optional: Display current speed
            speed_text = font_small.render(f"Speed: {current_speed}", True, WHITE)
            screen.blit(speed_text, (SCREEN_WIDTH - speed_text.get_width() - 10, 10))


        pygame.display.flip() # Update the full display Surface to the screen
        clock.tick(current_speed) # Control frame rate

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

