import pygame as pg, asyncio, sys, random, math
from perlin_noise import *
from asset import *
from player import *
from particle import *

class GameChunk():
    def __init__(self, sizex, sizey, globalx, globaly, seed):
        self.data = [[0 for i in range(sizex)] for j in range(sizey)]
        self.decorations = [[0 for i in range(sizex)] for j in range(sizey)]
        self.sizex = sizex
        self.sizey = sizey
        self.globalx = globalx
        self.globaly = globaly
        self.biome1 = PerlinNoise(4, seed) # biome noise
        self.pollution = PerlinNoise(4, seed * 2010 + 44) # pollution noise
        self.oceanic = PerlinNoise(4, seed * 3020 + 55) # oceanic noise
        self.particles = [0]*5
        self.ready = False
        for i in range(5):
            self.particles[i] = Particle(misclist[0], 0, 0, False)
    
    def populate_tiles(self):
        for i in range(0, self.sizex-1, 1):
            for j in range(0, self.sizey-1, 1):
                if self.biome1([i*.025, j*.025]) > -0.1 and self.biome1([i*.025, j*.025]) < 0.15:
                    self.data[i][j] = 4
                elif self.biome1([i*0.025, j*.025]) >= 0.15:
                    if self.pollution([i*.1, j*.1]) > -0.2:
                        self.data[i][j] = 0
                    else:
                        self.data[i][j] = 3
                else:
                    self.data[i][j] = 1
                if self.oceanic([i*.025, j*.025]) + .1 - math.sqrt(math.pow(self.sizex/2-i, 2)+math.pow(self.sizey/2-j, 2))/(self.sizex*3) < 0:
                    self.data[i][j] = 2
        self.ready = True

    def generate_decoration_layer(self):
        for i in range(0, self.sizex-1, 1):
            for j in range(0, self.sizey-1, 1):
                if self.oceanic([i*.025, j*.025]) + .1 - math.sqrt(math.pow(self.sizex/2-i, 2)+math.pow(self.sizey/2-j, 2))/(self.sizex*3) < 0 or self.pollution([i*.1, j*.1]) < -0.4:
                    self.decorations[i][j] = 0
                elif self.biome1([i*.025, j*.025]) > -0.1 and self.biome1([i*.025, j*.025]) < .15:
                    x = random.randint(0, 10)
                    self.decorations[i][j] = 4 if x >= 8 and x <= 10 else 2 if x == 7 else 6 if x == 6 else 0
                elif self.biome1([i*.025, j*.025]) >= .15:
                    x = random.randint(0, 10)
                    self.decorations[i][j] = 0 if self.data[i][j] == 3 else 1 if x >= 8 and x <= 10 else 2 if x == 7 else 5 if x == 6 else 0
                else:
                    x = random.randint(0, 10)
                    self.decorations[i][j] = 3 if x >= 8 and x <= 10 else 0
        self.decorations[32][32] = 0

    def draw_chunk(self, screen, player: Player):
        for i in range(self.sizex-1):
            for j in range (self.sizey-1):
                screen.blit(assetlist[self.data[i][j]], (self.globalx*64*self.sizex+i*64-player.x+320, self.globaly*64*self.sizey+j*64-player.y+320))
    
    def draw_decorators(self, screen, player: Player):
        for i in range(self.sizex-1):
            for j in range (self.sizey-1):
                if self.decorations[i][j] != 0:
                    screen.blit(dassetlist[self.decorations[i][j]].image, (self.globalx*64*self.sizex+i*64-player.x+320, self.globaly*64*self.sizey+j*64-player.y+320))

    def get_id(self, tilex, tiley):
        if self.ready:
            return self.data[tilex][tiley]
        else:
            return -1

    def restore_tile(self, tilex, tiley):
        print(f'attempting restoration at {tilex}, {tiley} with an id equal to {self.data[tilex][tiley]}')
        if self.data[tilex][tiley] == 3:
            self.data[tilex][tiley] = 0
            for i in range(5):
                self.particles[i] = Particle(misclist[0], tilex, tiley)
            return True
        else:
            return False
        
    def restore_decor(self, tilex, tiley):
        print(f'attempting restoration at {tilex}, {tiley} with an id equal to {self.data[tilex][tiley]}')
        if self.decorations[tilex][tiley] == 5:
            self.decorations[tilex][tiley] = 1
            for i in range(5):
                self.particles[i] = Particle(misclist[0], tilex, tiley)
            return True
        elif self.decorations[tilex][tiley] == 6:
            self.decorations[tilex][tiley] = 4
            for i in range(5):
                self.particles[i] = Particle(misclist[0], tilex, tiley)
            return True
        else:
            return False
