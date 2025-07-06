import pyxel
import math
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

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
    
class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 50
        self.bullets = []
        self.shoot_interval = 10
        self.shoot_timer = 0

    def update(self):
        self.y += 0.1

        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0

            for _ in range (5):
                bullet_x = pyxel.rndi(0, SCREEN_WIDTH - 1)
                self.bullets.append(BossBullet(bullet_x, self.y + 32))

            for bullet in self.bullets:
                bullet.update()

            if bullet.y >= SCREEN_HEIGHT:
                self.bullets.remove(bullet)

class BossBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        self.y += 2

    def draw(self):
        pyxel.rect(self.x, self.y, 1, 2, 
                   pyxel.COLOR_RED)