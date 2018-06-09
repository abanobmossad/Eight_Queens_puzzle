from _sitebuiltins import _Printer
from itertools import product
from tkinter import *  # import tkinter for GUI purposes
import random,time

# ---------------------- #
# creating gui window   |
# ---------------------- #

master = Tk()  # make window
master.title('8 Queens user version')  # window title
master.grid()  # grid to place objects in right places
master.resizable(False, False)
cell_width = 75  # chess board cell width
cell_height = 75  # chess board cell height
w = 8 * 75  # width for the Tk root
h = 8 * 80 # height for the Tk root
# get screen width and height
ws = master.winfo_screenwidth()  # width of the screen
hs = master.winfo_screenheight()  # height of the screen
# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (w / 2)
y = (hs / 4) - (h / 3.5)
# set the dimensions of the screen
# and where it is placed
master.geometry('%dx%d+%d+%d' % (w, h, x, y))
rect = {}  # store all chess board cell right places
oval = {}  # store all oval on chess board cell  places

DARK_SQUARE_COLOR = '#CF8440'  # cell dark color
LIGHT_SQUARE_COLOR = '#FEE4C3'  # cell light color

# the top label and result board
l = Label(master, font=("Cambria", 18, "bold"), text="Welcome  to  8  Queen  Puzzle  game", fg='#526187',
          bg='#EBBD63')
l.grid(row=1, column=1, sticky='NWNESWSE')  # set on top the grid

# create the canvas that contain all the board cells
w = Canvas(master, width=8 * cell_width, height=8 * cell_height)
w.grid(row=3, column=1, sticky='NWNESWSE')  # place it on the middle of the grid
massage = [""]
motivation = ["Good", "Excellent Move", "That's a very Good move", "I'm never doubt your intelligent", "Your the man"]
right_solution = [0]
win=[False]

# -----------------------------------------------------------------------------
# --------------#
# Timer function|
# --------------#
sec=[0]
men=[0]
def update_clock():
    s=str(l.cget("text")).split("   ♦")
    sec[0] += 1
    if sec[0]==59:
        men[0]+=1
        sec[0]=0
    l.configure(text=s[0]+"   ♦"+'0H:'+str(men[0])+'M:'+str(sec[0])+"S♦")
    if not win[0]:
        master.after(1000, update_clock)
update_clock()
# -----------------------------------------------------------------------------

# ------------------------------------------------------ #
# Function to check if all the rows have single queen  |
# ------------------------------------------------------ #


def duplicate(qro):
    if len(qro) != len(set(qro)):  # check if the length of the list is still the same if removed the duplication
        massage[0] = " Row Error (Undo by click it again)"
        return True
    else:
        return False


# --------------------------------------------------------------------------

# ----------------------------------------- #
# Function to check for diagonal conflict |
# ----------------------------------------- #


def diagonal_conflict(qr):
    for col in range(len(qr) - 1, 0, -1):
        for i in range(col):
            if qr[i] < 0 or qr[col] < 0:
                continue

            elif col - i == abs(qr[col] - qr[i]):
                massage[0] = " Diagonal Error (Undo by click it again)"
                return True

    return False


# -----------------------------------------------------------------------------

# -------------------------------------------------------------------- #
# Function to draw chess board with its all cells the dark and light |
# -------------------------------------------------------------------- #


def draw():
    for column in range(8):  # draw all 8 columns
        for row in range(8):  # draw all 8 rows
            x1 = column * cell_width  # move to the next column by the cell width so all next to each other no gaps
            y1 = row * cell_height  # move to the next row by the cell height so all next to each other no gaps
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            color = [LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR][(row - column) % 2]  # switch colors on diagonal mater

            # create the squares and store it's place in rect var
            rect[row, column] = w.create_rectangle(x1, y1, x2, y2, fill=color, outline=color, tag="rect")

            # create oval in the center of the square and store it's place on oval var
            oval[row, column] = w.create_oval(x1 + 10, y1 + 10, x2 - 10, y2 - 10, fill=color, outline=color, tag='oval')
            w.tag_bind('oval', '<ButtonPress-1>', click_square_cell)


# -----------------------------------------------------------------------------

q = [-1, -2, -3, -4, -5, -6, -7, -8]  # main chromosome of the empty chess board
counting_values = []  # contain place of all the queens the right and the wrong
error_values = []  # contain the error places of the queens
error_value = []  # contain the error row values

# -----------------------------------------------------------------------------

# ----------------#
# Reset the game |
# ----------------#

btn = Button()


def reset():
    w.delete("all")
    draw()
    q[:] = [-1, -2, -3, -4, -5, -6, -7, -8]
    l.configure(font=("Cambria", 17, "bold"), text="New Game!! that's mean you solve it ☺ ", fg='#526187',
                bg='#EBBD63')
    btn.destroy()
    ws = 8 * 75  # width for the Tk root
    hs = 8 * 80  # height for the Tk root
    master.geometry('%dx%d' % (ws, hs))
    win[0]=False
    sec[0]=0
    men[0]=0
    update_clock()

