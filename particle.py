from asset import *
from player import *
import random

class Particle():
    def __init__(self, img, tilex, tiley, alive=True):
        self.img = img
        self.tilex = tilex
        self.tiley = tiley
        self.lifespan = 100+random.randint(0, 25) if alive else -99
        self.xoffset = random.random()*50-25
        self.yoffset = random.random()*50-25

    def draw(self, screen, player: Player):
        if self.lifespan > 0:
            screen.blit(self.img, (self.tilex*64-player.x+320+self.xoffset+16, self.tiley*64-player.y+320+self.yoffset+16))
            self.yoffset-=0.2
            self.lifespan-=1