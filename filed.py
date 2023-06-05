import pygame


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








def calculation(n, pos1, xdeviance, ydeviance,sample):
                return abs(math.ceil(pos1[0] + xdeviance*(n/(sample*2)))), abs(math.ceil(pos1[1] + (ydeviance*(n/(sample*2)))))

def drawline(pos1,pos2,r,g,b):
    xdeviance = pos2[0] - pos1[0]
    ydeviance = pos2[1] - pos1[1]

    samplesize = 50


    for n in range(samplesize*2):
        collision(calculation(n+1, pos1, xdeviance,ydeviance,samplesize))


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
size = (1660, 1050)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
done = False
clock = pygame.time.Clock()

walls = []

walls.append(wall((size[0]/2,0),size))

walls.append(wall((0,0),(40,40)))

walls.append(wall((60,60),(100,100)))

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)

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


    for obj in walls:
        obj.draw()


    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)



# Close the window and quit.
pygame.quit()
