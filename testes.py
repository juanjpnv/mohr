import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.properties import NumericProperty
from kivy.animation import Animation

kivy.require('1.9.1')


class Principal(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SistemaSlide(BoxLayout):
    valor = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Plano(Image):
    angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def muda_angulo(self, ang):
        angulo = ang
        Animation(center=self.center, angle=angulo).start(self)


class Testes(App):
    def build(self):
        return Principal()


Testes().run()
