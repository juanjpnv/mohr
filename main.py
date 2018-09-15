import kivy
import math
from grau3 import terceiro_grau

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


# ============ Estado Plano de Tensão ============================
class TelaDoPlano(Screen):  # Estado Plano de Tensão
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


# ============ Gráfico ============================
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

    def desenha(self, raio, centro_x, xstress, ystress, xyshear, angulo_ps1):
        self.limpa_grafico()

        if raio == 0:
            pass
        else:
            self.angulo = angulo_ps1 * 2 * math.pi / 360  # transformação para radianos
            self.define_tamanho_grafico(raio, centro_x)
            self.desenha_eixo_cartesianos()
            self.desenha_circulo(raio, centro_x)
            self.desenha_linha(xstress, ystress, xyshear)
            self.desenha_angulo(centro_x, raio)

    def desenha_circulo(self, raio, centro_x):
        self.plot_circulo = MeshLinePlot(color=[1, 0, 0, 1])
        self.plot_circulo.points = [(centro_x + raio*math.cos(theta*.01), raio*math.sin(theta*.01))
                                    for theta in range(0, 1300)]  # 130 => 40*pi (para dar 2 voltas completas)
        self.propriedade_grafico.add_plot(self.plot_circulo)

    def define_tamanho_grafico(self, raio, centro_x):
        # Define os limites do quadrado dos graficos
        self.ymax = int(1.1*raio + 1)
        self.ymin = -self.ymax

        self.xmax = centro_x + self.ymax
        self.xmin = centro_x - self.ymax

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

    def desenha_angulo(self, centro_x, raio):
        self.arco_angulo = MeshLinePlot(color=[1, 1, 0, 1])
        self.arco_angulo.points = [(centro_x + 0.1*raio * math.cos(theta * .1),
                                    0.1*raio * math.sin(theta * .1)) for theta in range(0, int(20*self.angulo+2))]
        self.propriedade_grafico.add_plot(self.arco_angulo)

    def limpa_grafico(self):
        self.angulo = 0.0
        self.propriedade_grafico.remove_plot(self.plot_circulo)
        self.propriedade_grafico.remove_plot(self.eixo_x)
        self.propriedade_grafico.remove_plot(self.eixo_y)
        self.propriedade_grafico.remove_plot(self.plot_linha_inicial)
        self.propriedade_grafico.remove_plot(self.arco_angulo)


