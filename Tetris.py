

import pygame
import random
import numpy as np
# Visual variables
s_width = 600
s_height = 700
BLOCK_SIZE = 30
top_left_of_board = (40,70)

# Game Variables
types = [0, 1, 2, 3, 4, 5, 6]
colors = [1, 2, 3, 4, 5, 6, 7]
rgbcolours = [(0, 0, 0), (200, 100, 100), (255, 200, 100), (0, 100, 100),
              (100, 255, 100), (100, 100, 255), (100, 0, 100), (100, 100, 0)]
WIDTH = 10
HEIGHT = 20
FALL_SPEED = 3
SCORE_FOR_ROW = 100
MULTI_ROW_MULTIPLIER = 2
SCORE = 0
# Coordinates of each shape with top left being 0,0, y axis increase as it goes down
SHAPE_COORDINATES = {0: [(0, 0), (0, 1), (1, 0), (1, 1)],
                     1: [(0, 0), (0, 1), (1, 1), (1, 2)],
                     2: [(1, 0), (1, 1), (0, 1), (0, 2)],
                     3: [(0, 0), (0, 1), (0, 2), (0, 3)],
                     4: [(0, 0), (0, 1), (0, 2), (1, 1)],
                     5: [(0, 0), (0, 1), (0, 2), (1, 0)],
                     6: [(0, 0), (0, 1), (0, 2), (1, 2)],}


# General shape class
class shape:
    def __init__(self, type, rotation):
        self.type = type
        self.rotation = rotation
        self.color = colors[type]
        self.coordinates = SHAPE_COORDINATES[type]


class SCORE:
    def __init__(self):
        self.score = 0

    def update(selfs):
        self.score += 100
        print(self.score)


def add_piece(piece, board):
    return draw_piece(piece, board)


# occupied coords come in tuples (y, x, color)
def create_board(WIDTH, HEIGHT, occupied_coords):
    board = np.zeros((HEIGHT, WIDTH))
    for coord in occupied_coords:
        board[coord[0]][coord[1]] = coord[2]
    return board


# changes the coordinates of a piece, -1 is left, 0 is down, 1 is right
def move_piece(piece, direction):
    new_coords = []
    if direction == 0:
        for coord in piece.coordinates:
            new_coords.append((coord[0] + 1, coord[1]))
    else:
        for coord in piece.coordinates:
            new_coords.append((coord[0], coord[1] + direction))

    return new_coords


def draw_piece(piece, board):
    for coord in piece.coordinates:
        board[coord[0]][coord[1]] = piece.color
    return board


def down_collision(piece, occupied_coords):
    for coord in drop_piece(piece):
        if coord[0] > 19 or occupied_collision(coord, occupied_coords):
            return True
    return False


def lateral_collision(piece, occupied_coords, direction):
    for coord in move_lateral(piece, direction):
        if coord[1] < 0 or coord[1] > 9 or occupied_collision(coord, occupied_coords):
            return True
    return False


def occupied_collision(coord, occupied_coords):
    # Remove color value for occupied coords
    occupied_coords_no_color = []
    for i in occupied_coords:
        occupied_coords_no_color.append((i[0], i[1]))
    if coord in occupied_coords_no_color:
        return True
    return False


def move_lateral(piece, direction):
    return move_piece(piece, direction)


def drop_piece(piece):
    return move_piece(piece, 0)


def rotate_piece(piece):
    new_coords = []
    counter_clockwise_rotation_matrix = np.array([[0, -1],
                                                  [1, 0]])

    # difference between current coord0 and template coord0
    translation = (piece.coordinates[0+1])

    shape_centered_at_0 = []
    for coord in piece.coordinates:
        shape_centered_at_0.append((coord[0] - translation[0], coord[1] - translation[1]))

    # create a list of 2x1 numpy matrices of the shapes coordinates
    structured_shape_template = []
    for coord in shape_centered_at_0:
        structured_shape_template.append(np.array(([coord[0]], [coord[1]])))

    # rotate the shape template
    rotated_shape_centered_at_0 = []
    for m in structured_shape_template:
        rotated_shape_centered_at_0.append(np.dot(counter_clockwise_rotation_matrix, m))

    # return rotated coordinates to a sinlge list of tuples
    rotated_coords = []
    for element in rotated_shape_centered_at_0:
        rotated_coords.append((element[0][0], element[1][0]))

    # translate it to the old piece location
    for i in rotated_coords:
        new_coords.append((i[0] + translation[0], i[1] + translation[1]))

    return new_coords


def rotated_collision(piece, occupied_coords):
    for coord in rotate_piece(piece):
        #Check for laterally on the board
        if coord[1] < 0 or coord[1] >= WIDTH:
            return True
        # Check for vertically on the board
        if coord[0] < 0 or coord[0] >= HEIGHT:
            return True
        # Check for collisions
        if occupied_collision(coord, occupied_coords):
            return True
    return False


