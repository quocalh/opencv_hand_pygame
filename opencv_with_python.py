import pygame
import math
from pygame.locals import *
from setting import *
import os

import cv2
import mediapipe 
import time
from matplotlib import  pyplot as plt

os.chdir('D:/vspython/symbol_resources')


# TOO EXHAUSTED TO CREATE MULTIPLES FILES -------------------------- sprite ig
class object(pygame.sprite.Sprite):
    spritegroup = pygame.sprite.Group()

    def __init__(self, x, y, width, height, color = 'red'):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center = (x,y))

        object.spritegroup.add(self)

    def update(self):
        pass
        
# PUSHING USING RECURSION (fix completed, go try in the object_pushign_recursion_test)--------------------

def move__pushing__recursion__(movin_box,  vector, CheckingSprites = object, Firstime = True, maxobject = True): # IF FIRST TIME NEED BC NO NEED TO REMEARSURE THE NEXT OBJECT FOR SURE
    CheckingSprites = [box for box in object.spritegroup if box is not movin_box]
    # BASED SEARCHING FOR BOXES , MAKE IT TRANSFER VECTOR FIRST THEN ADD IF ELSE STATEMENT WOULD BE FINE
    VectorMultipler = vector

    for box in [box for box in CheckingSprites if movin_box.rect.top <= box.rect.top <= movin_box.rect.bottom or movin_box.rect.top <= box.rect.bottom <= movin_box.rect.bottom]:
        if pygame.sprite.spritecollideany(movin_box, CheckingSprites):
            box = pygame.sprite.spritecollideany(movin_box, CheckingSprites)
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
            # else:
            
            box.rect.move_ip(VectorMultipler)
            
            move__pushing__recursion__(box, VectorMultipler, CheckingSprites, False)

                # print(VectorMultipler)

            
        # if collide (chấn chỉnh sao cho hai tam cach nhau hop li)
    # pass

# if top2 < top1 < bottom 2 or top2 < bottom1 < bottom2 # SWEEP AND PRUNE


# SETUP PYGAME, CV2 --------------------------------------------------------------------------------------------------------------------------

pygame.init()

keys = 512 * [False]
mouse = 3 * [False]

running = True

pygame.display.set_caption('cowboy cat')

clock  = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

capture = cv2.VideoCapture(1)

PreviousRun = time.time()

success, img = capture.read()

# MAIN (ONE FILE ONLY)---------------  --- 

class HandDetector:

    def __init__(self, mode = False, MaxHand = 2, detectioncon = 0.5, trackcon = 0.5) -> None:
        
        self.mode = mode
        self.MaxHand = MaxHand
        self.DetectionCon = detectioncon
        self.TrackCon = trackcon


        self.mpHands = mediapipe.solutions.hands
        # self.Hands = self.mpHands.Hands(self.mode, self.MaxHand, self.DetectionCon, self.TrackCon)
        self.Hands = self.mpHands.Hands()
        self.mpDraw = mediapipe.solutions.drawing_utils
        
    @staticmethod
    def BranchRetrivialID(id, x, y, list_of_IDs = [], function = None):
        coordinates = []

        if id in list_of_IDs:
            coordinates.append((x, y))
            if function:
                function(x, y)
        # print('sajkdfhaksjhf')

        return coordinates

    @staticmethod
    def DotProduct(Pivot, TheNextPoint, ThePreviousPoint): # that prev point from the RetrivialPath
        
        ThePreviousVector = (Pivot[0] - ThePreviousPoint[0], Pivot[1] - ThePreviousPoint[1])
        TheTargetVector = (TheNextPoint[0] - Pivot[0], TheNextPoint[1] - Pivot[1])

        MagnitudePreviousVector =  ((ThePreviousVector[0] * ThePreviousVector[0] + ThePreviousVector[1] * ThePreviousVector[1]) ** 0.5)
        MagnitudeTargetVector = ((TheTargetVector[0] * TheTargetVector[0] + TheTargetVector[1] * TheTargetVector[1]) ** 0.5)

        NormalizedPreviousVector =  ThePreviousVector[0] / MagnitudePreviousVector, ThePreviousVector[1] / MagnitudePreviousVector
        NormalizedTargetVector = TheTargetVector[0] / MagnitudeTargetVector, TheTargetVector[1] / MagnitudeTargetVector

        return NormalizedPreviousVector[0] * NormalizedTargetVector[0] + NormalizedPreviousVector[1] * NormalizedTargetVector[1]
    
    @staticmethod
    def Magnitude(vector):
        return (vector[0]**2 + vector[1]**2)**0.5

    def indentify_a_punch(EnumerateIDPosition): # enumurate() but position not lm
        knuckles = (5, 9, 13, 17)
        fingers =  (8, 12, 16, 20)
        length_each_finger = () 

        for i in range(len(knuckles)):
            
            return True
        return False

        # for id, lm in EnumerateHandLandmark:
        #     if id in [4, 8, 12, 16, 20]:
        #         pass

        pass

    def Dectecting(self, show = True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        self.result = self.Hands.process(imgRGB)

        if self.result.multi_hand_landmarks and show:

            for HandLandMark in self.result.multi_hand_landmarks:

                self.mpDraw.draw_landmarks(img, HandLandMark, self.mpHands.HAND_CONNECTIONS)

                for id, lm in enumerate(HandLandMark.landmark):
                    
                    Width, Height, c = img.shape
                    Width, Height = 640, 480
                    
                    
                    x, y  = int(lm.x * Width), int(lm.y  * Height)

                    def lightup(x, y):
                        cv2.circle(img, (x, y), 5, (0, 255, 0), 5)
                    HandDetector1.BranchRetrivialID(id, x, y, [8], lightup)
                    
            return enumerate(HandLandMark.landmark)
        
    @staticmethod
    def ShowFPS(show = True, font = False):

        global PreviousRun

        DeltaTime = time.time() - PreviousRun

        FPS = 1 / DeltaTime
        cv2.putText(img, 'FPS: ' + str(int(FPS)), (10, 70), 
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 0 , 0), 3)   
        if show:
            cv2.putText(img, 'FPS: ' + str(int(FPS)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255 , 0), 3)

        PreviousRun = time.time()
    


