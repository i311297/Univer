from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.ttk as ttk
import json
import networkx as nx

class js:
    def __init__(self):
        self.dct = 0

def Convert(lst):
    res_dct = {lst[i][0]: lst[i][1] for i in range(0, len(lst))}
    return res_dct

def obr(d):
    G = nx.Graph()
    films = []
    for i in d:
        films.append([i['name'], [j['title'] for j in i['films']]])

        levels = []
    for i in range(len(films)):
        for j in range(1,len(films)):
            levels.append([[films[i][0],films[j][0]], set(films[i][1]).intersection(films[j][1])])
    for i in  levels:
        if len(i[1])>0:
            G.add_edge(*tuple(i[0]))
    return G, films


def numberOfBacon(name, G):
    return len(nx.shortest_path(G, name, 'Kevin Bacon')) - 1


def internationale(name, G, films):
    actors = nx.shortest_path(G, name, 'Kevin Bacon')
    dct = Convert(films)
    text = []
    for i in range(len(actors) - 1):
        text.append(actors[i] + " снимался(лась) в фильмах с " + actors[i + 1] + " " +
                    str(set(dct[actors[i]]).intersection(set(dct[actors[i + 1]]))) + ";" + '\n')
    return text


### tk kinter

def click():
    name = comb.get()
    data = js.dct
    g, films = obr(data)
    nb = numberOfBacon(name, g)
    i = internationale(name, g, films)

    lab1.config(text='Число Бэйкона для ' + str(name) + ': ' + str(nb))
    lab2.config(text=''.join(i))


def fileN():
    filename = askopenfilename()
    with open(filename) as json_file:
        js.dct = json.load(json_file)
        data = js.dct
    names = []
    for i in data:
        names.append(i['name'])

    comb.config(values=names)
    comb.set(names[0])


window = Tk()
window.title("Число Бэйкона")
window.resizable(0, 0)
window.configure(bg='white')
x = (window.winfo_screenwidth() - window.winfo_reqwidth()) / 2
y = (window.winfo_screenheight() - window.winfo_reqheight()) / 2
window.wm_geometry("+%d+%d" % (x, y))

frame2 = Frame(window, height=400, width=600, bg='white')
frame1 = Frame(window, width=800, bg='white')
frame3 = Frame(window, width=800, height=400, bg='white')
frame4 = Frame(window, width=800, height=400, bg='white')
frame2.grid(column=0, row=1)
frame1.grid(column=0, row=0)
frame3.grid(column=0, row=2)
frame4.grid(column=0, row=3)
lab1 = Label(frame4, bg='white')
lab1.grid(column=0, row=0)
lab2 = Label(frame4, bg='white')
lab2.grid(column=0, row=1)
comb = ttk.Combobox(frame2, height=20, width=15, font=("Calibri Bold", 12), justify='center')
comb.grid(column=0, row=0)

text = Label(frame1, text='Выберите актера', font=("Calibri Bold", 12), bg="white")
butChoose = Button(frame2, text='Выбрать файл', command=fileN, font=("Calibri Bold", 12))
but = Button(frame3, text='Применить', font=("New Times Romans", 12), width=18, command=click)
but.grid(column=2, row=2, pady=15, ipady=5)
text.grid(column=0, row=1)
butChoose.grid(column=1, row=0)

window.mainloop()