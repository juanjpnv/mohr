# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager


class Principal(ScreenManager):
    pass


class TelaDoPlano(Screen):  # Estado Plano de Tensão
    pass


class TelaDoPlanoDeformacao(Screen):  # Estado Plano de Deformação
    pass


class TelaTensaoTri(Screen):
    pass


class Mohr(App):
    def build(self):
        return Principal()


Mohr().run()
