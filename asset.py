import pygame as pg, asyncio, sys, random, math

assetlist = [0]*10
assetlist[0] = pg.transform.scale(pg.image.load("assets/tiles/grass.png"), (64, 64))
assetlist[1] = pg.transform.scale(pg.image.load("assets/tiles/sand.png"), (64, 64))
assetlist[2] = pg.transform.scale(pg.image.load("assets/tiles/water.png"), (64, 64))
assetlist[3] = pg.transform.scale(pg.image.load("assets/tiles/dirt.png"), (64, 64))
assetlist[4] = pg.transform.scale(pg.image.load("assets/tiles/tropicalgrass.png"), (64, 64))

misclist = [0]*10
misclist[0] = pg.transform.scale(pg.image.load("assets/misc/particle.png"), (32, 32))
misclist[1] = pg.transform.scale(pg.image.load("assets/misc/particle2.png"), (32, 32))

class Decoration():
    def __init__(self, image, passable):
        self.image = image
        self.passable = passable

dassetlist = [0]*10
dassetlist[1] = Decoration(pg.transform.scale(pg.image.load("assets/decoration/tree.png"), (64, 64)), True)
dassetlist[2] = Decoration(pg.transform.scale(pg.image.load("assets/decoration/rock.png"), (64, 64)), False)
dassetlist[3] = Decoration(pg.transform.scale(pg.image.load("assets/decoration/cactus.png"), (64, 64)), True)
dassetlist[4] = Decoration(pg.transform.scale(pg.image.load("assets/decoration/tropicaltree.png"), (64, 64)), True)
dassetlist[5] = Decoration(pg.transform.scale(pg.image.load("assets/decoration/cuttree.png"), (64, 64)), True)
dassetlist[6] = Decoration(pg.transform.scale(pg.image.load("assets/decoration/cuttropicaltree.png"), (64, 64)), True)

entitylist = [0]*10
entitylist[0] = pg.transform.scale(pg.image.load("assets/entity/toad.png"), (64, 64))
entitylist[1] = pg.transform.scale(pg.image.load("assets/entity/fennec.png"), (64, 64))
entitylist[2] = pg.transform.scale(pg.image.load("assets/entity/player.png"), (64, 64))