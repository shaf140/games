import pygame
import random

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10
DRAGON_SPEED = 15
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
DRAGON_COLOR = (255, 165, 0)  # Color for the dragon

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False
        self.apples_eaten = 0
        self.is_dragon = False

    def move(self):
        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        if new_head in self.positions or not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            return False  # Collision detected

        self.positions = [new_head] + self.positions[:-1]

        if self.grow:
            self.positions.append(self.positions[-1])
            self.grow = False
        return True

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def eat_apple(self):
        self.grow = True
        self.apples_eaten += 1
        if self.apples_eaten >= 10:
            self.is_dragon = True

    def get_color(self):
        return DRAGON_COLOR if self.is_dragon else SNAKE_COLOR

# Apple class
class Apple:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def respawn(self):
        self.position = self.random_position()

# Draw grid
def draw_grid(screen):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, (40, 40, 40), rect, 1)

# Main game loop
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Load dragon head image and scale it to fit grid size
    dragon_head_img = pygame.image.load("dragon_head.png")  # Replace with the path to your dragon image
    dragon_head_img = pygame.transform.scale(dragon_head_img, (GRID_SIZE, GRID_SIZE))

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)

        # Move the snake
        if not snake.move():
            running = False  # Game over when the snake collides

        # Check if snake eats the apple
        if snake.positions[0] == apple.position:
            snake.eat_apple()
            apple.respawn()

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw grid
        draw_grid(screen)

        # Draw apple
        apple_rect = pygame.Rect(apple.position[0] * GRID_SIZE, apple.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, APPLE_COLOR, apple_rect)

        # Draw snake
        for i, position in enumerate(snake.positions):
            if i == 0 and snake.is_dragon:  # Draw dragon head for the snake's head if it's a dragon
                screen.blit(dragon_head_img, (position[0] * GRID_SIZE, position[1] * GRID_SIZE))
            else:
                snake_rect = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, snake.get_color(), snake_rect)

        # Update the screen
        pygame.display.update()

        # Control the speed
        clock.tick(DRAGON_SPEED if snake.is_dragon else SNAKE_SPEED)

    pygame.quit()

if __name__ == "__main__":
    main()
