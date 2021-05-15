# -*- coding: utf-8 -*-

from numpy import (sin, cos, tan, pi, exp, sqrt, arange, meshgrid, linspace)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import (clf, gcf, subplots_adjust, figure)
from tkinter.ttk import (Combobox, Button, Style)
from tkinter import (Label, Entry, Tk, S, N, E, W, SE, SW, NE, NW)
from sys import exit
import os
from tkinter import *

LARGE_FONT = ("TIMES NEW ROMAN", 14, "bold", "italic")


def testVal(inStr, acttyp):
    if acttyp == '1':
        if not inStr.isdigit():
            return False
    return True


def EXIT():
    os.abort()


def time_minus():
    global time
    if time > 0:
        time -= 1
        time_label.configure(text=time)
        plotting()


def time_plus():
    global time
    time += 1
    time_label.configure(text=time)
    plotting()


def get(entry):
    value = entry.get()
    try:
        return int(value)
    except ValueError:
        return None


def plotting():
    global size_lines_entry
    global frequincy
    global moda_n
    global moda_m
    global label
    global f_kr
    clf()
    if (len(frequincy.get()) == 0) or (len(a_x_size_entry.get()) == 0) or (len(b_x_size_entry.get()) == 0) or (
            len(table_n.get()) == 0) or (len(table_m.get()) == 0):
        clf()
        label.configure(text="Заполните поля!", bg="gainsboro")
        label.grid(row=0, column=4, columnspan=3, padx=10, pady=15, sticky=S + N)
        gcf().canvas.draw()
        return
    label.configure(text=" ")

    cc = 3e10  # ñêîðîñòü ñâåòà
    ff = get(frequincy)
    f = ff * 1e9  # ÷àñòîòó ïåðåâîäèì â Ãö
    w = 2 * pi * f
    lyam = cc / f  # ðàçìåð âîëíîâîäà ïî îñè z    
    hh = w / cc  # âîëíîâîå ÷èñëî
    n = get(table_n)
    m = get(table_m)
    a = get(a_x_size_entry)
    b = get(b_x_size_entry)
    tt = time
    t = tt / 1e12
    c = lyam
    h = 0.01  # øàã ñåòêè
    k = get(size_lines_entry)
    kappa = sqrt(((pi * n / a) ** 2) + ((pi * m / b) ** 2))
    kappaX = pi * n / a
    kappaY = pi * m / b
    f_kr = (cc * kappa) / (2 * pi)  # êðèòè÷åñêàÿ ÷àñòîòà
    lyam_kr = cc / f_kr
    def V_gr():
        return cc*sqrt(1 - pow(lyam/lyam_kr,2))
    # îïðåäåëèì ñðåç
    C1 = 0
    C2 = 0
    if n != 0 and m == 0:
        if (n % 2) != 0:
            C1 = a / 2
        else:
            C1 = a / (2 * n)
    elif n == 0 and m != 0:
        if (m % 2) != 0:
            C2 = b / 2
        else:
            C2 = b / (2 * m)

    # êîíåö
    # TE H
    def TE_H_XY(x, y):
        return ((abs(sin(kappaX * x))) / (abs(sin(kappaY * y)))) * cos(w * t + pi / 2)

    def TE_H_YZ(y, z):
        return (abs(sin(kappaY * y))) * cos(w * t - hh * z + pi / 2)

    def TE_H_XZ(x, z):
        return (abs(sin(kappaX * x))) * cos(w * t - hh * z + pi / 2)

    # E
    def TE_E_XY(x, y):
        return abs(cos(kappaY * y)) * abs(cos(kappaX * x)) * cos(w * t)
    
    #TE10
 #==========================================================================================================   
    def TE10_H_XY(x, y):
        return abs(sin(kappaX * x)) * exp(hh * tan(w * t) * y)

    def TE10_H_XZ(x, z):
        return abs(sin(kappaX * x)) * cos(w * t - hh * z)

    def TE10_H_YZ(y, z):
        return exp(kappaX * (cos(kappaX * C1) / sin(kappaX * C1)) * y) * sin(w * t - hh * z)

    def TE10_E_XY(x, y):
        return (w / (kappaX * cc)) * abs(sin(kappaX * x) * cos(kappaX * x) * sin(kappaX*x))

    
    def TE10_E_YZ(y, z):
        return  cos(w * t - hh * y) #* (w / (kappaX * cc)) #* sin(kappaX * y)  #0.1 - cos(w * t - hh * y + 0.2) * (w / (kappaX * cc))
 #==========================================================================================================   
    
    
    #TE01 
    def TE01_H_XY(x, y):
        return abs(sin(kappaY * y)) * exp(hh * tan(w * t) * x)

    def TE01_H_XZ(x, z):
        return exp(kappaY * (cos(kappaY * C2) / sin(kappaY * C2)) * x) * cos(w * t - hh * z)

    def TE01_H_YZ(y, z):
        return abs(sin(kappaY * y)) * cos(w * t - hh * z)

    def TE01_E_XY(x, y):
        return (w / (kappaY * cc)) * abs(sin(kappaY * y)) * sin(w * t)

    # TM H
    def TM_H_XY(x, y):
        return abs(sin(kappaX * x)) * abs(sin(kappaY * y)) * cos(w * t + pi / 2)

    # TM E
    def TM_E_XY(x, y):
        return (abs(cos(kappaY * y))) / (abs(cos(kappaX * x))) * cos(w * t)

    def TM_E_XZ(x, z):
        return (abs(cos(kappaX * x))) * cos(w * t - hh * z)

    def TM_E_YZ(y, z):
        return (abs(cos(kappaY * y))) * cos(w * t - hh * z)

    # Ñòðîèì ãðàôèêè çäåñü
    def makeData(b1, b2):
        a1 = arange(0, b1, h)
        a2 = arange(0, b2, h)
        a1grid, a2grid = meshgrid(a1, a2)
        return a1grid, a2grid

    if f > f_kr:
        fig = figure(figsize=(7, 5), facecolor="gainsboro")
        XY = fig.add_subplot(3, 1, 1)
        YZ = fig.add_subplot(3, 1, 2)
        XZ = fig.add_subplot(3, 1, 3)

        fig.set_figwidth(5)
        fig.set_figheight(5)

        x1, y1 = makeData(a, b)
        y2, z2 = makeData(b, c)
        x3, z3 = makeData(a, c)
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().grid(row=0, column=4, rowspan=17, padx=10, pady=5, sticky=S + N)

        if combobox.get() == "TE":  # ïðîâåðÿåì òèï âîëí è äàëüøå ñ÷èòûâàåì ìîäó
            if n != 0 and m != 0:
                XY.contour(x1, y1, TE_H_XY(x1, y1), linspace(-1, 1, k), colors='b')
            elif n != 0 and m == 0:
                XY.contour(x1, y1, TE10_H_XY(y1, 0), linspace(-1, 1, k), colors='b')
            elif n == 0 and m != 0:
                XY.contour(x1, y1, TE01_H_XY(x1, y1), linspace(-1, 1, k), colors='b')
            XY.set_xlabel('x')
            XY.set_ylabel('y')
            
            if n != 0 and m != 0:
                XY.contour(x1, y1, TE_E_XY(x1, y1), linspace(-1, 1, k), colors='r')
            elif n != 0 and m == 0:
                XY.contour(x1, y1, TE10_E_XY(x1, y1), linspace(-1, 1, k), colors='r')
                #YZ.contour(x1, y1, TE10_E_XY(x1, y1), linspace(-1, 1, k), colors='r')
            elif n == 0 and m != 0:
                XY.contour(x1, y1, TE01_E_XY(x1, y1), linspace(-1, 1, k), colors='r')
            XY.set_xlabel('x')
            XY.set_ylabel('y')

            if n != 0 and m != 0:
                YZ.contour(z2, y2, TE_H_YZ(y2, z2), linspace(-1, 1, k), colors='b')
            elif n != 0 and m == 0:
                YZ.contour(x1, y1, TE10_H_XY(y1, 0), linspace(-1, 1, k), colors='b')
                YZ.contour(x1, y1, TE10_E_YZ(x1, y1), linspace(-1, 1, k), colors='r')
            elif n == 0 and m != 0:
                YZ.contour(z2, y2, TE01_H_YZ(y2, z2), linspace(-1, 1, k), colors='b')
            YZ.set_xlabel('z')
            YZ.set_ylabel('y')

            if n != 0 and m != 0:
                XZ.contour(z3, x3, TE_H_XZ(x3, z3), linspace(-1, 1, k), colors='b')
            elif n != 0 and m == 0:
                XZ.contour(z3, x3, TE10_H_XZ(x3, z3), linspace(-1, 1, k), colors='b')
            elif n == 0 and m != 0:
                XZ.contour(z3, x3, TE01_H_XZ(x3, z3), linspace(-1, 1, k), colors='b')
            XZ.set_xlabel('z')
            XZ.set_ylabel('x')





        else:
            if n != 0 and m != 0:
                XY.contour(x1, y1, TM_H_XY(x1, y1), linspace(-1, 1, k), colors='b')
                XY.set_xlabel('x')
                XY.set_ylabel('y')

                XY.contour(x1, y1, TM_E_XY(x1, y1), linspace(-1, 1, k), colors='r')
                XY.set_xlabel('x')
                XY.set_ylabel('y')

                YZ.contour(z2, y2, TM_E_YZ(y2, z2), linspace(-1, 1, k), colors='r')
                YZ.set_xlabel('z')
                YZ.set_ylabel('y')

                XZ.contour(z3, x3, TM_E_XZ(x3, z3), linspace(-1, 1, k), colors='r')
                XZ.set_xlabel('z')
                XZ.set_ylabel('x')
            else:
                label = Label(window, text="E R R O R !", font=LARGE_FONT, bg="gainsboro")
                label.grid(row=3, column=4, columnspan=3, padx=30, sticky=SW)
                gcf().canvas.draw()

                # åñëè ÷àñòîòà íèæå êðèòè÷åñêîé âîëíû íå ðàñïðîñòðîÿíÿþòñÿ
    # è òàêæå âûâåäåì ñàìó êðèòè÷åñêóþ ÷àñòîòó

    else:
        label = Label(window, text="Частота ниже критической!", font=LARGE_FONT, bg="gainsboro")
        label.grid(row=5, column=4, columnspan=2, padx=30, sticky=SW)
    subplots_adjust(wspace=0.5, hspace=0.5)
    gcf().canvas.draw()
    w_label = Label(window, text="Критическая частота(ГГц): ", font=LARGE_FONT, bg="gainsboro")
    w_label.grid(row=11, column=0, columnspan=4, padx=30, sticky=SW)
    wk_label = Label(window, text=f_kr / 1e9, bg="gainsboro", font=LARGE_FONT)
    wk_label.grid(row=11, column=1, columnspan=7, padx=90, sticky=SW)


