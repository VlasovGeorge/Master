from tkinter import *
from tkinter import messagebox
import time # импорт времени
import random

pole = Tk()

app_running = True #приложение работает

size_canvas_x = 500 # размера поля
size_canvas_y = 500
s_x = s_y = 10  # размер игрового поля
s_y = 10
step_x = size_canvas_x // s_x  # шаг по горизонтали
step_y = size_canvas_y // s_y  # шаг по вертикали
size_canvas_x = step_x * s_x
size_canvas_y = step_y * s_y
delta_menu_x = 4
menu_x = step_x * delta_menu_x  # 250
menu_y = 40
ships = s_x // 2  # определяем максимальное кол-во кораблей
ship_len1 = s_x // 4  # длина первого типа корабля
ship_len2 = s_x // 3  # длина второго типа корабля
ship_len3 = s_x // 2  # длина третьего типа корабля
enemy_ships1 = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)] # список кораблей игрока 1
enemy_ships2 = [[0 for i in range(s_x + 1)] for i in range(s_y + 1)] #  список кораблей игрока 2
list_ids = []  # список объектов canvas


points1 = [[-1 for i in range(s_x)] for i in range(s_y)] # points1 - список куда мы кликнули мышкой, для удаления избыточности в коде, если -1, то клика не было
points2 = [[-1 for i in range(s_x)] for i in range(s_y)] # points2 - список куда кликнул мышкой второй игрок

boom = [[0 for i in range(s_x)] for i in range(s_y)]# boom - список попаданий по кораблям противника

ships_list = [] # ships_list - список кораблей игрока 1 и игрока 2

# print(enemy_ships1)

def on_closing(): # функция закрытия окна
    global app_running
    if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"): # создание окна для закрытия("ок" или "отмена")
        app_running = False
        pole.destroy()


pole.protocol("WM_DELETE_WINDOW", on_closing) # для закрытия окна
pole.title("Игра Морской Бой") # название игры
pole.resizable(0, 0) # неизменяемость поля
pole.wm_attributes("-topmost", 1) # уствновка настроек для холста, окна поверх других окон
canvas = Canvas(pole, width=size_canvas_x + menu_x + size_canvas_x, height=size_canvas_y + menu_y, bd=0,
                highlightthickness=0) # задание параметров
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="white") # создание прямоугольника на холсте (по 4 координатам)
canvas.create_rectangle(size_canvas_x + menu_x, 0, size_canvas_x + menu_x + size_canvas_x, size_canvas_y,
                        fill="lightyellow")
canvas.pack() # для отображения созданного всего выше
pole.update() # добавление в поле


def draw_table(offset_x=0): # игнорирование байтового смещения, байтов, смещение указателя чтения/записи файла, смещение по х
    for i in range(0, s_x + 1):
        canvas.create_line(offset_x + step_x * i, 0, offset_x + step_x * i, size_canvas_y)
    for i in range(0, s_y + 1):
        canvas.create_line(offset_x, step_y * i, offset_x + size_canvas_x, step_y * i)


draw_table() # наше оконце
draw_table(size_canvas_x + menu_x) # все поле

