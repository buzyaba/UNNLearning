from tkinter import *
import random
import fileinput

SCREEN_WIDTH = "800"
SCREEN_HEIGHT = "600"

def thomasAlg(mat, f):
    size = len(mat)
    alpha = [0]
    beta = [0]
    x = [0] * size
    for i in range(size-1):
        alpha.append(-mat[i][2]/(-mat[i][0]*alpha[i]+mat[i][1]))
        beta.append((f[i]-mat[i][0]*beta[i])/(mat[i][0]*alpha[i]+mat[i][1]))

    x[size-1] = (f[size-1]-mat[size-2][0]*beta[size-1])/(mat[size-2][1]+mat[size-2][0]*alpha[size-1])
    for i in reversed(range(size-1)):
        x[i] = alpha[i+1]*x[i+1] + beta[i+1]
    return x

def calculateSpline(p):
    n = len(p)
    a = [p[i-1][1] for i in range(1, n)]
    b = [0]*(n-1)
    h = [ p[i][0]-p[i-1][0] for i in range(1, n)]
    d = [0]*(n-1)
    f = [3*(p[i+1][1]-p[i][1])/h[i]-3*(p[i][1]-p[i-1][1])/h[i-1] for i in range(1, n-1)]

    mtx = [[0]*3 for i in range(n-2)]
    mtx[0] = [h[1], 2*(h[0]+h[1]), 0]
    mtx[n-3] = [0, 2*(h[n-3]+h[n-2]), h[n-3]]
    for i in range(1, n-3):
        mtx[i] = [h[i+1], 2*(h[i]+h[i+1]), h[i]]

    c = thomasAlg(mtx, f)
    c.insert(0, 0)
    c.append(0)
    for i in range(1, n):
        b[i-1] = (p[i][1]-p[i-1][1])/h[i-1] - c[i-1]*h[i-1] - h[i-1] * ((c[i]-c[i-1])/3)
        d[i-1] = (c[i] - c[i-1])/(3*h[i-1]) 

    print("a: ", *a)
    print("b: ", *b)
    print("c: ", *c)
    print("d: ", *d)
    print("h: ", *h)
    print("f: ", *f)
    




def on_close(window):
    points.sort()
    pointsList.delete(0, END)
    for elem in points:
        pointsList.insert(END, str(elem))
    window.destroy()

def addPoints(pnts_list, entry):
    string1 = entry[0].get()
    string2 = entry[1].get()
    try:
        x = float(string1)
        y = float(string2)

        for elem in points:
            if x == elem[0]:
                raise Exception
    except Exception:
        pass
    else:
        pnts_list.insert(END, "(" + string1 +", " + string2 + ")")
        points.append((x, y))
    entry[0].delete(0, END)
    entry[1].delete(0, END)


def on_button_click(instance):
    if instance["text"] == "Add points":
        addWidget = Toplevel()
        addWidget.grab_set()
        addWidget.title("Add")
        addWidget.resizable(False, False)
        addWidget.bind("<Return>", lambda event: addPoints(points_list, entries))
        addWidget.protocol("WM_DELETE_WINDOW", lambda: on_close(addWidget))
        frame1 = Frame(addWidget)
        frame2 = Frame(addWidget)
        entry1 = Entry(frame1, width = 10)
        entry2 = Entry(frame1, width = 10)
        entries = [entry1, entry2]
        points_list = Listbox(frame2)
        labelX = Label(frame1, text="X:")
        labelY = Label(frame1, text="Y:")
        frame1.pack()
        frame2.pack()
        labelX.grid(row = 0, column = 0)
        labelY.grid(row = 1, column = 0)
        entry1.grid(row = 0, column = 1)
        entry2.grid(row = 1, column = 1)
        points_list.pack()
    elif instance["text"]=="Generate points":
        points.clear()
        pointsList.delete(0, END)
        for i in range(8):
            x = round(float(random.uniform(-15, 15)), 1)
            y = round(float(random.uniform(-15, 15)), 1)
            for i in range(len(points)):
                if x == points[i][0]:
                    x = round(float(random.uniform(-15, 15)), 1)
                    i = 0
            points.append((x, y))
        points.sort()
        for elem in points:
            pointsList.insert(END, str(elem))
    elif instance['text'] == "Calculate Spline":
        calculateSpline(points)    



root = Tk()
points = list()

#INITIALIZE WINDOW
root.title("Spline Interpolation")
root.geometry(SCREEN_WIDTH+"x"+SCREEN_HEIGHT)
root.resizable(False, False)

#ADDING WIDGETS
button1 = Button(text="Add points", height=1, font="roboto 11", command= lambda: on_button_click(button1))
button2 = Button(text="Generate points", height=1, font="roboto 11", command=lambda: on_button_click(button2))
button3 = Button(text="Calculate Spline", font="roboto 11", command=lambda: on_button_click(button3))
label = Label(text="Points:", font="roboto 12")
pointsList = Listbox(width=17, height=15)

#PACKING
button1.place(x=650, y=100)
button2.place(x=650, y=50)
button3.place(x=650, y=480)
label.place(x=650, y=150)
pointsList.place(x=650, y=175)

root.mainloop()