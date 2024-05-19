import random
from gamechunk import *
import pygame as pg

class Entity():
    def __init__(self, img, goodentity, suitabletileid, validradius, speed, chunk: GameChunk):
        self.img = img
        self.processedimg = img
        self.x = random.randint(0, chunk.sizex-1)*64
        self.y = random.randint(0, chunk.sizey-1)*64
        self.ogx = self.x
        self.ogy = self.y
        self.goodentity = goodentity
        self.suitabletileid = suitabletileid
        self.validradius = validradius
        self.speed = speed
        self.respawnable = False
        self.findspawnloc(chunk)
        '''self.dir = 0
        self.dist = 0'''
        self.dist = self.validradius
        self.dir = random.randint(0, 3)
        # print("attempting pathfind")
        self.currentlypathing = False
        self.ai = True

        self.particles = [0]*5
        for i in range(5):
            self.particles[i] = Particle(misclist[0], 0, 0, False)

    def findspawnloc(self, chunk: GameChunk):
        self.x = random.randint(0, chunk.sizex-1)*64
        self.y = random.randint(0, chunk.sizey-1)*64
        suitablex = (int)(self.x/64)
        suitabley = (int)(self.y/64)
        self.currentlypathing = False
        x = 0
        while not self.valid2(suitablex, suitabley, chunk) and x < 50:
            suitablex = random.randint(0, chunk.sizex-1)
            suitabley = random.randint(0, chunk.sizey-1)
            print("LOOKING FOR SPAWN LOC")
            print(f'the sx: {suitablex}, sy: {suitabley}, and the id is {chunk.get_id(suitablex, suitabley)}')
            x+=1
        if x < 50:
            print("spawn loc found")
            self.x = suitablex*64
            self.y = suitabley*64
            self.ogx = self.x
            self.ogy = self.y
        else:
            self.x = 99999
            self.y = 99999
            self.ai = False

    def capture(self, x: int, y: int, player: Player, chunk: GameChunk):
        drawnx = 0-player.x+320+self.x+32
        drawny = 0-player.y+320+self.y+32
        if x <= drawnx + 32 and x >= drawnx - 32 and y <= drawny + 32 and y >= drawny - 32:
            print("capt success")
            for i in range(5):
                self.particles[i] = Particle(misclist[0 if not self.goodentity else 1], (int)(self.x/64), (int)(self.y/64))
            self.findspawnloc(chunk)
            return -1 if self.goodentity else 1
        else:
            print("capture fail")
            return 0
    
    def update(self, chunk: GameChunk, delta: int):
        if self.ai:
            if random.randint(0, 40) == 36 and not self.currentlypathing:
                self.pathfind(chunk)
            if self.currentlypathing:
                #print("yea im pathing")
                self.walk(self.dist, self.dir, delta)


    def pathfind(self, chunk: GameChunk):
        if not self.currentlypathing:
            self.ogx = self.x
            self.ogy = self.y
            self.dist = random.randint(1, self.validradius)
            self.dir = random.randint(0, 3)
            x = 0
            while not self.valid(self.dir, self.dist, chunk) or x < 5:
                self.dist = random.randint(1, self.validradius)
                self.dir = random.randint(0, 3)
                x+=1
            if self.valid(self.dir, self.dist, chunk):
                self.currentlypathing = True

    def valid(self, dir: int, dist: int, chunk: GameChunk):
        try:
            if dir == 0:
                return chunk.data[(int)(self.x/64)-(self.dist)][(int)(self.y/64)] == self.suitabletileid
            if dir == 1:
                return chunk.data[(int)(self.x/64)+(self.dist)][(int)(self.y/64)] == self.suitabletileid
            if dir == 2:
                return chunk.data[(int)(self.x/64)][(int)(self.y/64)-(self.dist)] == self.suitabletileid
            if dir == 3:
                return chunk.data[(int)(self.x/64)][(int)(self.y/64)+self.dist] == self.suitabletileid
        except:
            return False
    
    def valid2(self, x: int, y: int, chunk: GameChunk):
        return chunk.get_id(x, y) == self.suitabletileid

    def walk(self, dist, dir, delta):
        dspeed = self.speed*delta
        if dir == 1 and self.x < self.ogx+dist*64:
            self.processedimg = pg.transform.rotate(self.img, 270)
            self.x+=dspeed
            if self.x >= self.ogx+dist*64:
                self.currentlypathing = False

        if dir == 0 and self.x > self.ogx-dist*64:
            self.processedimg = pg.transform.rotate(self.img, 90)
            self.x-=dspeed
            if self.x <= self.ogx-dist*64:
                self.currentlypathing = False

        if dir == 3 and self.y < self.ogy+dist*64:
            self.y+=dspeed
            self.processedimg = pg.transform.rotate(self.img, 180)
            if self.y >= self.ogy+dist*64:
                self.currentlypathing = False

        if dir == 2 and self.y > self.ogy-dist*64:
            self.y-=dspeed
            self.processedimg = pg.transform.rotate(self.img, 0)
            if self.y <= self.ogy-dist*64:
                self.currentlypathing = False

    def draw(self, screen: pg.display, player: Player):
        if self.ai:
            screen.blit(self.processedimg, (0-player.x+320+self.x, 0-player.y+320+self.y))