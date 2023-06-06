import pygame
import keyboard
import math


class wall():
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        print(self.pos1)
        self.pos2 = pos2
        print(self.pos2)

        self.sizex = abs(pos1[0]-pos2[0])
        print(self.sizex)
        self.sizey = abs(pos1[1]-pos2[1])
        print(self.sizey)

    def draw(self):
        pygame.draw.rect(screen,RED,(self.pos1[0],self.pos1[1],self.sizex,self.sizey))

    def collision(self,point):
        if point[0] >= self.pos1[0] and point[0] <= self.pos2[0] and point[1] >= self.pos1[1] and point[1] <= self.pos2[1]:
            return True
        else:
            return False


class player():
    def __init__(self,pos):
        self.pos = pos
        self.velocity = [0,0]
    def draw(self):
        pygame.draw.circle(screen, (255,255,255), self.pos, 10)
    def update(self,walls):
        if keyboard.is_pressed("w"):
            self.velocity[1] -= 1
        if keyboard.is_pressed("a"):
            self.velocity[0] -= 1
        if keyboard.is_pressed("s"):
            self.velocity[1] += 1
        if keyboard.is_pressed("d"):
            self.velocity[0] += 1
        self.velocity[0] *= 0.9
        self.velocity[1] *= 0.9
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        for obj in walls:
            if obj.collision([self.pos[0]+10,self.pos[1]]):
                self.velocity[0] = 0
                self.pos[0] = obj.pos1[0]-10
            elif obj.collision([self.pos[0]-10,self.pos[1]]):
                self.velocity[0] = 0
                self.pos[0] = obj.pos2[0]+10
            if obj.collision([self.pos[0], self.pos[1]-10]):
                self.velocity[1] = 0
                self.pos[1] = obj.pos2[1]+10
            elif obj.collision([self.pos[0],self.pos[1]+10]):
                self.velocity[1] = 0
                self.pos[1] = obj.pos1[1]-10


def calculation(n, pos1, xdeviance, ydeviance,sample):
                return abs(math.ceil(pos1[0] + xdeviance*(n/(sample*2)))), abs(math.ceil(pos1[1] + (ydeviance*(n/(sample*2)))))

def drawline(pos1,angle,distance):



    pos2 = (x,y)

    xdeviance = pos2[0] - pos1[0]
    ydeviance = pos2[1] - pos1[1]

    samplesize = 50

    for n in range(samplesize):
        collision(calculation(n+1, pos1, xdeviance,ydeviance,samplesize))


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
size = (1000,700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
done = False
clock = pygame.time.Clock()


playerobj = player([500,300])

angle = 0

walls = []

walls.append(wall((0,0),(40,40)))
walls.append(wall((60,60),(100,100)))

walls.append(wall((0,0),(10,700)))
walls.append(wall((10,0),(1000,10)))

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)

    playerobj.update(walls)



    if pygame.mouse.get_pressed()[0]:
        collided = False
        point = pygame.mouse.get_pos()
        for obj in walls:
            if obj.collision(point):
                collided = True
                #find point of collision
                break
        if collided:
            print("true")
        else:
            print("false")

    if keyboard.is_pressed("right"):
        angle -= 1
        if angle < 0:
            angle = 360
    if keyboard.is_pressed("left"):
        angle += 1
        if angle > 360:
            angle = 1
    radians = angle * 3.14159 /180


    x1 = 50 * math.sin(radians)
    y1 = 50 * math.cos(radians)

    shootpos = (playerobj.pos[0]+x1,playerobj.pos[1]+y1)


    for obj in walls:
        obj.draw()

    playerobj.draw()

    for n in range(5):
        shootpos = (playerobj.pos[0]+(x1*n),playerobj.pos[1]+(y1*n))
        pygame.draw.circle(screen,(255,255,255),shootpos,2)



    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)



# Close the window and quit.
pygame.quit()