window = Tk()
window.title()
window.protocol("WM_DELETE", EXIT)
window.attributes("-alpha", 1)
window.resizable(width=True, height=True)
window['bg'] = 'gainsboro'
window.title("Model Volnovoda")
w = 950
h = 700
sw = window.winfo_screenwidth()
sh = window.winfo_screenheight()
window.geometry('%dx%d+%d+%d' % (w, h, (sw - w) / 2, (sh - h) / 2))

label_n = Label(window, text="Выберите тип волны:", font=LARGE_FONT, bg="gainsboro", fg="black")
label_n.grid(row=0, column=0, columnspan=2, padx=30, pady=10, sticky=SW)

style = Style()
style.configure("BW.TLabel", font=LARGE_FONT, foreground="black", background="gold")
combobox = Combobox(value=["TE", "TM"], height=2, width=3, state="readonly", style="BW.TLabel")
combobox.set("TE")
combobox.grid(row=1, column=2, columnspan=2, sticky=SW)
window.option_add("*TCombobox*Listbox*Background", 'gold')
window.option_add("*TCombobox*Listbox*Foreground", 'green')

moda_label = Label(window, text="Выберите моду:", font=LARGE_FONT, bg="gainsboro")
moda_label.grid(row=1, column=0, columnspan=4, padx=30, sticky=SW)

