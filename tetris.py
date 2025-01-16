import random
import pygame

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = 10, 20
PREVIEW_X = GRID_WIDTH * GRID_SIZE
PREVIEW_WIDTH = 300  # Adjusted width of the preview panel to reduce the space on the right

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)  # New background color for the side panel
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 255, 0),  # Yellow
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 165, 0),  # Orange
    (128, 0, 128)   # Purple
]

# Tetris shapes
SHAPES = [
    [[1, 1, 1, 1]],              # I
    [[1, 1], [1, 1]],            # O
    [[0, 1, 1], [1, 1, 0]],      # S
    [[1, 1, 0], [0, 1, 1]],      # Z
    [[1, 0, 0], [1, 1, 1]],      # L
    [[0, 0, 1], [1, 1, 1]],      # J
    [[0, 1, 0], [1, 1, 1]]       # T
]

class Tetris:
    def __init__(self):
        self.board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.create_new_piece()
        self.next_piece = self.create_new_piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False

    def create_new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {'shape': shape, 'x': GRID_WIDTH // 2 - len(shape[0]) // 2, 'y': 0, 'color': color}

    def move_piece_left(self):
        self.current_piece['x'] -= 1
        if self.check_collision():
            self.current_piece['x'] += 1

    def move_piece_right(self):
        self.current_piece['x'] += 1
        if self.check_collision():
            self.current_piece['x'] -= 1

    def move_piece_down(self):
        self.current_piece['y'] += 1
        if self.check_collision():
            self.current_piece['y'] -= 1
            self.lock_piece()
            self.clear_full_lines()
            self.current_piece = self.next_piece
            self.next_piece = self.create_new_piece()

    def rotate_piece(self):
        old_shape = self.current_piece['shape']
        self.current_piece['shape'] = [list(row) for row in zip(*reversed(old_shape))]
        if self.check_collision():
            self.current_piece['shape'] = old_shape

    def check_collision(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_piece['x'] + x
                    new_y = self.current_piece['y'] + y
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return True
                    if new_y >= 0 and self.board[new_y][new_x] != 0:
                        return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.current_piece['y'] + y][self.current_piece['x'] + x] = self.current_piece['color']

    def clear_full_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.board) if all(row)]
        for i in lines_to_clear:
            del self.board[i]
            self.board.insert(0, [0] * GRID_WIDTH)
            self.lines_cleared += 1
        self.update_score(len(lines_to_clear))

    def update_score(self, lines):
        if lines > 0:
            self.score += (100 * lines) * self.level
            self.level = 1 + self.lines_cleared // 10

    def draw(self, screen):
        screen.fill(BLACK)
        # Draw the main board
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw the current piece
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_piece['color'],
                                     ((self.current_piece['x'] + x) * GRID_SIZE,
                                      (self.current_piece['y'] + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw the side panel background
        pygame.draw.rect(screen, GRAY, (PREVIEW_X, 0, PREVIEW_WIDTH, SCREEN_HEIGHT))

        self.draw_preview(screen)
        self.draw_score(screen)

    def draw_preview(self, screen):
        # Define the margin to adjust the position of the preview block inside the black box
        preview_x_offset = 10  # Adjust this value to move the preview left/right
        preview_y_offset = 10  # Adjust this value to move the preview up/down

        # Draw the black box for the preview area
        preview_width = len(self.next_piece['shape'][0]) * GRID_SIZE  # Width of the preview block area
        preview_height = len(self.next_piece['shape']) * GRID_SIZE  # Height of the preview block area
        pygame.draw.rect(screen, BLACK, (PREVIEW_X, 150, preview_width + 50, preview_height + 50))  # Draw a box with a slight border

        # Now draw the preview pieces on top of the black box with adjusted offsets
        for y, row in enumerate(self.next_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.next_piece['color'],
                                    (PREVIEW_X + x * GRID_SIZE + preview_x_offset,
                                    150 + y * GRID_SIZE + preview_y_offset, GRID_SIZE, GRID_SIZE))

    def draw_score(self, screen):
        font = pygame.font.SysFont('Arial', 24)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(level_text, (PREVIEW_X + 10, 50))
        screen.blit(score_text, (PREVIEW_X + 10, 100))

    def check_game_over(self):
        for x in range(GRID_WIDTH):
            if self.board[0][x] != 0:
                self.game_over = True
                break

def main():
    tetris = Tetris()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running:
        if tetris.game_over:
            font = pygame.font.SysFont('Arial', 48)
            game_over_text = font.render("GAME OVER", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
            continue

        tetris.draw(screen)
        pygame.display.flip()  # Refresh the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.move_piece_left()
                elif event.key == pygame.K_RIGHT:
                    tetris.move_piece_right()
                elif event.key == pygame.K_DOWN:
                    tetris.move_piece_down()
                elif event.key == pygame.K_UP:
                    tetris.rotate_piece()
                elif event.key == pygame.K_SPACE:
                    while not tetris.check_collision():
                        tetris.current_piece['y'] += 1
                    tetris.current_piece['y'] -= 1
                    tetris.lock_piece()
                    tetris.clear_full_lines()
                    tetris.current_piece = tetris.next_piece
                    tetris.next_piece = tetris.create_new_piece()

        tetris.move_piece_down()
        tetris.check_game_over()
        clock.tick(1)

if __name__ == "__main__":
    main()
