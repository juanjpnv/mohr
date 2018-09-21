import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from math import cos, sin, pi

c = 0
R = 10
x = []
y = []

a, b = [], []

theta = list(range(0, 629))
for t in theta:
    x.append(c+R*cos(t/100))
    y.append(c+R*sin(t/100))

print('x=', x)
print('y=', y)

plt.plot(x, y)
plt.ylabel('some numbers')


class MyApp(App):
    def build(self):
        box = BoxLayout()
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return box


MyApp().run()