label_m = Label(window, text="m: ", font=LARGE_FONT, bg="gainsboro")
label_m.grid(row=3, column=2, padx=10, sticky=W)
table_m = Entry(window, width=5, bg="gold", selectbackground='black', validate="key")
table_m['validatecommand'] = (table_m.register(testVal), '%P', '%d')
table_m.grid(row=3, column=3, sticky=NW)

label_n = Label(window, text="n: ", font=LARGE_FONT, bg="gainsboro")
label_n.grid(row=3, column=0, padx=10, sticky=E)
table_n = Entry(window, width=5, bg="gold", selectbackground='black', validate="key")
table_n['validatecommand'] = (table_n.register(testVal), '%P', '%d')
table_n.grid(row=3, column=1, sticky=NW)

label_m = Label(window, text="Введите частоту(Ггц): ", font=LARGE_FONT, bg="gainsboro")
label_m.grid(row=5, column=0, columnspan=2, padx=30, pady=15, sticky=NE)

frequincy = Entry(window, width=5, bg="gold", selectbackground='black', validate="key")
frequincy['validatecommand'] = (frequincy.register(testVal), '%P', '%d')
frequincy.grid(row=5, column=2, columnspan=2, pady=15, ipadx=5, sticky=NW)

waveguide_size = Label(window, text="Введите размер волновода (см):", font=LARGE_FONT, bg="gainsboro")
waveguide_size.grid(row=6, column=0, columnspan=4, padx=30, sticky=W)

