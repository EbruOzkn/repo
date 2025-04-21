import pygame
import random
import time
from maze_solver import Solver
import ctypes

WIDTH = 1000
HEIGHT = 700
OFFSET = 100

# Define colours
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
COLOR_LIGHT = (170, 170, 170)

# Maze variables
w = 20  # Width of cell
N = 30  # Size of the NxN grid
CELLS = []  # Contains all Cell objects

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Button variables
BUTTON_WIDTH = 140
BUTTON_HEIGHT = 40
BUTTON_POS_X = WIDTH - BUTTON_WIDTH - 30
BUTTON_KRUSKAL = screen.get_height() - 600
BUTTON_PRIM = screen.get_height() - 550

pygame.display.set_caption("Maze")
bg_img = pygame.image.load('bg.jpg')

font = pygame.font.SysFont("Corbel", 40)
g_txt = font.render("GENERATE", True, (100, 0, 200))
bg_img.blit(g_txt, (800, 55))

g_txt = font.render("SOLVE", True, (100, 0, 200))
bg_img.blit(g_txt, (840, 240))

BUTTON_DFS = screen.get_height() - 300
BUTTON_BFS = screen.get_height() - 350
BUTTON_DIJKSTRA = screen.get_height() - 400


class Cell:
    def __init__(self, row, column, x, y, visited):
        self.row = row  # row position in the 2D array CELLS
        self.column = column  # column position in the 2D array CELLS
        self.x = x  # x coordinate of the cell
        self.y = y  # y coordinate of the cell
        self.visited = visited  # check if we have already visited the cell

        # This is for disjoint set data structure for Kruskal
        self.parent = self
        self.size = 1
        # This is for Depth-First Search solver
        self.openWalls = []
        # This is for Dijkstra
        self.passOver = None
        self.prev = None


class Wall:
    def __init__(self, cell1, cell2):
        self.cell1 = cell1
        self.cell2 = cell2


