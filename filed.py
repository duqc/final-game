import pygame
import keyboard
import math


class wall():
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2

        self.sizex = abs(pos1[0]-pos2[0])
        self.sizey = abs(pos1[1]-pos2[1])

    def draw(self):
        pygame.draw.rect(screen,RED,(self.pos1[0],self.pos1[1],self.sizex,self.sizey))

    def collision(self,point):
        if point[0] >= self.pos1[0] and point[0] <= self.pos2[0] and point[1] >= self.pos1[1] and point[1] <= self.pos2[1]:

            right = abs(point[0] - self.pos1[0])
            left = abs(point[0] - self.pos2[0])
            down = abs(point[1] - self.pos1[1])
            up = abs(point[1] - self.pos2[1])

            thething = 1
            smallest = right
            if smallest > left:
                smallest = left
                thething = 2
            if smallest > down:
                smallest = down
                thething = 3
            if smallest > up:
                thething = 4
            return (True, thething)
        else:
            return (False, 0)

class projectile():
    def __init__(self,pos,angle):
        self.pos = pos
        self.angle = angle
        self.ticker = 0
        self.timer = 500
    def update(self,distance, walls):
        if self.ticker != 0:
            self.ticker -= 1
        x1 = distance * math.sin(self.angle)
        y1 = distance * math.cos(self.angle)
        if self.ticker <= 0:
            collided = False
            for obj in walls:
                if obj.collision([self.pos[0]+x1,self.pos[1]+y1])[0]:
                    collided = True
                    collisionpos = [self.pos[0]+x1,self.pos[1]+y1]
                    collidedObj = obj
                    break
            if collided:
                drawline(self.pos, collisionpos, collidedObj)
            else:
                self.pos = [self.pos[0]+x1,self.pos[1]+y1]

            self.ticker = 30
        pygame.draw.circle(screen,(0,0,255), self.pos, 2)
        self.timer -= 1
        if self.timer == 0:
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
            if obj.collision([self.pos[0]+10,self.pos[1]])[0]:
                self.velocity[0] = 0
                self.pos[0] = obj.pos1[0]-10
            elif obj.collision([self.pos[0]-10,self.pos[1]])[0]:
                self.velocity[0] = 0
                self.pos[0] = obj.pos2[0]+10
            if obj.collision([self.pos[0], self.pos[1]-10])[0]:
                self.velocity[1] = 0
                self.pos[1] = obj.pos2[1]+10
            elif obj.collision([self.pos[0],self.pos[1]+10])[0]:
                self.velocity[1] = 0
                self.pos[1] = obj.pos1[1]-10



def calculation(n, pos1, xdeviance, ydeviance,sample):
                return abs((pos1[0] + xdeviance*(n/(sample*2)))), abs(pos1[1] + (ydeviance*(n/(sample*2))))

def drawline(pos1,pos2,obj):


    xdeviance = pos2[0] - pos1[0]
    ydeviance = pos2[1] - pos1[1]

    samplesize = 20

    for n in range(samplesize):
        if obj.collision(calculation((n*2)+1, pos1, xdeviance,ydeviance,samplesize))[0]:

            sidehit = obj.collision(calculation((n*2)+1, pos1, xdeviance,ydeviance,samplesize))[1]

            print(sidehit)

            incursionpos = calculation((n*2)+1, pos1, xdeviance,ydeviance,samplesize)
            break



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


testing = False

pygame.init()
size = (1000,700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
done = False
clock = pygame.time.Clock()


playerobj = player([500,300])

angle = 0



bullets = []


walls = []

walls.append(wall((-100,-100),(10,700)))
walls.append(wall((10,-100),(1000,10)))
walls.append(wall((990,0),(1300,800)))
walls.append(wall((0,690),(1000,800)))

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)

    playerobj.update(walls)



    if keyboard.is_pressed("right"):
        angle -= 0.5
        if angle < 0:
            angle = angle + 360
    if keyboard.is_pressed("left"):
        angle += 0.5
        if angle > 360:
            angle = angle -360
    radians = angle * 3.14159 /180


    x1 = 50 * math.sin(radians)
    y1 = 50 * math.cos(radians)

    shootpos = (playerobj.pos[0]+x1,playerobj.pos[1]+y1)



    if keyboard.is_pressed("space") and not bullets:
        bullets.append(projectile(playerobj.pos, radians))

    for obj in walls:
        obj.draw()

    playerobj.draw()

    for n in range(5):
        shootpos = (playerobj.pos[0]+(x1*n),playerobj.pos[1]+(y1*n))
        pygame.draw.circle(screen,(255,255,255),shootpos,2)

    for obj in bullets:
            if obj.update(50,walls):
                bullets.remove(obj)

    pygame.display.flip()
    # --- Limit to 60 frames per second

    clock.tick(60)



# Close the window and quit.
pygame.quit()
