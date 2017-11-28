# картинки 400 х 400 маркировка правой нижней клетки серым цветом + шум

# Подключение модулей

import os, tkinter, random
from PIL import Image, ImageTk, ImageDraw

# dir_name = "nums"
SIDE = 4
#IMG = "23.jpg"
images_list = ("1.jpg","2.jpg","3.jpg","4.jpg","5.jpg","6.jpg","7.jpg","8.jpg",
               "9.jpg","10.jpg","11.jpg","12.jpg","13.jpg","14.jpg","15.jpg","16.jpg",
               "17.jpg","18.jpg","19.jpg","20.jpg","21.jpg","22.jpg","23.jpg","24.jpg",
               "25.jpg","26.jpg","27.jpg","28.jpg","29.jpg","30.jpg","31.jpg","32.jpg","33.jpg","34.jpg")

IMG = images_list[random.randint(0,len(images_list)-1)]
moves = 0

# Окончание игры путем сравнения расположения фишек
# с первоначальным положением индексов картинок
p=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] # начальный список индексов
def IsSolution():
    result = True
    for i in p:
        if p[i] != i:
            result = False
            break
    return result


def label_above(curr):
    ''' Вернуть соседа сверху
    '''
    return labels[(curr.row - 1) * SIDE + curr.column]


def label_under(curr):
    ''' Вернуть соседа снизу
    '''
    return labels[(curr.row + 1) * SIDE + curr.column]


def label_left(curr):
    ''' Вернуть соседа слева
    '''
    return labels[curr.row * SIDE + curr.column - 1]


def label_right(curr):
    ''' Вернуть соседа справа
    '''
    return labels[curr.row * SIDE + curr.column + 1]


def render(curr, near):
    ''' Отрисовка расположения двух клеток
    '''
    # if near is not None:
    if near:
        curr.grid(row=curr.row, column=curr.column)
        near.grid(row=near.row, column=near.column)


def exchange(curr, near):
    ''' Обмен местами клеток в общем списке
    '''
    # if near is not None:
    global EndOfGame
    global p
    global moves
    if near:
        ci = curr.row * SIDE + curr.column
        ni = near.row * SIDE + near.column
        labels[ci], labels[ni] = labels[ni], labels[ci]

        p[ci],p[ni] = p[ni],p[ci]   # обмен индексов

        # Вывод количества ходов

        moves += 1
        label_3 = tkinter.Label(main_window, text=str(moves))
        label_3.grid(row=5, column=1)
        if IsSolution():
            label_4 = tkinter.Label(main_window, text='Победа!')
            label_4.grid(row=6, column=0)
            EndOfGame=True


def key_press(btn):
    ''' Основная логика перемещения на игровом поле.
        Основной элемент логики - пустая клетка - от неё определяем соседа.
        Потом меняем координаты пустой клетки и соседа.
    '''
    near = None  # <- None - специальное значение в Питоне - "ничто"

    global EndOfGame # При окончании игры отключаем клавиши
    EndOfGame = False
    if not(EndOfGame):
        if btn == 'r' and curr.column > 0:
            # print('Вправо')
            near = label_left(curr)
            curr.column -= 1
            near.column += 1
        elif btn == 'l' and curr.column < SIDE - 1:
            # print('Влево')
            near = label_right(curr)
            curr.column += 1
            near.column -= 1
        elif btn == 'u' and curr.row < SIDE - 1:
            # print('Вверх')
            near = label_under(curr)
            curr.row += 1
            near.row -= 1
        elif btn == 'd' and curr.row > 0:
            # print('Вниз')
            near = label_above(curr)
            curr.row -= 1
            near.row += 1

        exchange(curr, near)
        render(curr, near)


def mix_up():
    ''' Перемешивание клеток
        SIDE ** 4 - взято для лучшего перемешивания,
         т.к. не все вызовы функции нажатия кнопок
         будут приводить клеток к движению на поле
    '''
    global moves
    buttons = ['d', 'u', 'l', 'r']
    for i in range(SIDE ** 4):
        x = random.choice(buttons)  # <- choice - функция из модуля random
        # print('ход {}: {}'.format(i, x))
        key_press(x)
        moves = -1

'''
# выделение правого нижнего квадратика серым цветом для новых картинок

def markir():
    image = Image.open(IMG)

    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()

    for i in range(width-width//4,width):
        for j in range(height-height//4,height):
            a = pix[i, j][0]
            b = pix[i, j][1]
            c = pix[i, j][2]
            s = (a + b + c) // 3
            draw.point((i, j), (s, s, s))
    image.save(IMG)

# добавление шумов в правый нижний угол

def shum():
    image = Image.open(IMG)
    factor = 50
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()

    for i in range(width-width//4,width):
        for j in range(height-height//4,height):
            rand = random.randint(-factor, factor)
            a = pix[i, j][0] + rand
            b = pix[i, j][1] + rand
            c = pix[i, j][2] + rand
            if (a < 0):
                a = 0
            if (b < 0):
                b = 0
            if (c < 0):
                c = 0
            if (a > 255):
                a = 255
            if (b > 255):
                b = 255
            if (c > 255):
                c = 255
            draw.point((i, j), (a, b, c))
    image.save(IMG)
'''
def get_regions(image):
    ''' Функция разбиения изображения на квадратики.
        На входе ожидает объект PIL.Image
        Возвращает список картинок-квадратиков ImageTk.PhotoImage
    '''
    regions = []
    pixels = image.width // SIDE
    for i in range(SIDE):
        for j in range(SIDE):
            x1 = j * pixels
            y1 = i * pixels
            x2 = j * pixels + pixels
            y2 = i * pixels + pixels
            box = (x1, y1, x2, y2)
            region = image.crop(box)
            region.load()
            regions.append(ImageTk.PhotoImage(region))
    return regions


main_window = tkinter.Tk()
main_window.title("Puzzle 15")

# Включить обе процедуры для новых картинок
# markir()
# shum()

image=Image.open(IMG)
image_objects_list = get_regions(image)


labels = []

for i in range(SIDE):
    for j in range(SIDE):
        # переход от 2D в 1D
        x = i * SIDE + j
        label = tkinter.Label(main_window, image=image_objects_list[x])
        label.grid(row=i, column=j)
        # дополнительные атрибуты объекта label
        label.row = i
        label.column = j
        label.x = x
        labels.append(label)

curr = labels[-1]


# EndOfGame=False
label_2 = tkinter.Label(main_window, text='Ходов = ')
label_2.grid(row=5,column=0)

# mix_up
main_window.after(2000, mix_up)

main_window.bind('<Up>', lambda x: key_press('u'))
main_window.bind('<Down>', lambda x: key_press('d'))
main_window.bind('<Left>', lambda x: key_press('l'))
main_window.bind('<Right>', lambda x: key_press('r'))
main_window.bind('<q>', lambda x: exit(0))


main_window.mainloop()
