import pygame
from tkinter import *
from  tkinter import ttk
import tkinter as tk
import random
import sqlite3
import time
from datetime import date


pygame.init()

con = sqlite3.connect('userscore.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS tscores
                (username text, score int, date text)''')

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

def check_lost(locked_pos, surface, score, username):
    for pos in locked_pos:
        if pos[1] <= 0:
            myfont = pygame.font.SysFont("Futura", 50)

            label = myfont.render("YOU LOST", 3, (200, 200, 200))
            surface.blit(label, (320, 300))
            pygame.display.update()
            pygame.time.delay(2000)
            update_score(username, score)
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


def draw_score(surface, high_score, score=0): #display score
    #score
    myfont = pygame.font.SysFont("monospace", 20)
    label1 = myfont.render('Score: ', 1, (255,255,255))
    surface.blit(label1, (580, 400))
    label2 = myfont.render(str(score), 1, (255, 255, 255))
    surface.blit(label2, (680, 400))

    #high score
    label = myfont.render('High Score: ' + str(high_score), 1, (255, 255, 255))
    surface.blit(label, (580, 450))
    pygame.display.update()


def draw_player(surface,username):
    x_pos = 50
    y_pos = 50

    myfont = pygame.font.SysFont("monospace", 20)

    label = myfont.render("Player: "+ username, 1, (255, 0, 0))
    surface.blit(label, (x_pos, y_pos))


def draw_holdshape(hold_shape, surface):
    x_pos = 50
    y_pos = 200

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


def update_score(username, new_score):
    cur.execute("INSERT INTO tscores VALUES (?,?,?)",
                   (username, new_score, date.today().strftime('%d/%m/%Y')))
    con.commit()

def max_score(name):
    cur.execute('SELECT MAX(score) FROM tscores WHERE username=?', [name])
    return cur.fetchone()[0]

def main(username):
    if username == "guest":
        high_score = "n/a"
    else:
        high_score = max_score(username)

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
    score=0

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
        draw_score(surface, high_score, score)
        draw_player(surface, username)
        pygame.display.update()

        if check_lost(locked_positions, surface, score, username):
            break


def user_stats(name):
    global screen_s
    #screen_s = Toplevel(root)
    #screen_s.title("stats")
    #screen_s.geometry("500x500")

    # Creating tkinter window
    window = tk.Tk()
    window.resizable(width=1, height=1)
    window.title("STATS")

    # Using treeview widget
    treev = ttk.Treeview(window, selectmode='browse')

    # Calling pack method w.r.to treeview
    treev.pack(side=RIGHT)

    # Constructing vertical scrollbar
    # with treeview
    verscrlbar = ttk.Scrollbar(window,
                               orient="vertical",
                               command=treev.yview)

    # Calling pack method w.r.to vertical
    # scrollbar
    verscrlbar.pack(side='right', fill='x')

    # Configuring treeview
    treev.configure(xscrollcommand=verscrlbar.set)

    # Defining number of columns
    treev["columns"] = ("1", "2", "3")
    # Defining heading
    treev['show'] = 'headings'

    # Assigning the width and anchor to  the
    # respective columns
    treev.column("1", width=90, anchor='c')
    treev.column("2", width=90, anchor='se')
    treev.column("3", width=90, anchor='se')

    # Assigning the heading names to the
    # respective columns

    treev.heading("1", text="Player")
    treev.heading("2", text="Score")
    treev.heading("3", text="Date")

    # Inserting the items and their features to the
    # columns built

    cur.execute('SELECT username, score, date FROM tscores WHERE username=?', [name])
    lst = cur.fetchall()

    for value in lst:
        treev.insert("", 'end', text="L1",
                     values=(value[0], value[1], value[2]))


    # Using treeview widget
    tree2 = ttk.Treeview(window, selectmode='browse')

    # Calling pack method w.r.to treeview
    tree2.pack(side=LEFT)

    # Constructing vertical scrollbar
    # with treeview
    verscrlbar = ttk.Scrollbar(window,
                               orient="vertical",
                               command=tree2.yview)

    # Calling pack method w.r.to vertical
    # scrollbar
    verscrlbar.pack(side='left', fill='x')

    # Configuring treeview
    tree2.configure(xscrollcommand=verscrlbar.set)

    # Defining number of columns
    tree2["columns"] = ("1", "2")
    # Defining heading
    tree2['show'] = 'headings'

    # Assigning the width and anchor to  the
    # respective columns
    tree2.column("1", width=90, anchor='c')
    tree2.column("2", width=90, anchor='se')

    # Assigning the heading names to the
    # respective columns

    tree2.heading("1", text="Player")
    tree2.heading("2", text="Score")

    # Inserting the items and their features to the
    # columns built

    cur.execute('SELECT username, MAX(score) FROM tscores GROUP BY username ORDER BY 2 DESC LIMIT 5')
    lst_scoreboard = cur.fetchall()

    for info in lst_scoreboard:
        tree2.insert("", 'end', text="L1",
                     values=(info[0], info[1]))

    cur.execute('SELECT AVG(score) FROM tscores WHERE username=?', [name])
    avgscore = cur.fetchone()[0]
    Label(window, text="Average Score: " + str(avgscore), width=20, heigh=5).pack(side=BOTTOM)

    cur.execute('SELECT MAX(score) FROM tscores WHERE username=?', [name])
    highscore = cur.fetchone()[0]
    Label(window, text="High Score: " + str(highscore), width=20, heigh=5).pack(side=BOTTOM)

    cur.execute('SELECT COUNT(*) FROM tscores WHERE username=?', [name])
    highscore = cur.fetchone()[0]
    Label(window, text="Games Played: " + str(highscore), width=20, heigh=5).pack(side=BOTTOM)

    window.mainloop()

def start(username):
    screen_g.destroy()
    screen_l.destroy()
    root.destroy()
    main(username)

def before_game(username):
    global screen_g
    screen_g = Toplevel(root)
    screen_g.title("user")
    screen_g.geometry("300x250")

    Label(screen_g, text="").pack()
    Button(screen_g, text="Stats", width=20, heigh=5, command=lambda: user_stats(username)).pack()
    Label(screen_g, text="").pack()
    Button(screen_g, text="Start Game", width=20, heigh=5, command=lambda : start(username)).pack()
    Label(screen_g, text="").pack()


def register_user():
    username_info = username.get()
    password_info = password.get()

    file=open("userinfo.txt", "a")
    file.write(username_info)
    file.write(" ")
    file.write(password_info)
    file.write("\n")
    file.close

    username_entry.delete(0,END)
    password_entry.delete(0,END)

    Label(screen_r, text = "Regristration Sucess", fg="green").pack()
    screen_r.destroy()

def register():
    global screen_r
    screen_r = Toplevel(root)
    screen_r.title("Register")
    screen_r.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry

    username = StringVar()
    password = StringVar()

    Label(screen_r, text="Please enter details below").pack()
    Label(screen_r, text="").pack()
    Label(screen_r, text="Username * ").pack()
    username_entry = Entry(screen_r, textvariable = username)
    username_entry.pack()
    Label(screen_r, text="Password * ").pack()
    password_entry= Entry(screen_r,textvariable=password)
    password_entry.pack()
    Label(screen_r, text="").pack()

    Button(screen_r, text="Register", width="10", height="1", command = register_user).pack()


def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()

    username_entry1.delete(0, END)
    password_entry1.delete(0, END)

    for line in open("userinfo.txt","r").readlines(): # Read the lines
        login_info = line.split() # Split on the space, and store the results in a list of two strings
        if username1 == login_info[0]:
            if password1 == login_info[1]:
                Label(screen_l, text="login sucess").place(x=100, y=200)
                before_game(username1)
                break
            else:
                Label(screen_l, text="incorrect password").place(x=100, y=200)
        else:
            Label(screen_l, text="user not found").place(x=100, y=200)

def login():
    global screen_l
    screen_l = Toplevel(root)
    screen_l.title("Login")
    screen_l.geometry("300x250")
    Label(screen_l, text="Please enter details below to login").pack()
    Label(screen_l, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_entry1
    global password_entry1

    Label(screen_l, text="Username * ").pack()
    username_entry1 = Entry(screen_l, textvariable=username_verify)
    username_entry1.pack()
    Label(screen_l, text="Password * ").pack()
    password_entry1 = Entry(screen_l, textvariable=password_verify)
    password_entry1.pack()
    Label(screen_l, text="").pack()

    Button(screen_l, text="Login", width=10, heigh=1,command=login_verify).pack()

def login_register():
    global root
    root = Tk()
    root.title("Login/Register")
    root.geometry("300x200")

    Label(text="Login or Register", bg="grey", width="300", height="2").pack()
    Label(text="").pack()
    Button(text="Login", width="30", height="2", command=login).pack()
    Label(text="").pack()
    Button(text="Register", width="30", height="2", command=register).pack()
    Label(text="").pack()

    root.mainloop()

def main_menu(surface):
    font = pygame.font.SysFont('timesnewroman', 30)

    label1 = font.render('Press space to play as GUEST', 1, (255,255,255))
    label2 = font.render('Press u to login/register as USER', 1, (255, 255, 255))
    image = pygame.image.load(r"C:\Users\joyce\PycharmProjects\games\tetris-logo.jpg")

    run = True
    while run:
        win.fill((0,0,0))
        win.blit(image, (100, 100))
        surface.blit(label1, (260, 550))
        surface.blit(label2, (270, 600))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main("guest")
                if event.key == pygame.K_u:
                    login_register()
                break

    pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu(win)  # start game
