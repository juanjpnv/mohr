# -*- coding: utf-8 -*-
import kivy
import math
from grau3 import terceiro_grau

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.uix.image import Image

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

kivy.require('1.10.0')

""" 
Simbolos, abreviações e siglas usadas no código
Considerando: s -> sigma, t -> tau
    sx: Stress X
    sy: Stress Y
    sz: Stress Z
    s1: Principal Stress 1
    s2: Principal Stress 2
    s3: Principal Stress 3
    smed: Medium Stress
    txy: Shear XY
    tyx: Shear YZ
    tzx: Shear ZX
    tmax: Maximum Shear
    t1: Principal Shear 1
    t2: Principal Shear 2
    t3: Principal Shear 3
    r: radius
    cnt: center
    tht: theta
    ang: angle
"""


class Principal(ScreenManager):
    """
    Classe esqueleto para uso no arquivo mohr.kv
    """
    pass


# ============ Estado Plano de Tensão ============================
class TelaDoPlano(Screen):  # Estado Plano de Tensão
    """
    Classe esqueleto para uso no arquivo mohr.kv
    """
    pass


class InserirValores(GridLayout):
    """
    Classe esqueleto para uso no arquivo mohr.kv
    Possui as funções necessárias para receber os dados do usuário e calcular os valores do Estado Plano de Tensão
    """
    def __init__(self, **kwargs):
        """
        Inicia as variaveis entrada e saida que serão usadas para armazer os dados de entrada do usuário e o
        resultado dos cálculos
        """
        super().__init__(**kwargs)
        self.entrada = 0  # armazena os valores do usuário em formato float
        self.saida = 0  # armazena os resultado dos cálculos
        self.grafico = []

    # Esta função pega os valores digitados e os transforma em valores float
    def pegar_valores(self):
        """
        Recebe o valor dos usuários através de TextInput e guarda o valor nas variáveis adequadas;
        A função testa se todos os valores são numéricos, caso não sejam, uma exceção é levantada.
        """
        try:  # Testa se os valores são todos números
            sx = float(self.ids.entrada_tensaoX.text)
            sy = float(self.ids.entrada_tensaoY.text)
            txy = float(self.ids.entrada_cisalhante.text)
            self.entrada = [sx, sy, txy]
        except ValueError:  # Se houver algum valor que não seja numerico, essa mensagem de erro é retornada
            self.entrada = ['0', '0', '0']
            self.grafico = [0, 0, 0, 0, 0]

    # Recebe os valores floats e calcula
    def calcular_tensoes(self, sx, sy, txy):
        try:
            tmax = round((((sx - sy)/2)**2 + txy**2)**0.5, 3)  # Cálculo do Cisalhamento máximo
            smed = (sx + sy)/2  # Cálculo da Tensão Média
            ps1 = smed + tmax  # Cálculo da Tensão Principal 1
            ps2 = smed - tmax  # Cálculo da Tensão Principal 2

            # Cálculo do ângulo principal 1. Evita que haja erro de divisão por zero no cálculo do arcotangente
            if (txy == 0) or (sx == sy and sx == 0):
                ang_ps1 = 0
            elif sx == sy and sx != 0:
                ang_ps1 = math.copysign(45.0, txy)
            else:
                ang_ps1 = math.degrees(math.atan(2*txy/(sx-sy)))/2

            # Abaixo evita-se que haja um ângulo negativo
            if ang_ps1 < 0:
                ang_ps1 = ang_ps1 + 180.0

            # Calculo do angulo principal 2 (evitando numeros negativos ou maiores que 180)
            ang_ps2 = ang_ps1 + 90 if ang_ps1 < 90 else ang_ps1 - 90

            # Calculo angulo de cisalhamento máximo (evitando numeros negativos ou maiores que 90 graus)
            ang_s = ang_ps1 + 45.0 if ang_ps1 < 45 else ang_ps1 - 45.0

            self.saida = [round(ps1, 2), round(ps2, 2), round(tmax, 2), round(ang_ps1, 2),
                          round(ang_ps2, 2), round(ang_s, 2), round(smed, 2)]

            self.grafico = [round(tmax, 2), round(smed, 2), sx, sy, txy]

        except TypeError or ValueError:
            self.saida = 0, 0, 0, 0, 0, 0, 0
            self.grafico = [0, 0, 0, 0, 0]

    # Executa os processos de calculo ao pressionar o botão
    def calcular(self):
        self.pegar_valores()
        sx, sy, txy = self.entrada
        self.calcular_tensoes(sx, sy, txy)

    # Executa os processos de limpeza
    def limpa(self):
        self.entrada = [0, 0, 0]
        self.grafico = [0, 0, 0, 0, 0]
        self.saida = [0, 0, 0, 0, 0, 0, 0]
        self.ids.entrada_tensaoX.text = ''
        self.ids.entrada_tensaoY.text = ''
        self.ids.entrada_cisalhante.text = ''


