# THIS EXSIST TO EXPERIMENT, HAVE NOT DONE YET XD

import pygame
import os
from setting import *
from pygame.locals import *
import math

os.chdir('D:/vspython/symbol_resources')

# SETUP --------------------------------------------------------------------


# ----------------
pygame.init()

keys = 512 * [False]
mouse = 20 * [False]

running = True

pygame.display.set_caption('cowboy cat')

clock  = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

class object(pygame.sprite.Sprite):
    spritegroup = pygame.sprite.Group()

    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill('red')
        self.rect = self.image.get_rect(center = (x,y))

        object.spritegroup.add(self)

    def update(self):
        pass
        

def sweep_and_prunes(): # detect if clicked
    
    # core
    pass


    


object1 = object(100, 100, 50, 50)
object1 = object(500, 100, 50, 50)
object1 = object(500, 500, 50, 50)
object1 = object(500, 300, 50, 50)

object_held = False


def move__pushing__recursion__(movin_box,  vector, CheckingSprites = object, Firstime = True, maxobject = True): # IF FIRST TIME NEED BC NO NEED TO REMEARSURE THE NEXT OBJECT FOR SURE
    CheckingSprites = [box for box in object.spritegroup if box is not movin_box]
    # BASED SEARCHING FOR BOXES , MAKE IT TRANSFER VECTOR FIRST THEN ADD IF ELSE STATEMENT WOULD BE FINE
    VectorMultipler = vector
    if not CheckingSprites:
        return
    for box in [box for box in CheckingSprites if movin_box.rect.top <= box.rect.top <= movin_box.rect.bottom or movin_box.rect.top <= box.rect.bottom <= movin_box.rect.bottom]:
        if pygame.sprite.spritecollideany(movin_box, CheckingSprites):
            box = pygame.sprite.spritecollideany(movin_box, CheckingSprites)

            # if box == parent: return # no cycle => no exceed recursion ig:D

            # print(pygame.sprite.spritecollide(movin_box, CheckingSprites, False))
            if Firstime:
                range_list = (
                                math.hypot(box.rect.midleft[0] - movin_box.rect.centerx, box.rect.midleft[1] - movin_box.rect.centery), # 0
                                math.hypot(box.rect.midtop[0] - movin_box.rect.centerx, box.rect.midtop[1] - movin_box.rect.centery), # 1
                                math.hypot(box.rect.midright[0] - movin_box.rect.centerx, box.rect.midright[1] - movin_box.rect.centery), # 2
                                math.hypot(box.rect.midbottom[0] - movin_box.rect.centerx, box.rect.midbottom[1] - movin_box.rect.centery), # 3
                                 )
                # print('nah')
                #                 3
                #           _____________
                #           |           |
                #           |           |
                #        0  |           |  2
                #           |           |
                #           |___________|
                #                 1
                # min_value = min(range_list)
                EdgeAllow = [i for i, range in enumerate(range_list) if range == min(range_list)] # GET THE MIN RANGE (CAN PUSH DIAGNALY XD)
                # EdgeAllow = [range_list.index(min(range_list))]
                VectorMultipler = [0, 0] # Base move
                # print(EdgeAllow)
                for Edge in EdgeAllow: 
                    if Edge % 2: # Y AXIS
                        VectorMultipler[1] = 1
                        #         colliding...
                        # ___________________________________
                        # |\ \ \ \ \|X X X X X X|/ / / / / /|
                        # |\ \ \ \ \|X X X X X X|/ / / / / /|
                        # |\ \ \ \ \|X X X X X X|/ / / / / /|
                        #
                        # NOT WORKING RN child of problem
                        # Bottom_Or_Top = box.rect.midbottom[1] * (Edge == 3) + box.rect.midtop[1] * (Edge == 1)
                        CenterDistance = (
                                          ((box.rect.centery - box.rect.midbottom[1]) + (movin_box.rect.centery - movin_box.rect.midbottom[1])) * (Edge == 3)) + (
                                          ((box.rect.centery - box.rect.midtop[1]) + (movin_box.rect.centery - movin_box.rect.midtop[1])) * (Edge == 1)
                                         ) # AB
                        RealCenterDistance = (box.rect.centery - movin_box.rect.centery) # AC
                        VectorExtract = CenterDistance - RealCenterDistance    # CB
                        # box.rect.move_ip((0, VectorExtract))
                        VectorMultipler[1] = VectorExtract

                    if not Edge % 2: # X AXIS
                        # VectorMultipler[0] = 1
                        CenterDistance = (
                                          ((box.rect.centerx - box.rect.midleft[0]) + (movin_box.rect.centerx - movin_box.rect.midleft[0])) * (Edge == 0)) + (
                                          ((box.rect.centerx - box.rect.midright[0]) + (movin_box.rect.centerx - movin_box.rect.midright[0])) * (Edge == 2)
                                         ) # AB
                        RealCenterDistance = (box.rect.centerx - movin_box.rect.centerx) # AC
                        VectorExtract = CenterDistance - RealCenterDistance    # CB
                        # box.rect.move_ip((VectorExtract, 0))
                        VectorMultipler[0] = VectorExtract
            
            box.rect.move_ip(VectorMultipler)
            
            move__pushing__recursion__(box, VectorMultipler, CheckingSprites, False)
            print(CheckingSprites)

MousePosition = pygame.mouse.get_pos()
LastMousePostion = pygame.mouse.get_pos()

while running:
    screen.fill('black')

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
            exit()

        if event.type == KEYDOWN:
            keys[event.key] = True
        if event.type == KEYUP:
            keys[event.key] = False
        
        if event.type == MOUSEBUTTONDOWN:
            mouse[event.button] = True

        if event.type == MOUSEBUTTONUP:
            mouse[event.button] = False
            # object_held = False

    if mouse[1]: # LEFT CLICKED
        MousePosition = pygame.mouse.get_pos()
        for box in [box for box in object.spritegroup if box.rect.top < MousePosition[1] < box.rect.bottom]: # SWEEP AND PRUNE

            if box.rect.colliderect(pygame.Rect(MousePosition[0], MousePosition[1], 10, 10)):

                if event.type == MOUSEMOTION:
                    vector = MousePosition[0] - LastMousePostion[0], MousePosition[1] - LastMousePostion[1]
                    # FROM HERE ACTUALLY
                    # func(vector)
                    move__pushing__recursion__(box, [vector[0], vector[1]])

                    box.rect.move_ip(vector[0], vector[1])
                    



    object.spritegroup.update()
    object.spritegroup.draw(screen)
  

    pygame.display.update()
    clock.tick(60)        

    LastMousePostion = MousePosition


