from tkinter import *
import sys

board = [[0] * 8 for i in range(8)]
count = 0
probabilities = []


#
# check of duplicates in one row and columns
def duplicate(q):
    if len(q) != len(set(q)):
        return True
    else:
        return False


# --------------------------------------------------------------------------
# check for diagonal conflict
def diagonal_conflict(q):
    for col in range(7, 0, -1):
        for i in range(col):
            if col - i == abs(q[col] - q[i]):
                return True
    return False


# --------------------------------------------------------------------------
# print the the board in grid view
def print_board(Matrix):
    for i in range(len(Matrix[1])):
        print("  " + str(i), sep='  ', end='', flush=True)
    print("")
    for i, element in enumerate(Matrix):
        print(str(i) + ''.join(str(element)))


# ----------------------------------------------------------------------------
# drawing board section
def draw(w, LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR, rect, oval, cell_width, cell_height):
    count = 0
    for column in range(8):
        for row in range(8):
            x1 = column * cell_width
            y1 = row * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            color = [LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR][(row - column) % 2]

            rect[row, column] = w.create_rectangle(x1, y1, x2, y2, fill=color)
            oval[row, column] = w.create_oval(x1 + 20, y1 + 20, x2 - 20, y2 - 20, fill=color, outline=color)


def locate_queen(row, column, rect, w):
    queen_id = rect[row, column]
    w.itemconfig(queen_id, fill="#030303")


# create new window for every solution
def create_window(q, count):
    master = Tk()
    master.grid()
    master.configure(bg='#fff')
    master.resizable(False, False)
    l = Label(master, font=("zorque", 18), text="Welcome  to  8  Queen  Puzzle  solutions\n#" + str(count), fg='#fff',
              bg='#344146')
    l.grid(row=1, column=1, sticky='NWNESWSE')
    w = 8 * 70  # width for the Tk root
    h = 8 * 85  # height for the Tk root
    # get screen width and height
    ws = master.winfo_screenwidth()  # width of the screen
    hs = master.winfo_screenheight()  # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (w / 2)
    y = (hs / 5) - (h / 5)
    # set the dimensions of the screen
    # and where it is placed
    master.geometry('%dx%d+%d+%d' % (w, h, x, y))
    master.title('8 Queen puzzle number of possible solutions \'92\'')
    cell_width = 70
    cell_height = 70

    rect = {}
    oval = {}

    DARK_SQUARE_COLOR = '#D28C47'
    LIGHT_SQUARE_COLOR = '#FECE9E'

    w = Canvas(master, width=8 * cell_width, height=8 * cell_height)
    w.grid(row=2, column=1, sticky='NWNESWSE')
    btn = Button(font=("ARCADECLASSIC", 12), text='Next >> #' + str(count + 1), command=lambda: master.destroy(),
                 bg="#EBBD63", fg="#3C3741")
    btn.grid(row=3, column=1, sticky='NWNESWSE')
    btn1 = Button(font=("ARCADECLASSIC", 12), text='Quit', command=lambda: sys.exit(), bg="#EBBD63", fg="#3C3741")
    btn1.grid(row=4, column=1, sticky='NWNESWSE')

    draw(w, LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR, rect, oval, cell_width, cell_height)
    # --------------------------------------------------------------------------
    # fill the board with Queens places
    for row in q:
        board[row][q.index(row)] = '.'
        locate_queen(row, q.index(row), oval, w)
    mainloop()


# --------------------------------------------------------------------------
# perform the algorithm for all probabilities

for i1 in range(8):
    for i2 in range(8):
        for i3 in range(8):
            for i4 in range(8):
                for i5 in range(8):
                    for i6 in range(8):
                        for i7 in range(8):
                            for i8 in range(8):
                                probabilities = [i1, i2, i3, i4, i5, i6, i7, i8]
                                if duplicate(probabilities) or diagonal_conflict(probabilities):
                                    continue
                                else:
                                    count += 1
                                    print("the solution number", count, ">>", probabilities)
                                create_window(probabilities, count)
                                print_board(board)
                                board = [[0] * 8 for i in range(8)]  # reset the board for an other probability