def sort_occupied_coords(occupied_coords, new_coords):
    # add the new coordinates and sort the list
    occupied_coords = occupied_coords + new_coords
    occupied_coords.sort(reverse=True, key=lambda tup: (tup[0], tup[1]))
    return occupied_coords


def remove_full_rows(sorted_coords, score):
    # check if there are 10 tuples with the same y value
    row = -1
    for i in range(len(sorted_coords)-9):
        if sorted_coords[i][0] == sorted_coords[i+9][0]:
            row = i
            break

    # there is a full row
    row_removed = sorted_coords
    if row != -1:
        # remove that row and shift coords
        row_removed = sorted_coords[:i]
        for coord in sorted_coords[i+10:]:
            row_removed.append((coord[0] + 1, coord[1], coord[2]))

        # repeat
        score += 100
        rows_and_score = remove_full_rows(row_removed, score)
        row_removed = rows_and_score[0]
        score = rows_and_score[1]
    return [row_removed, score]


def draw_board(board, win):

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    #draw in colour for each coordinate and draw grey seperation lines for top/left edges
    for i in range(WIDTH):

        for j in range(HEIGHT):
            color = rgbcolours[int(board[j][i])]

            pygame.draw.rect(win, color, (top_left_of_board[0] + i*BLOCK_SIZE, top_left_of_board[1] + j*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

            pygame.draw.line(win, (100, 100, 100), (top_left_of_board[0], top_left_of_board[1] + j * BLOCK_SIZE),
                             (top_left_of_board[0] + 300, top_left_of_board[1] + j * BLOCK_SIZE), 2)
        pygame.draw.line(win, (100, 100, 100), (top_left_of_board[0] + i * BLOCK_SIZE, top_left_of_board[1]),
                         (top_left_of_board[0] + i * BLOCK_SIZE, top_left_of_board[1] + 600), 2)

    # Bottom horizontal line
    pygame.draw.line(win, (100, 100, 100), (top_left_of_board[0], top_left_of_board[1] + HEIGHT*BLOCK_SIZE),
                     (top_left_of_board[0] + WIDTH*BLOCK_SIZE, top_left_of_board[1] + HEIGHT*BLOCK_SIZE), 2)
    # Right Edge Vertical Line
    pygame.draw.line(win, (100, 100, 100), (top_left_of_board[0] + WIDTH*BLOCK_SIZE, top_left_of_board[1]),
                     (top_left_of_board[0] + WIDTH*BLOCK_SIZE, top_left_of_board[1] + HEIGHT*BLOCK_SIZE), 2)
    pygame.display.update()

def update_score(score, win):
    label = myfont.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(label, (10, 10))
    print(score)


def main_loop(win):
    run = True
    fall_time = 0
    occupied_coords = []
    score = 0
    move_command = 0
    # clock = pygame.time.Clock()
    current_piece = shape(random.choice(types), 0)

    # Main loop
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Set which key was pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_command = -1
                if event.key == pygame.K_RIGHT:
                    move_command = 1
                if event.key == pygame.K_DOWN:
                    move_command = 0
                if event.key == pygame.K_UP:
                    move_command = 2

                if move_command == 2:
                    if rotated_collision(current_piece, occupied_coords):
                        pass
                    else:
                        current_piece.coordinates = rotate_piece(current_piece)

                # Move
                if move_command == 1 or move_command == -1:
                    if lateral_collision(current_piece, occupied_coords, move_command):
                        pass
                    else:
                        current_piece.coordinates = move_lateral(current_piece, move_command)

                # Drop
                if move_command == 0:
                    if down_collision(current_piece, occupied_coords):
                        collision_coords = []
                        for coord in current_piece.coordinates:
                            if coord[0] == 0:
                                run = False
                                break
                            else:
                                collision_coords.append((coord[0], coord[1], current_piece.color))

                        occupied_coords = sort_occupied_coords(occupied_coords, collision_coords)

                        #remove rows if necessary and update score
                        coords_and_score = remove_full_rows(occupied_coords, score)
                        occupied_coords = coords_and_score[0]
                        score = coords_and_score[1]

                        update_score(score, win)
                        current_piece = shape(random.choice(types), 0)
                    else:
                        current_piece.coordinates = drop_piece(current_piece)

                # Draw board
                board = create_board(WIDTH, HEIGHT, occupied_coords)
                board = draw_piece(current_piece, board)
                #print(board)
                draw_board(board, win)

    pygame.quit()

pygame.init()
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
myfont = pygame.font.SysFont("monospace", 76)
main_loop(win)

