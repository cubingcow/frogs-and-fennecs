import pygame as pg, asyncio, sys, random, math
from asset import *

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, color, speed):
        super().__init__()
        self.image = entitylist[2]
        self.processedimg = self.image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.x = x
        self.y = y

    def update(self, chunk, delta):
        keys = pg.key.get_pressed()
        dspeed = self.speed*delta
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            if (self.valid_pos(chunk, self.x-dspeed, self.y)):
                self.processedimg = pg.transform.rotate(self.image, 90)
                self.x -= dspeed/2 if self.is_slowed(chunk, self.x-dspeed, self.y) else dspeed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            if (self.valid_pos(chunk, self.x+dspeed, self.y)):
                self.processedimg = pg.transform.rotate(self.image, 270)
                self.x += dspeed/2 if self.is_slowed(chunk, self.x+dspeed, self.y) else dspeed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.processedimg = pg.transform.rotate(self.image, 0)
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.processedimg = pg.transform.rotate(self.image, 325)
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.processedimg = pg.transform.rotate(self.image, 45)
            if (self.valid_pos(chunk, self.x, self.y-dspeed)):
                self.y -= dspeed/2 if self.is_slowed(chunk, self.x, self.y-dspeed) else dspeed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.processedimg = pg.transform.rotate(self.image, 180)
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.processedimg = pg.transform.rotate(self.image, 225)
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.processedimg = pg.transform.rotate(self.image, 135)
            if (self.valid_pos(chunk, self.x, self.y+dspeed)):
                self.y += dspeed/2 if self.is_slowed(chunk, self.x, self.y+dspeed) else dspeed

    def valid_pos(self, chunk, x, y):
        tilex = (int)(x/64)
        tiley = (int)(y/64)
        #print(f'tilex : {tilex}, tiley : {tiley}')
        if x < 0 or y < 0 or tilex > chunk.sizex-1 or tiley > chunk.sizey-1:
            return False
        try:
            if chunk.decorations[tilex][tiley] == 0:
                return True
            return dassetlist[chunk.decorations[tilex][tiley]].passable
        except:
            return False
        
    def is_slowed(self, chunk, x, y):
        tilex = (int)(x/64)
        tiley = (int)(y/64)
        #print(f'tilex : {tilex}, tiley : {tiley}')
        try:
            if chunk.data[tilex][tiley] == 2:
                return True
            else:
                return False
        except:
            return False

    def draw(self, screen):
        screen.blit(self.processedimg, (320-self.image.get_width()/2, 320-self.image.get_height()/2))