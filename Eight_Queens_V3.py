from tkinter import *
import sys

# -----------------------------------------------------------------------------
# creating gui window
master = Tk()
master.title('8 Queens user version')
master.grid()
master.resizable(False,False)
cell_width = 70
cell_height = 70

rect = {}
oval = {}

DARK_SQUARE_COLOR = '#CF8440'
LIGHT_SQUARE_COLOR = '#FEE4C3'

l = Label(master, font=("Cambria", 22), text="Welcome  to  8  Queen  Puzzle  solutions", fg='#fff',
          bg='#344146')
l.grid(row=1, column=1, sticky='NWNESWSE')
w = Canvas(master, width=8*cell_width, height=8*cell_height)
w.grid(row=2, column=1, sticky='NWNESWSE')
btn = Button(font=("ARCADECLASSIC", 12), text='Check solution', command=lambda: check(),
             bg="#EBBD63", fg="#3C3741")
btn.grid(row=3, column=1, sticky='NWNESWSE')
btn1 = Button(font=("ARCADECLASSIC", 12), text='Quit', command=lambda: sys.exit(), bg="#EBBD63", fg="#3C3741")
btn1.grid(row=4, column=1, sticky='NWNESWSE')
# -----------------------------------------------------------------------------
probabilities = [ ]


# -----------------------------------------------------------------------------
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
            if q[i] <0 or q[col]<0:
                continue

            elif col - i == abs(q[ col ] - q[ i ]):
                return True
    return False


# -----------------------------------------------------------------------------
# drawing the window
def draw():
    for column in range(8):
        for row in range(8):
            x1 = column * cell_width
            y1 = row * cell_height
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            color = [ LIGHT_SQUARE_COLOR, DARK_SQUARE_COLOR ][ (row - column) % 2 ]

            rect[ row, column ] = w.create_rectangle(x1, y1, x2, y2, fill=color,tag="rect")

            oval[ row, column ] = w.create_oval(x1 + 20, y1 + 20, x2 - 20, y2 - 20, fill=color, outline=color,tag='oval')
            w.tag_bind('oval', '<ButtonPress-1>',onObjectClick)


# -----------------------------------------------------------------------------
q = [ -1, -2, -3, -4, -5, -6, -7, -8 ]
counting_values=[]


# -----------------------------------------------------------------------------
# getting the row and column from the user
def onObjectClick(event):
    rect_value = event.widget.find_closest(event.x, event.y)[ 0 ]
    if rect_value in counting_values:
        print("in")
        for k, v in oval.items():
            if v == rect_value:
                q[k[1]] = -1*(k[1]+1)
                counting_values.remove(rect_value)
        queen_id = rect_value
        w.itemconfig(queen_id, fill="#EBBD63")
    else:
        counting_values.append(rect_value)
        for k, v in oval.items():
            if v == rect_value:
                q[k[1]] = k[0]
                if duplicate(q) or diagonal_conflict(q) :
                    print('error')


        queen_id = rect_value
        w.itemconfig(queen_id, fill="black")
    print(q)

draw()


# -----------------------------------------------------------------------------
# check the user solution
def check():

    if -1 not in q:
        flag = False
        count = 0
        for i1 in range(8):
            for i2 in range(8):
                for i3 in range(8):
                    for i4 in range(8):
                        for i5 in range(8):
                            for i6 in range(8):
                                for i7 in range(8):
                                    for i8 in range(8):
                                        probabilities = [ i1, i2, i3, i4, i5, i6, i7, i8 ]
                                        if duplicate(probabilities) or diagonal_conflict(probabilities):
                                            continue
                                        else:
                                            count += 1
                                            print("Checking all solution probabilities", count)
                                            if q == probabilities:
                                                flag = True
                                                break


        if flag:
            l.configure(text='Your solution is true ☻')  # user solution right
        else:
            l.configure(text='Your solution is false ︶︿︶')  # user solution wrong
    else:
        l.configure(text='You\'re stupid I\'m not even using my artificial intelligence to know that it \'s wrong',
                    font=("Cambria", 11))  # user solution wrong

mainloop()