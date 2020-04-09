# -*- coding: utf-8 -*-

from kivy.app import App # импорт класса конструктора для приложения
from kivy.lang import Builder # импорт строителя kv файла
from kivy.uix.button import Button # импорт виджета кнопки
from kivy.uix.widget import Widget # импорт класса создания классов новых виджетов
from kivy.uix.boxlayout import BoxLayout # импорт виджета для расположения виджетов в связке
from kivy.uix.label import Label # импорт виджета для отображения текста
from kivy.uix.screenmanager import ScreenManager, Screen # импорт виджета для управления экранами
from kivy.graphics import Line, RoundedRectangle, Color, Rectangle # импорт инструмментов рисования на экране
from kivy.core.window import Window # импорт управления размером экрана
from kivy.uix.image import Image
import random
from io import open # импорт управления кодировкой для записи и считывания из файла
import time # импорт для сбора метрик по времени
from kivy.clock import Clock # импорт для управления активностями с таймингом
from functools import partial #импорт для управления активностями с таймингом
from Client import send
Window.size = (300,500) #размеры окна
#цвета для отрисовок элементов на экране
YELLOW = (1, 1, 0)
BLACK = (0,0,0)
PINK = (1, 0, 1)
GREEN = (0,190/255,0)
WHITE = (1,1,1)
RED = (1,0,0)

Language = 0 # флаг фиксации выбранного языка
Number_test = 0
p = 0
metrics = [0,0,0,0,0,0,0,0,0,0,0,0,0]

#конструкторы для построения пустых kv файлов
scr_rus = Builder.load_file("Empty.kv") # конструктор приложения с русским языком
scr_en = Builder.load_file("Empty.kv") # конструктор приложения с английским языком


class First_Screen(App):
# самый первый класс строящий первое окно с выбором языка
# далее идут два метода для построения приложений с выбранным языком
# Они останавливают работу текущего App приложения и строят новое в зависимости от выбранного языка
    def Language_English(self):
        global Language
        Language = 2
        self.stop()
        metrics[0] = Language
        Gen_Menu_en().run()

    def Language_Russian(self):
        global Language
        Language = 1
        self.stop()
        metrics[0] = Language
        Gen_Menu_rus().run()
# метод-конструктор для построения первого окна приложения
    def build(self):
        with open("First_Screen.kv", encoding='utf8') as f:
            Screen_first = Builder.load_string(f.read())
        return Screen_first

class Second_Screen(Screen):
# экран для заполнения информации о пациенте
    check_purification_m = 0 # флаг для проверки на наличии галки у мужсокого пола
    wid = 1.5
    pol = ""
    check_purification_w = 0# флаг для проверки на наличие галки у женского пола
    disease = 0
    soglas = 0
    global metrics

    def Text(self,text_1,text_2,text_3):
    # метод возвращает данные из заполненых полей
        data = []
        data.append(text_1)
        data.append(text_2)
        data.append(text_3)
        metrics[1] = data[0]
        metrics[3] = data[1]
        metrics[5] = data[2]
        return data

    def purification_m(self,btn):
    # метод закраски поля для галки в мужском чек боксе
        with btn.canvas:
            Color(*WHITE)
            Rectangle(pos=(btn.pos), size = (btn.size))
        self.check_purification_m = 0 # меняем влаг для уведомления об отсутсвии галки
        self.pol = "Women" # меняем пол так как если произошла закраска поля, значит галка выбора была поставлена в друг чек боксе

    def purification_w(self,btn):
        # метод закраски поля для галки в женском чек боксе
        with btn.canvas:
            Color(*WHITE)
            Rectangle(pos=(btn.pos), size = (btn.size))
        self.check_purification_w = 0  # меняем влаг для уведомления об отсутсвии галки
        self.pol = "Men"  # меняем пол так как если произошла закраска поля, значит галка выбора была поставлена в друг чек боксе

    def paint_check_m(self):
    # метод ставит галочку в поле для выбора мужского пола
        btn = self.children[0].children[0].children[-5].children[3] # обращаемся к этому виджету
        #проверяем наличие галки у поля для мужсского пола (0- ее нет)
        if self.check_purification_m == 0:
            #отрисовываем галку в поле
            with btn.canvas:
                Color(*GREEN)
                Line(points=[btn.pos[0]+self.wid, btn.pos[1] + btn.height/2,
                             btn.pos[0]+ btn.width/2, btn.pos[1]+self.wid,
                             btn.pos[0] + btn.width - self.wid, btn.pos[1] + btn.height - self.wid], width=self.wid, cap = "round", joint = 'round')
            self.check_purification_m = 1 #отмечаем наличие поставленной галки
            self.pol = "Men" # созранем название текущего выбранного пола
            # если есть наличие галки в поля для женского пола то мы ее убираем, оставляя галку только в мужском
            if self.check_purification_w == 1:
                self.purification_w(self.children[0].children[0].children[-5].children[1])
        else:
            # при наличии галки мы ее убираем в случае нажатия
            self.purification_m(btn)
        metrics[2] = self.pol

    def paint_check_w(self):
        # Все тоже самое что и в методе paint_check_m
            btn = self.children[0].children[0].children[-5].children[1]
            if self.check_purification_w == 0:
                with btn.canvas:
                    Color(*GREEN)
                    Line(points=[btn.pos[0] + self.wid, btn.pos[1] + btn.height / 2,
                                 btn.pos[0] + btn.width / 2,btn.pos[1] + self.wid,
                                 btn.pos[0] + btn.width - self.wid, btn.pos[1] + btn.height - self.wid], width=self.wid)
                self.check_purification_w = 1
                self.pol = "Women"
                if self.check_purification_m == 1:
                    self.purification_m(self.children[0].children[0].children[-5].children[3])
            else:
                self.purification_w(btn)
            metrics[2] = self.pol

    def purification_disease(self,btn):
    # закраска поля для отметки о наличии заболеваний
        with btn.canvas:
            Color(*WHITE)
            Rectangle(pos=(btn.pos), size = (btn.size))
        self.disease = 0

    def paint_check_disease(self):
    # метод для отметки галки в поле наличия заболевания ( схож с методами для мужского и женского пола)
        btn = self.children[0].children[0].children[5]
        if self.disease == 0:
            with btn.canvas:
                Color(*GREEN)
                Line(points=[btn.pos[0] + self.wid, btn.pos[1] + btn.height / 2,
                             btn.pos[0] + btn.width / 2,btn.pos[1] + self.wid,
                             btn.pos[0] + btn.width - self.wid, btn.pos[1] + btn.height - self.wid], width=self.wid)
            self.disease = 1
        else:
            self.purification_disease(btn)
        metrics[4] = self.disease

    def purification_soglas(self,btn):
    # метод для закраски поля о наличии согласия
        with btn.canvas:
            Color(*WHITE)
            Rectangle(pos=(btn.pos), size = (btn.size))
        self.soglas = 0

    def paint_check_soglas(self):
    # метод  для простановки галки в поле для отметки о согласии обработки личных данных
        btn = self.children[0].children[0].children[1]
        if self.soglas == 0:
            with btn.canvas:
                Color(*GREEN)
                Line(points=[btn.pos[0] + self.wid, btn.pos[1] + btn.height / 2,
                             btn.pos[0] + btn.width / 2,btn.pos[1] + self.wid,
                             btn.pos[0] + btn.width - self.wid, btn.pos[1] + btn.height - self.wid], width=self.wid)
            self.soglas = 1
        else:
            self.purification_soglas(btn)
        #print(self.soglas)

    def cameback(self):
    # метод для возврата на предыдущий экран с выбором языка
        global Language
        if Language == 1:
            global scr_rus
            scr_rus.current_Screen("Empty_Screen")
            Gen_Menu_rus().stop()
        elif Language == 2:
            global scr_en
            scr_en.current_Screen("Empty_Screen")
            Gen_Menu_en().stop()
        First_Screen().run()

    def next_screen(self):
    #переход на новый экран
        if self.soglas == 1:
            global Language
            if Language == 1:
                scr_rus.current_Screen("Fourth_Screen")
            elif Language == 2:
                scr_en.current_Screen("Fourth_Screen")

    def __init__(self, **kwargs):
    # конструктор построения исходного экрана
        super(Second_Screen, self).__init__(**kwargs)

