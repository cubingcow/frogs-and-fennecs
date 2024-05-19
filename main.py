import pygame as pg, asyncio, sys, random, math, time
from gamechunk import GameChunk
from asset import *
from player import *
from entity import *

pg.init()
screen = pg.display.set_mode((640, 640))

def renderStandardText(font: pg.font.Font, txt: str, locationx, locationy):
    text = font.render(txt, True, (0, 0, 0))
    screen.blit(text, (locationx+2, locationy+2))
    text = font.render(txt, True, (255, 255, 255))
    screen.blit(text, (locationx, locationy))

def getwidth(font: pg.font.Font, txt: str):
    return font.render(txt, True, (0, 0, 0)).get_width()

async def main():
    seed = random.randint(-999999, 999999)
    font = pg.font.Font("assets/font/rainyhearts.ttf", 36)
    player = Player(32+32*64, 32+32*64, 30, 30, (0, 0, 0), 1)
    chunk = GameChunk(64, 64, 0, 0, seed)
    frogs = [0]*30
    fennecs = [0]*15
    chunk.populate_tiles()
    chunk.generate_decoration_layer()
    points = 0
    hasstarted = False
    highscore = 0
    for i in range(30):
        frogs[i] = Entity(entitylist[0], False, 4, 5, 1, chunk)
    for i in range(15):
        fennecs[i] = Entity(entitylist[1], True, 1, 5, 2, chunk)

    last_time = time.time()

    while True:
        start = time.time()
        screen.fill((77, 109, 243))
        if not hasstarted:
            start = time.time()
            end = time.time()+30
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                hasstarted = True
                if (int)(end-start) > 0:
                    posX, posY = pg.mouse.get_pos()
                    if chunk.restore_tile((int)((player.x+posX-320)/64), (int)((player.y+posY-320)/64)):
                        points+=1
                    if chunk.restore_decor((int)((player.x+posX-320)/64), (int)((player.y+posY-320)/64)):
                        points+=1 
                    for frog in frogs:
                        points += frog.capture((int)(posX), (int)(posY), player, chunk)
                    for fennec in fennecs:
                        points += fennec.capture((int)(posX), (int)(posY), player, chunk)
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and not hasstarted:
                hasstarted = True
            if event.type == pg.KEYDOWN and event.key == pg.K_p and (int)(end-start) <= 0:
                seed = random.randint(-999999, 999999)
                player = Player(32+32*64, 32+32*64, 30, 30, (0, 0, 0), 1)
                chunk = GameChunk(64, 64, 0, 0, seed)
                frogs = [0]*30
                fennecs = [0]*15
                chunk.populate_tiles()
                chunk.generate_decoration_layer()
                points = 0
                hasstarted = False
                for i in range(30):
                    frogs[i] = Entity(entitylist[0], False, 4, 5, 1, chunk)
                for i in range(15):
                    fennecs[i] = Entity(entitylist[1], True, 1, 5, 2, chunk)

        # Calculate delta time
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        dt*=75
        
        chunk.draw_chunk(screen, player)
        for i in range(30):
            frogs[i].update(chunk, dt)
            frogs[i].draw(screen, player)
        for i in range(15):
            fennecs[i].update(chunk, dt)
            fennecs[i].draw(screen, player)
        
        if ((int)(end-start) > 0):
            player.update(chunk, dt)

        player.draw(screen)
        chunk.draw_decorators(screen, player)
        for p in chunk.particles:
            p.draw(screen, player)
        for f in frogs:
            for p in f.particles:
                p.draw(screen, player)
        for e in fennecs:
            for p in e.particles:
                p.draw(screen, player)

        renderStandardText(font, f"Points: {points}", 10, 10)
        renderStandardText(font, f"Time left: {(int)(end-start) if (end-start)>= 0 else 0}", 10, 50)
        renderStandardText(font, f"High score: {highscore}", 10, 90)

        if ((int)(end-start) <= 0):
            if highscore < points:
                highscore = points
            renderStandardText(font, f"Time's up! Your score: {points}", 320 - getwidth(font, f"Time's up! Your score: {points}")//2, 300)
            renderStandardText(font, f"Press P to play again", 320 - getwidth(font, f"Press P to play again")//2, 340)

        #text = font.render("Welcome to My Game", True, (255, 255, 255))
        
        #screen.blit(text, (640 // 2 - text.get_width() // 2, 10))

        pg.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())
