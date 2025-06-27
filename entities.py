import pyxel
from constants import SCREEN_HEIGHT

class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        if self.y < SCREEN_HEIGHT:
            self.y += 1

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 
                  72, 0, 16, 16, pyxel.COLOR_WHITE)


class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def update(self):
        self.y -= self.dy
        self.x += self.dx

    def draw(self):
        pyxel.rect(self.x, self.y, 2, 4, pyxel.COLOR_LIGHT_BLUE)


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 6

    def update(self):
        self.timer -= 1

    def draw(self):
        if self.timer > 4:
            pyxel.circ(self.x, self.y, 4, pyxel.COLOR_ORANGE)
        elif self.timer > 2:
            pyxel.circ(self.x, self.y, 3, pyxel.COLOR_RED)
        else:
            pyxel.circ(self.x, self.y, 2, pyxel.COLOR_YELLOW)


class Heart:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        if self.y < SCREEN_HEIGHT:
            self.y += 1

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 
                  55, 0, 10, 10, pyxel.COLOR_PURPLE)
        