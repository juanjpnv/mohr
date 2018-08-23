import kivy
import math

from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

from kivy.properties import NumericProperty, ObjectProperty
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.garden.graph import Graph, MeshLinePlot

kivy.require('1.10.0')


class Principal(ScreenManager):
    pass


class TelaDoPlano(Screen):
    pass


class TelaDoPlanoDeformacao(Screen):
    pass


class TelaDoGrafico(Screen):
    pass


class InserirValores(GridLayout):
    entrada = 0  # armazena os valores do usuário em formato float
    saida = 0  # armazena os resultado dos cálculos

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Executa os processos de calculo ao pressionar o botão
    def calcular(self):
        self.pegar_valores()
        self.calcular_tensoes(*self.entrada)

    # Executa os processos de limpeza
    def limpa(self):
        self.entrada = [0, 0, 0]
        self.saida = ['-', '-', '-', '-', '-', '-', '-']
        self.ids.entrada_tensaoX.text = ''
        self.ids.entrada_tensaoY.text = ''
        self.ids.entrada_cisalhante.text = ''

    # Esta função pega os valores digitados e os transforma em valores float
    def pegar_valores(self):
        try:  # Testa se os valores são todos numeros
            xstress = float(self.ids.entrada_tensaoX.text)
            ystress = float(self.ids.entrada_tensaoY.text)
            xyshear = float(self.ids.entrada_cisalhante.text)
            self.entrada = [xstress, ystress, xyshear]
        except ValueError:  # Se houver algum valor que não seja numerico, essa mensagem de erro é retornada
            self.entrada = '0', '0', '0'

    # Recebe os valores floats e calcula
    def calcular_tensoes(self, xstress, ystress, xyshear):
        try:
            maxshear = round((((xstress - ystress)/2)**2 + xyshear**2)**0.5, 3)  # Cálculo do Cisalhamento máximo
            avs = (xstress + ystress)/2  # Cálculo da Tensão Média
            ps1 = avs + maxshear  # Cálculo da Tensão Principal 1
            ps2 = avs - maxshear  # Cálculo da Tensão Principal 2

            # Cálculo do ângulo principal 1. Evita que haja erro de divisão por zero no cálculo do arcotangente
            if (xyshear == 0) or (xstress == ystress and xstress == 0):
                angulo_ps1 = 0
            elif xstress == ystress and xstress != 0:
                angulo_ps1 = math.copysign(45.0, xyshear)
            else:
                angulo_ps1 = math.degrees(math.atan(2*xyshear/(xstress-ystress)))/2
            # Abaixo evita-se que haja um ângulo negativo
            if angulo_ps1 < 0:
                angulo_ps1 = angulo_ps1 + 180.0

            # Calculo do angulo principal 2 (evitando numeros negativos ou maiores que 180)
            if angulo_ps1 < 90:
                angulo_ps2 = angulo_ps1 + 90
            else:
                angulo_ps2 = angulo_ps1 - 90

            # Calculo angulo de cisalhamento máximo (evitando numeros negativos ou maiores que 90 graus)
            if angulo_ps1 < 45:
                angulo_s = angulo_ps1 + 45.0
            else:
                angulo_s = angulo_ps1 - 45.0

            self.saida = [round(ps1, 2), round(ps2, 2), round(maxshear, 2), round(angulo_ps1, 2),
                          round(angulo_ps2, 2), round(angulo_s, 2), round(avs, 2)]

        except TypeError or ValueError:
            self.saida = 0, 0, 0, 0, 0, 0, 0