class WidgetGrafico3D(Widget):
    # graficos
    propriedade_grafico = ObjectProperty(None)

    # traçados
    plot_circulo1 = 0
    plot_circulo2 = 0
    plot_circulo3 = 0
    eixo_x = 0
    eixo_y = 0

    # Propriedades do grafico
    xmin = NumericProperty(0)
    xmax = NumericProperty(0)
    ymin = NumericProperty(0)
    ymax = NumericProperty(0)

    def desenha_circulos(self, centro1, raio1, centro2, raio2, centro3, raio3):
        # circulo1
        self.plot_circulo1 = MeshLinePlot(color=[1, 0, 0, 1])
        self.plot_circulo1.points = [(centro1 + raio1 * math.cos(theta * .01), raio1 * math.sin(theta * .01))
                                     for theta in range(0, 1300)]  # 130 => 40*pi (para dar 2 voltas completas)
        self.propriedade_grafico.add_plot(self.plot_circulo1)

        # circulo2
        self.plot_circulo2 = MeshLinePlot(color=[0, 1, 0, 1])
        self.plot_circulo2.points = [(centro2 + raio2 * math.cos(theta * .01), raio2 * math.sin(theta * .01))
                                     for theta in range(0, 1300)]  # 130 => 40*pi (para dar 2 voltas completas)
        self.propriedade_grafico.add_plot(self.plot_circulo2)

        # circulo2
        self.plot_circulo3 = MeshLinePlot(color=[0, 0, 1, 1])
        self.plot_circulo3.points = [(centro3 + raio3 * math.cos(theta * .01), raio3 * math.sin(theta * .01))
                                     for theta in range(0, 1300)]  # 130 => 40*pi (para dar 2 voltas completas)
        self.propriedade_grafico.add_plot(self.plot_circulo3)

    def define_tamanho_grafico(self, centro1, raio1):
        # Define os limites do quadrado dos graficos
        self.ymax = int(1.1*raio1 + 1)
        self.ymin = -self.ymax

        self.xmax = centro1 + self.ymax
        self.xmin = centro1 - self.ymax

    def desenha_eixos(self):
        # Desenho dos graficos
        self.eixo_x = MeshLinePlot(color=[0, 1, 1, 1])
        self.eixo_x.points = [(self.xmin, 0), (self.xmax, 0)]
        self.eixo_y = MeshLinePlot(color=[0, 1, 1, 1])
        self.eixo_y.points = [(0, self.ymin), (0, self.ymax)]

        # Exibindo os graficos
        self.propriedade_grafico.add_plot(self.eixo_x)
        self.propriedade_grafico.add_plot(self.eixo_y)

    def limpa_grafico(self):
        self.propriedade_grafico.remove_plot(self.plot_circulo1)
        self.propriedade_grafico.remove_plot(self.plot_circulo2)
        self.propriedade_grafico.remove_plot(self.plot_circulo3)
        self.propriedade_grafico.remove_plot(self.eixo_x)
        self.propriedade_grafico.remove_plot(self.eixo_y)

    def desenha(self, centro1, raio1, centro2, raio2, centro3, raio3):
        self.limpa_grafico()
        self.define_tamanho_grafico(centro1, raio1)
        self.desenha_eixos()
        self.desenha_circulos(centro1, raio1, centro2, raio2, centro3, raio3)


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
        gamaxy = float(self.ids.input_gamaxy.text)

        self.entrada = [ex, ey, gamaxy]

    def calcula_plano_deforma(self, ex, ey, yxy):
        # Cálculo das deformações
        ymax = 2.0 * (((ex - ey) / 2.0) ** 2.0 + (yxy / 2.0) ** 2.0) ** .5
        emed = (ex + ey) / 2.0
        e1 = emed + ymax/2.0
        e2 = emed - ymax/2.0

        # Cálculo dos angulos
        alpha1 = ((math.atan(yxy/(ex - ey)))/2.0)*180.0/math.pi
        alpha2 = alpha1 + 90.0
        alphagama = alpha1 + 45.0

        self.saida = [round(e1, 3), round(e2, 3), round(ymax, 3), round(emed, 3),
                      round(alpha1, 3), round(alpha2, 3), round(alphagama, 3)]

    def organiza_dados_grafico(self):
        self.grafico = [self.saida[2] / 2, self.saida[3], self.entrada[0], self.entrada[1],
                        self.entrada[2] / 2, self.saida[4]]

    def calcular(self):
        self.pega_valor()
        self.calcula_plano_deforma(*self.entrada)
        self.organiza_dados_grafico()

    def limpar(self):
        self.ids.input_ex.text = ''
        self.ids.input_ey.text = ''
        self.ids.input_gamaxy.text = ''


class SaidaPlanoDeformacao(GridLayout):
    def valores(self, valores):
        self.ids.label_result_e1.text = str(valores[0])
        self.ids.label_result_e2.text = str(valores[1])
        self.ids.label_result_gamamax.text = str(valores[2])
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

    def pega_valor(self):
        try:
            sx = float(self.ids.entrada_tensaoX.text)
            sy = float(self.ids.entrada_tensaoY.text)
            sz = float(self.ids.entrada_tensaoZ.text)
            txy = float(self.ids.entrada_cisXY.text)
            tyz = float(self.ids.entrada_cisYZ.text)
            tzx = float(self.ids.entrada_cisXZ.text)
            self.entrada = [sx, sy, sz, txy, tyz, tzx]
        except ValueError:
            self.entrada = ['error', 'error', 'error', 'error', 'error', 'error']

    def calcular_principal(self, sx, sy, sz, txy, tyz, tzx):
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

    def organiza_dados_graficos(self, s1, s2, s3, t13, t12, t23):
        centro1 = round((s1 + s3) / 2, 3)
        raio1 = round(t13, 3)
        centro2 = round((s1 + s2) / 2, 3)
        raio2 = round(t12, 3)
        centro3 = round((s2 + s3) / 2)
        raio3 = round(t23, 3)
        self.grafico = [centro1, raio1, centro2, raio2, centro3, raio3]

    def calcular(self):
        self.pega_valor()
        if 'error' in self.entrada:
            self.saida = self.entrada
        else:
            self.calcular_principal(*self.entrada)
            self.organiza_dados_graficos(*self.saida)

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


# ============ Método Principal ===============================
class Mohr(App):
    def build(self):
        return Principal()


if __name__ == '__main__':
    Mohr().run()