def build_grid():
    x = OFFSET  # x-axis
    y = 50  # y-axis
    for i in range(0, N):
        CELLS.append([])
        for j in range(0, N):
            pygame.draw.line(bg_img, (128, 0, 128), (x, y), (x + w, y), 2)  # Top line of square
            x = x + w
            pygame.draw.line(bg_img, (128, 0, 128), (x, y), (x, y + w), 2)  # Right line of square
            y = y + w
            pygame.draw.line(bg_img, (128, 0, 128), (x, y), (x - w, y), 2)  # Bottom line of square
            x = x - w
            pygame.draw.line(bg_img, (128, 0, 128), (x, y), (x, y - w), 2)  # Left line of square
            y = y - w

            # Add cell to list of all cells
            CELLS[i].append(Cell((y - 50) // w, (x - OFFSET) // w, x, y, False))

            # Add wall to list of all walls

            x = x + w

        x = OFFSET
        y = y + w

    # Create entrance and exit
    pygame.draw.line(bg_img, (0, 0, 0), (CELLS[0][0].x, CELLS[0][0].y), (CELLS[0][0].x, CELLS[0][0].y + w), 1)
    pygame.draw.line(bg_img, (0, 0, 0), (CELLS[N - 1][N - 1].x + w, CELLS[N - 1][N - 1].y),
                     (CELLS[N - 1][N - 1].x + w, CELLS[N - 1][N - 1].y + w), 1)


def text_Kruskal(button):
    small_font = pygame.font.SysFont('Corbel', 30)
    text_Kruskal = small_font.render('Kruskal', True, WHITE)
    text_rect = text_Kruskal.get_rect()
    text_rect.center = button.center
    bg_img.blit(text_Kruskal, text_rect)


def text_Prim(button):
    small_font = pygame.font.SysFont('Corbel', 30)
    text_Prim = small_font.render('Prim', True, WHITE)
    text_rect = text_Prim.get_rect()
    text_rect.center = button.center
    bg_img.blit(text_Prim, text_rect)


def text_Dfs(button):
    small_font = pygame.font.SysFont('Corbel', 30)
    text_Dfs = small_font.render('DFS', True, WHITE)
    text_rect = text_Dfs.get_rect()
    text_rect.center = button.center
    bg_img.blit(text_Dfs, text_rect)


def text_Bfs(button):
    small_font = pygame.font.SysFont('Corbel', 30)
    text_Bfs = small_font.render('BFS', True, WHITE)
    text_rect = text_Bfs.get_rect()
    text_rect.center = button.center
    bg_img.blit(text_Bfs, text_rect)


def text_Dijkstra(button):
    small_font = pygame.font.SysFont('Corbel', 30)
    text_Dijkstra = small_font.render('Dijkstra', True, WHITE)
    text_rect = text_Dijkstra.get_rect()
    text_rect.center = button.center
    bg_img.blit(text_Dijkstra, text_rect)


def create_buttons():
    color_dark = (100, 10, 70)
    b2 = pygame.draw.rect(bg_img, color_dark, [BUTTON_POS_X, BUTTON_KRUSKAL, BUTTON_WIDTH, BUTTON_HEIGHT])
    b3 = pygame.draw.rect(bg_img, color_dark, [BUTTON_POS_X, BUTTON_PRIM, BUTTON_WIDTH, BUTTON_HEIGHT])
    b4 = pygame.draw.rect(bg_img, color_dark, [BUTTON_POS_X, BUTTON_DFS, BUTTON_WIDTH, BUTTON_HEIGHT])
    b5 = pygame.draw.rect(bg_img, color_dark, [BUTTON_POS_X, BUTTON_BFS, BUTTON_WIDTH, BUTTON_HEIGHT])
    b6 = pygame.draw.rect(bg_img, color_dark, [BUTTON_POS_X, BUTTON_DIJKSTRA, BUTTON_WIDTH, BUTTON_HEIGHT])

    text_Kruskal(b2)
    text_Prim(b3)
    text_Dfs(b4)
    text_Bfs(b5)
    text_Dijkstra(b6)


def get_unvisited_neighbors(cell):
    neighbors = []

    # Check if left neighbor exists and is unvisited
    if (cell.column >= 1) and (not CELLS[cell.row][cell.column - 1].visited):
        neighbors.append(CELLS[cell.row][cell.column - 1])

    # Check if right neighbor exists and is unvisited
    if (cell.column < N - 1) and (not CELLS[cell.row][cell.column + 1].visited):
        neighbors.append(CELLS[cell.row][cell.column + 1])

    # Check if top neighbor exists and is unvisited
    if (cell.row >= 1) and (not CELLS[cell.row - 1][cell.column].visited):
        neighbors.append(CELLS[cell.row - 1][cell.column])

    # Check if top neighbor exists and is unvisited
    if (cell.row < N - 1) and (not CELLS[cell.row + 1][cell.column].visited):
        neighbors.append(CELLS[cell.row + 1][cell.column])

    return neighbors


def create_path(current_cell, next_cell):
    # black = (50, 0, 100)  # color code for black
    black = (33, 18, 51)  # color code for black

    # Next cell is to the right of current cell
    if next_cell.x > current_cell.x:
        pygame.draw.line(screen, black, (next_cell.x, next_cell.y), (next_cell.x, next_cell.y + w), 2)
        if not ("E" in current_cell.openWalls):
            current_cell.openWalls.append("E")
        if not ("W" in next_cell.openWalls):
            next_cell.openWalls.append("W")
    # Next cell is to the left of current cell
    elif next_cell.x < current_cell.x:
        pygame.draw.line(screen, black, (current_cell.x, current_cell.y), (current_cell.x, current_cell.y + w), 2)
        if not ("W" in current_cell.openWalls):
            current_cell.openWalls.append("W")
        if not ("E" in next_cell.openWalls):
            next_cell.openWalls.append("E")
    # Next cell is under the current cell
    elif next_cell.y > current_cell.y:
        pygame.draw.line(screen, black, (next_cell.x, next_cell.y), (next_cell.x + w, next_cell.y), 2)
        if not ("S" in current_cell.openWalls):
            current_cell.openWalls.append("S")
        if not ("N" in next_cell.openWalls):
            next_cell.openWalls.append("N")
    # Next cell is above the current cell
    elif next_cell.y < current_cell.y:
        pygame.draw.line(screen, black, (current_cell.x, current_cell.y), (current_cell.x + w, current_cell.y), 2)
        if not ("N" in current_cell.openWalls):
            current_cell.openWalls.append("N")
        if not ("S" in next_cell.openWalls):
            next_cell.openWalls.append("S")
    pygame.display.flip()
    time.sleep(0.005)


def get_all_walls():
    walls = []
    for i in range(0, N):
        for j in range(0, N):
            CELLS[i][j].visited = True
            neighbors = get_unvisited_neighbors(CELLS[i][j])
            for neighbor in neighbors:
                walls.append(Wall(CELLS[i][j], neighbor))

    return walls


# Find the parent of the current cell with path compression
def find(cell):
    if cell.parent != cell:
        cell.parent = find(cell.parent)
        return cell.parent

    else:
        return cell


# Check if cell1 and cell2 are in the same set. If not, combine them
def union(cell1, cell2):
    x = find(cell1)
    y = find(cell2)

    if x == y:
        return True

    if x.size > y.size:
        y.parent = x
        x.size = x.size + y.size

    else:
        x.parent = y
        y.size = y.size + x.size

    return False


def kruskal():
    walls = get_all_walls()  # Contains all Wall objects

    while len(walls) != 0:
        num = random.randint(0, len(walls) - 1)  # Choosing a random wall
        choice = walls.pop(num)
        if not union(choice.cell1, choice.cell2):
            create_path(choice.cell1, choice.cell2)


# Getting the walls
def get_walls(cell):
    cell.visited = True
    neighbors = get_unvisited_neighbors(cell)
    walls = []

    for neighbor in neighbors:
        walls.append(Wall(cell, neighbor))

    return walls


def prim():
    num = random.randint(0, len(CELLS) - 1)
    choice = random.choice(CELLS[num])  # pick a random starting cell

    walls = get_walls(choice)  # Will contain a list of walls from the cells we pick

    while len(walls) != 0:
        num = random.randint(0, len(walls) - 1)
        choice = walls.pop(num)  # Choose random wall

        if not (choice.cell1.visited and choice.cell2.visited):
            if not choice.cell1.visited:
                walls = walls + get_walls(choice.cell1)
            else:
                walls = walls + get_walls(choice.cell2)

            create_path(choice.cell1, choice.cell2)


def reset():
    screen.blit(bg_img, (0, 0))
    global CELLS
    CELLS = []
    build_grid()
    create_buttons()
    pygame.display.flip()


def draw_path(path, color=BLUE):
    pygame.draw.circle(screen, GREEN, (690, 640), 5, 10)
    pygame.display.flip()
    time.sleep(0.0005)
    for cell in list(path.keys()):
        currentCell = path[cell]
        centerX = CELLS[currentCell[0]][currentCell[1]].x + (w / 2)
        centerY = CELLS[currentCell[0]][currentCell[1]].y + (w / 2)
        pygame.draw.circle(screen, color, (centerX, centerY), 5, 10)
        pygame.display.flip()
        time.sleep(0.00005)
    pygame.draw.circle(screen, GREEN, (110, 60), 5, 10)
    pygame.display.flip()


class Application:
    def run(self):
        flag = False
        reset()
        running = True
        screen.blit(bg_img, (0, 0))
        pygame.display.flip()
        while running:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if BUTTON_POS_X <= mouse[0] <= BUTTON_POS_X + BUTTON_WIDTH and \
                            BUTTON_KRUSKAL <= mouse[1] <= BUTTON_KRUSKAL + BUTTON_HEIGHT:
                        reset()
                        kruskal()

                        flag = True

                    if BUTTON_POS_X <= mouse[0] <= BUTTON_POS_X + BUTTON_WIDTH and \
                            BUTTON_PRIM <= mouse[1] <= BUTTON_PRIM + BUTTON_HEIGHT:
                        reset()
                        prim()
                        flag = True

                    if flag:
                        if BUTTON_POS_X <= mouse[0] <= BUTTON_POS_X + BUTTON_WIDTH and \
                                BUTTON_DFS <= mouse[1] <= BUTTON_DFS + BUTTON_HEIGHT:
                            allPath, path = Solver.DFS(CELLS[0][0], N, CELLS)
                            draw_path(allPath, GREEN)
                            draw_path(path, WHITE)

                        if BUTTON_POS_X <= mouse[0] <= BUTTON_POS_X + BUTTON_WIDTH and \
                                BUTTON_BFS <= mouse[1] <= BUTTON_BFS + BUTTON_HEIGHT:
                            allPath, path = Solver.BFS(CELLS[0][0], N, CELLS)
                            draw_path(allPath, YELLOW)
                            draw_path(path, BLUE)

                        if BUTTON_POS_X <= mouse[0] <= BUTTON_POS_X + BUTTON_WIDTH and \
                                BUTTON_DIJKSTRA <= mouse[1] <= BUTTON_DIJKSTRA + BUTTON_HEIGHT:
                            allPath, path = Solver.Dijkstra(CELLS[0][0], N, CELLS)
                            draw_path(allPath, RED)
                            draw_path(path, PURPLE)
                    else:
                        ctypes.windll.user32.MessageBoxW(0, "Please first generate maze!", "Warning", 0)

            if not running:
                pygame.quit()
