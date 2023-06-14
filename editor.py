import pygame
import keyboard
import math
import csv
import ast

class wall():
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2

        self.type = 1

        self.on = 1

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

class winnermode(wall):
    def __init__(self, pos1, pos2):
        super().__init__(pos1,pos2)
        self.type = 2
    def collision(self, point):
        if point[0] >= self.pos1[0] and point[0] <= self.pos2[0] and point[1] >= self.pos1[1] and point[1] <= self.pos2[1]:
            return(True, 5)
        else:
            return(False,0)
    def draw(self):
        pygame.draw.rect(screen,GREEN,(self.pos1[0],self.pos1[1],self.sizex,self.sizey))

class line():
    def __init__(self,pos1,pos2):
        self.pos1 = pos1
        self.pos2 = pos2
        self.timer = 40
    def update(self):
        fade = self.timer/40
        print(fade)
        pygame.draw.line(screen, [255*fade,255*fade,255*fade], self.pos1, self.pos2, int(7*fade))
        pygame.draw.circle(screen,[255*fade,255*fade,255*fade], (self.pos1[0]+int(2*fade),self.pos1[1]+int(2*fade)) ,int(4*fade))
        if self.timer == 0:
            return True
        else:
            self.timer -= 1
            return False


class projectile():
    def __init__(self,pos,angle):
        self.pos = pos
        self.angle = angle
        self.ticker = 0
        self.timer = 2000
    def update(self,distance, walls, iteration):
        global lines
        if self.ticker != 0:
            self.ticker -= 1
        x1 = distance * math.sin(self.angle)
        y1 = distance * math.cos(self.angle)

        pos1 = self.pos
        if self.ticker <= 0:
            collided = False
            for obj in walls:
                this = obj.collision([self.pos[0]+x1,self.pos[1]+y1])
                if this[0]:
                    if this[1] == 5:
                        return "lol"
                    collided = True
                    collisionpos = [self.pos[0]+x1,self.pos[1]+y1]
                    collidedObj = obj
                    break
            if collided:
                bruh = drawline(self.pos, collisionpos, collidedObj)
                lines.append(line(self.pos, bruh[1]))
                distleft = 50 - math.sqrt((abs(self.pos[0]-bruh[1][0]))**2 + (abs(self.pos[1]-bruh[1][1]))**2)
                if bruh[0] == 1:
                    self.angle = -self.angle
                    self.pos = bruh[1]
                elif bruh[0] == 2:
                    self.angle = -self.angle
                    self.pos = bruh[1]
                elif bruh[0] == 3:
                    normal = math.pi
                    self.angle = normal-self.angle
                    self.pos = bruh[1]
                elif bruh[0] == 4:
                    normal = math.pi
                    self.angle = normal-self.angle
                    self.pos = bruh[1]

                """
                match bruh[0]:
                    case 1:

                    case 2:
                        self.angle = -self.angle
                        self.pos = bruh[1]
                    case 3:
                        normal = math.pi
                        self.angle = normal-self.angle
                        self.pos = bruh[1]
                    case 4:
                        normal = math.pi
                        self.angle = normal-self.angle
                        self.pos = bruh[1]
                    """

                self.update(distleft, walls, 1)

            else:
                self.pos = [self.pos[0]+x1,self.pos[1]+y1]
                lines.append(line(pos1,self.pos))
            self.ticker = 10
        if not iteration == 0:
          lines.append(line(pos1,self.pos))
        pygame.draw.circle(screen,(0,0,255), self.pos, 2)
        self.timer -= 1
        return self.timer == 0


class player():
    def __init__(self,pos):
        self.pos = pos
        self.velocity = [0,0]
    def draw(self):
        pygame.draw.circle(screen, (255,255,255), self.pos, 10)
    def update(self,walls):
        if keyboard.is_pressed("w"):
            self.velocity[1] -= 0.5
        if keyboard.is_pressed("a"):
            self.velocity[0] -= 0.5
        if keyboard.is_pressed("s"):
            self.velocity[1] += 0.5
        if keyboard.is_pressed("d"):
            self.velocity[0] += 0.5
        self.velocity[0] *= 0.8
        self.velocity[1] *= 0.8
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

    for n in range(samplesize*2):
        if obj.collision(calculation((n*2)+1, pos1, xdeviance,ydeviance,samplesize))[0]:
            sidehit = obj.collision(calculation((n*2)+1, pos1, xdeviance,ydeviance,samplesize))[1]
            incursionpos = calculation((n*2)+1, pos1, xdeviance,ydeviance,samplesize)
            return sidehit, incursionpos



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

lines = []

bullets = []


walls = []
walls.append(wall((-100,-100),(size[0],10)))
walls.append(wall((size[0]-20,-100),(size[0]+100,size[1]+60)))
walls.append(wall((-100,-100),(10,size[1]+60)))
walls.append(wall((-100,size[1]-10),(size[0]+100,size[1]+100)))


"""
walls.append(wall((300,400),(600,420)))
walls.append(winnermode((300,450),(350,500)))

with open('level1.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    for x in walls[4:]:
        writer.writerow([x.pos1,x.pos2,x.type,x.on])
"""



with open('levelx.csv', 'r', newline='') as infile:
    reader = csv.reader(infile)
    for x in reader:
        peram = []
        for y in x:
            if len(y) == 1:
                peram.append(int(y))
            else:
                peram.append(ast.literal_eval(y))
        if peram[2] == 1:
            walls.append(wall(peram[0],peram[1]))
        elif peram[2] == 2:
            walls.append(winnermode(peram[0],peram[1]))







# -------- Main Program Loop -------------------------------------------------------------------------------------------------------------------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)

    playerobj.update(walls)

    if keyboard.is_pressed("right"):
        angle -= 1
        if angle < 0:
            angle = angle + 360
    if keyboard.is_pressed("left"):
        angle += 1
        if angle > 360:
            angle = angle -360
    radians = angle * 3.14159 /180


    x1 = 50 * math.sin(radians)
    y1 = 50 * math.cos(radians)

    shootpos = (playerobj.pos[0]+x1,playerobj.pos[1]+y1)


    if keyboard.is_pressed("space")and not bullets:
        bullets.append(projectile(playerobj.pos, radians))

    for obj in walls:
        obj.draw()

    playerobj.draw()

    for n in range(5):
        shootpos = (playerobj.pos[0]+(x1*n),playerobj.pos[1]+(y1*n))
        pygame.draw.circle(screen,(255,255,255),shootpos,2)

    for obj in lines:
        if obj.update():
            lines.remove(obj)

    for obj in bullets:
            winner = obj.update(50,walls, 0)
            if winner == "lol":
                c = 4/3
                walls = walls[      :3       +1]
                lines = []
                bullets.remove(obj)
                playerobj = player([500,300])
                angle = 0
            elif winner:
                bullets.remove(obj)


    pygame.display.flip()
    # --- Limit to 60 frames per second

    clock.tick(60)



# Close the window and quit.
pygame.quit()