class Color_Trail_Test(Widget):
# класс типа виджет для построения тестов для части А и B
    def wrong_btn(self,i,btn):
    #вызывается для закрашивания в красный цвет,в случае ошибки
        with btn.canvas:
            Color(*RED)
            self.round = RoundedRectangle(pos=(self.mas_pos_8[i], self.mas_pos_8[i + 1]), size=(self.diametr, self.diametr),
                             radius=[100])
        self.count_wrong += 1

    def camback_paint(self,i,*largs):
        # методы вызова обратной закраски
        i = int(i)
        print(i)
        btn = self.mas_child_obj[int(i/2)]
        lbl = self.paint(i,btn)
        btn.add_widget(lbl)

    def line(self,i):
        # соединительная линия между, верно соединеными кругами
        with self.canvas:
            Color(*BLACK)
            Line(points=[self.pos_center_points[i], self.pos_center_points[i+1]], width=1.5)

    def callback_1(self):
        # активности при нажатии
        self.mas_register_num_button[0] = 1
        self.event.cancel()
        self.event = Clock.schedule_interval(lambda dt: self.help(), 10)

    def callback_2(self):
        flag = 0
        k = 1
        for i in range(1):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[1] = 2
            self.line(0)
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
        else:
            self.wrong_btn(2,self.mas_child_obj[1])
            Clock.schedule_once(partial(self.camback_paint,'2'), 0.5)

    def callback_3(self):
        flag = 0
        k = 1
        for i in range(2):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[2] = 3
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(1)
        else:
            self.wrong_btn(4, self.mas_child_obj[2])
            Clock.schedule_once(partial(self.camback_paint, '4'), 0.5)

    def callback_4(self):
        flag = 0
        k = 1
        for i in range(3):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[3] = 4
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(2)
        else:
            self.wrong_btn(6, self.mas_child_obj[3])
            Clock.schedule_once(partial(self.camback_paint, '6'), 0.5)

    def callback_5(self):
        flag = 0
        k = 1
        for i in range(4):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[4] = 5
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(3)
        else:
            self.wrong_btn(8, self.mas_child_obj[4])
            Clock.schedule_once(partial(self.camback_paint, '8'), 0.5)

    def callback_6(self):
        flag = 0
        k = 1
        for i in range(5):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[5] = 6
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(4)
        else:
            self.wrong_btn(10, self.mas_child_obj[5])
            Clock.schedule_once(partial(self.camback_paint, '10'), 0.5)

    def callback_7(self):
        flag = 0
        k = 1
        for i in range(6):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[6] = 7
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(5)
        else:
            self.wrong_btn(12, self.mas_child_obj[6])
            Clock.schedule_once(partial(self.camback_paint, '12'), 0.5)

    def callback_8(self):
        k = 1
        flag = 0
        for i in  range(7):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k +=1
        if self.col == 8:
            if flag == 0:
                self.mas_register_num_button[7] = 8
                next_screen = True
            else:
                next_screen = False
                self.wrong_btn(14, self.mas_child_obj[7])
                Clock.schedule_once(partial(self.camback_paint, '14'), 0.5)
            next_screen = True
            if next_screen == True:
                global metrics, Number_test, Language, scr_rus, scr_en
                if Number_test == 1:
                    metrics[6] = time.time() - metrics[6]
                    metrics[7] = self.count_wrong
                    metrics[8] = self.count_help
                elif Number_test == 2:
                    metrics[9] = time.time() - metrics[9]
                    metrics[10] = self.count_wrong
                    metrics[11] = self.count_help
                Number_test = 0
                if Language == 1:
                    scr_rus.current_Screen(self.Screen_name)
                elif Language == 2:
                    scr_en.current_Screen(self.Screen_name)
        else:
            if flag == 0:
                self.mas_register_num_button[7] = 8
                self.event.cancel()
                self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
                self.line(6)
            else:
                self.wrong_btn(14, self.mas_child_obj[7])
                Clock.schedule_once(partial(self.camback_paint, '14'), 0.5)

    def callback_9(self):
        flag = 0
        k = 1
        for i in range(8):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[8] = 9
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(7)
        else:
            self.wrong_btn(16, self.mas_child_obj[8])
            Clock.schedule_once(partial(self.camback_paint, '16'), 0.5)

    def callback_10(self):
        flag = 0
        k = 1
        for i in range(9):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[9] = 10
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(8)
        else:
            self.wrong_btn(18, self.mas_child_obj[9])
            Clock.schedule_once(partial(self.camback_paint, '18'), 0.5)

    def callback_11(self):
        flag = 0
        k = 1
        for i in range(10):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[10] = 11
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(9)
        else:
            self.wrong_btn(20, self.mas_child_obj[10])
            Clock.schedule_once(partial(self.camback_paint, '20'), 0.5)

    def callback_12(self):
        flag = 0
        k = 1
        for i in range(11):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[11] = 12
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(10)
        else:
            self.wrong_btn(22, self.mas_child_obj[11])
            Clock.schedule_once(partial(self.camback_paint, '22'), 0.5)

    def callback_13(self):
        flag = 0
        k = 1
        for i in range(12):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[12] = 13
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(11)
        else:
            self.wrong_btn(24, self.mas_child_obj[12])
            Clock.schedule_once(partial(self.camback_paint, '24'), 0.5)

    def callback_14(self):
        flag = 0
        k = 1
        for i in range(13):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[13] = 14
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(12)
        else:
            self.wrong_btn(26, self.mas_child_obj[13])
            Clock.schedule_once(partial(self.camback_paint, '26'), 0.5)

    def callback_15(self):
        flag = 0
        k = 1
        for i in range(14):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[14] = 15
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(13)
        else:
            self.wrong_btn(28, self.mas_child_obj[14])
            Clock.schedule_once(partial(self.camback_paint, '28'), 0.5)

    def callback_16(self):
        flag = 0
        k = 1
        for i in range(15):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[15] = 16
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(14)
        else:
            self.wrong_btn(30, self.mas_child_obj[15])
            Clock.schedule_once(partial(self.camback_paint, '30'), 0.5)

    def callback_17(self):
        flag = 0
        k = 1
        for i in range(16):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[16] = 17
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(15)
        else:
            self.wrong_btn(32, self.mas_child_obj[16])
            Clock.schedule_once(partial(self.camback_paint, '32'), 0.5)

    def callback_18(self):
        flag = 0
        k = 1
        for i in range(17):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[17] = 18
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(16)
        else:
            self.wrong_btn(34, self.mas_child_obj[17])
            Clock.schedule_once(partial(self.camback_paint, '34'), 0.5)

    def callback_19(self):
        flag = 0
        k = 1
        for i in range(18):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[18] = 19
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(17)
        else:
            self.wrong_btn(36, self.mas_child_obj[18])
            Clock.schedule_once(partial(self.camback_paint, '36'), 0.5)

    def callback_20(self):
        flag = 0
        k = 1
        for i in range(19):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[19] = 20
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(18)
        else:
            self.wrong_btn(38, self.mas_child_obj[19])
            Clock.schedule_once(partial(self.camback_paint, '38'), 0.5)

    def callback_21(self):
        flag = 0
        k = 1
        for i in range(20):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[20] = 21
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(19)
        else:
            self.wrong_btn(40, self.mas_child_obj[20])
            Clock.schedule_once(partial(self.camback_paint, '40'), 0.5)

    def callback_22(self):
        flag = 0
        k = 1
        for i in range(21):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[21] = 22
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(20)
        else:
            self.wrong_btn(42, self.mas_child_obj[21])
            Clock.schedule_once(partial(self.camback_paint, '42'), 0.5)

    def callback_23(self):
        flag = 0
        k = 1
        for i in range(22):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[22] = 23
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(21)
        else:
            self.wrong_btn(44, self.mas_child_obj[22])
            Clock.schedule_once(partial(self.camback_paint, '44'), 0.5)

    def callback_24(self):
        flag = 0
        k = 1
        for i in range(23):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 0:
            self.mas_register_num_button[23] = 24
            self.event.cancel()
            self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
            self.line(22)
        else:
            self.wrong_btn(46, self.mas_child_obj[23])
            Clock.schedule_once(partial(self.camback_paint, '46'), 0.5)

    def callback_25(self):
        flag = 0
        k = 1
        for i in range(24):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if self.col == 25 or self.col == 26:
            if flag == 0:
                self.mas_register_num_button[24] = 25
                next_screen = True
            else:
                next_screen = False
                self.wrong_btn(48, self.mas_child_obj[24])
                Clock.schedule_once(partial(self.camback_paint, '48'), 0.5)
            next_screen = True
            if next_screen == True:
                global metrics, Number_test, Language, scr_rus, scr_en
                if Number_test == 1:
                    metrics[6] = time.time() - metrics[6]
                    metrics[7] = self.count_wrong
                    metrics[8] = self.count_help
                elif Number_test == 2:
                    metrics[9] = time.time() - metrics[9]
                    metrics[10] = self.count_wrong
                    metrics[11] = self.count_help
                    send(metrics)
                Number_test = 0
                print(metrics)
                if Language == 1:
                    scr_rus.current_Screen(self.Screen_name)
                elif Language == 2:
                    scr_en.current_Screen(self.Screen_name)
        else:
            if flag == 0:
                self.mas_register_num_button[24] = 25
                self.event.cancel()
                self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
                self.line(23)
            else:
                self.wrong_btn(48, self.mas_child_obj[24])
                Clock.schedule_once(partial(self.camback_paint, '48'), 0.5)

    def callback_26(self, num):
        flag = 0
        k = 1
        for i in range(25):
            if self.mas_register_num_button[i] != k:
                flag = 1
            k += 1
        if flag == 1:
            self.wrong_btn(2*num, self.mas_child_obj[num])
            Clock.schedule_once(partial(self.camback_paint, str(num*2)), 0.5)


    def sortline_1(self, mas_pos_8):
        i = 0
        while i<len(mas_pos_8)-1:
            j = i+2
            while j< len(mas_pos_8):
                if mas_pos_8[i] > mas_pos_8[j]:
                    buf_x = mas_pos_8[i]
                    buf_y = mas_pos_8[i+1]
                    mas_pos_8[i] = mas_pos_8[j]
                    mas_pos_8[i+1] = mas_pos_8[j+1]
                    mas_pos_8[j] = buf_x
                    mas_pos_8[j+1] = buf_y
                j+=2
            i+=2
        return mas_pos_8

    def sortline_2(self, mas_pos_8):
        i = 0
        while i<len(mas_pos_8)-1:
            j = i+2
            while j< len(mas_pos_8):
                if mas_pos_8[i] < mas_pos_8[j]:
                    buf_x = mas_pos_8[i]
                    buf_y = mas_pos_8[i+1]
                    mas_pos_8[i] = mas_pos_8[j]
                    mas_pos_8[i+1] = mas_pos_8[j+1]
                    mas_pos_8[j] = buf_x
                    mas_pos_8[j+1] = buf_y
                j+=2
            i+=2
        return mas_pos_8

    def sortline_3(self, mas_pos_8):
        i = 1
        while i<len(mas_pos_8):
            j = i+2
            while j< len(mas_pos_8):
                if mas_pos_8[i] < mas_pos_8[j]:
                    buf_x = mas_pos_8[i-1]
                    buf_y = mas_pos_8[i]
                    mas_pos_8[i] = mas_pos_8[j]
                    mas_pos_8[i-1] = mas_pos_8[j-1]
                    mas_pos_8[j] = buf_y
                    mas_pos_8[j-1] = buf_x
                j+=2
            i+=2
        return mas_pos_8

    def sortline_4(self, mas_pos_8):
        i = 1
        while i<len(mas_pos_8):
            j = i+2
            while j< len(mas_pos_8):
                if mas_pos_8[i] > mas_pos_8[j]:
                    buf_x = mas_pos_8[i - 1]
                    buf_y = mas_pos_8[i]
                    mas_pos_8[i] = mas_pos_8[j]
                    mas_pos_8[i - 1] = mas_pos_8[j - 1]
                    mas_pos_8[j] = buf_y
                    mas_pos_8[j - 1] = buf_x
                j+=2
            i+=2
        return mas_pos_8

    def help_btn(self,i,btn):
        #метод закраски в зеленный в случае ывзова подсказки
        with btn.canvas:
            Color(*GREEN)
            self.round = RoundedRectangle(pos=(self.mas_pos_8[i], self.mas_pos_8[i + 1]), size=(self.diametr, self.diametr),
                             radius=[100])
        self.count_help += 1


    def help(self):
        # метод вызова подсказки
        pos = 0
        for i in range((len(self.mas_register_num_button))):
            if self.mas_register_num_button[i] == 0:
                pos = i
                break
        self.help_btn(pos*2,self.children[len(self.mas_register_num_button) - 1 - pos])
        num = str(pos*2)
        Clock.schedule_once(partial(self.camback_paint, num), 0.5)

    def paint(self,i,btn):
        # метод закраски круга и проставления нужного номера
        global Number_test
        str_num = str(int(i / 2) + 1)
        if Number_test != 2:
            if (int(i / 2) + 1) % 2 != 0:
                with btn.canvas:
                    Color(*BLACK)
                    RoundedRectangle(pos=(self.mas_pos_8[i], self.mas_pos_8[i + 1]), size=(self.diametr, self.diametr), radius=[100])
                    Color(*PINK)
                    RoundedRectangle(pos=(self.mas_pos_8[i]+self.obr/2, self.mas_pos_8[i + 1]+ self.obr/2), size=(self.diametr-self.obr, self.diametr-self.obr), radius=[100])
            else:
                with btn.canvas:
                    Color(*BLACK)
                    RoundedRectangle(pos=(self.mas_pos_8[i], self.mas_pos_8[i + 1]), size=(self.diametr, self.diametr),radius=[100])
                    Color(*YELLOW)
                    RoundedRectangle(pos=(self.mas_pos_8[i]+self.obr/2, self.mas_pos_8[i + 1]+ self.obr/2), size=(self.diametr-self.obr, self.diametr-self.obr), radius=[100])
        else:
            if int(str_num) > 25:
                if (int(i / 2) + 1) % 2 == 0:
                    with btn.canvas:
                        Color(*BLACK)
                        RoundedRectangle(pos=(self.mas_pos_8[i], self.mas_pos_8[i + 1]),
                                         size=(self.diametr, self.diametr), radius=[100])
                        Color(*PINK)
                        RoundedRectangle(pos=(self.mas_pos_8[i] + self.obr / 2, self.mas_pos_8[i + 1] + self.obr / 2),
                                         size=(self.diametr - self.obr, self.diametr - self.obr), radius=[100])
                else:
                    with btn.canvas:
                        Color(*BLACK)
                        RoundedRectangle(pos=(self.mas_pos_8[i], self.mas_pos_8[i + 1]),
                                         size=(self.diametr, self.diametr), radius=[100])
                        Color(*YELLOW)
                        RoundedRectangle(pos=(self.mas_pos_8[i] + self.obr / 2, self.mas_pos_8[i + 1] + self.obr / 2),
                                         size=(self.diametr - self.obr, self.diametr - self.obr), radius=[100])
            else:
                if (int(i / 2) + 1) % 2 != 0:
                    with btn.canvas:
                        Color(*BLACK)
                        RoundedRectangle(pos=(self.mas_pos_8[i], self.mas_pos_8[i + 1]),
                                         size=(self.diametr, self.diametr), radius=[100])
                        Color(*PINK)
                        RoundedRectangle(pos=(self.mas_pos_8[i] + self.obr / 2, self.mas_pos_8[i + 1] + self.obr / 2),
                                         size=(self.diametr - self.obr, self.diametr - self.obr), radius=[100])
                else:
                    with btn.canvas:
                        Color(*BLACK)
                        RoundedRectangle(pos=(self.mas_pos_8[i], self.mas_pos_8[i + 1]),
                                         size=(self.diametr, self.diametr), radius=[100])
                        Color(*YELLOW)
                        RoundedRectangle(pos=(self.mas_pos_8[i] + self.obr / 2, self.mas_pos_8[i + 1] + self.obr / 2),
                                         size=(self.diametr - self.obr, self.diametr - self.obr), radius=[100])

        if Number_test != 2:
            lbl = Label(text='[color=000000]' + str_num,
                        markup=True,
                        text_size=(self.diametr, self.diametr),
                        font_size=int(self.diametr*3/5),
                        halign="center",
                        center=[btn.pos[0] + self.diametr / 2, btn.pos[1] + self.diametr / 2],
                        valign="center")
        else:
            if int(str_num) > 25:
                str_num = str(int((i - 48) / 2) + 1)
                lbl = Label(text='[color=000000]' + str_num,
                            markup=True,
                            text_size=(self.diametr, self.diametr),
                            font_size=int(self.diametr*3/5),
                            halign="center",
                            center=[btn.pos[0] + self.diametr / 2, btn.pos[1] + self.diametr / 2],
                            valign="center")
            else:
                str_num = str(int(i / 2) + 1)
                lbl = Label(text='[color=000000]' + str_num,
                            markup=True,
                            text_size=(self.diametr, self.diametr),
                            font_size=int(self.diametr*3/5),
                            halign="center",
                            center=[btn.pos[0] + self.diametr / 2, btn.pos[1] + self.diametr / 2],
                            valign="center")
        #print(btn.pos[0] + self.diametr / 2, btn.pos[1] + self.diametr / 2)
        return lbl

    def __init__(self,col,size_x,size_y,Screen_name, **kwargs):
    # конструктор приложения (стаит точки, их разметки, прорисовку, а также содержи твсе необходимые аргументы класса)
        super(Color_Trail_Test, self).__init__(**kwargs)
        self.Screen_name = Screen_name
        self.diametr = size_x / 16
        self.obr = 3
        self.col = col
        self.count_help = 0
        self.count_wrong = 0
        self.mas_pos_8 = []
        global Number_test
        mas_pos_equation_8 = []
        mas_radius_padding = [[]]
        self.mas_pos_8.append(random.randint(int(self.diametr) + 1, size_x - int(self.diametr) - 1))
        self.mas_pos_8.append(random.randint(int(self.diametr) + 1, size_y - int(self.diametr) - 1))
        center_pos_x = self.mas_pos_8[0] + self.diametr / 2
        center_pos_y = self.mas_pos_8[1] + self.diametr / 2
        mas_radius_padding[0].append(center_pos_x - self.diametr*2)
        mas_radius_padding[0].append(center_pos_x + self.diametr*2)
        mas_radius_padding[0].append(center_pos_y - self.diametr*2)
        mas_radius_padding[0].append(center_pos_y + self.diametr*2)
        k=2
        flag = 0
        for i in range(1,col):
            self.mas_pos_8.append(random.randint(int(self.diametr)+1, size_x-int(self.diametr)-1))
            self.mas_pos_8.append(random.randint(int(self.diametr)+1, size_y-int(self.diametr)-1))
            j = 0
            while j < len(mas_radius_padding):
                while (self.mas_pos_8[k]< (mas_radius_padding[j][1]) and self.mas_pos_8[k]> (mas_radius_padding[j][0])) and (self.mas_pos_8[k+1]< (mas_radius_padding[j][3]) and self.mas_pos_8[k+1]> (mas_radius_padding[j][2])):
                    self.mas_pos_8[k] = random.randint(int(self.diametr) + 1, size_x - int(self.diametr) - 1)
                    self.mas_pos_8[k+1] = random.randint(int(self.diametr) + 1, size_y - int(self.diametr) - 1)
                    flag = 1
                if flag == 1:
                    j = 0
                    flag = 0
                else:
                    j += 1
            center_pos_x = self.mas_pos_8[k] + self.diametr / 2
            center_pos_y = self.mas_pos_8[k + 1] + self.diametr / 2
            mas_radius_padding.append([])
            mas_radius_padding[i].append(center_pos_x - self.diametr*2)
            mas_radius_padding[i].append(center_pos_x + self.diametr*2)
            mas_radius_padding[i].append(center_pos_y - self.diametr*2)
            mas_radius_padding[i].append(center_pos_y + self.diametr*2)
            k += 2
        k = 0
        if col != 8:
            if Number_test == 1:
                generator_A = 2
            else:
                generator_A = 0
            #print(Number_test)
            if Number_test == 2:
                generator_B = 2
            else:
                generator_B = 0
            if generator_A == 1:
                position_A = [size_x / 2 - self.diametr, size_y / 2 - self.diametr,  # 1
                                size_x * 2 / 3 + self.diametr, size_y / 3 - self.diametr,  # 2
                                size_x / 2 + self.diametr, size_y / 6,  # 3
                                size_x * 4 / 5, size_y / 9,  # 4
                                size_x * 3 / 4, size_y / 2 - self.diametr,  # 5
                                size_x  / 3, size_y / 2 + self.diametr,  # 6
                                size_x * 3 / 4 + self.diametr, size_y * 3 / 5,  # 7
                                size_x * 9 / 10, size_y / 4 - self.diametr,  # 8
                                size_x * 6 / 7, size_y / 10 - 2* self.diametr,  # 9
                                size_x / 2 - 2 * self.diametr, size_y / 10,  # 10
                                size_x / 2, size_y / 4,  # 11
                                size_x / 5, size_y / 3 + self.diametr,  # 12
                                size_x / 4 + self.diametr, size_y / 6 - self.diametr,  # 13
                                size_x / 10, size_y / 10 + self.diametr,  # 14
                                size_x / 5 - 2*self.diametr, size_y / 2,  # 15
                                size_x / 2 , size_y * 2 / 3,  # 16
                                size_x * 7 / 8, size_y * 2 / 3 - self.diametr,  # 17
                                size_x * 4 / 5 + self.diametr, size_y * 7 / 8,  # 18
                                size_x * 2 / 5, size_y * 3 / 4,  # 19
                                size_x / 5 + 2 * self.diametr, size_y * 4 / 5,  # 20
                                size_x * 2 / 3, size_y * 8 / 9,  # 21
                                size_x / 9, size_y * 9 / 10,  # 22
                                size_x / 10, size_y / 2 + 2*self.diametr,  # 23
                                size_x * 2 / 9, size_y * 2 / 3 + self.diametr,  # 24
                                size_x * 3 / 4 - self.diametr, size_y * 2 / 3 + self.diametr]  # 25
            elif generator_A == 2:
                position_A = [size_x / 2 + self.diametr, size_y / 2 - self.diametr,  # 1
                                size_x / 3 - self.diametr, size_y / 3 - self.diametr,  # 2
                                size_x / 2 - self.diametr, size_y / 6,  # 3
                                size_x / 5, size_y / 9,  # 4
                                size_x / 4, size_y / 2 - self.diametr,  # 5
                                size_x * 2 / 3, size_y / 2 + self.diametr,  # 6
                                size_x / 4 - self.diametr, size_y * 3 / 5,  # 7
                                size_x / 10, size_y / 4 - self.diametr,  # 8
                                size_x / 7, size_y / 12,  # 9
                                size_x / 2 + 2 * self.diametr, size_y / 10,  # 10
                                size_x / 2, size_y / 4,  # 11
                                size_x * 4 / 5, size_y / 3 + self.diametr,  # 12
                                size_x * 3 / 4 - self.diametr, size_y / 6 - self.diametr,  # 13
                                size_x * 9 / 10, size_y / 10 + self.diametr,  # 14
                                size_x * 4 / 5 + self.diametr, size_y / 2,  # 15
                                size_x / 2 - self.diametr, size_y * 2 / 3,  # 16
                                size_x / 8, size_y * 2 / 3 - self.diametr,  # 17
                                size_x / 5 - self.diametr, size_y * 7 / 8,  # 18
                                size_x * 3 / 5, size_y * 3 / 4,  # 19
                                size_x * 4 / 5, size_y * 4 / 5,  # 20
                                size_x / 3, size_y * 8 / 9,  # 21
                                size_x * 8 / 9, size_y * 9 / 10,  # 22
                                size_x * 9 / 10, size_y / 2 + self.diametr,  # 23
                                size_x * 7 / 9, size_y * 2 / 3 + self.diametr,  # 24
                                size_x / 4 + self.diametr, size_y * 2 / 3 + self.diametr]  # 25
            elif generator_A == 3:
                position_A = [size_x / 2 - self.diametr, size_y / 2 + self.diametr,  # 1
                                size_x * 2 / 3 + self.diametr, size_y * 2 / 3 + 2 * self.diametr,  # 2
                                size_x / 2 + self.diametr, size_y * 5 / 6,  # 3
                                size_x * 4 / 5, size_y * 8 / 9,  # 4
                                size_x * 3 / 4, size_y / 2 + self.diametr,  # 5
                                size_x / 3, size_y / 2 - self.diametr,  # 6
                                size_x * 3 / 4 + self.diametr, size_y * 2 / 5,  # 7
                                size_x * 9 / 10, size_y * 3 / 4 + self.diametr,  # 8
                                size_x * 6 / 7, size_y - 2 * self.diametr,  # 9
                                size_x / 2 - 2 * self.diametr, size_y * 9 / 10,  # 10
                                size_x / 2, size_y * 3 / 4,  # 11
                                size_x / 5, size_y * 2 / 3 - self.diametr,  # 12
                                size_x / 4 + self.diametr, size_y * 5 / 6 + self.diametr,  # 13
                                size_x / 10, size_y * 9 / 10 - self.diametr,  # 14
                                size_x / 5 - 2 * self.diametr, size_y / 2,  # 15
                                size_x / 2 + self.diametr, size_y / 3,  # 16
                                size_x * 7 / 8, size_y / 3 + self.diametr,  # 17
                                size_x * 4 / 5 + self.diametr, size_y / 8,  # 18
                                size_x * 2 / 5, size_y / 4,  # 19
                                size_x / 5 + 2 * self.diametr, size_y / 5,  # 20
                                size_x * 2 / 3, size_y / 9,  # 21
                                size_x / 9, size_y / 10,  # 22
                                size_x / 10, size_y / 2 - 2 * self.diametr,  # 23
                                size_x * 2 / 9, size_y / 3 - self.diametr,  # 24
                                size_x * 3 / 4 - self.diametr, size_y / 3 - self.diametr]  # 25
            if generator_A != 0:
                self.mas_pos_8 = []
                for i in range(len(position_A)):
                    self.mas_pos_8.append(position_A[i])
            if generator_B == 1:
                position_osn_B = [size_x / 2 + self.diametr, size_y / 2 + self.diametr,  # 1
                                size_x / 3 - self.diametr, size_y * 2 / 3 + self.diametr,  # 2
                                size_x / 2 - self.diametr, size_y * 5 / 6,  # 3
                                size_x / 5, size_y * 8 / 9,  # 4
                                size_x / 4, size_y / 2 + self.diametr,  # 5
                                size_x * 2 / 3, size_y / 2 - self.diametr,  # 6
                                size_x / 4 - self.diametr, size_y * 2 / 5,  # 7
                                size_x / 10, size_y * 3 / 4 + self.diametr,  # 8
                                size_x / 7, size_y - 2 * self.diametr,  # 9
                                size_x / 2 + 2 * self.diametr, size_y * 9 / 10,  # 10
                                size_x / 2, size_y * 3 / 4,  # 11
                                size_x * 4 / 5, size_y * 2 / 3 - self.diametr,  # 12
                                size_x * 3 / 4 - self.diametr, size_y * 5 / 6 + self.diametr,  # 13
                                size_x * 9 / 10, size_y * 9 / 10 - self.diametr,  # 14
                                size_x * 4 / 5 + self.diametr, size_y / 2,  # 15
                                size_x / 2 - self.diametr, size_y / 3,  # 16
                                size_x / 8, size_y / 3 + self.diametr,  # 17
                                size_x / 5 - self.diametr, size_y / 8,  # 18
                                size_x * 3 / 5, size_y / 4,  # 19
                                size_x * 4 / 5 - 2 * self.diametr, size_y / 5,  # 20
                                size_x / 3, size_y / 9,  # 21
                                size_x * 8 / 9, size_y / 10,  # 22
                                size_x * 9 / 10, size_y / 2 - 2 * self.diametr,  # 23
                                size_x * 7 / 9, size_y / 3 - self.diametr,  # 24
                                size_x / 4 + self.diametr, size_y / 3 - self.diametr]  # 25
                position_dop_B = [size_x / 2 - self.diametr, size_y / 2 + self.diametr,  # 1
                                size_x / 2 - int(1.5*self.diametr), size_y * 5 / 6 -  2*self.diametr,  # 2
                                size_x / 5 + self.diametr, size_y * 8 / 9 - 2*self.diametr,  # 3
                                size_x / 4 + 2*self.diametr, size_y / 2 + 2*self.diametr,  # 4
                                size_x * 2 / 3, size_y / 2 + self.diametr,  # 5
                                size_x / 3 + self.diametr, size_y / 2 - self.diametr,  # 6
                                size_x / 10 - int(1.5*self.diametr), size_y * 3 / 4 + self.diametr,  # 7
                                size_x / 7 + self.diametr, size_y - self.diametr,  # 8
                                size_x / 2 , size_y * 9 / 10 + self.diametr,  # 9
                                size_x / 2 - self.diametr, size_y * 9 / 10 - 5 * self.diametr,  # 10
                                size_x * 4 / 5 - 2*self.diametr, size_y * 2 / 3 - self.diametr,  # 11
                                size_x * 3 / 4 - int(1.5*self.diametr), size_y * 5 / 6 - self.diametr,  # 12
                                size_x * 9 / 10, size_y * 9 / 10 + self.diametr,  # 13
                                size_x * 4 / 5, size_y / 2  - 2*self.diametr,  # 14
                                size_x / 2 + self.diametr, size_y / 3 ,  # 15
                                size_x / 2 - 5 * self.diametr, size_y / 3 - self.diametr,  # 16
                                size_x / 5 - int(2.5*self.diametr), size_y / 8,  # 17
                                size_x * 3 / 5 - 3* self.diametr, size_y / 4,  # 18
                                size_x * 2 / 5 + 3*self.diametr, size_y / 4 - int(2.5 * self.diametr),  # 19
                                size_x / 3, size_y / 9 - 2*self.diametr,  # 20
                                size_x * 8 / 9, size_y / 10 - 2*self.diametr,  # 22
                                size_x * 9 / 10 - self.diametr, size_y / 2 - 6 * self.diametr,  # 23
                                size_x * 7 / 9, size_y / 3 - 3*self.diametr,  # 24
                                size_x / 4, size_y / 3 - 2*self.diametr]  # 25
            elif generator_B == 2:
                position_osn_B = [size_x / 2 - self.diametr, size_y / 2 - self.diametr,  # 1
                                size_x * 2 / 3 + self.diametr, size_y / 3 - self.diametr,  # 2
                                size_x / 2 + self.diametr, size_y / 6,  # 3
                                size_x * 4 / 5, size_y / 9,  # 4
                                size_x * 3 / 4, size_y / 2 - self.diametr,  # 5
                                size_x / 3, size_y / 2 + self.diametr,  # 6
                                size_x * 3 / 4 + self.diametr, size_y * 3 / 5,  # 7
                                size_x * 9 / 10, size_y / 4 - self.diametr,  # 8
                                size_x * 6 / 7, size_y / 10 - 2 * self.diametr,  # 9
                                size_x / 2 - 2 * self.diametr, size_y / 10,  # 10
                                size_x / 2, size_y / 4,  # 11
                                size_x / 5, size_y / 3 + self.diametr,  # 12
                                size_x / 4 + self.diametr, size_y / 6 - self.diametr,  # 13
                                size_x / 10, size_y / 10 + self.diametr,  # 14
                                size_x / 5 - 2 * self.diametr, size_y / 2,  # 15
                                size_x / 2, size_y * 2 / 3,  # 16
                                size_x * 7 / 8, size_y * 2 / 3 - self.diametr,  # 17
                                size_x * 4 / 5 + self.diametr, size_y * 7 / 8,  # 18
                                size_x * 2 / 5, size_y * 3 / 4,  # 19
                                size_x / 5 + 2 * self.diametr, size_y * 4 / 5,  # 20
                                size_x * 2 / 3, size_y * 8 / 9,  # 21
                                size_x / 9, size_y * 9 / 10,  # 22
                                size_x / 10, size_y / 2 + 2 * self.diametr,  # 23
                                size_x * 2 / 9, size_y * 2 / 3 + self.diametr,  # 24
                                size_x * 3 / 4 - self.diametr, size_y * 2 / 3 + self.diametr]  # 25
                position_dop_B = [size_x / 2 + 3*self.diametr, size_y / 2 - 3*self.diametr,  # 1
                                size_x * 2 / 3 - self.diametr, size_y / 3 - self.diametr,  # 2
                                size_x * 4 / 5- int(1.5 * self.diametr), size_y / 9 - self.diametr,  # 3
                                size_x * 3 / 4, size_y / 2 + self.diametr,  # 4
                                size_x / 3, size_y / 2 - self.diametr,  # 5
                                size_x / 2 + self.diametr, size_y / 2 +  self.diametr,  # 6
                                size_x * 3 / 4 + 3 * self.diametr, size_y * 3 / 5 - self.diametr,  # 7
                                size_x * 6 / 7 - 3* self.diametr, size_y / 10 - 2 * self.diametr,  # 8
                                size_x / 2 - 2 * self.diametr, size_y / 10 - 2* self.diametr,  # 9
                                size_x / 2, size_y / 10 + self.diametr,  # 10
                                size_x / 2 - 3 * self.diametr, size_y / 4 + self.diametr,  # 11
                                size_x / 4 - self.diametr, size_y / 6 - 3*self.diametr,  # 12
                                size_x / 10 + self.diametr, size_y / 10 + 2*self.diametr,  # 13
                                size_x / 10 - self.diametr, size_y / 4,  # 14
                                size_x / 2 + self.diametr, size_y * 2 / 3 - int(1.5*self.diametr),  # 15
                                size_x * 7 / 8 + self.diametr, size_y * 2 / 3 + self.diametr,  # 16
                                size_x * 8 / 9, size_y * 4 / 5 + 3*self.diametr,  # 17
                                size_x, size_y,  # 18
                                size_x * 2 / 5 - 2*self.diametr, size_y * 3 / 4,  # 19
                                size_x * 2 / 3 - 2* self.diametr, size_y * 8 / 9 + self.diametr,  # 20
                                size_x / 4, size_y * 8 / 9 - self.diametr,  # 21
                                size_x / 10 - self.diametr, size_y / 2 +  self.diametr,  # 22
                                size_x / 9 + 2 * self.diametr, size_y * 2 / 3 - self.diametr,  # 23
                                size_x * 3 / 4 + self.diametr, size_y * 2 / 3 + int(1.5*self.diametr)]  # 24
            elif generator_B == 3:
                position_osn_B = [size_x / 2 + self.diametr, size_y / 2 - self.diametr,  # 1
                                size_x / 3 - self.diametr, size_y / 3 - self.diametr,  # 2
                                size_x / 2 - self.diametr, size_y / 6,  # 3
                                size_x / 5, size_y / 9,  # 4
                                size_x / 4, size_y / 2 - self.diametr,  # 5
                                size_x * 2 / 3, size_y / 2 + self.diametr,  # 6
                                size_x / 4 - self.diametr, size_y * 3 / 5,  # 7
                                size_x / 10, size_y / 4 - self.diametr,  # 8
                                size_x / 7, size_y / 12,  # 9
                                size_x / 2 + 2 * self.diametr, size_y / 10,  # 10
                                size_x / 2, size_y / 4,  # 11
                                size_x * 4 / 5, size_y / 3 + self.diametr,  # 12
                                size_x * 3 / 4 - self.diametr, size_y / 6 - self.diametr,  # 13
                                size_x * 9 / 10, size_y / 10 + self.diametr,  # 14
                                size_x * 4 / 5 + self.diametr, size_y / 2,  # 15
                                size_x / 2 - self.diametr, size_y * 2 / 3,  # 16
                                size_x / 8, size_y * 2 / 3 - self.diametr,  # 17
                                size_x / 5 - self.diametr, size_y * 7 / 8,  # 18
                                size_x * 3 / 5, size_y * 3 / 4,  # 19
                                size_x * 4 / 5, size_y * 4 / 5,  # 20
                                size_x / 3, size_y * 8 / 9,  # 21
                                size_x * 8 / 9, size_y * 9 / 10,  # 22
                                size_x * 9 / 10, size_y / 2 + self.diametr,  # 23
                                size_x * 7 / 9, size_y * 2 / 3 + self.diametr,  # 24
                                size_x / 4 + self.diametr, size_y * 2 / 3 + self.diametr]  # 25
                position_dop_B = [size_x / 3, size_y / 3 + self.diametr,  # 2
                                size_x / 2 - self.diametr, size_y / 6 + 3 * self.diametr,  # 3
                                size_x / 5 - (0.5*self.diametr), size_y / 9 + self.diametr,  # 4
                                size_x / 4 - 3 * self.diametr, size_y / 2 - 2 * self.diametr,  # 5
                                size_x * 2 / 3 - 3 * self.diametr, size_y / 2 + int(0.75*self.diametr),  # 6
                                size_x / 4 - 4 * self.diametr, size_y * 3 / 5,  # 7
                                size_x / 10 -self.diametr, size_y / 4 + 3 * self.diametr,  # 8
                                size_x / 7 + self.diametr, size_y / 12 - self.diametr,  # 9
                                size_x / 2 + 2, size_y / 10 + self.diametr,  # 10
                                size_x / 2 + 3 * self.diametr, size_y / 4 + self.diametr,  # 11
                                size_x * 4 / 5 - 2 * self.diametr, size_y / 3 + self.diametr,  # 12
                                size_x * 3 / 4, size_y / 6 - 3 * self.diametr,  # 13
                                size_x * 9 / 10+ int(0.5*self.diametr), size_y / 10 + 7 * self.diametr,  # 14
                                size_x * 4 / 5 - self.diametr, size_y / 2,  # 15
                                size_x * 4 / 5 - 2 * self.diametr, size_y * 2 / 3,  # 16
                                size_x / 8 - self.diametr, size_y * 2 / 3 + self.diametr,  # 17
                                size_x / 5 - 2*self.diametr, size_y * 7 / 8 - 2*self.diametr,  # 18
                                size_x * 3 / 5, size_y * 3 / 4 - 2* self.diametr,  # 19
                                size_x * 4 / 5 +  int(0.5*self.diametr), size_y * 4 / 5 - self.diametr,  # 20
                                size_x * 2 / 3- 2* self.diametr, size_y * 8 / 9 + self.diametr,  # 21
                                size_x * 8 / 9 - self.diametr, size_y * 9 / 10 - self.diametr,  # 22
                                size_x * 9 / 10 - self.diametr, size_y / 2 + 2*self.diametr,  # 23
                                size_x * 7 / 9 - self.diametr, size_y * 2 / 3 - self.diametr,  # 24
                                size_x / 4 + self.diametr, size_y * 2 / 3 + 3 * self.diametr]  # 25
            if generator_B != 0:
                self.mas_pos_8 = []
                for i in range(len(position_osn_B)):
                    self.mas_pos_8.append(position_osn_B[i])
                for i in range(len(position_dop_B)):
                    self.mas_pos_8.append(position_dop_B[i])
        i = 0
        self.pos_center_points = []
        while i < (int(len(self.mas_pos_8))):
            self.pos_center_points.append([])
            str_num = str(int(i / 2) + 1)
            btn = Button(
                id = str_num,
                background_color=(0,0,0,0),
                pos=(self.mas_pos_8[i], self.mas_pos_8[i + 1]),
                size_hint = (None,None),
                height = self.diametr,
                width = self.diametr
            )
            lbl = self.paint(i, btn)
            self.pos_center_points[int(i / 2)].append(btn.pos[0] + self.diametr / 2)
            self.pos_center_points[int(i / 2)].append(btn.pos[1] + self.diametr / 2)
            btn.add_widget(lbl)
            self.add_widget(btn)
            i += 2
        self.size_img = int(size_x/8)
        self.img_start = Image(source = 'image/thumbnail_start.jpg',size_hint = (None,None),
                               size = (self.size_img,self.size_img),pos = (self.mas_pos_8[0]-self.size_img, self.mas_pos_8[1]-self.diametr/2))
        if col == 8:
            self.img_finish = Image(source = 'image/thumbnail_finish.jpg',size_hint = (None,None),
                                   size = (self.size_img,self.size_img),pos = (self.mas_pos_8[-2] - self.size_img, self.mas_pos_8[-1]-self.diametr/2))
        elif col == 25 or col == 26:
            self.img_finish = Image(source='image/thumbnail_finish.jpg', size_hint=(None, None),
                                    size=(self.size_img, self.size_img),pos=(self.mas_pos_8[48] - self.size_img, self.mas_pos_8[49] - self.diametr / 2))
        self.add_widget(self.img_start)
        self.add_widget(self.img_finish)
        self.mas_register_num_button = []
        for i in range(int(len(self.mas_pos_8)/2)):
            self.mas_register_num_button.append(0)
        print(len(self.mas_pos_8))
        print(self.children)
        self.mas_child_obj = []
        for i in range(len(self.children)-1,-1,-1):
            self.mas_child_obj.append(self.children[i])
        print(self.mas_child_obj)
        if col == 26:
            self.mas_child_obj[0].on_press = self.callback_1
            self.mas_child_obj[1].on_press = self.callback_2
            self.mas_child_obj[2].on_press = self.callback_3
            self.mas_child_obj[3].on_press = self.callback_4
            self.mas_child_obj[4].on_press = self.callback_5
            self.mas_child_obj[5].on_press = self.callback_6
            self.mas_child_obj[6].on_press = self.callback_7
            self.mas_child_obj[7].on_press = self.callback_8
            self.mas_child_obj[8].on_press = self.callback_9
            self.mas_child_obj[9].on_press = self.callback_10
            self.mas_child_obj[10].on_press = self.callback_11
            self.mas_child_obj[11].on_press = self.callback_12
            self.mas_child_obj[12].on_press = self.callback_13
            self.mas_child_obj[13].on_press = self.callback_14
            self.mas_child_obj[14].on_press = self.callback_15
            self.mas_child_obj[15].on_press = self.callback_16
            self.mas_child_obj[16].on_press = self.callback_17
            self.mas_child_obj[17].on_press = self.callback_18
            self.mas_child_obj[18].on_press = self.callback_19
            self.mas_child_obj[19].on_press = self.callback_20
            self.mas_child_obj[20].on_press = self.callback_21
            self.mas_child_obj[21].on_press = self.callback_22
            self.mas_child_obj[22].on_press = self.callback_23
            self.mas_child_obj[23].on_press = self.callback_24
            self.mas_child_obj[24].on_press = self.callback_25
            for i in range(25,len(self.children)):
                #Clock.schedule_once(partial(self.callback_26, i))
                self.mas_child_obj[i].on_press = partial(self.callback_26,i)
        elif col == 25:
            self.mas_child_obj[0].on_press = self.callback_1
            self.mas_child_obj[1].on_press = self.callback_2
            self.mas_child_obj[2].on_press = self.callback_3
            self.mas_child_obj[3].on_press = self.callback_4
            self.mas_child_obj[4].on_press = self.callback_5
            self.mas_child_obj[5].on_press = self.callback_6
            self.mas_child_obj[6].on_press = self.callback_7
            self.mas_child_obj[7].on_press = self.callback_8
            self.mas_child_obj[8].on_press = self.callback_9
            self.mas_child_obj[9].on_press = self.callback_10
            self.mas_child_obj[10].on_press = self.callback_11
            self.mas_child_obj[11].on_press = self.callback_12
            self.mas_child_obj[12].on_press = self.callback_13
            self.mas_child_obj[13].on_press = self.callback_14
            self.mas_child_obj[14].on_press = self.callback_15
            self.mas_child_obj[15].on_press = self.callback_16
            self.mas_child_obj[16].on_press = self.callback_17
            self.mas_child_obj[17].on_press = self.callback_18
            self.mas_child_obj[18].on_press = self.callback_19
            self.mas_child_obj[19].on_press = self.callback_20
            self.mas_child_obj[20].on_press = self.callback_21
            self.mas_child_obj[21].on_press = self.callback_22
            self.mas_child_obj[22].on_press = self.callback_23
            self.mas_child_obj[23].on_press = self.callback_24
            self.mas_child_obj[24].on_press = self.callback_25
        elif col == 8:
            self.mas_child_obj[0].on_press = self.callback_1
            self.mas_child_obj[1].on_press = self.callback_2
            self.mas_child_obj[2].on_press = self.callback_3
            self.mas_child_obj[3].on_press = self.callback_4
            self.mas_child_obj[4].on_press = self.callback_5
            self.mas_child_obj[5].on_press = self.callback_6
            self.mas_child_obj[6].on_press = self.callback_7
            self.mas_child_obj[7].on_press = self.callback_8


        self.event = Clock.schedule_interval(lambda dt: self.help(), 10)
        self.event.cancel()

