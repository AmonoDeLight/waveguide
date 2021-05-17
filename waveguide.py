# -*- coding: utf-8 -*-

from numpy import (sin, cos, tan, pi, exp, sqrt, arange, meshgrid, linspace)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import (clf, gcf, subplots_adjust, figure)
from tkinter.ttk import (Combobox, Button, Style)
from tkinter import (Label, Entry, Tk, S, N, E, W, SE, SW, NE, NW)
from sys import exit
import os
from tkinter import *

LARGE_FONT = ("Archangelsk Regular", 14, "bold", "italic")


def onScale(tim):
    global time
    time = int(float(tim))
    time_label.configure(text=time)
    plotting()


def testVal(inStr, acttyp):
    if acttyp == '1':
        if not inStr.isdigit():
            return False
    return True


def EXIT():
    os.abort()


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
        label.configure(text="Заполните поля!", bg="#1A1A1D", fg="#bbbbbf")
        label.place(relx=.19, rely=.75, anchor="c", height=50, width=450)
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
        return cc * sqrt(1 - pow(lyam / lyam_kr, 2))

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

    # TE10
    # ==========================================================================================================
    def TE10_H_XY(x, y):
        return abs(sin(kappaX * x)) * exp(hh * tan(w * t) * y)

    def TE10_H_XZ(x, z):
        return abs(sin(kappaX * x)) * cos(w * t - hh * z)

    def TE10_H_YZ(y, z):
        return exp(kappaX * (cos(kappaX * C1) / sin(kappaX * C1)) * y) * sin(w * t - hh * z)

    def TE10_E_XY(x, y):
        return abs(sin(kappaX*x)*cos(kappaX*x)*sin(kappaX*x))

    def TE10_E_YZ(y, z):
        return cos( w * t - hh * y)  # * (w / (kappaX * cc)) #* sin(kappaX * y)  #0.1 - cos(w * t - hh * y + 0.2) * (w / (kappaX * cc))

    # ==========================================================================================================

    # TE01
    def TE01_H_XY(x, y):
        return abs(sin(kappaY * y)) * exp(hh * tan(w * t) * x)

    def TE01_H_XZ(x, z):
        return exp(kappaY * (cos(kappaY * C2) / sin(kappaY * C2)) * x) * cos(w * t - hh * z)

    def TE01_H_YZ(y, z):
        return abs(sin(kappaY * y)) * cos(w * t - hh * z)

    def TE01_E_XY(x, y):
        return (w / (kappaY * cc)) * abs(sin(kappaY * y) * cos(kappaY * y) * sin(kappaY * y))

    def TE01_E_XZ(x, z):
        return cos(w * t - hh * x)

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
        fig = figure(figsize=(9, 6), facecolor="#4e4e52", edgecolor="white")
        fig.set_figheight(8)
        fig.set_figwidth(6)
        XY = fig.add_subplot(3, 1, 1)
        YZ = fig.add_subplot(3, 1, 2)
        XZ = fig.add_subplot(3, 1, 3)

        x1, y1 = makeData(a, b)
        y2, z2 = makeData(b, c)
        x3, z3 = makeData(a, c)
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().place(relx=.7, rely=.53, anchor="c")

        if combobox.get() == "TE":  # ïðîâåðÿåì òèï âîëí è äàëüøå ñ÷èòûâàåì ìîäó
            if n != 0 and m != 0:
                XY.contour(x1, y1, TE_H_XY(x1, y1), linspace(-1, 1, k), colors='b')
            elif n != 0 and m == 0:
                XY.contour(x1, y1, TE10_H_XY(y1, 0), linspace(-1, 1, k), colors='b')
            elif n == 0 and m != 0:
                XY.contour(x1, y1, TE01_H_XY(0, x1), linspace(-1, 1, k), colors='b')
            XY.set_xlabel('x')
            XY.set_ylabel('y')

            if n != 0 and m != 0:
                XY.contour(x1, y1, TE_E_XY(x1, y1), linspace(-1, 1, k), colors='r')
            elif n != 0 and m == 0:
                XY.contour(x1, y1, TE10_E_XY(x1, y1), linspace(-1, 1, k), colors='r')
                # YZ.contour(x1, y1, TE10_E_XY(x1, y1), linspace(-1, 1, k), colors='r')
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
                XZ.contour(x1, y1, TE01_H_XY(0, x1), linspace(-1, 1, k), colors='b')
                XZ.contour(x1, y1, TE01_E_XZ(y1, 0), linspace(-1, 1, k), colors='r')
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
                label = Label(window, text="E R R O R !", font=LARGE_FONT, bg="#1A1A1D", fg="#bbbbbf")
                label.grid(row=16, column=0, sticky=W, padx=30)
                gcf().canvas.draw()


    else:
        label = Label(window, text="Частота ниже критической!", font=LARGE_FONT, bg="#1A1A1D", fg="#bbbbbf")
        label.grid(row=15, column=0, sticky=W, padx=30)
    subplots_adjust(wspace=0.5, hspace=0.5)
    gcf().canvas.draw()
    w_label = Label(window, text="Критическая частота(ГГц): ", font=LARGE_FONT, bg="#1A1A1D", fg="#bbbbbf")
    w_label.grid(row=14, column=0, sticky=W, padx=30)
    wk_label = Label(window, text=f_kr / 1e9, bg="#1A1A1D", fg="#bbbbbf", font=LARGE_FONT)
    wk_label.place(relx=.28, rely=.588, anchor="c")


