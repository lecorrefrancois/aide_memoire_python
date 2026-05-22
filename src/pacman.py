import pygame
import random
from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


@dataclass
class Position:
    x: int
    y: int

    def move(self, direction: Direction) -> "Position":
        dx, dy = direction.value
        return Position(self.x + dx, self.y + dy)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Pacman:
    def __init__(self, x: int, y: int, grid_size: int):
        self.pos = Position(x, y)
        self.next_pos = Position(x, y)
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.grid_size = grid_size
        self.size = grid_size - 2

    def update_direction(self, direction: Direction):
        self.next_direction = direction

    def move(self, maze):
        # Try to move in the next direction first
        next_pos = self.next_pos.move(self.next_direction)
        if self._is_valid_move(next_pos, maze):
            self.pos = next_pos
            self.direction = self.next_direction
        else:
            # Otherwise, continue in the current direction
            next_pos = self.pos.move(self.direction)
            if self._is_valid_move(next_pos, maze):
                self.pos = next_pos
        self.next_pos = self.pos

    def _is_valid_move(self, pos: Position, maze) -> bool:
        if not (0 <= pos.x < len(maze[0]) and 0 <= pos.y < len(maze)):
            return False
        return maze[pos.y][pos.x] != 1

    def draw(self, screen):
        x = self.pos.x * self.grid_size
        y = self.pos.y * self.grid_size
        pygame.draw.circle(screen, (255, 255, 0),
                          (x + self.grid_size // 2, y + self.grid_size // 2),
                          self.size // 2)


class Ghost:
    def __init__(self, x: int, y: int, grid_size: int, color):
        self.pos = Position(x, y)
        self.grid_size = grid_size
        self.size = grid_size - 2
        self.color = color
        self.move_counter = 0

    def move(self, maze):
        self.move_counter += 1
        if self.move_counter % 2 == 0:  # Slower than Pacman
            directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
            random.shuffle(directions)

            for direction in directions:
                next_pos = self.pos.move(direction)
                if self._is_valid_move(next_pos, maze):
                    self.pos = next_pos
                    break

    def _is_valid_move(self, pos: Position, maze) -> bool:
        if not (0 <= pos.x < len(maze[0]) and 0 <= pos.y < len(maze)):
            return False
        return maze[pos.y][pos.x] != 1

    def draw(self, screen):
        x = self.pos.x * self.grid_size
        y = self.pos.y * self.grid_size
        pygame.draw.rect(screen, self.color,
                        (x + 1, y + 1, self.size, self.size))


class PacmanGame:
    GRID_SIZE = 20
    WIDTH = 560
    HEIGHT = 560
    FOOD_COLOR = (200, 100, 100)
    EMPTY = 0
    WALL = 1

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pacman")
        self.clock = pygame.time.Clock()
        self.cols = self.WIDTH // self.GRID_SIZE
        self.rows = self.HEIGHT // self.GRID_SIZE

        self.maze = self._generate_maze()
        self.food = self._place_food()
        self.pacman = Pacman(1, 1, self.GRID_SIZE)
        self.ghosts = [
            Ghost(7, 7, self.GRID_SIZE, (255, 0, 0)),
            Ghost(8, 7, self.GRID_SIZE, (255, 184, 255)),
            Ghost(7, 8, self.GRID_SIZE, (0, 255, 255)),
        ]

        self.score = 0
        self.running = True

    def _generate_maze(self):
        maze = [[self.EMPTY] * self.cols for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                if i == 0 or i == self.rows - 1 or j == 0 or j == self.cols - 1:
                    maze[i][j] = self.WALL

        for i in range(2, self.rows - 2, 2):
            for j in range(2, self.cols - 2, 2):
                maze[i][j] = self.WALL
                if random.random() < 0.3:
                    maze[i][j + 1] = self.WALL
                if random.random() < 0.3:
                    maze[i + 1][j] = self.WALL

        return maze

    def _place_food(self):
        food = set()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == self.EMPTY and not (i == 1 and j == 1):
                    food.add((j, i))
        return food

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.pacman.update_direction(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    self.pacman.update_direction(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    self.pacman.update_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.pacman.update_direction(Direction.RIGHT)

    def update(self):
        self.pacman.move(self.maze)

        for ghost in self.ghosts:
            ghost.move(self.maze)

        if (self.pacman.pos.x, self.pacman.pos.y) in self.food:
            self.food.remove((self.pacman.pos.x, self.pacman.pos.y))
            self.score += 10

        for ghost in self.ghosts:
            if self.pacman.pos == ghost.pos:
                self.running = False

    def draw(self):
        self.screen.fill((0, 0, 0))

        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == self.WALL:
                    x = j * self.GRID_SIZE
                    y = i * self.GRID_SIZE
                    pygame.draw.rect(self.screen, (33, 33, 222),
                                    (x, y, self.GRID_SIZE, self.GRID_SIZE))

        for x, y in self.food:
            px = x * self.GRID_SIZE + self.GRID_SIZE // 2
            py = y * self.GRID_SIZE + self.GRID_SIZE // 2
            pygame.draw.circle(self.screen, self.FOOD_COLOR, (px, py), 2)

        self.pacman.draw(self.screen)
        for ghost in self.ghosts:
            ghost.draw(self.screen)

        font = pygame.font.Font(None, 24)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(10)

        pygame.quit()
        print(f"Game Over! Final Score: {self.score}")


if __name__ == "__main__":
    game = PacmanGame()
    game.run()