class Fourth_Screen(Screen):
    #класс экрана содержащий тренировку перед тестом А
    def __init__(self, **kwargs):
        super(Fourth_Screen, self).__init__(**kwargs)
        self.box = BoxLayout(orientation = "vertical",size_hint = (None,None), height = Window.size[1], width = Window.size[0])
        lbl = Label( text = 'Вам нужно соединить круги с числами в восходящем порядке: например, 1 – 2 – 3 – 4 и так далее. Чтобы соединить круги, нажмите сначала на один, а потом на другой. Выполняйте задание как можно быстрее – это задание на скорость. Давайте сначала потренируемся!',
                     color = (0,0,0,1),
                     size_hint= (1, None),
                     text_size = (Window.size[0],Window.size[1]/4),
                     font_size = Window.size[1]/40,
                     halign="center",
                     valign= "middle"
                     )
        self.box.add_widget(lbl)
        self.box.add_widget(Color_Trail_Test(8,Window.size[0],Window.size[1]*(3/4),'Fifth_Screen'))
        self.add_widget(self.box)

    def __del__(self):
        self.clear_widgets()

class Fifth_Screen(Screen):
    # класс экрана содержащий сам тест А
    def remove(self):
        self.remove_widget(self.box)
        global metrics, Number_test
        Number_test = 1
        self.add_widget(Color_Trail_Test(25,Window.size[0],Window.size[1],'Seventh_Screen'))
        metrics[6] = time.time()

    def back(self):
        global Language
        if Language == 1:
            scr_rus.current_Screen("Fourth_Screen")
        elif Language == 2:
            scr_en.current_Screen("Fourth_Screen")

    def __init__(self, **kwargs):
        super(Fifth_Screen, self).__init__(**kwargs)
        self.box = BoxLayout(size_hint = (.8,.3),
                             pos = (Window.size[0]*0.1,Window.size[1]*(0.35)),
                             spacing = 2)
        global Language
        if Language == 1:
            self.btn_1 = Button( id = "button",
                                 text = "Вернуться\nк тренировке",
                                 background_normal = "white",
                                 background_color = ((200/255),(200/255),(200/255),(200/255)),
                                 color = (0,0,0,1))
            self.btn_2 = Button( id = "button",
                                 text = "Начать тест А",
                                 background_normal="white",
                                 background_color=((200 / 255), (200 / 255), (200 / 255), (200 / 255)),
                                 color=(0, 0, 0, 1))
            self.box.add_widget(self.btn_1)
            self.box.add_widget((self.btn_2))
        self.btn_2.on_press = self.remove
        self.btn_1.on_press = self.back
        self.add_widget(self.box)

