# fix collision system, check before commit to new coords


import pygame
import random
import numpy as np

types = [0, 1, 2, 3, 4, 5]
colors = [1, 2, 3, 4, 5, 6]
WIDTH = 10
HEIGHT = 20
FALL_SPEED = 3
#Coordinates of each shape with top left being 0,0, y axis increase as it goes down
SHAPE_COORDINATES = {0: [(0, 0), (0, 1), (1, 0), (1, 1)],
                     1: [(0, 0), (0, 1), (1, 1), (1, 2)]}

# General shape class
class shape:
    def __init__(self, type, rotation):
        self.type = type
        self.rotation = rotation
        self.color = colors[type]
        self.coordinates = SHAPE_COORDINATES[type]


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

    if direction == 0:
        print( 'Drop to: ', new_coords)
    else:
        print( 'Move to: ', new_coords)
    return new_coords

def draw_piece(piece, board):
    for coord in piece.coordinates:
        board[coord[0]][coord[1]] = piece.color
    return board


def down_collision(piece, occupied_coords):
    for coord in drop_piece(piece):
        if coord[0] >19 or occupied_collision(coord, occupied_coords):
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
    translation = (piece.coordinates[0])

    shape_centered_at_0 = []
    for coord in piece.coordinates:
        shape_centered_at_0.append((coord[0] - translation[0], coord[1] - translation[1]))

    #create a list of 2x1 numpy matrices of the shapes coordinates
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

    print( 'Rotate to: ', new_coords)
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


def main_loop():
    run = True
    fall_time = 0
    occupied_coords = []
    i = 0
    #clock = pygame.time.Clock()
    #current_piece = shape(random.choice(types), 0)
    current_piece = shape(1, 0)

    # Main loop
    while run:

        print( 'At: ', current_piece.coordinates)

        #Spin
        if rotated_collision(current_piece, occupied_coords):
            pass
        else:
            current_piece.coordinates = rotate_piece(current_piece)


        #Move
        if lateral_collision(current_piece, occupied_coords, 1):
            pass
        else:
            current_piece.coordinates = move_lateral(current_piece, 1)


        #Drop
        if down_collision(current_piece, occupied_coords):
            for coord in current_piece.coordinates:
                occupied_coords.append((coord[0], coord[1], current_piece.color))
            current_piece = shape(random.choice([0,1]), 0)

            #Run 10 pieces to check collisions
            if i > 2:
                run = False
            i += 1
        else:
            current_piece.coordinates = drop_piece(current_piece)

        board = create_board(WIDTH, HEIGHT, occupied_coords)
        #print(current_piece.coordinates)
        #print(occupied_coords)
        board = draw_piece(current_piece, board)
        print(board, '\n\n')



main_loop()