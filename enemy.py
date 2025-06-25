import pyxel
import math
from constants import SCREEN_HEIGHT

class Enemy:
    def __init__(self, x, y, enemy_type = "normal"):
        self.x = x
        self.y = y
        self.type = enemy_type

    def update(self):
        if self.y < SCREEN_HEIGHT:
            if self.type == "normal":
                self.y += 2
            elif self.type == "fast":
                self.y += 4
            elif self.type == "zig":
                self.y += 2
                self.x += math.sin(self.y / 10) * 2

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 
                  88, 0, 16, 15, pyxel.COLOR_WHITE)