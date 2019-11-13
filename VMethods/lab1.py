from tkinter import *
import random
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

SCREEN_WIDTH = "800"
SCREEN_HEIGHT = "600"

def thomasAlg(a, b, c, f):
    size = len(f)
    alpha = [0]
    beta = [0]
    x = [0] * size
    for i in range(size-1):
        alpha.append(-b[i]/(-a[i]*alpha[i]+c[i]))
        beta.append((f[i]-a[i]*beta[i])/(a[i]*alpha[i]+c[i]))

    x[size-1] = (f[size-1]-a[size-2]*beta[size-1])/(c[size-2]+a[size-2]*alpha[size-1])
    for i in reversed(range(size-1)):
        x[i] = alpha[i+1]*x[i+1] + beta[i+1]
    return x

def calculateSpline(p):
    n = len(p)
    a = [p[i-1][1] for i in range(1, n)]
    b = [0]*(n-1)
    h = [p[i+1][0]-p[i][0] for i in range(n-1)]
    d = [0]*(n-1)
    f = [3*(p[i+1][1]-p[i][1])/h[i]-3*(p[i][1]-p[i-1][1])/h[i-1] for i in range(1, n-1)]

    A = [h[i] for i in range(1, n-1)]
    B = [h[i+1] for i in range(n-2)]
    C = [2*(h[i]+h[i+1]) for i in range(n-2)]
    c = thomasAlg(A, B, C, f)
    c.insert(0, 0)
    c.append(0)
    polynoms = [] * (n-1)
    for i in range(n-1):
        b[i] = (p[i+1][1]-a[i])/h[i] - c[i]*h[i] - h[i]*((c[i+1]-c[i])/3)
        d[i] = (c[i+1] - c[i])/(3*h[i])
        polynoms.append({"a":a[i], "b":b[i], "c":c[i], "d":d[i], "dist":(p[i][0], p[i+1][0])})

    file = open("coeff.txt", "w")
    for i in range(n-1):
        file.write("a{0}={1}, b{0}={2}, c{0}={3}, d{0}={4}, range: {5}\n".format(i+1, 
        round(polynoms[i]["a"], 3), round(polynoms[i]["b"], 3), round(polynoms[i]["c"], 3), 
        round(polynoms[i]["d"], 3), polynoms[i]["dist"]))
    file.close()
    return polynoms
    
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
        polynoms = calculateSpline(points)
        fig = plt.figure(figsize=(6, 5), dpi=100)
        x = [np.arange(polynoms[i]["dist"][0], polynoms[i]["dist"][1], 0.01) for i in range(len(polynoms))]
        for i in range(len(polynoms)):
            fig.add_subplot(111).plot(x[i], polynoms[i]["a"] + polynoms[i]["b"]*(x[i]-points[i][0])
            +polynoms[i]["c"]*((x[i]-points[i][0])**2) + polynoms[i]["d"]*((x[i]-points[i][0])**3))
        canvas.figure = fig
        canvas.draw()
    elif instance['text'] == "Clear":
        points.clear()
        pointsList.delete(0, END)



root = Tk()
points = list()
polynoms = dict()
figure = plt.figure()
canvas = FigureCanvasTkAgg(figure)

#INITIALIZE WINDOW
root.title("Spline Interpolation")
root.geometry(SCREEN_WIDTH+"x"+SCREEN_HEIGHT)
root.resizable(False, False)

#ADDING WIDGETS

button1 = Button(text="Add points", height=1, font="roboto 11", command= lambda: on_button_click(button1))
button2 = Button(text="Generate points", height=1, font="roboto 11", command=lambda: on_button_click(button2))
button3 = Button(text="Calculate Spline", font="roboto 11", command=lambda: on_button_click(button3))
button4 = Button(text="Clear", font="roboto 11", command=lambda: on_button_click(button4))
label = Label(text="Points:", font="roboto 12")
pointsList = Listbox(width=17, height=15)

#PACKING
button1.place(x=650, y=100)
button2.place(x=650, y=50)
button3.place(x=650, y=480)
button4.place(x=650, y=520)
canvas.get_tk_widget().place(x=10, y=50)
label.place(x=650, y=150)
pointsList.place(x=650, y=175)

root.mainloop()