window = Tk()
window.title()
window.protocol("WM_DELETE", EXIT)
window.attributes("-alpha", 1)
window.state("zoomed")
window.resizable(width=True, height=True)
window['bg'] = '#1A1A1D'
window.title("Volnovodka")
w = 1850
h = 1080
sw = window.winfo_screenwidth()
sh = window.winfo_screenheight()


label_n = Label(window, text="Выберите тип волны:", font=LARGE_FONT, bg="#1A1A1D", fg="#bbbbbf")
label_n.grid(row=0, column=0, padx=30, sticky=W)

style = Style()
style.configure("BW.TLabel", font=LARGE_FONT, foreground="#bbbbbf", background="#4E4E50")
combobox = Combobox(value=["TE", "TM"], height=2, width=3, state="readonly", font=LARGE_FONT, style="BW.TLabel")
combobox.set("TE")
combobox.grid(row=0, column=3)
window.option_add("*TCombobox*Listbox*Background", '#4E4E50')
window.option_add("*TCombobox*Listbox*Foreground", '#1A1A1D')

label_kostya = Label(window, text="Люблю кортошку", font=LARGE_FONT, bg="#1A1A1D", fg="#1A1A1D")
label_kostya.grid(row=1, column=0)

moda_label = Label(window, text="Выберите моду:", font=LARGE_FONT, bg="#1A1A1D", fg="#bbbbbf")
moda_label.grid(row=2, column=0, columnspan=4, padx=30, sticky=SW)

label_m = Label(window, text="m: ", font=LARGE_FONT, bg="#1A1A1D", fg="#bbbbbf")
label_m.grid(row=3, column=2)
table_m = Entry(window, width=5, bg="#4E4E50", selectbackground='black', font=LARGE_FONT, fg="#bbbbbf", validate="key")
table_m['validatecommand'] = (table_m.register(testVal), '%P', '%d')
table_m.grid(row=3, column=3)

label_n = Label(window, text="n: ", font=LARGE_FONT, bg="#1A1A1D", fg="#bbbbbf")
label_n.grid(row=2, column=2, padx=10)
table_n = Entry(window, width=5, bg="#4E4E50", selectbackground='#bbbbbf', font=LARGE_FONT, fg="#bbbbbf", validate="key")
table_n['validatecommand'] = (table_n.register(testVal), '%P', '%d')
table_n.grid(row=2, column=3)

label_sveta = Label(window, text="Люблю пиццу", font=LARGE_FONT, bg="#1A1A1D", fg="#1A1A1D")
label_sveta.grid(row=4, column=0)

label_m = Label(window, text="Введите частоту(ГГц): ", font=LARGE_FONT, bg="#1A1A1D", fg="#bbbbbf")
label_m.grid(row=5, column=0, padx=30, sticky=W)

frequincy = Entry(window, width=5, bg="#4E4E50", selectbackground='black', font=LARGE_FONT, fg="#bbbbbf", validate="key")
frequincy['validatecommand'] = (frequincy.register(testVal), '%P', '%d')
frequincy.grid(row=5, column=3)