# -----------------------------------------------------------------------------

# ------------------------------------------#
# getting the row and column from the user |
# ------------------------------------------#


def click_square_cell(event):
    if sum(x >= 0 for x in q) == 8:
        l.configure(text="Congratulation you win in", font=("Cambria", 22), fg='#11CD86',
                    bg="#445252")  # user solution wrong
        btn = Button()
        btn.configure(text="NewGame", font=("Cambria", 16), fg="#E6E6E6", bg="#248888", command=reset)
        btn.grid(row=4, column=1, sticky='NWNESWSE')
        ws = 8 * 75  # width for the Tk root
        hs = 8 * 86  # height for the Tk root
        master.geometry('%dx%d' % (ws, hs))
        win[0]=True

    else:
        rect_value = event.widget.find_closest(event.x, event.y)[0]  # get the square place on click
        queen_id = rect_value  # select the queen id to change it's color

        if rect_value in counting_values:  # check if i click it once or not if it is infill the oval
            for k, v in oval.items():
                if v == rect_value and v not in error_values:  # remove the values from all lists and main chromosome list
                    q[k[1]] = -1 * (k[1] + 1)  # do remove

                if v == rect_value:
                    counting_values.remove(rect_value)  # do remove
                    try:  # if any lists exception pop up
                        error_value.remove(k[0])  # do remove
                    except ValueError:
                        pass  # don't do any thing only don't show it to me

            if rect_value in error_values:  # check if it one of the error values
                error_values.remove(rect_value)  # do remove
            l.configure(text="That's much better", font=("Cambria", 22), fg="#E6E6E6",
                        bg="#248888")  # user solution wrong
            w.itemconfig(queen_id, fill="#D6B572", outline='#D6B572')  # change the color
            # ------------------------------------------------------------------
        else:  # if it's the first time i click the square

            counting_values.append(rect_value)  # store the place in the all values list
            the_value=0
            for k, v in oval.items():
                if v == rect_value:
                    if k[0] in error_value:  # if it in the list of row errors
                        massage[0] = " Row Error (Undo by click it again)"
                        l.configure(text=massage[0], font=("Cambria", 22), fg="#F72100",
                                    bg="#263149")  # user solution wrong

                    if q[k[1]] < 0:  # check if the place of the queen is empty or not
                        q[k[1]] = k[0]
                        the_value=k[1]
                        w.itemconfig(queen_id, fill="black", outline='black')  # highlight it to black "good move"
                        mot = motivation[random.randrange(0, len(motivation) - 1)]  # motivation word for player
                        l.configure(text=mot, font=("Cambria", 22), fg="#fff", bg="#066FA5")
                        if sum(x >= 0 for x in q) == 8:
                            l.configure(text="Congratulation you win in", font=("Cambria", 22), fg='#11CD86',
                                        bg="#445252")  # user solution wrong
                            btn = Button()
                            btn.configure(text="NewGame", font=("Cambria", 16), fg="#E6E6E6", bg="#248888",
                                          command=reset)
                            btn.grid(row=4, column=1, sticky='NWNESWSE')
                            ws = 8 * 75  # width for the Tk root
                            hs = 8 * 86  # height for the Tk root
                            master.geometry('%dx%d' % (ws, hs))
                            win[0] = True


                    else:  # not empty and store it in error lists
                        l.configure(text=massage[0], font=("Cambria", 22), fg="#F72100",
                                    bg="#263149")  # user solution wrong
                        error_values.append(rect_value)
                        error_value.append(k[0])
                        w.itemconfig(queen_id, fill="red", outline='red')  # highlight it to red "error"

            # check every list for the type of the error
            for val in error_values:  # Column error
                if rect_value == val:
                    massage[0] = " Column Error (Undo by click it again)"
                    l.configure(text=massage[0], font=("Cambria", 22), fg="#F72100",
                                bg="#263149")  # user solution wrong
                    break  # break the loop

                # Diagonal error
                elif abs(rect_value - val) % 18 == 0 or abs(rect_value - val) % 14 == 0 and rect_value != val:
                    massage[0] = " Diagonal Error (Undo by click it again)"
                    l.configure(text=massage[0], font=("Cambria", 22), fg="#F72100",
                                bg="#263149")  # user solution wrong
                w.itemconfig(queen_id, fill="red", outline='red')  # highlight it to red "error"

            # check error in original chromosome
            if duplicate(q) or diagonal_conflict(q):
                l.configure(text=massage[0], font=("Cambria", 22), fg="#F72100", bg="#263149")  # user solution wrong
                w.itemconfig(queen_id, fill="red", outline='red')
                try:
                    q[the_value]=-1*(the_value+1)
                except:
                    pass
        print(q)

draw()  # call draw
mainloop()  # for make the window continue running until close it
