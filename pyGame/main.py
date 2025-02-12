
import pygame

from settings import *
from fonts import *
from sprites import *

pygame.init()
pygame.display.set_caption(TITLE)

class WINDOW:
    def __init__(self):
        self.SCR = pygame.display.set_mode(RESOLUTION)

        STG['MAP'][1] = ["WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
                         "W                              W",
                         "W                     W        W",
                         "W                              W",
                         "W      W                       W",
                         "W                              W",
                         "W                              W",
                         "W                              W",
                         "W         WW                   W",
                         "W       WW             W       W",
                         "W         WW          W        W",
                         "W        W                     W",
                         "W            W                 W",
                         "W                              W",
                         "W                              W",
                         "W                              W",
                         "W                              W",
                         "W                              W",
                         "W                  WWWW        W",
                         "W                          W   W",
                         "W         WWWW             W   W",
                         "W                              W",
                         "W                              W",
                         "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"]

        self.MAP_SFC = MAP() # Scrolling (MAP) (S)ur(F)a(C)e
        
        self.FPS = pygame.time.Clock()
        self.SEC = 0
        
        self.TILE = 64
        self.CUR = 1
        self.RUNNING = True

        self.RECTLANGE_COUNT = 0
        self.PLAYER_COUNT = 0
        self.FLOOR_COUNT = 0
        self.WALL_COUNT = 0
        self.ENEMY_COUNT = 0

        self.SPG_PLAYERS = pygame.sprite.Group()
        self.SPG_FLOORS = pygame.sprite.Group()
        self.SPG_WALLS = pygame.sprite.Group()
        self.SPG_ENEMIES = pygame.sprite.Group()
        self.SPG_RECTLANGES = pygame.sprite.Group()

        self.UPDATE_PLAYERS()
        self.UPDATE_ENEMIES()
        self.UPDATE_MAP()
        self.UPDATE_RECTLANGES()

        self.MAP_SFC.MAP = pygame.transform.scale(self.MAP_SFC.MAP, (self.TILE*len(STG['MAP'][1][0]), self.TILE*len(STG['MAP'][1])))

        self.WINDOW_BORDER = pygame.Rect(0, 0, WIDTH, HEIGHT)

        self.RUN()

    def RUN(self):
        self.WHILE()

    def WHILE(self):
        while self.RUNNING:
            self.FPS.tick(60)

            self.EVENTS()
            self.UPDATE()

    def EVENTS(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.STOP()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.STOP()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.SPG_WALLS = pygame.sprite.Group()
                    self.WALL_COUNT = 0
                    self.CUR += 1
                    self.UPDATE_MAP()

        try:
            for a in range(1, self.PLAYER_COUNT+1):
                self.PLAYER_1.MOVE(self.MAP_SFC, self.SPG_WALLS)
            for a in range(1, self.RECTLANGE_COUNT+1):
                self.RECTLANGE_1.MOVE(self.SPG_WALLS)
            self.ENEMY_1.MOVE(self.SPG_WALLS, self.SPG_RECTLANGES)
            self.ENEMY_2.MOVE(self.SPG_WALLS, self.SPG_RECTLANGES)
            self.ENEMY_3.MOVE(self.SPG_WALLS, self.SPG_RECTLANGES, self.SPG_PLAYERS)
            self.ENEMY_4.MOVE(self.SPG_WALLS, self.SPG_RECTLANGES, self.SPG_PLAYERS)
            self.ENEMY_5.MOVE(self.SPG_WALLS, self.SPG_RECTLANGES)
            self.ENEMY_6.MOVE(self.SPG_WALLS, self.SPG_RECTLANGES)
        except Exception as ex:
            pass#print(ex)

    def UPDATE(self):
        self.SCR.fill(BLACK)
        self.MAP_SFC.MAP.fill(LT_GREEN)
        
        self.SPG_FLOORS.draw(self.MAP_SFC.MAP)
        self.SPG_WALLS.draw(self.MAP_SFC.MAP)
        self.SPG_ENEMIES.draw(self.MAP_SFC.MAP)
        self.SPG_PLAYERS.draw(self.MAP_SFC.MAP)
        self.SPG_RECTLANGES.draw(self.MAP_SFC.MAP)
        
        self.SCR.blit(self.MAP_SFC.MAP, (self.MAP_SFC.x, self.MAP_SFC.y))

        pygame.draw.rect(self.SCR, BLACK, self.WINDOW_BORDER, 16)
 
        pygame.display.update()

    def STOP(self):
        self.RUNNING = False
        pygame.quit()

    def UPDATE_PLAYERS(self):
        self.PLAYER_1 = PLAYER(self, WIDTH/2, HEIGHT/2,
                               self.TILE//2, self.TILE//2,
                               4)

        for a in range(1, self.PLAYER_COUNT+1):
            P = getattr(self, "PLAYER_"+str(a))
            self.SPG_PLAYERS.add(P)

    def UPDATE_RECTLANGES(self):
        self.RECTLANGE_1 = RECTLANGE(self, self.TILE, self.TILE,
                                     self.TILE*2, self.TILE*2,
                                     4)

        for a in range(1, self.RECTLANGE_COUNT+1):
            P = getattr(self, "RECTLANGE_"+str(a))
            self.SPG_RECTLANGES.add(P)
        
    def UPDATE_ENEMIES(self):
        self.ENEMY_1 = ENEMY(self, self.TILE*5, self.TILE*5,
                             self.TILE, self.TILE,
                             4, RED, "VERTICAL")

        self.ENEMY_2 = ENEMY(self, self.TILE*10, self.TILE*5,
                             self.TILE, self.TILE,
                             4, RED, "HORIZONTAL")

        self.ENEMY_3 = ENEMY(self, WIDTH/2, HEIGHT/2,
                             self.TILE//2, self.TILE//2,
                             2, RED, "AI")

        self.ENEMY_4 = ENEMY(self, WIDTH/2, HEIGHT/2,
                             self.TILE//2, self.TILE//2,
                             1, RED, "AI")

        self.ENEMY_5 = ENEMY(self, WIDTH/2, HEIGHT/2,
                             self.TILE//2, self.TILE//2,
                             16, RED, "VERTICAL")

        self.ENEMY_6 = ENEMY(self, 128, HEIGHT/2,
                             self.TILE//2, self.TILE//2,
                             16, RED, "HORIZONTAL")

        for a in range(1, self.ENEMY_COUNT+1):
            E = getattr(self, "ENEMY_"+str(a))
            self.SPG_ENEMIES.add(E)

    def UPDATE_MAP(self):
        x=y=w=f=0
        for row in STG['MAP'][self.CUR]:
            for col in row:
                if col == "W":
                    setattr(self, "WALL_"+str(w+1), WALL(self, x*self.TILE, y*self.TILE, self.TILE, self.TILE))
                    w += 1
                if col == " ":
                    setattr(self, "FLOOR_"+str(f+1), FLOOR(self, x*self.TILE, y*self.TILE, self.TILE, self.TILE))
                    f += 1
                x += 1
            y += 1
            x = 0
        for a in range(1, self.WALL_COUNT+1):
            W = getattr(self, "WALL_"+str(a))
            self.SPG_WALLS.add(W)
        for a in range(1, self.FLOOR_COUNT+1):
            F = getattr(self, "FLOOR_"+str(a))
            self.SPG_FLOORS.add(F)

FV = WINDOW()