a_x_size = Label(window, text="a: ", font=LARGE_FONT, bg="gainsboro")
a_x_size.grid(row=7, column=0, padx=30, sticky=NE)
a_x_size_entry = Entry(window, width=5, bg="gold", selectbackground='black', validate="key")
a_x_size_entry['validatecommand'] = (a_x_size_entry.register(testVal), '%P', '%d')
a_x_size_entry.grid(row=7, column=1, sticky=NW)

b_x_size = Label(window, text="b: ", font=LARGE_FONT, bg="gainsboro")
b_x_size.grid(row=7, column=2, padx=30, sticky=NE)
b_x_size_entry = Entry(window, width=5, bg="gold", selectbackground='black', validate="key")
b_x_size_entry['validatecommand'] = (b_x_size_entry.register(testVal), '%P', '%d')
b_x_size_entry.grid(row=7, column=3, sticky=NW)

size_lines = Label(window, text="Количество линей уровня: ", font=LARGE_FONT, bg="gainsboro")
size_lines.grid(row=8, column=0, columnspan=2, padx=30, pady=10, sticky=SW)
size_lines_entry = Entry(window, width=5, bg="gold", selectbackground='black', validate="key")
size_lines_entry['validatecommand'] = (size_lines_entry.register(testVal), '%P', '%d')
size_lines_entry.grid(row=8, column=2, columnspan=2, pady=10, sticky=SW)

click = Button(window, text="Построить графики силовых линий", font=LARGE_FONT, command=plotting)
click.grid(row=10, column=0, columnspan=3, pady=90, sticky=S)

label = Label(window, text=" ", font=LARGE_FONT, bg="gainsboro")
label.grid(row=10, column=14, columnspan=17, padx=10, sticky=S + N)
time = 0
label_time = Label(window, text="Время: ", font=LARGE_FONT, bg="gainsboro")
label_time.grid(row=9, column=0, columnspan=1, padx=30, pady=15, sticky=SW)
time_label = Label(window, text=time, font=LARGE_FONT, bg="gainsboro")
time_label.grid(row=9, column=0, columnspan=1, padx=90, pady=15, sticky=SW)
time_plus = Button(window, text="-->", bg="gold", command=time_plus)
time_plus.grid(row=9, column=2, columnspan=1, pady=15, sticky=SW)
time_minus = Button(window, text="<--", bg="gold", command=time_minus)
time_minus.grid(row=9, column=1, columnspan=1, pady=15, sticky=SW)

label_color = Label(window, text="H-синий\n E-красный", font=LARGE_FONT, bg="gainsboro")
label_color.grid(row=0, column=2, columnspan=1, pady=10, sticky=S)

window.mainloop()