# OBJECT INIT ------------------------------------------------
        



object1 = object(100, 100, 100, 100, 'blue')
object1 = object(350, 100, 100, 100)
object1 = object(500, 100, 100, 100)
object1 = object(500, 500, 100, 100, 'yellow')
object1 = object(300, 300, 100, 100, 'brown')




# MAIN ---------------------------------------------------------------

HandDetector1 = HandDetector()

FingerCapture = [False] * 100
FingerHold = [False] * 5

Object1 = pygame.Rect(100, 100, 50, 50)

Recent_Finger = [False] * 100

while running:

    # CV2
    success, img = capture.read()

    Fingers = HandDetector1.Dectecting()

    # EVENT FINGER --------------------------

    if Fingers: # if there is finger


        for id, lm in Fingers:
            # FingerCapture[id] = int(lm.x * 640), int(lm.y  * 480)
            FingerCapture[id] = lm.x * (WIDTH - 50), lm.y  * (HEIGHT + 150)
            # FingerCapture[id] = lm.x * WIDTH, lm.y  * HEIGHT + 150

    HandDetector1.ShowFPS()

    cv2.imshow('xanh', img)# at the bottom

    if cv2.waitKey(1) ==  ord('q'):
        break




    # pygame
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            running = False
            exit()

        if event.type == KEYDOWN:
            keys[event.key] = True

        if event.type == KEYUP:
            keys[event.key] = False

    # PRINT OUT THE OBJECT
    object.spritegroup.update()
    object.spritegroup.draw(screen)


    if FingerCapture[8] and FingerCapture[4]: # DETECT AN INDEX FINGER! (DROP AND DRAG)
        if math.hypot(FingerCapture[8][0] - FingerCapture[12][0], FingerCapture[8][1] - FingerCapture[12][1]) > 90: # ALLOWED IF THERE IS NO NEARBY MIDDLE FINGER
            
            if math.hypot(FingerCapture[8][0] - FingerCapture[12][0], FingerCapture[8][1] - FingerCapture[12][1]) > 40: # A PUNCH FORM FOR INDEX FINGER
                pygame.draw.circle(screen, 'Green', FingerCapture[8], 10)

            if math.hypot(FingerCapture[8][0] - FingerCapture[4][0], FingerCapture[8][1] - FingerCapture[4][1]) < 60: # IF THUMB NEABY TURN RED, HELD
                # pygame.draw.circle(screen, 'purple', FingerCapture[8], 10)
                FingerHold = True
                

    if FingerHold and Recent_Finger[8]: # if FINGER HELD
        print('certified')
        MousePosition = pygame.mouse.get_pos()

        for i, box in enumerate(object.spritegroup):
            if box.rect.colliderect(pygame.Rect(Recent_Finger[8][0], Recent_Finger[8][1], 10, 10)):

                    pygame.draw.circle(screen, 'purple', FingerCapture[8], 10)

                    vector = FingerCapture[8][0] - Recent_Finger[8][0], FingerCapture[8][1] - Recent_Finger[8][1]

                    move__pushing__recursion__(box, [vector[0], vector[1]])

                    box.rect.move_ip(vector[0], vector[1])
                    

    Recent_Finger = FingerCapture

    FingerCapture = [False] * 100
    FingerHold = False

    pygame.display.update()
    clock.tick(600)        

capture.release()