label_antosha = Label(window, text="Люблю абрикосы", font=LARGE_FONT, bg="#1A1A1D", fg="#1A1A1D")
label_antosha.grid(row=6, column=0)

waveguide_size = Label(window, text="Введите размер волновода (см):", font=LARGE_FONT, bg="#1A1A1D", fg="#bbbbbf")
waveguide_size.grid(row=7, column=0, columnspan=4, padx=30, sticky=W)

a_x_size = Label(window, text="a: ", font=LARGE_FONT, bg="#1A1A1D", fg="#bbbbbf")
a_x_size.grid(row=7, column=2, padx=30, sticky=NE)
a_x_size_entry = Entry(window, width=5, bg="#4E4E50", font=LARGE_FONT, selectbackground='#1A1A1D', fg="#bbbbbf", validate="key")
a_x_size_entry['validatecommand'] = (a_x_size_entry.register(testVal), '%P', '%d')
a_x_size_entry.grid(row=7, column=3)

b_x_size = Label(window, text="b: ", font=LARGE_FONT, bg="#1A1A1D", fg="#bbbbbf")
b_x_size.grid(row=8, column=2, padx=30, sticky=NE)
b_x_size_entry = Entry(window, width=5, bg="#4E4E50", font=LARGE_FONT, selectbackground='#1A1A1D', fg="#bbbbbf", validate="key")
b_x_size_entry['validatecommand'] = (b_x_size_entry.register(testVal), '%P', '%d')
b_x_size_entry.grid(row=8, column=3)

label_grisha = Label(window, text="Люблю гулять", font=LARGE_FONT, bg="#1A1A1D", fg="#1A1A1D")
label_grisha.grid(row=9, column=0)

size_lines = Label(window, text="Количество линей уровня: ", font=LARGE_FONT, bg="#1A1A1D", fg="#bbbbbf")
size_lines.grid(row=10, column=0, columnspan=2, padx=30, pady=10, sticky=SW)
size_lines_entry = Entry(window, width=5, bg="#4E4E50", font=LARGE_FONT, selectbackground='#1A1A1D', fg="#bbbbbf", validate="key")
size_lines_entry['validatecommand'] = (size_lines_entry.register(testVal), '%P', '%d')
size_lines_entry.grid(row=10, column=3)

label_nastya = Label(window, text="Люблю делать ненужные вещи, да", font=LARGE_FONT, bg="#1A1A1D", fg="#1A1A1D")
label_nastya.grid(row=11, column=0)

label = Label(window, text=" ", font=LARGE_FONT, bg="#1A1A1D")
label.grid(row=11, column=14, columnspan=17, padx=10, sticky=S + N)
time = 0
label_time = Label(window, text="Время: ", font=LARGE_FONT, bg="#1A1A1D", fg="#bbbbbf")
label_time.grid(row=12, column=0, columnspan=1, padx=30, pady=15, sticky=SW)
time_label = Label(window, text=time, font=LARGE_FONT, bg="#1A1A1D", fg="#1A1A1D")
time_label.grid(row=122, column=122, columnspan=122, padx=1000, pady=1000, sticky=SW)

scale = Scale(window, orient="horizontal", from_=0, to=100, bg="#1A1A1D", fg="#bbbbbf", command=onScale)
label_time_entry = scale
scale.place(relx=.227, rely=.48, anchor="c", height=50, width=300)

label_marina = Label(window, text="а нужные не люблю, ага", font=LARGE_FONT, bg="#1A1A1D", fg="#1A1A1D")
label_marina.grid(row=13, column=0)

click = Button(window, text="Построить графики силовых линий", bg="#1A1A1D", fg="#bbbbbf", font=LARGE_FONT, command=plotting)
click.place(relx=.19, rely=.7, anchor="c", height=50, width=450)

label_color = Label(window, text="H-синий, E-красный", anchor="n", font=LARGE_FONT,  bg="#4e4e52", fg="#bbbbbf",)
label_color.place(relx=.7, rely=.5, anchor="c", height=800, width=700, bordermode=OUTSIDE)

window.mainloop()
