import pygame
import random

pygame.init()

I = [['0000',
      '1111',
      '0000',
      '0000'],
     ['0100',
      '0100',
      '0100',
      '0100'],
     ['0000',
      '0000',
      '1111',
      '0000'],
     ['0010',
      '0010',
      '0010',
      '0010']]

O = [['1100',
      '1100',
      '0000',
      '0000'],
     ['1100',
      '1100',
      '0000',
      '0000'],
     ['1100',
      '1100',
      '0000',
      '0000'],
     ['1100',
      '1100',
      '0000',
      '0000']]

L = [['0100',
      '0100',
      '0110',
      '0000'],
     ['0000',
      '1110',
      '1000',
      '0000'],
     ['1100',
      '0100',
      '0100',
      '0000'],
     ['0010',
      '1110',
      '0000',
      '0000']]

J = [['0100',
      '0100',
      '1100',
      '0000'],
     ['1000',
      '1110',
      '0000',
      '0000'],
     ['0110',
      '0100',
      '0100',
      '0000'],
     ['0000',
      '1110',
      '0010',
      '0000']]

S = [['0000',
      '0110',
      '1100',
      '0000'],
     ['1000',
      '1100',
      '0100',
      '0000'],
     ['0110',
      '1100',
      '0000',
      '0000'],
     ['0100',
      '0110',
      '0010',
      '0000']]

Z = [['0000',
      '1100',
      '0110',
      '0000'],
     ['0100',
      '1100',
      '1000',
      '0000'],
     ['1100',
      '0110',
      '0000',
      '0000'],
     ['0010',
      '0110',
      '0100',
      '0000']]

T = [['0000',
      '1110',
      '0100',
      '0000'],
     ['0100',
      '1100',
      '0100',
      '0000'],
     ['0100',
      '1110',
      '0000',
      '0000'],
     ['0100',
      '0110',
      '0100',
      '0000']]

# GLOBALS VARS
column = 10
row = 20

s_width = 800
s_height = 650
t_width = 300
t_height = 600
grid_x = (s_width - t_width) / 2
grid_y = (s_height - t_height) / 2
unit = t_width / column

lstShape = [I, O, L, J, S, Z, T]
lstColour = [(0, 255, 255), (255, 255, 0), (255, 127, 0), (0, 0, 255), (255, 0, 0), (0, 255, 0), (128, 0, 128)]


class Peice:
    def __init__(self, shape, colour, rotation, x, y):
        self.shape = shape  # 0-6
        self.colour = colour  # 0-6
        self.rotation = rotation  # 0-3
        self.x = x;
        self.y = y;

def get_holdshape(shape):
    return Peice(shape.shape, shape.colour, random.randint(0,3), 5, -1)

def get_shape():
    shape = random.choice(lstShape)
    index = lstShape.index(shape)
    colour = lstColour[index]
    rotation = random.randint(0, 3)
    x = 4
    y = -1

    return Peice(shape, colour, rotation, x, y)

def check_lost(locked_pos, surface, score):
    for pos in locked_pos:
        if pos[1] <= 0:
            myfont = pygame.font.SysFont("Futura", 50)

            label = myfont.render("YOU LOST", 3, (200, 200, 200))
            surface.blit(label, (320, 300))
            pygame.display.update()
            pygame.time.delay(2000)
            update_score(score)
            return True

    return False

def check_collisionRotate(locked_pos, curr_shape):
    shape = curr_shape.shape
    rotation = curr_shape.rotation
    piece = shape[rotation]

    for y in range(4):
        line = piece[y]
        for x in range(4):
            if line[x] == "1":
                if curr_shape.x + x >= column:
                    if x == 0:
                        return -4
                    elif x == 1:
                        return -3
                    elif x == 2:
                        return -2
                    elif x == 3:
                        return -1

                elif curr_shape.x + x <= -1:
                    if x == 0:
                        return 1
                    elif x == 1:
                        return 2
                    elif x == 2:
                        return 3
                    elif x == 3:
                        return 4
                elif (curr_shape.x + x, curr_shape.y + y) in locked_pos:
                    return 10
    return 0

def check_collisionLR(locked_pos, curr_shape):
    shape = curr_shape.shape
    rotation = curr_shape.rotation
    piece = shape[rotation]

    for y in range(4):
        line = piece[y]
        for x in range(4):
            if line[x] == "1":
                if curr_shape.x + x == column or curr_shape.x + x == -1:
                    return True
                elif (curr_shape.x + x, curr_shape.y + y) in locked_pos:
                    return True
    return False