class Seventh_Screen(Screen):
    # класс содержащий тренировку перед тестом В
    def __init__(self, **kwargs):
        super(Seventh_Screen, self).__init__(**kwargs)
        self.box = BoxLayout(orientation="vertical", size_hint=(None, None), height=Window.size[1],
                             width=Window.size[0])
        lbl = Label(
            text='А теперь вам нужно соединить круги с числами в восходящем порядке, при этом чередуя цвета: например, 1 розовый – 2 желтый – 3 розовый – 4 желтый и так далее. Выполняйте и это задание как можно быстрее – измеряется ваша скорость. Давайте потренируемся!',
            color=(0, 0, 0, 1),
            size_hint=(1, None),
            text_size=(Window.size[0], Window.size[1] / 4),
            font_size=Window.size[1] / 40,
            halign="center",
            valign="middle"
            )
        self.box.add_widget(lbl)
        self.box.add_widget(Color_Trail_Test(8, Window.size[0], Window.size[1] * (3 / 4), 'Eighth_Screen'))
        self.add_widget(self.box)

class Eighth_Screen(Screen):
    #класс содержащий тест В
    def remove(self):
        self.remove_widget(self.box)
        global metrics, Number_test
        Number_test = 2
        self.add_widget(Color_Trail_Test(26,Window.size[0], Window.size[1], 'Ninth_Screen'))
        metrics[9] = time.time()
    def back(self):
        global Language
        if Language == 1:
            scr_rus.current_Screen("Seventh_Screen")
        elif Language == 2:
            scr_en.current_Screen("Seventh_Screen")
    def __init__(self, **kwargs):
        super(Eighth_Screen, self).__init__(**kwargs)
        self.box = BoxLayout(size_hint=(.8, .3),
                             pos=(Window.size[0] * 0.1, Window.size[1] * (0.35)),
                             spacing=2)
        global Language
        if Language == 1:
            self.btn_1 = Button(id="button",
                                text="Вернуться\nк тренировке",
                                background_normal="white",
                                background_color=((200 / 255), (200 / 255), (200 / 255), (200 / 255)),
                                color=(0, 0, 0, 1))
            self.btn_2 = Button(id="button",
                                text="Начать тест B",
                                background_normal="white",
                                background_color=((200 / 255), (200 / 255), (200 / 255), (200 / 255)),
                                color=(0, 0, 0, 1))
            self.box.add_widget(self.btn_1)
            self.box.add_widget((self.btn_2))
        self.btn_2.on_press = self.remove
        self.btn_1.on_press = self.back
        self.add_widget(self.box)

