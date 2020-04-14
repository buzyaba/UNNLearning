import tkinter as tk
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

SCREEN_WIDTH = "800"
SCREEN_HEIGHT = "600"

z_axis = 0

def rungeKuttaMethod_4th_order(x0=0, dx0=0, *, step=1, error=1):
    
    t0 = int_range[0]

    points_list = [[], []]

    dx1_dt = lambda t, x1, x2: x2
    dx2_dt = lambda t, x1, x2: -1*sigma*x2 - math.sin(x1)

    step_x = x0
    step_dx = dx0

    half_step_x = x0
    half_step_dx = dx0

    dbl_step_x = x0
    dbl_step_dx = dx0

    while t0 < int_range[1]+1:
        k1 = dx1_dt(t0, x0, dx0)
        m1 = dx2_dt(t0, x0, dx0)

        k2 = dx1_dt(t0+0.5*step, x0+0.5*step*k1, dx0+0.5*step*m1)
        m2 = dx2_dt(t0+0.5*step, x0+0.5*step*k1, dx0+0.5*step*m1)

        k3 = dx1_dt(t0+0.5*step, x0+0.5*step*k2, dx0+0.5*step*m2)
        m3 = dx2_dt(t0+0.5*step, x0+0.5*step*k2, dx0+0.5*step*m2)

        k4 = dx1_dt(t0+step, x0+step*k3, dx0+step*m3)
        m4 = dx2_dt(t0+step, x0+step*k3, dx0+step*m3)

        step_x = x0 + (step/6.0)*(k1+2*k2+2*k3+k4)
        step_dx = dx0 + (step/6.0)*(m1+2*m2+2*m3+m4)

        for _ in range(2):
            k1 = dx1_dt(t0, x0, dx0)
            m1 = dx2_dt(t0, x0, dx0)
            
            k2 = dx1_dt(t0+0.25*step, x0+0.5*k1, dx0+0.25*step*m1)
            m2 = dx2_dt(t0+0.25*step, x0+0.25*step*k1, dx0+0.25*step*m1)

            k3 = dx1_dt(t0+0.25*step, x0+0.25*step*k2, dx0+0.25*step*m2)
            m3 = dx2_dt(t0+0.25*step, x0+0.25*step*k2, dx0+0.25*step*m2)

            k4 = dx1_dt(t0+0.5*step, x0+0.5*step*k3, dx0+0.5*step*m3)
            m4 = dx2_dt(t0+0.5*step, x0+0.5*step*k3, dx0+0.5*step*m3)

            half_step_x = x0 + (step/12.0)*(k1+2*k2+2*k3+k4)
            half_step_dx = dx0 + (step/12.0)*(m1+2*m2+2*m3+m4)

        S = (half_step_x-step_x)/15

        if abs(S) > error:
            step = step/2
            k1 = dx1_dt(t0, x0, dx0)
            m1 = dx2_dt(t0, x0, dx0)

            k2 = dx1_dt(t0+0.5*step, x0+0.5*step*k1, dx0+0.5*step*m1)
            m2 = dx2_dt(t0+0.5*step, x0+0.5*step*k1, dx0+0.5*step*m1)

            k3 = dx1_dt(t0+0.5*step, x0+0.5*step*k2, dx0+0.5*step*m2)
            m3 = dx2_dt(t0+0.5*step, x0+0.5*step*k2, dx0+0.5*step*m2)

            k4 = dx1_dt(t0+step, x0+step*k3, dx0+step*m3)
            m4 = dx2_dt(t0+step, x0+step*k3, dx0+step*m3)

            x0 += (step/6.0)*(k1+2*k2+2*k3+k4)
            dx0 += (step/6.0)*(m1+2*m2+2*m3+m4)

            points_list[0].append(x0)
            points_list[1].append(dx0)

            t0 += step

        elif abs(S) > error/32 and abs(S) <= error:
            x0 = step_x
            dx0 = step_dx

            points_list[0].append(x0)
            points_list[1].append(dx0)

            t0 += step
        elif abs(S) < error/32:
            x0 = step_x
            dx0 = step_dx

            points_list[0].append(x0)
            points_list[1].append(dx0)

            t0 += step
            step = 2*step

    return points_list

def calculate_func():
    global step, error, sigma
    try:
        step = float(step_input.get())
        error = float(error_input.get())
        sigma = float(sigma_input.get())
        if x is None or dx_dt is None or int_range is None:
            tk.messagebox.showinfo(title="Error", message="On of a variables: range, x, x'- has None type")
            return
    except Exception:
        tk.messagebox.showinfo(title="Error", message="On of a variables: step, error, sigma- has None type")
        return
    else:
        global z_axis
        if z_axis == 0:
            plt.axvline(0, color="black", linewidth=1, linestyle="dashed")
            plt.axhline(0, color="black", linewidth=1, linestyle="dashed")
            plot.plot(0, 0, color="black", marker=".")
            z_axis = 1
        
        func = rungeKuttaMethod_4th_order(x, dx_dt, step=step, error=error)
    
        plot.plot(func[0], func[1])
            
        canvas.draw()




def clear_func():
    global figure, plot, z_axis
    figure.clf()
    plot = figure.add_subplot(111)
    z_axis = 0
    canvas.draw()


def add_range(entries):
    global int_range
    i = 0 if entries[0].get() < entries[1].get() else 1
    int_range = (float(entries[i].get()), float(entries[1-i].get()))
    range_label['text'] = "Range: [ {0}, {1} ]".format(int_range[0], int_range[1])

