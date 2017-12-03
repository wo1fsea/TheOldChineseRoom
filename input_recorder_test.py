from pykeyboard import PyKeyboardEvent
from pymouse import PyMouseEvent
from threading import Thread

global x, y, z
x_, y_, z_ = [], [], []


class MouseListener(PyMouseEvent):
    def __init__(self):
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):
        self.output(x, y, button)

    def output(self, x, y, button):
        x_.append(x)
        y_.append(y)
        z_.append(button)


if __name__ == '__main__':
    mouselistener = MouseListener()
    mt = Thread(target=mouselistener.run)
    mt.start()
    while True:
        print(x_, y_, z_)
