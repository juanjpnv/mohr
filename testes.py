from math import cos, sin
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

'''Simbolos, siglas e abreviações:
    r: raio
    cnt: centro
    tht: theta'''


class Principal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gera_grafico(0, 0)

    def pontos_circulo(self, r, cnt_x, cnt_y=0):
        # gerar os pontos do círculo:
        x = []
        y = []
        tht_vezes_100 = list(range(0, 630))  # cria uma lista de numeros inteiros de 0 até 629 (aproximadamente 2pi*100)
        for tht in tht_vezes_100:
            tht = tht/100
            x.append(cnt_x + r*cos(tht))
            y.append(cnt_y + r*sin(tht))

        return x, y

    def gera_grafico(self, r, cnt_x, cnt_y=0):
        # tema escuro
        plt.style.use('dark_background')

        # dados de plotagem
        s, t = self.pontos_circulo(r, cnt_x, cnt_y=cnt_y)

        # variavel que armazena o grafico
        fig, grafico = plt.subplots()

        # plots
        grafico.plot(s, t)  # desenha o círculo

        # eixos, limites e grade
        grafico.grid(True, linestyle='-.')
        grafico.set(xlabel='', ylabel='', title='Círculo de Mohr', aspect='equal')

        # invertendo o eixo do grafico
        y1, y2 = plt.ylim()
        plt.ylim(y2, y1)

        self.ids.origem.clear_widgets()
        self.ids.origem.add_widget(FigureCanvasKivyAgg(plt.gcf()))


class Testes(App):

    def build(self):
        return Principal()


Testes().run()