class SaidaValores(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Busca pelos labels com 'ids' contidos em SaidaValores e muda o que esta escrito neles.
    # O novo texto do label é recebido pela função
    def imprimir_tensoes(self, ps1, ps2, tmax, ang_ps1, ang_ps2, ang_s, smed):
        self.ids.resultado_x.text = str(ps1) + ' MPa'
        self.ids.resultado_y.text = str(ps2) + ' MPa'
        self.ids.resultado_cisalhante.text = str(tmax) + ' MPa'
        self.ids.resultado_angulo.text = str(ang_ps1) + '°'
        self.ids.resultado_angulo2.text = str(ang_ps2) + '°'
        self.ids.resultado_angulo3.text = str(ang_s) + '°'
        self.ids.resultado_med.text = str(smed) + ' MPa'


# =========== Estado Plano de Deformação =====================
class TelaDoPlanoDeformacao(Screen):  # Estado Plano de Deformação
    pass


class EntradaPlanoDeformacao(GridLayout):
    entrada = []
    saida = []
    grafico = []

    def pega_valor(self):
        ex = float(self.ids.input_ex.text)
        ey = float(self.ids.input_ey.text)
        yxy = float(self.ids.input_gamaxy.text)

        self.entrada = [ex, ey, yxy]

    def calcula_plano_deforma(self, ex, ey, yxy):
        # Cálculo das deformações
        ymax = 2.0 * (((ex - ey) / 2.0) ** 2.0 + (yxy / 2.0) ** 2.0) ** .5
        emed = (ex + ey) / 2.0
        e1 = emed + ymax/2.0
        e2 = emed - ymax/2.0

        # Cálculo do angulos principal 1. Evita que haja erro de divisão por zero no cálculo do arcotangente
        if yxy == 0 and (ex-ey) == 0:
            alpha1 = 0.0
        elif (ex == ey) and (yxy != 0):
            alpha1 = 45.0
        else:
            alpha1 = ((math.atan(yxy/(ex - ey)))/2.0)*180.0/math.pi
        # Evita valor negativo pros angulos
        alpha1 = alpha1 if alpha1 > 0 else 180 + alpha1
        alpha2 = alpha1 + 90.0 if alpha1 < 90 else alpha1 - 90
        alphagama = alpha1 + 45.0 if alpha1 < 45 else alpha1 - 45

        self.saida = [round(e1, 3), round(e2, 3), round(ymax, 3), round(emed, 3),
                      round(alpha1, 3), round(alpha2, 3), round(alphagama, 3)]

    def organiza_dados_grafico(self):
        self.grafico = [self.saida[2] / 2, self.saida[3], self.entrada[0], self.entrada[1],
                        self.entrada[2] / 2]

    def calcular(self):
        try:
            self.pega_valor()
            self.calcula_plano_deforma(*self.entrada)
            self.organiza_dados_grafico()
        except ValueError or TypeError:
            self.entrada = [0, 0, 0]
            self.saida = [0, 0, 0, 0, 0, 0, 0]
            self.grafico = [0, 0, 0, 0, 0]

    def limpar(self):
        self.ids.input_ex.text = ''
        self.ids.input_ey.text = ''
        self.ids.input_gamaxy.text = ''


class SaidaPlanoDeformacao(GridLayout):
    def valores(self, valores):
        self.ids.label_result_e1.text = str(valores[0])
        self.ids.label_result_e2.text = str(valores[1])
        self.ids.label_result_gamamax.text = str(valores[2])
        self.ids.label_result_emed.text = str(valores[3])
        self.ids.label_result_alpha1.text = str(valores[4])
        self.ids.label_result_alpha2.text = str(valores[5])
        self.ids.label_result_alphagama.text = str(valores[6])


# =============== Estado Triaxial de Tensao ====================
class TelaTensaoTri(Screen):
    pass


class InserirTensaoTri(GridLayout):
    saida = []
    entrada = []
    grafico = []

    def pega_valor(self):  # pega os valores digitados e os converte para float
        try:  # pega e testa todos os valores
            sx = float(self.ids.entrada_tensaoX.text)
            sy = float(self.ids.entrada_tensaoY.text)
            sz = float(self.ids.entrada_tensaoZ.text)
            txy = float(self.ids.entrada_cisXY.text)
            tyz = float(self.ids.entrada_cisYZ.text)
            tzx = float(self.ids.entrada_cisXZ.text)
            self.entrada = [sx, sy, sz, txy, tyz, tzx]
        except ValueError:  # Caso o usuário tenha digitado algum valor não numérico, é retornado a mensagem de erro.
            self.entrada = ['error', 'error', 'error', 'error', 'error', 'error']

    def calcular_principal(self, sx, sy, sz, txy, tyz, tzx):  # Calcula as tensões principais
        """ Considerando: s -> sigma. t -> tau
        Esta função recebe:
        sx: Stress X - sy: Stress Y - sz: Stress Z
        txy: Shear XY - tyx: Shear YZ - tzx: Shear ZX"""
        # Coeficientes da equação de terceiro grau
        a3 = 1
        a2 = -(sx + sy + sz)
        a1 = sx * sy + sx * sz + sy * sz - txy ** 2 - tyz ** 2 - tzx ** 2
        a0 = -(sx * sy * sz + 2 * txy * tyz * tzx - (tyz ** 2) * sx - (tzx ** 2) * sy - (txy ** 2) * sz)
        # Aplica a resolução da equação e retorna o resultado em ordem crescente:
        s3, s2, s1 = sorted(terceiro_grau(a3, a2, a1, a0))
        # Calcula-se os valores dos cisalhamentos maximos
        t13, t12, t23 = round((s1 - s3)/2, 3), round((s1 - s2)/2, 3), round((s2 - s3)/2, 3)
        # Armazena em forma de lista.
        self.saida = [s1, s2, s3, t13, t12, t23]

    def organiza_dados_graficos(self, s1, s2, s3, t13, t12, t23):  # Gera a lista de dados usados pra desenhar o gráfico
        # Calcula e arredonda os valores a serem usados.
        cnt1 = round((s1 + s3) / 2, 3)
        r1 = round(t13, 3)
        cnt2 = round((s1 + s2) / 2, 3)
        r2 = round(t12, 3)
        cnt3 = round((s2 + s3) / 2)
        r3 = round(t23, 3)
        # Organiza uma lista "grafico" com os valores que serão usados para desenhar o gráfico.
        self.grafico = [r1, cnt1, r2, cnt2, r3, cnt3]

    def calcular(self):  # Chama todas as funções anteriores.
        self.pega_valor()  # pega os valores digitados pelo usuário e confere se todos são numéricos.
        if 'error' in self.entrada:  # entra aqui caso não sejam todos os valores numéricos
            self.saida = self.entrada  # imprime a mensagem de erro
            self.grafico = [0, 0, 0, 0, 0, 0]  # envia valores nulos para que não seja desenhado nenhum gráfico
        else:  # entra aqui caso não haja nenhum erro com a entrada de dados.
            self.calcular_principal(*self.entrada)  # calcula as tensões principais
            self.organiza_dados_graficos(*self.saida)  # Gera a lista de dados usados pra desenhar o gráfico

    def limpar(self):
        self.ids.entrada_tensaoX.text = '\u03C3x'
        self.ids.entrada_tensaoY.text = '\u03C3y'
        self.ids.entrada_tensaoZ.text = '\u03C3z'
        self.ids.entrada_cisXY.text = '\u03C4xy'
        self.ids.entrada_cisYZ.text = '\u03C4yz'
        self.ids.entrada_cisXZ.text = '\u03C4xz'


class SaidaTensaoTri(GridLayout):
    def imprime_principais(self, s1, s2, s3, t13, t12, t23):
        self.ids.label_result_s1.text = '\u03C31 = '+str(s1)
        self.ids.label_result_s2.text = '\u03C32 = '+str(s2)
        self.ids.label_result_s3.text = '\u03C33 = '+str(s3)
        self.ids.label_result_t13.text = '\u03C413 = '+str(t13)
        self.ids.label_result_t12.text = '\u03C412 = '+str(t12)
        self.ids.label_result_t23.text = '\u03C423 = '+str(t23)


# ============== Widgets ===============
class Plano(Image):
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def muda_angulo(self, ang):
        angulo = ang
        Animation(center=self.center, angle=angulo).start(self)


# =============== MatPlotLib ===============
class WidgetGrafico(BoxLayout):
    """
    Simbolos, siglas e abreviações:
        r: raio
        cnt: centro
        tht: theta
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def pontos_circulo(r, cnt):
        # gerar os pontos do círculo:
        x = []
        y = []
        tht_vezes_100 = list(range(0, 630))  # cria uma lista de numeros inteiros de 0 até 629 (aproximadamente 2pi*100)
        for tht in tht_vezes_100:  # Gera duas listas com os valores para X e Y
            tht = tht/100
            x.append(cnt + r*math.cos(tht))
            y.append(r*math.sin(tht))
        return x, y

    def grafico_2d(self, r, cnt, sx, sy, txy):
        plt.style.use('dark_background')  # tema escuro

        x, y = self.pontos_circulo(r, cnt)  # dados de plotagem do circulo

        fig, grafico = plt.subplots()  # variavel que armazena o grafico

        grafico.plot(x, y)  # plot do círculo
        grafico.plot([sx, sy], [txy, -txy])

        grafico.grid(True, linestyle='--')  # grade
        grafico.set(xlabel='Tensão Normal', ylabel='Cisalhamento', title='Círculo de Mohr', aspect='equal')  # ajustes

        ylim1, ylim2 = plt.ylim()  # invertendo o eixo do grafico
        plt.ylim(ylim2, ylim1)  # invertendo o eixo do grafico

        self.clear_widgets()
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def grafico_3d(self, r1, cnt1, r2, cnt2, r3, cnt3):
        plt.style.use('dark_background')  # tema escuro

        x1, y1 = self.pontos_circulo(r1, cnt1)  # dados de plotagem do circulo
        x2, y2 = self.pontos_circulo(r2, cnt2)  # dados de plotagem do circulo
        x3, y3 = self.pontos_circulo(r3, cnt3)  # dados de plotagem do circulo

        fig, grafico = plt.subplots()  # variavel que armazena o grafico

        grafico.plot(x1, y1)  # plot do círculo 1
        grafico.plot(x2, y2)  # plot do círculo 2
        grafico.plot(x3, y3)  # plot do círculo 3

        grafico.grid(True, linestyle='--')  # grade
        grafico.set(xlabel='Tensão Normal', ylabel='Cisalhamento', title='Círculo de Mohr', aspect='equal')  # ajustes

        ylim1, ylim2 = plt.ylim()  # invertendo o eixo do grafico
        plt.ylim(ylim2, ylim1)  # invertendo o eixo do grafico

        self.clear_widgets()
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))


# ============ Método Principal ===============================
class Mohr(App):
    def build(self):
        return Principal()


if __name__ == '__main__':
    Mohr().run()