class Ninth_Screen(Screen):
    # класс экрна результатов прохождения теста
    def __init__(self, **kwargs):
        super(Ninth_Screen, self).__init__(**kwargs)
        global metrics
        #with self.canvas:
        #    Color(*BLACK)
        #    RoundedRectangle(pos=(Window.size[0] * 0.2, Window.size[1] * (0.2)), size=(self.box.size[0], self.box.size[1]))
        #self.box = BoxLayout(orientation = "vertical")
        self.label_osn = Label(text= "[b]Ваши результаты:[/b]\n\n ",
                markup = True,
                color= (0,0,0,1),
                pos_hint= {'center_x': 0.5, 'center_y': 0.705},
                size_hint= (1.0,1.0),
                #text_size= self.size,
                halign="center",
                valign="middle")
        print(Window.size)
        buf_A = "[b]Результаты части А:[/b]\n\nОбщее вермя выполнения: "+str(metrics[-6])+" c.\n" + "Кол-во ошибок: " + str(metrics[-5]) +"\nКол-во верных: " + str(metrics[-4]) + "\n\n"
        buf_B = "[b]Результаты части B:[/b]\n\nОбщее вермя выполнения: "+str(metrics[-3])+" c.\n" + "Кол-во ошибок: " + str(metrics[-2]) +"\nКол-во верных: " + str(metrics[-1]) + "\n\n"
        self.label_1 = Label(text=buf_A + buf_B,
                               markup=True,
                               color=(0, 0, 0, 1),
                               pos_hint={'center_x': 0.5, 'center_y': 0.5},
                               size_hint=(1.0, 1.0),
                              # height=Window.size[0],
                              # width=Window.size[1],
                               #text_size=self.size,
                               halign="left",
                               valign="top")
        self.label_2 = Label(text="[b]Спасибо за участие![/b] ",
                               markup=True,
                               color=(0, 0, 0, 1),
                               pos_hint={'center_x': 0.5, 'center_y': 0.3},
                               size_hint=(1.0, 1.0),
                               # text_size= self.size,
                               halign="center",
                               valign="middle")
        #self.box.add_widget(self.label_osn)
        self.add_widget(self.label_osn)
        self.add_widget(self.label_1)
        self.add_widget(self.label_2)

class Empty_Screen(Screen):
    pass

class ScreenManagement(ScreenManager):
# класс управления экранами
    def current_Screen(self,Screen_name):
        self.current = Screen_name

class Gen_Menu_rus(App):
# класс запуска Main_rus.kv для построения приложения на русском языке
    global metrics
    def build(self):
        with open("Main_rus.kv", encoding='utf8') as f:
            Screen_Manager_rus = Builder.load_string(f.read())
        global scr_rus
        scr_rus = Builder.load_file("Empty.kv") #обнуляем каждый новый вызов конструктора
        scr_rus = Screen_Manager_rus # заполняем его новым экземпляром
        return Screen_Manager_rus

class Gen_Menu_en(App):
# класс запуска Main_en.kv для построения приложения на английском языке
# он еще не завершен ! ! ! ! ! ! ! ! ! !
    def build(self):
        Screen_Manager_en = Builder.load_file("Main_en.kv")
        global scr_en
        scr_en = Screen_Manager_en
        return Screen_Manager_en

# скрипт запуска первого окна приложения
if __name__ == '__main__':
    First_Screen().run()