class SaidaValores(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Busca pelos labels com 'ids' contidos em SaidaValores e muda o que esta escrito neles.
    # O novo texto do label é recebido pela função
    def imprimir_tensoes(self, ps1, ps2, maxshear, angulo_ps1, angulo_ps2, angulo_s, avs):
        self.ids.resultado_x.text = str(ps1) + ' MPa'
        self.ids.resultado_y.text = str(ps2) + ' MPa'
        self.ids.resultado_cisalhante.text = str(maxshear) + ' MPa'
        self.ids.resultado_angulo.text = str(angulo_ps1) + u'\u00B0'
        self.ids.resultado_angulo2.text = str(angulo_ps2) + u'\u00B0'
        self.ids.resultado_angulo3.text = str(angulo_s) + u'\u00B0'
        self.ids.resultado_med.text = str(avs) + ' MPa'


class Plano(Image):
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def muda_angulo(self, ang):
        angulo = ang
        Animation(center=self.center, angle=angulo).start(self)


class WidgetGrafico(Widget):
    # graficos
    propriedade_grafico = ObjectProperty(None)

    # traçados
    plot_circulo = 0            # Gráfico do circulo
    plot_linha_inicial = 0      # Linha do ponto inicial
    arco_angulo = 0             # Arco do angulo
    eixo_x = 0                  # Linha do eixo X
    eixo_y = 0                  # Linha do eixo Y

    # Propriedades do grafico
    xmin = NumericProperty(0)
    xmax = NumericProperty(0)
    ymin = NumericProperty(0)
    ymax = NumericProperty(0)
    angulo = NumericProperty(0)

    def desenha(self, maxshear, avs, xstress, ystress, xyshear, angulo_ps1):
        self.limpa_grafico()

        if maxshear == 0:
            pass
        else:
            self.angulo = angulo_ps1 * 2 * math.pi / 360  # transformação para radianos
            self.define_tamanho_grafico(maxshear, avs)
            self.desenha_eixo_cartesianos()
            self.desenha_circulo(maxshear, avs)
            self.desenha_linha(xstress, ystress, xyshear)
            self.desenha_angulo(avs, maxshear)

    def desenha_circulo(self, maxshear, avs):
        self.plot_circulo = MeshLinePlot(color=[1, 0, 0, 1])
        self.plot_circulo.points = [(avs + maxshear*math.cos(theta*.01), maxshear*math.sin(theta*.01))
                                    for theta in range(0, 1300)]  # 130 => 40*pi (para dar 2 voltas completas)
        self.propriedade_grafico.add_plot(self.plot_circulo)

    def define_tamanho_grafico(self, maxshear, avs):
        # Define os limites do quadrado dos graficos
        self.ymax = int(1.1*maxshear + 1)
        self.ymin = -self.ymax

        self.xmax = int(avs) + self.ymax
        self.xmin = int(avs) - self.ymax

    def desenha_eixo_cartesianos(self):
        # Desenho dos graficos
        self.eixo_x = MeshLinePlot(color=[0, 1, 1, 1])
        self.eixo_x.points = [(self.xmin, 0), (self.xmax, 0)]
        self.eixo_y = MeshLinePlot(color=[0, 1, 1, 1])
        self.eixo_y.points = [(0, self.ymin), (0, self.ymax)]

        # Exibindo os graficos
        self.propriedade_grafico.add_plot(self.eixo_x)
        self.propriedade_grafico.add_plot(self.eixo_y)

    def desenha_linha(self, xstress, ystress, xyshear):
        self.plot_linha_inicial = MeshLinePlot(color=[0, 1, 0, 1])
        self.plot_linha_inicial.points = [(xstress, xyshear), (ystress, -xyshear)]
        self.propriedade_grafico.add_plot(self.plot_linha_inicial)

    def desenha_angulo(self, avs, maxshear):
        self.arco_angulo = MeshLinePlot(color=[1, 1, 0, 1])
        self.arco_angulo.points = [(avs + 0.1*maxshear * math.cos(theta * .1),
                                    0.1*maxshear * math.sin(theta * .1)) for theta in range(0, int(20*self.angulo+2))]
        self.propriedade_grafico.add_plot(self.arco_angulo)

    def limpa_grafico(self):
        self.angulo = 0.0
        self.propriedade_grafico.remove_plot(self.plot_circulo)
        self.propriedade_grafico.remove_plot(self.eixo_x)
        self.propriedade_grafico.remove_plot(self.eixo_y)
        self.propriedade_grafico.remove_plot(self.plot_linha_inicial)
        self.propriedade_grafico.remove_plot(self.arco_angulo)


class Mohr(App):
    def build(self):
        return Principal()


if __name__ == '__main__':
    Mohr().run()
