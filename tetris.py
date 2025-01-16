import pygame
import random

pygame.init()

# Screen size
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (128, 0, 128)   # Purple
]

# Define the shapes of the blocks
SHAPES = [
    [[1, 1, 1, 1]],                        # I shape
    [[1, 1], [1, 1]],                      # O shape
    [[0, 1, 0], [1, 1, 1]],                # T shape
    [[1, 1, 0], [0, 1, 1]],                # S shape
    [[0, 1, 1], [1, 1, 0]],                # Z shape
    [[1, 1, 1], [1, 0, 0]],                # L shape
    [[1, 1, 1], [0, 0, 1]]                 # J shape
]

class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {'shape': shape, 'color': color, 'x': 4, 'y': 0}

    def valid_move(self, shape, offset_x, offset_y):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_piece['x'] + x + offset_x
                    new_y = self.current_piece['y'] + y + offset_y
                    if new_x < 0 or new_x >= 10 or new_y >= 20 or (new_y >= 0 and self.grid[new_y][new_x]):
                        return False
        return True

    def rotate_piece(self):
        shape = self.current_piece['shape']
        rotated_shape = [list(row) for row in zip(*shape[::-1])]
        if self.valid_move(rotated_shape, 0, 0):
            self.current_piece['shape'] = rotated_shape

    def drop_piece(self):
        if self.valid_move(self.current_piece['shape'], 0, 1):
            self.current_piece['y'] += 1
        else:
            self.lock_piece()
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()
            if not self.valid_move(self.current_piece['shape'], 0, 0):
                print(f"Game Over! Final score: {self.score}")
                pygame.quit()
                quit()

    def hard_drop_piece(self):
        while self.valid_move(self.current_piece['shape'], 0, 1):
            self.current_piece['y'] += 1
        self.drop_piece()

    def lock_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(row)]
        for i in lines_to_clear:
            del self.grid[i]
            self.grid.insert(0, [0 for _ in range(10)])
            self.score += 100

    def draw(self, screen):
        screen.fill(BLACK)
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_piece['color'],
                                     ((self.current_piece['x'] + x) * GRID_SIZE, (self.current_piece['y'] + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT), 5)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    tetris = Tetris()
    running = True
    drop_speed = 500  # milliseconds
    last_drop = pygame.time.get_ticks()

    while running:
        screen.fill(BLACK)
        tetris.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if tetris.valid_move(tetris.current_piece['shape'], -1, 0):
                        tetris.current_piece['x'] -= 1
                elif event.key == pygame.K_RIGHT:
                    if tetris.valid_move(tetris.current_piece['shape'], 1, 0):
                        tetris.current_piece['x'] += 1
                elif event.key == pygame.K_DOWN:
                    tetris.drop_piece()
                elif event.key == pygame.K_UP:
                    tetris.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    tetris.hard_drop_piece()

        if pygame.time.get_ticks() - last_drop > drop_speed:
            tetris.drop_piece()
            last_drop = pygame.time.get_ticks()

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