def add_conds(entries):
    global x, dx_dt

    x = float(entries[0].get())
    dx_dt = float(entries[1].get())

    condition_x_label["text"] = "x = %.3f" % x
    condition_dx_label["text"] = "x' = %.3f" % dx_dt

def onButtonClick(instance):
    if instance["text"] == "Choose a range":
        range_popup = tk.Toplevel()
        range_popup.grab_set()
        range_popup.title("Choose a range")
        range_popup.geometry("240x120")
        range_popup.resizable(False, False)

        vcmd = range_popup.register(validate_negative)

        start_label = tk.Label(range_popup, text="Start", font=("roboto", 14))
        start_input = tk.Entry(range_popup, width=15, validate="all", validatecommand=(vcmd, '%P'))

        end_label = tk.Label(range_popup, text="End", font=("roboto", 14))
        end_input = tk.Entry(range_popup, width=15, validate="all", validatecommand=(vcmd, '%P'))

        range_popup.bind("<Return>", lambda event: add_range((start_input, end_input)))

        start_label.pack()
        start_input.pack()
        end_label.pack()
        end_input.pack()
    elif instance["text"] == "Initial condition":
        init_popup = tk.Toplevel()
        init_popup.grab_set()
        init_popup.title("Choose an initial conditions")
        init_popup.geometry("240x60")
        init_popup.resizable(False, False)

        vcmd = init_popup.register(validate_negative)

        condition_x_label = tk.Label(init_popup, text="x", font=("roboto", 14))
        condition_dx_label = tk.Label(init_popup, text="x'", font=("roboto", 14))

        condition_x_input = tk.Entry(init_popup, width=15, validate="all", validatecommand=(vcmd, '%P'))
        condition_dx_input = tk.Entry(init_popup, width=15, validate="all", validatecommand=(vcmd, '%P'))

        init_popup.bind("<Return>", lambda event: add_conds((condition_x_input, condition_dx_input)))

        condition_x_label.grid(row=1, column=0)
        condition_x_input.grid(row=1, column=1)

        condition_dx_label.grid(row=2, column=0)
        condition_dx_input.grid(row=2, column=1)

def onPlotClick(event):
    global x, dx_dt

    x = event.xdata
    dx_dt = event.ydata

    condition_x_label["text"] = "x = %.3f" % x
    condition_dx_label["text"] = "x' = %.3f" % dx_dt



def validate(P):
    if P != "":
        try:
            float(P)
            return True
        except Exception:
            return False
    else:
        return True

def validate_negative(P):
    if P != "" and P != "-":
        try:
            float(P)
            return True
        except Exception:
            return False
    else:
        return True


# MAIN VARIABLES
int_range = None
x = None
dx_dt = None
step = float()
error = float()
sigma = float()

# WINDOW INIT
root = tk.Tk()
root.title("Phase portrait")
root.geometry(SCREEN_WIDTH+"x"+SCREEN_HEIGHT)
root.resizable(False, False)

# WIDGETS
figure = plt.figure(figsize=(5, 5), dpi=100)
plot = figure.add_subplot(111)
canvas = FigureCanvasTkAgg(figure)
canvas.mpl_connect('button_press_event', onPlotClick)
move = NavigationToolbar2Tk(canvas, root)

vcmd = (root.register(validate))

sigma_label = tk.Label(text="σ", font=("roboto", 12))
sigma_input = tk.Entry(width=7, validate="all", validatecommand=(vcmd, '%P'))
sigma_input.insert(tk.END, "0")

error_label = tk.Label(text="Error", font="roboto-11")
error_input = tk.Entry(width=7, validate="all", validatecommand=(vcmd, '%P'))
error_input.insert(tk.END, "0")

step_label = tk.Label(text="Step", font="roboto-11")
step_input = tk.Entry(width=7, validate="all", validatecommand=(vcmd, '%P'))
step_input.insert(tk.END, "0")

init_condition = tk.Button(text="Initial condition", font="roboto-11", height=1, command=lambda: onButtonClick(init_condition))
range_button = tk.Button(text="Choose a range", font="roboto-11", height=1, command=lambda: onButtonClick(range_button))
calc_button = tk.Button(text="Calculate", font="roboto-11", height=1, command=calculate_func)
clear_button = tk.Button(text="Clear", font="roboto-11", height=1, command=clear_func)

equation_frame = tk.Frame(root, bg="light blue")
equation_name_label = tk.Label(equation_frame, text="Equation:", font=("roboto", 14), bg="light blue")
equation_label = tk.Label(equation_frame, text='''x" + σx' + sinx = 0''', font=("roboto", 12), bg="light blue")
range_label = tk.Label(equation_frame, text="Range: ", font=("roboto", 12), bg="light blue")
conditions_label_name = tk.Label(equation_frame, text="Initial conditions:", font=("roboto", 14), bg="light blue")
condition_x_label = tk.Label(equation_frame, text="x = ", font=("roboto", 12), bg="light blue")
condition_dx_label = tk.Label(equation_frame, text="x' = ", font=("roboto", 12), bg="light blue")


# PACKING
canvas.get_tk_widget().place(x=10, y=50)
move.place(x=10, y=10)

sigma_label.place(x=680, y=400)
sigma_input.place(x=710, y=400)

error_label.place(x=550, y=450)
error_input.place(x=600, y=450)

step_label.place(x=550, y=400)
step_input.place(x=600, y=400)

init_condition.place(x=550, y=250)
range_button.place(x=550, y=300)
calc_button.place(x=550, y=350)
clear_button.place(x=700, y=500)

equation_name_label.pack()
equation_label.pack()
range_label.pack()
conditions_label_name.pack()
condition_x_label.pack()
condition_dx_label.pack()
equation_frame.place(x=550, y=50)

root.mainloop()