def check_collision(locked_pos, curr_shape):

    shape = curr_shape.shape
    rotation = curr_shape.rotation
    piece = shape[rotation]

    for y in range(4):
        line = piece[y]
        for x in range(len(line)):
            if line[x] == "1":
                if curr_shape.y + y == row:
                    return True
                elif (curr_shape.x + x, curr_shape.y + y) in locked_pos:
                    return True
    return False

def clear_rows(locked_pos):
    lst_clear = []
    lst_to20 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
    completed_row = dict.fromkeys(lst_to20, 0)

    #counts the filled blocks for each row
    for block in locked_pos:
        num = completed_row[block[1]]
        completed_row[block[1]] = num + 1

    #creates list of filled rows
    for block in completed_row:
        if completed_row[block] == 10:
            lst_clear.append(block)

    lines = len(lst_clear)

    # removing the filled rows from locked position
    if len(lst_clear) > 0:
        for x in lst_clear:
            for block in list(locked_pos):
                if block[1] == x:
                    locked_pos.pop(block)

    # removing the filled rows from locked position
    if len(lst_clear) > 0:
        for x in lst_clear:
            for block in list(locked_pos):
                if block[1] == x:
                    locked_pos.pop(block)

        while len(lst_clear) != 0:
            for i in range(lst_clear[0], 0,-1):
                for block in list(locked_pos):
                    if (block[1] == i and block[1] < lst_clear[0]):
                        locked_pos[block[0], block[1] + 1] = locked_pos[block]
                        locked_pos.pop(block)
            lst_clear.pop(0)

            for i in range(len(lst_clear)):
                lst_clear[i] += 1

    return lines


# saves the landed shape position in locked pos
def save_position(curr_shape, locked_pos):
    shape = curr_shape.shape
    rotation = curr_shape.rotation
    piece = shape[rotation]

    for y in range(4):
        row = piece[y]
        for x in range(len(row)):
            if row[x] == "1":
                locked_pos[(curr_shape.x + x, curr_shape.y + y)] = curr_shape.colour

    return locked_pos


def draw_score(surface, score = 0, high_score = 0): #display score
    #score
    myfont = pygame.font.SysFont("monospace", 20)
    label = myfont.render('Score: ' + str(score), 1, (255,255,255))
    surface.blit(label, (580, 400))

    #high score
    label = myfont.render('High Score: ' + high_score, 1, (255, 255, 255))
    sx = 200
    sy = 150
    surface.blit(label, (580, 450))

def draw_holdshape(hold_shape, surface):
    x_pos = 50
    y_pos = 100

    myfont = pygame.font.SysFont("monospace", 20)

    label = myfont.render("Hold Shape (c)", 1, (255, 255, 255))
    surface.blit(label, (x_pos, y_pos))

    if hold_shape != 0:
        shape = hold_shape.shape
        rotation = hold_shape.rotation
        piece = shape[rotation]

        for y in range(4):
            line = piece[y]
            for x in range(4):
                if line[x] == "1":
                    pygame.draw.rect(surface, hold_shape.colour,
                                     pygame.Rect(x_pos + (x * unit) + 10, y_pos + (y * unit) + 50, unit, unit))
                else:
                    pygame.draw.rect(surface, (0,0,0),
                                     pygame.Rect(x_pos + (x * unit) + 10, y_pos + (y * unit) + 50, unit, unit))


def draw_nextshape(next_shape, surface):
    x_pos = grid_x + t_width + 50
    y_pos = grid_y + 100

    myfont = pygame.font.SysFont("monospace", 23)

    label = myfont.render("Next Shape", 1, (255, 255, 255))
    surface.blit(label, (x_pos, y_pos))

    shape = next_shape.shape
    rotation = next_shape.rotation
    piece = shape[rotation]

    for y in range(4):
        line = piece[y]
        for x in range(4):
            if line[x] == "1":
                pygame.draw.rect(surface, next_shape.colour,
                                 pygame.Rect(x_pos + (x * unit) + 10, y_pos + (y * unit) + 50, unit, unit))
            else:
                pygame.draw.rect(surface, (0,0,0),
                                 pygame.Rect(x_pos + (x * unit) + 10, y_pos + (y * unit) + 50, unit, unit))


#draws the locked positions shape
def draw_locked(locked_pos, surface):
    for key in locked_pos:
        pygame.draw.rect(surface, locked_pos[key], pygame.Rect(grid_x + (key[0] * unit), grid_y + (key[1] * unit), unit, unit))

