# -*- coding: utf-8 -*-
import kivy
import math
from grau3 import terceiro_grau

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.lang.builder import Builder

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

kivy.require('1.10.0')

""" 
Simbolos, abreviações e siglas usadas no código
Considerando: s -> sigma, t -> tau
    sx: Tensão Normal X
    sy: Tensão Normal Y
    sz: Tensão Normal Z
    s1: Tensão Principal 1
    s2: Tensão Principal 2
    s3: Tensão Principal 3
    smed: Tensão Normal Média
    txy: Tensão Cisalhante XY
    tyx: Tensão Cisalhante YZ
    tzx: Tensão Cisalhante ZX
    tmax: Tensão Cisalhante Máxima
    t1: Tensão Cisalhante Principal 1
    t2: Tensão Cisalhante Principal 2
    t3: Tensão Cisalhante Principal 3
    r: raio
    cnt: centro
    tht: teta
    ang: angulo
"""


class Principal(ScreenManager):
    """
    Classe esqueleto para uso no arquivo GUImohr.kv
    """
    pass


class Menu(Screen):
    pass


class TelaDoPlano(Screen):  # Estado Plano de Tensão
    """
    Classe esqueleto para uso no arquivo GUImohr.kv
    """
    pass


class TelaDoPlanoDeformacao(Screen):  # Estado Plano de Deformação
    pass


# ============== Widgets ===============
class InserirValores(GridLayout):
    # Variáveis globais
    simbolos = ListProperty(['σX', 'σY', 'τ'])
    unidade = StringProperty('')
    tipo = StringProperty('')
    entrada = 0
    saida = 0
    grafico = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Esta função pega os valores digitados e os transforma em valores float
    def pegar_valores(self):
        x = float(self.ids.entra_X.text)
        y = float(self.ids.entra_Y.text)
        xy = float(self.ids.entra_cis.text)
        self.entrada = [x, y, xy]

    # Recebe os valores floats e calcula
    def calcular_tensoes(self, sx, sy, txy):
        tmax = round((((sx - sy)/2)**2 + txy**2)**0.5, 3)  # Cálculo do Cisalhamento máximo
        smed = (sx + sy)/2  # Cálculo da Tensão Média
        ps1 = smed + tmax  # Cálculo da Tensão Principal 1
        ps2 = smed - tmax  # Cálculo da Tensão Principal 2

        # Angulo principal 1. Evita divisão por zero no arco tangente
        if (txy == 0) or (sx == sy and sx == 0):
            ang_ps1 = 0
        elif sx == sy and sx != 0:
            ang_ps1 = math.copysign(45.0, txy)
        else:
            ang_ps1 = math.degrees(math.atan(2*txy/(sx-sy)))/2

        # Evita ângulo negativo
        ang_ps1 = ang_ps1 if ang_ps1 > 0 else 180 + ang_ps1
        ang_ps2 = ang_ps1 + 90 if ang_ps1 < 90 else ang_ps1 - 90
        ang_s = ang_ps1 + 45.0 if ang_ps1 < 45 else ang_ps1 - 45.0

        self.saida = [round(ps1, 2), round(ps2, 2), round(tmax, 2), round(ang_ps1, 2), round(ang_ps2, 2), round(ang_s, 2), round(smed, 2)]
        self.grafico = [round(tmax, 2), round(smed, 2), sx, sy, txy]

    def calcular_deforma(self, ex, ey, yxy):
        # Cálculo das deformações
        ymax = 2.0 * (((ex - ey) / 2.0) ** 2.0 + (yxy / 2.0) ** 2.0) ** .5
        emed = (ex + ey) / 2.0
        e1 = emed + ymax/2.0
        e2 = emed - ymax/2.0

        # Angulos principal 1. Evita divisão por zero
        if yxy == 0 and (ex-ey) == 0:
            ang_1 = 0.0
        elif (ex == ey) and (yxy != 0):
            ang_1 = 45.0
        else:
            ang_1 = ((math.atan(yxy/(ex - ey)))/2.0)*180.0/math.pi
        # Evita valor negativo pros angulos
        ang_1 = ang_1 if ang_1 > 0 else 180 + ang_1
        ang_2 = ang_1 + 90.0 if ang_1 < 90 else ang_1 - 90
        ang_gama = ang_1 + 45.0 if ang_1 < 45 else ang_1 - 45

        self.saida = [round(e1, 3), round(e2, 3), round(ymax, 3), round(ang_1, 3), round(ang_2, 3), round(ang_gama, 3), round(emed, 3)]
        self.grafico = [round(ymax/2, 2), round(emed, 2), ex, ey, yxy/2]

    # Executa os processos de calculo ao pressionar o botão
    def calcular(self):
        try:
            self.pegar_valores()
            if self.tipo == 'tensao':
                self.calcular_tensoes(*self.entrada)
            elif self.tipo == 'deform':
                self.calcular_deforma(*self.entrada)

        except ValueError or TypeError:
            self.entrada = [0, 0, 0]
            self.saida = [0, 0, 0, 0, 0, 0, 0]
            self.grafico = [0, 0, 0, 0, 0]

    # Executa os processos de limpeza
    def limpar(self):
        self.entrada = [0, 0, 0]
        self.grafico = [0, 0, 0, 0, 0]
        self.saida = [0, 0, 0, 0, 0, 0, 0]
        self.ids.entra_X.text = ''
        self.ids.entra_Y.text = ''
        self.ids.entra_cis.text = ''


class SaidaValores(GridLayout):
    pass


class Elemento(Image):
    angle = NumericProperty(0)
    tamanho = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tamanho = self.height if self.height < self.width else self.width

    def muda_angulo(self, ang):
        angulo = ang
        Animation(center=self.center, angle=angulo).start(self)


class SistemaSlide(BoxLayout):
    pass


# =============== Estado Triaxial de Tensao ====================
class TelaTensaoTri(Screen):
    pass


class InserirTensaoTri(GridLayout):
    pass


class SaidaTensaoTri(GridLayout):
    pass


# =============== MatPlotLib ===============
class WidgetGrafico(BoxLayout):
    pass


# ============ Método Principal ===============================
class Mohr(App):
    def build(self):
        Builder.load_string(open("GUImohr.kv", encoding="utf-8").read(), rulesonly=True)
        return Principal()


if __name__ == '__main__':
    Mohr().run()
