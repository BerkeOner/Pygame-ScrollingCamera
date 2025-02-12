
import pygame

from settings import *

class BAR():
    def __init__(self, window, x, y, w, h, color, outline, bd):
        self.FV = window
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.COLOR = color
        self.OUTLINE = outline
        self.BD = bd
        self.RECT = pygame.Surface((self.w, self.h))
        self.RECT.fill(self.COLOR)
        self.OUTLINE_RECT = pygame.Rect(self.x, self.y, self.w, self.h)
        self.UPDATE()

    def UPDATE(self, count=0):
        self.w += count
        if self.w < 0:
            self.w = self.OUTLINE_RECT.w
        if self.w > self.OUTLINE_RECT.w:
            self.w = self.OUTLINE_RECT.w
        self.RECT = pygame.transform.scale(self.RECT, (self.w, self.h))
        self.RECT.fill(self.COLOR)

class MAP():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.MAP = pygame.Surface(RESOLUTION)

    def MOVE(self, x1, y1):
        self.x += -x1
        self.y += -y1

class WALL(pygame.sprite.Sprite):
    def __init__(self, window, x, y, w, h, color=BROWN):
        pygame.sprite.Sprite.__init__(self)
        self.FV = window
        self.FV.WALL_COUNT += 1
        self.w = w
        self.h = h
        self.COLOR = color
        #self.image = pygame.Surface((self.w, self.h))
        self.image = pygame.image.load("data/assets/sprites/duvar.png").convert()
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        #self.image.fill(self.COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class FLOOR(pygame.sprite.Sprite):
    def __init__(self, window, x, y, w, h, color=LT_GREEN):
        pygame.sprite.Sprite.__init__(self)
        self.FV = window
        self.FV.FLOOR_COUNT += 1
        self.w = w
        self.h = h
        self.COLOR = color
        #self.image = pygame.Surface((self.w, self.h))
        self.image = pygame.image.load("data/assets/sprites/yer.png").convert()
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        #self.image.fill(self.COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class ENEMY(pygame.sprite.Sprite):
    def __init__(self, window, x, y, w, h, speed, color=RED, direction="VERTICAL"):
        pygame.sprite.Sprite.__init__(self)
        self.FV = window
        self.FV.ENEMY_COUNT += 1
        self.w = w
        self.h = h
        self.COLOR = color
        self.SPEED = speed
        #self.image = pygame.Surface((self.w, self.h))
        self.image = pygame.image.load("data/assets/sprites/dusman.png").convert()
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        #self.image.fill(self.COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.DIRECTION = direction

    def MOVE(self, walls, rectlanges, players=None):
        for rectlange in rectlanges:
            if rectlange.rect.x <= self.rect.x <= rectlange.rect.x+rectlange.w-self.w and rectlange.rect.y <= self.rect.y <= rectlange.rect.y+rectlange.h-self.h:
                pass
            else:
                if self.DIRECTION == "VERTICAL":
                    self.rect.y += self.SPEED
                    for wall in walls:
                        if self.rect.bottom == wall.rect.top and self.rect.x == wall.rect.x:
                            self.SPEED = -self.SPEED
                        if self.rect.top == wall.rect.bottom and self.rect.x == wall.rect.x:
                            self.SPEED = -self.SPEED
                if self.DIRECTION == "HORIZONTAL":
                    self.rect.x += self.SPEED
                    for wall in walls:
                        if self.rect.y == wall.rect.y and self.rect.right == wall.rect.left:
                            self.SPEED = -self.SPEED
                        if self.rect.y == wall.rect.y and self.rect.left == wall.rect.right:
                            self.SPEED = -self.SPEED
                if self.DIRECTION == "AI":
                    for player in players:
                        if player.rect.x < self.rect.x:
                            self.rect.x -= self.SPEED
                            for wall in walls:
                                if self.rect.colliderect(wall):
                                    self.rect.x += self.SPEED
                        if player.rect.y < self.rect.y:
                            self.rect.y -= self.SPEED
                            for wall in walls:
                                if self.rect.colliderect(wall):
                                    self.rect.y += self.SPEED
                        if player.rect.x > self.rect.x:
                            self.rect.x += self.SPEED
                            for wall in walls:
                                if self.rect.colliderect(wall):
                                    self.rect.x -= self.SPEED
                        if player.rect.y > self.rect.y:
                            self.rect.y += self.SPEED
                            for wall in walls:
                                if self.rect.colliderect(wall):
                                    self.rect.y -= self.SPEED

class PLAYER(pygame.sprite.Sprite):
    def __init__(self, window, x, y, w, h, speed, color=LT_CYAN):
        pygame.sprite.Sprite.__init__(self)
        self.FV = window
        self.FV.PLAYER_COUNT += 1
        self.w = w
        self.h = h
        self.SPEED = speed
        self.COLOR = color
        #self.image = pygame.Surface((self.w, self.h))
        self.image = pygame.image.load("data/assets/sprites/oyuncu.png").convert()
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        #self.image.fill(self.COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def MOVE(self, camera, walls):
        KEY = pygame.key.get_pressed()
        if KEY[pygame.K_UP]:
            self.rect.y -= self.SPEED
            camera.MOVE(0, -self.SPEED)
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.rect.y += self.SPEED
                    camera.MOVE(0, +self.SPEED)
        if KEY[pygame.K_LEFT]:
            self.rect.x -= self.SPEED
            camera.MOVE(-self.SPEED, 0)
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.rect.x += self.SPEED
                    camera.MOVE(+self.SPEED, 0)
        if KEY[pygame.K_DOWN]:
            self.rect.y += self.SPEED
            camera.MOVE(0, +self.SPEED)
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.rect.y -= self.SPEED
                    camera.MOVE(0, -self.SPEED)
        if KEY[pygame.K_RIGHT]:
            self.rect.x += self.SPEED
            camera.MOVE(+self.SPEED, 0)
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.rect.x -= self.SPEED
                    camera.MOVE(-self.SPEED, 0)

class RECTLANGE(pygame.sprite.Sprite):
    def __init__(self, window, x, y, w, h, speed, color=YELLOW):
        pygame.sprite.Sprite.__init__(self)
        self.FV = window
        self.FV.RECTLANGE_COUNT += 1
        self.w = w
        self.h = h
        self.SPEED = speed
        self.COLOR = color
        #self.image = pygame.Surface((self.w, self.h))
        self.image = pygame.image.load("data/assets/sprites/dortgen.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        #self.image.fill(self.COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def MOVE(self, walls):
        KEY = pygame.key.get_pressed()
        if KEY[pygame.K_w]:
            self.rect.y -= self.SPEED
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.rect.y += self.SPEED
        if KEY[pygame.K_a]:
            self.rect.x -= self.SPEED
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.rect.x += self.SPEED
        if KEY[pygame.K_s]:
            self.rect.y += self.SPEED
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.rect.y -= self.SPEED
        if KEY[pygame.K_d]:
            self.rect.x += self.SPEED
            for wall in walls:
                if self.rect.colliderect(wall):
                    self.rect.x -= self.SPEED





















