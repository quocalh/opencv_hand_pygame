# gg wp
import pygame
from pygame.locals import *
# from resources import *
import random
import math
import os
import random

os.chdir("D:/vspython/symbol_resources")

class Physic_entities(pygame.sprite.Sprite):
    Group_of_all_Sprites = pygame.sprite.Group()
    
    def __init__(self, name, x, y, velocity = 0):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load(name)
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(x, y)
        self.rect.center = x, y

        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        Physic_entities.Group_of_all_Sprites.add(self)

class Tree(Physic_entities):
    Trees = pygame.sprite.Group()
    def __init__(self, name, x, y, velocity=0):
        super().__init__(name, x, y, velocity)
        Tree.Trees.add(self)

    # def update():
# def bulding_a_tree():
# tree = Tree("tree_pixel.png", 1000, 1000)
# tree = Tree("tree_pixel.png", 150, 150)
# tree = Tree("tree_pixel.png", 200, 200)
# tree = Tree("tree_pixel.png", 250, 250)
# tree = Tree("tree_pixel.png", 250, 250)

def create_trees(number_of_trees):
    for i in range(number_of_trees):
        tree = Tree("tree_pixel.png", random.randint(0, 3648), random.randint(0, 3200))
    
create_trees(100)
    # Tree.Trees.add(tree)

# bulding_a_tree()




import pygame
from pygame.locals import *
# from resources import *
import random
import math
import os
# from entities import *


# os.chdir("D:/vspython/symbol_resources")
os.chdir('D:/vspython/open_cv/combine/subresources')

pygame.init()
WIDTH, HEIGHT = 800, 800
BoundaryX, BoundaryY = [[0, 3648], [0, 3200]]
FPS = 90

# text = pygame.font.Font(pixel_font, 40)
cowboy_image = 'cowboy.png'

class Player(pygame.sprite.Sprite):
    player_himself = pygame.sprite.Group()

    def __init__(self, x, y, velocity = 10, width = 70, height = 90):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(cowboy_image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (45, 59))

        self.position = pygame.math.Vector2(x, y)
        self.direction = pygame.math.Vector2()

        self.rect = self.image.get_rect()
        self.rect.center = self.position

        self.velocity = velocity

        
    def update(self, ): # player
        if self.direction.magnitude() > self.velocity:
            self.direction = self.direction.normalize() * self.velocity
        self.position += self.direction
        
        self.position.x = max(self.rect.width / 2, min(self.position.x, BoundaryX[1] - self.rect.width / 2))
        self.position.y = max(self.rect.height / 2, min(self.position.y, BoundaryY[1] - self.rect.height / 2))
        # self.rect.center = self.position
        # print(self.position)
        self.direction = pygame.math.Vector2()


        
        
class Camera:
    def __init__(self, surface, player, width = 800, height = 800):
        self.surface = surface
        self.Heigh, self.Width = height, width
        self.HalfWidth = width / 2
        self.HalfHeight = height / 2
        self.offset = pygame.Vector2()
        self.player = player
        
    # i am the vector god tbh
    def update(self):
        self.offset.x = self.HalfWidth - player.position.x
        self.offset.y = self.HalfHeight - player.position.y # worked perfectly
        
        # self.offset.x = min((self.offset.x, self.HalfWidth))
        # self.offset.y = min((self.offset.y, self.HalfHeight))
        # self.offset.x = min(self.offset.x, BoundaryX[0]) # the rect hit the corner
        # self.offset.y = min(self.offset.y, BoundaryY[0])

        self.offset.x = min(max(self.offset.x, - BoundaryX[1] + self.Width), BoundaryX[0])
        self.offset.y = min(max(self.offset.y, - BoundaryY[1] + self.Heigh) , BoundaryY[0])
        # print(self.offset)
        
        # apply that for tghe environment
        screen.blit(self.surface, self.offset)
        
        for sprite in sorted(Physic_entities.Group_of_all_Sprites, key = lambda sprite: sprite.position.y):
        # for sprite in Physic_entities.Group_of_all_Sprites:
            # offsetx, offsety = self.HalfWidth + sprite.position.x, self.HalfHeight + sprite.position.y # the old code 
            # sprite.rect.center = - player.position.x + offsetx, - player.position.y + offsety          # dont bother it
            offsetx, offsety = sprite.position.x + self.offset.x, sprite.position.y + self.offset.y
            sprite.rect.center =  offsetx,  offsety
            screen.blit(sprite.image, sprite.rect)
            # sprite.blit(self.surface, (offsetx,  offsety))

            
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
keys = 210 * [False]
player = Player(500, 500, 3)

Physic_entities.Group_of_all_Sprites.add(player)

Player.player_himself.add(player)
MousePosition = (0,0)

ground = pygame.image.load('ground.png')

Camera = Camera(ground, player)
Camera.update()

while running:
    # Camera
    screen.fill('lightblue')

    # screen.blit(ground, (100, 100))
    print(player in Physic_entities.Group_of_all_Sprites)
    Camera.update()

    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            MousePosition = pygame.mouse.get_pos()   
        if event.type == QUIT:
            running = False  
        if event.type == KEYUP:
            keys[event.key] = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            keys[event.key] = True
    if keys[K_w]:
        player.direction.y = - player.velocity
    if keys[K_s]:
        player.direction.y =  player.velocity
    if keys[K_a]:
        player.direction.x = - player.velocity
    if keys[K_d]:
        player.direction.x =  player.velocity

    # player.player_himself.draw(screen)
    Player.player_himself.update()
    # Physic_entities.Group_of_all_Sprites = sorted(Physic_entities.Group_of_all_Sprites, key = lambda sprite: sprite.position.y)
    # Physic_entities.Group_of_all_Sprites.draw(screen)

    # player.direction.x += 6
    
    pygame.display.update()
    clock.tick(FPS)


    