# draws current shape
def draw_tetris(curr_shape, surface):
    x_pos = (curr_shape.x * t_width)/ column
    y_pos = (curr_shape.y * t_height)/ row

    shape = curr_shape.shape
    rotation = curr_shape.rotation
    piece = shape[rotation]

    for y in range(4):
        line = piece[y]
        for x in range(4):
            if line[x] == "1":
                pygame.draw.rect(surface, curr_shape.colour, pygame.Rect(grid_x + x_pos + (x * unit), grid_y +
                                                                         y_pos + (y * unit), unit, unit))

    for x in range(10):
        pygame.draw.rect(surface, (0,0,0), pygame.Rect(grid_x + unit * x, 0, unit + 2, unit - 5))

# draws the grid
def draw_grid(surface):
    background = (50, 50, 50)
    white = (255, 255, 255)

    pygame.draw.rect(surface, background, pygame.Rect(grid_x, grid_y, t_width, t_height))
    pygame.draw.rect(surface, white, pygame.Rect(grid_x, grid_y, t_width, t_height), 2)

    for x in range(column):
        for y in range(row):
            pygame.draw.line(surface, white, (grid_x, grid_y + (y * (t_height / row))),
                             (grid_x + t_width, grid_y + (y * (t_height / row))))
            pygame.draw.line(surface, white, (grid_x + (x * (t_width / column)), grid_y),
                             (grid_x + (x * (t_width / column)), grid_y + t_height))


def update_score(new_score):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if new_score > int(score):
            f.write(str(new_score))  # overwrites any existing content


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score


def main():
    high_score = max_score()
    pygame.init()
    surface = pygame.display.set_mode((s_width, s_height))

    locked_positions = {}
    curr_shape = get_shape()
    next_shape = get_shape()
    holdshape = 0
    hold_counter = 0
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while True:

        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        # PIECE FALLING CODE
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            curr_shape.y += 1

        draw_grid(surface)
        draw_nextshape(next_shape, surface)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                quit()
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rotation = (curr_shape.rotation + 1) % 4
                    curr_shape.rotation = rotation
                    shift = check_collisionRotate(locked_positions, curr_shape)

                    if shift == 10: # 10 represents that the shift is going into locked pos block, undo rotation
                        rotation = (curr_shape.rotation - 1) % 4
                        curr_shape.rotation = rotation
                    else:
                        curr_shape.x += shift

                if event.key == pygame.K_DOWN:
                    if (check_collision(locked_positions, curr_shape) == False):
                        curr_shape.y += 1

                if event.key == pygame.K_LEFT:
                    curr_shape.x -= 1
                    if check_collisionLR(locked_positions, curr_shape):
                        curr_shape.x += 1

                if event.key == pygame.K_RIGHT:
                    curr_shape.x += 1
                    if check_collisionLR(locked_positions, curr_shape):
                        curr_shape.x -= 1

                if event.key == pygame.K_SPACE:
                    while (check_collision(locked_positions, curr_shape) == False):
                            curr_shape.y += 1

                if hold_counter == 0 and event.key == pygame.K_c:
                        hold_counter = 1
                        newholdshape = holdshape
                        holdshape = curr_shape

                        if newholdshape == 0:
                            curr_shape = next_shape
                            next_shape = get_shape()
                        else:
                            curr_shape = get_holdshape(newholdshape)  # choses a random shape and rotation and puts it in the middle of board

        score += clear_rows(locked_positions) * 10
        if check_collision(locked_positions, curr_shape):
            curr_shape.y -= 1
            locked_positions = save_position(curr_shape, locked_positions)
            curr_shape = next_shape
            next_shape = get_shape()
            hold_counter = 0
        else:
            draw_tetris(curr_shape, surface)

        draw_locked(locked_positions, surface)
        draw_holdshape(holdshape, surface)
        draw_score(surface, score, high_score)
        pygame.display.update()

        if check_lost(locked_positions, surface, score):
            break

def main_menu(surface):
    font = pygame.font.SysFont('timesnewroman', 30)
    label = font.render('Press any key to begin.', 1, (255,255,255))
    image = pygame.image.load(r"C:\Users\joyce\PycharmProjects\games\tetris-logo.jpg")

    run = True
    while run:
        win.fill((0,0,0))
        win.blit(image, (100, 100))
        surface.blit(label, (270, 550))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu(win)  # start game
