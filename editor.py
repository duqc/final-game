import pygame
import keyboard
import csv
import threading
import ast
from pynput import mouse

undoplus = 0

name = input("choose level name: example: level1.csv ")



undo = []
walltype = 1
def on_click(x, y, button, pressed):

    global pos1
    global walltype


    btn = button.name
    if pressed and btn == 'left':
        pos1 = pygame.mouse.get_pos()
        if keyboard.is_pressed("b"):
            for x in walls:
                if x.check(pos1):
                    walls.remove(x)

    elif btn == 'left':
        pos2 = pygame.mouse.get_pos()
        if walltype == 1:
            walls.append(wall((pos1),pos2,1,1))
        elif walltype == 2:
            walls.append(wall((pos1),pos2,2,1))
        elif walltype == 3:
            walls.append(wall((pos1),pos2,3,1))
        pos1 = None




listener = mouse.Listener(on_click=on_click)
listener.start()




pygame.init()
size = (1000,700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
done = False
clock = pygame.time.Clock()

class wall():
    def __init__(self,pos1,pos2,type,on):
        temppos = [pos1[0],pos1[1]]
        tempmousepos = [pos2[0],pos2[1]]
        if pos1[0] > pos2[0]:
            temppos[0] = mousepos[0]
            tempmousepos[0] = pos1[0]
        if pos1[1] > pos2[1]:
            temppos[1] = mousepos[1]
            tempmousepos[1] = pos1[1]

        self.pos1 = temppos
        self.pos2 = tempmousepos
        self.width = abs(pos1[0]-pos2[0])
        self.height = abs(pos1[1]-pos2[1])

        self.type = type
        self.on = 1
        if self.type == 1:
            self.colour = (255,0,0)
        elif self.type == 2:
            self.colour = (0,255,0)
        elif self.type == 3:
            self.colour = (255,255,255)
    def check(self,point):
        if point[0] >= self.pos1[0] and point[0] <= self.pos2[0] and point[1] >= self.pos1[1] and point[1] <= self.pos2[1]:
            return True
        else:
            return False


    def draw(self):
        if self.type == 3:
            pygame.draw.circle(screen,(255,255,255),self.pos1,10)
        else:
            pygame.draw.rect(screen,self.colour,(self.pos1[0],self.pos1[1],self.width,self.height))


ticker = 0

walls = []
walls.append(wall((-100,-100),(size[0],10),1,1))
walls.append(wall((size[0]-20,-100),(size[0]+100,size[1]+60),1,1))
walls.append(wall((-100,-100),(10,size[1]+60),1,1))
walls.append(wall((-100,size[1]-10),(size[0]+100,size[1]+100),1,1))



if name == "edit":
    name = input("ok choose what level you want to edit")
    with open(name, 'r', newline='') as infile:
        reader = csv.reader(infile)
        for x in reader:
            peram = []
            for y in x:
                if len(y) == 1:
                    peram.append(int(y))
                else:
                    peram.append(ast.literal_eval(y))
            walls.append(wall(peram[0],peram[1],peram[2],peram[3]))

done = False
the = 0

pos1 = None

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    screen.fill((0,0,0))
    for x in walls:
        x.draw()

    mousepos = pygame.mouse.get_pos()
    if pos1:
        temppos = [pos1[0],pos1[1]]
        tempmousepos = [mousepos[0],mousepos[1]]
        if pos1[0] > mousepos[0]:
            temppos[0] = mousepos[0]
            tempmousepos[0] = pos1[0]
        if pos1[1] > mousepos[1]:
            temppos[1] = mousepos[1]
            tempmousepos[1] = pos1[1]


        pygame.draw.rect(screen,(100,100,100),(temppos[0],temppos[1],abs(temppos[0]-tempmousepos[0]),abs(temppos[1]-tempmousepos[1])))

    if keyboard.is_pressed("2"):
        walltype = 2
    elif keyboard.is_pressed("1"):
        walltype = 1
    elif keyboard.is_pressed("3"):
        walltype = 3


    if ticker > 0:
        ticker -= 1


    if walltype == 1:
        pygame.draw.circle(screen,(100,0,0),(30,20),10)
    elif walltype == 2:
        pygame.draw.circle(screen,(0,100,0),(30,20),10)
    elif walltype == 3:
        pygame.draw.circle(screen,(100,100,100),(30,20),10)

    if keyboard.is_pressed("z") and ticker == 0:
        walls.pop()
        ticker = 10

    if keyboard.is_pressed("s"):
        with open(name, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            for x in walls[4:]:
                writer.writerow([x.pos1,x.pos2,x.type,x.on])
        listener.stop()
        pygame.quit()
        quit()


    pygame.display.flip()
    clock.tick(60)

listener.stop()
pygame.quit()
quit()