t0 = Label(pole, text="Игрок №1", font=("Helvetica", 16)) # установка подписей относительно игрового поля
t0.place(x=size_canvas_x // 2 - t0.winfo_reqwidth() // 2, y=size_canvas_y + 3)  # размещение по координатам
t1 = Label(pole, text="Игрок №2", font=("Helvetica", 16))
t1.place(x=size_canvas_x + menu_x + size_canvas_x // 2 - t1.winfo_reqwidth() // 2, y=size_canvas_y + 3)

t0.configure(bg="red") #цвета
t0.configure(bg="#f0f0f0")


def button_show_enemy1(): # кнопка для показа пкораблей ротивника
    for i in range(0, s_x):
        for j in range(0, s_y): # вертикаль/горизноталь
            if enemy_ships1[j][i] > 0:
                color = "red" # без нажатия, при нажатии кнопки
                if points1[j][i] != -1: # при нажатии
                    color = "green"
                _id = canvas.create_rectangle(i * step_x, j * step_y, i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)


def button_show_enemy2():
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships2[j][i] > 0:
                color = "red"
                if points2[j][i] != -1:
                    color = "green"
                _id = canvas.create_rectangle(size_canvas_x + menu_x + i * step_x, j * step_y,
                                              size_canvas_x + menu_x + i * step_x + step_x, j * step_y + step_y,
                                              fill=color)
                list_ids.append(_id)


def button_begin_again(): # list_ids работаем с этим списком кнопка начать заново
    global list_ids
    global points1, points2
    global boom
    global enemy_ships1, enemy_ships2
    for el in list_ids:
        canvas.delete(el)
    list_ids = []
    generate_ships_list() # будет обнуление
    # print(ships_list)
    enemy_ships1 = generate_enemy_ships()
    enemy_ships2 = generate_enemy_ships()
    points1 = [[-1 for i in range(s_x)] for i in range(s_y)] # координаты
    points2 = [[-1 for i in range(s_x)] for i in range(s_y)]
    boom = [[0 for i in range(s_x)] for i in range(s_y)]


b0 = Button(pole, text="Показать корабли Игрока №1", command=button_show_enemy1) # создание кнопочек
b0.place(x=size_canvas_x + 20, y=30) # виджеты по координатам

b1 = Button(pole, text="Показать корабли Игрока №2", command=button_show_enemy2)
b1.place(x=size_canvas_x + 20, y=70)

b2 = Button(pole, text="Начать заново!", command=button_begin_again)
b2.place(x=size_canvas_x + 20, y=110)


def draw_point(x, y): # здесь мы инициализируем функцию для кружочков и крестиков при простом нажатии
    # print(enemy_ships1[y][x])
    if enemy_ships1[y][x] == 0:
        color = "red"
        id1 = canvas.create_oval(x * step_x, y * step_y, x * step_x + step_x, y * step_y + step_y, fill=color)
        id2 = canvas.create_oval(x * step_x + step_x // 3, y * step_y + step_y // 3, x * step_x + step_x - step_x // 3, # адресуем кружочек, кружок внутри кружка
                                 y * step_y + step_y - step_y // 3, fill="white")
        list_ids.append(id1) # добавляем в наш лист для тогочо, чтобы обнулять при новой игре
        list_ids.append(id2)
    if enemy_ships1[y][x] > 0: # если все-таки попали,крестик
        color = "blue"
        id1 = canvas.create_rectangle(x * step_x, y * step_y + step_y // 2 - step_y // 10, x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color) # адресуем крестик
        id2 = canvas.create_rectangle(x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y, fill=color)
        list_ids.append(id1)
        list_ids.append(id2)


def draw_point2(x, y, offset_x=size_canvas_x + menu_x): # тоже самое, поле игрока норме 2
    # print(enemy_ships1[y][x])
    if enemy_ships2[y][x] == 0:
        color = "red"
        id1 = canvas.create_oval(offset_x + x * step_x, y * step_y, offset_x + x * step_x + step_x, y * step_y + step_y,
                                 fill=color)
        id2 = canvas.create_oval(offset_x + x * step_x + step_x // 3, y * step_y + step_y // 3,
                                 offset_x + x * step_x + step_x - step_x // 3,
                                 y * step_y + step_y - step_y // 3, fill="white")
        list_ids.append(id1)
        list_ids.append(id2)
    if enemy_ships2[y][x] > 0:
        color = "blue"
        id1 = canvas.create_rectangle(offset_x + x * step_x, y * step_y + step_y // 2 - step_y // 10, # создание прямоугольника на холсте
                                      offset_x + x * step_x + step_x,
                                      y * step_y + step_y // 2 + step_y // 10, fill=color)
        id2 = canvas.create_rectangle(offset_x + x * step_x + step_x // 2 - step_x // 10, y * step_y,
                                      offset_x + x * step_x + step_x // 2 + step_x // 10, y * step_y + step_y,
                                      fill=color)
        list_ids.append(id1)
        list_ids.append(id2)


def check_winner(x, y): # проверка победителя
    win = False
    if enemy_ships1[y][x] > 0:
        boom[y][x] = enemy_ships1[y][x]
    sum_enemy_ships1 = sum(sum(i) for i in zip(*enemy_ships1))
    sum_boom = sum(sum(i) for i in zip(*boom))
    # print(sum_enemy_ships1, sum_boom)
    if sum_enemy_ships1 == sum_boom:
        win = True
    return win


def check_winner2(): # проверка
    win = True
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships1[j][i] > 0:
                if points1[j][i] == -1:
                    win = False
    # print(win)
    return win


def check_winner2_igrok_2():
    win = True
    for i in range(0, s_x):
        for j in range(0, s_y):
            if enemy_ships2[j][i] > 0:
                if points2[j][i] == -1:
                    win = False
    # print(win)
    return win


def add_to_all(event): #куда кликнули мышкой
    global points1, points2
    _type = 0  # ЛКМ
    if event.num == 3:
        _type = 1  # ПКМ
    # print(_type)
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    # print(mouse_x, mouse_y)
    ip_x = mouse_x // step_x # получаем координаты ячейки
    ip_y = mouse_y // step_y # координаты игрового поля
    #  print(ip_x, ip_y, "_type:", _type)

    # первое игровое поле
    if ip_x < s_x and ip_y < s_y: # координаты, по которым ведем  проверку, был ли клик
        if points1[ip_y][ip_x] == -1: # клик, адресация новой точки
            points1[ip_y][ip_x] = _type # тип клика
            draw_point(ip_x, ip_y)
            # if check_winner(ip_x, ip_y): # создание поля для вывода победы
            if check_winner2():
                print("Победа Игрока №2 (Все корабли противника Игрока №1 подбиты)!!!!!")
                points1 = [[10 for i in range(s_x)] for i in range(s_y)]
                points2 = [[10 for i in range(s_x)] for i in range(s_y)]
        # print(len(list_ids))

    # второе игровое поле
    if ip_x >= s_x + delta_menu_x and ip_x <= s_x + s_x + delta_menu_x and ip_y < s_y:
        # print("ok")
        if points2[ip_y][ip_x - s_x - delta_menu_x] == -1:
            points2[ip_y][ip_x - s_x - delta_menu_x] = _type
            draw_point2(ip_x - s_x - delta_menu_x, ip_y)
            # if check_winner(ip_x, ip_y):
            if check_winner2_igrok_2():
                print("Победа Игрока №1 (Все корабли противника Игрока №2 подбиты)!!!!!")
                points1 = [[10 for i in range(s_x)] for i in range(s_y)]
                points2 = [[10 for i in range(s_x)] for i in range(s_y)]


canvas.bind_all("<Button-1>", add_to_all)  # ЛКМ привязка к событиям
canvas.bind_all("<Button-3>", add_to_all)  # ПКМ


def generate_ships_list():
    global ships_list
    ships_list = [] # список случайных длин кораблей
    # генерируем список случайных длин кораблей
    for i in range(0, ships):
        ships_list.append(random.choice([ship_len1, ship_len2, ship_len3]))
    # print(ships_list)


def generate_enemy_ships():
    global ships_list
    enemy_ships = [] # создание списка для вражеских кораблей

    # подсчет суммарной длины кораблей
    sum_1_all_ships = sum(ships_list) # чтобы не накладывались друг на друга
    sum_1_enemy = 0

    # print("sum: ", sum_1_all_ships)

    while sum_1_enemy != sum_1_all_ships: # генерируем список расположения ораблей противника, делае разброс таким образом, чтобы они не пересекались друг с другом
        # обнуляем массив кораблей врага
        enemy_ships = [[0 for i in range(s_x + 1)] for i in
                       range(s_y + 1)]  # +1 для доп. линии справа и снизу, для успешных проверок генерации противника

        for i in range(0, ships):
            len = ships_list[i]
            horizont_vertikal = random.randrange(1, 3)  # 1- горизонтальное 2 - вертикальное

            primerno_x = random.randrange(0, s_x)
            if primerno_x + len > s_x: # если больше
                primerno_x = primerno_x - len # то сдвигаем координату влево

            primerno_y = random.randrange(0, s_y)
            if primerno_y + len > s_y:
                primerno_y = primerno_y - len

            # print(horizont_vertikal, primerno_x,primerno_y)
            if horizont_vertikal == 1: # если горизонтальное размещение
                if primerno_x + len <= s_x:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + \
                                               enemy_ships[primerno_y][primerno_x + j] + \
                                               enemy_ships[primerno_y][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j] # соседние координаты
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет координат противника
                                enemy_ships[primerno_y][primerno_x + j] = i + 1  # записываем номер корабля(от ships_list[i])
                        except Exception: # если возникает исключение ничего не делаем
                            pass
            if horizont_vertikal == 2:
                if primerno_y + len <= s_y:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
                                               enemy_ships[primerno_y + j][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
                                               enemy_ships[primerno_y + j][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j][primerno_x - 1]
                            # print(check_near_ships)
                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y + j][primerno_x] = i + 1  # записываем номер корабля
                        except Exception:
                            pass

        # делаем подсчет 1ц
        sum_1_enemy = 0
        for i in range(0, s_x):
            for j in range(0, s_y):
                if enemy_ships[j][i] > 0:
                    sum_1_enemy = sum_1_enemy + 1

        # print(sum_1_enemy)
        # print(ships_list)
        # print(enemy_ships)
    return enemy_ships


generate_ships_list()
# print(ships_list)
enemy_ships1 = generate_enemy_ships()
enemy_ships2 = generate_enemy_ships()
# print("****************************")
# print(enemy_ships1)
# print("****************************")
# print(enemy_ships2)
# print("****************************")

while app_running: # правда
    if app_running: # если правда
        pole.update_idletasks()
        pole.update()
    time.sleep(0.005)
