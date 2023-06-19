
    #imports. probably the most important part of this code cause they do 90% of the work
    import pygame
    import keyboard
    import math
    import csv
    import ast
    import numpy as np
    import pyopencl as cl
    import random


    platforms = cl.get_platforms()
    ctx = cl.Context(
        dev_type = cl.device_type.ALL,
        properties=[(cl.context_properties.PLATFORM, platforms[0])]
    )

    prg = cl.Program(ctx, """
        __kernel void balls(
            __global const int *arraying    , __global int *res_g
            ) {
                //int gid = get_global_id(0);
                int width = get_global_size(0);
                int height = get_global_size(1);
                int channels = get_global_size(2);
                int weird_size = height * channels;

                int x = get_global_id(0);
                int y = get_global_id(1);
                int c = get_global_id(2);

                int id = c + y*channels + x*weird_size;
                //res_g[gid] = (arraying[gid]);


                uint lolr = 0;


                for (int ex = (x-1); ex <= (x+1); ex++) {
                    for (int wh = (y-1); wh <= (y+1); wh++) {
                        lolr += arraying[ex + wh*channels + ex*weird_size ];
                    }
                }
                lolr /= 9;

                res_g[id] = lolr;

                //res_g[gid] = (arraying[gid]);
            }
        """).build()
    queue = cl.CommandQueue(ctx)
    mf = cl.mem_flags


    def blur(array):

        arraying = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=array)

        res_g = cl.Buffer(ctx, mf.WRITE_ONLY, array.nbytes)
        knl = prg.balls
        knl(queue, array.shape, None, arraying, res_g)

        res_np = np.empty_like(array)
        cl.enqueue_copy(queue,res_np,res_g)
        nuts = res_np.reshape(array.shape)

        return nuts

    def drawline1(pos1,pos2,r,g,b):

        ydeviance = pos2[1] - pos1[1]

        xdeviance = pos2[0] - pos1[0]
        global brush
        #editable variables
        if brush < 4:
            samplesize = 50
        else:
             samplesize = math.ceil(abs(xdeviance+ydeviance)/10)


        for n in range(samplesize*2):
            drawatlocation(calculation1(n+1, pos1, xdeviance,ydeviance,samplesize),r,g,b)

    def drawatlocation(position,r1,g1,b1):
        global array
        global brush
        if not position[0] > len(array)-math.ceil(brush/2) and not position[1] > len(array[1])-math.ceil(brush/2):
            for x in range(brush):
                for y in range(brush):
                    if not keyboard.is_pressed('b'):
                        array[position[0]+int((x-math.floor(brush/2)))][position[1]+(y-math.floor(brush/2))] = [r1,g1,b1]





    #class of walls. use this to initalize a wall with startpoint and endpoint os pos1 and 2.
    class wall():
        #set the coords and do some math for the size
        def __init__(self, pos1, pos2):

            self.pos1 = pos1
            self.pos2 = pos2

            self.type = 1

            self.on = 1

            self.sizex = abs(pos1[0]-pos2[0])
            self.sizey = abs(pos1[1]-pos2[1])

        #if called draw self to screen. to be updated with .blit
        def draw(self):
            pygame.draw.rect(screen,RED,(self.pos1[0],self.pos1[1],self.sizex,self.sizey))

        #check if a point is inside of self, then return what side it hit. 1,2,3 or 4 for all 4 sides.
        def collision(self,point):
            if point[0] >= self.pos1[0] and point[0] <= self.pos2[0] and point[1] >= self.pos1[1] and point[1] <= self.pos2[1]:

                #i love abs()
                right = abs(point[0] - self.pos1[0])
                left = abs(point[0] - self.pos2[0])
                down = abs(point[1] - self.pos1[1])
                up = abs(point[1] - self.pos2[1])

                #bad code. thank god for the compiler
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

    #this is the class that is the green block. basically a wall but if i call collision() on it and it returns true, load the next level
    #subclass of wall, with new functions.
    class winnermode(wall):

        def __init__(self, pos1, pos2):
            super().__init__(pos1,pos2)
            self.type = 2
        def collision(self, point):
            #special 5 in the return.
            if point[0] >= self.pos1[0] and point[0] <= self.pos2[0] and point[1] >= self.pos1[1] and point[1] <= self.pos2[1]:
                return(True, 5)
            else:
                return(False,0)
        #same draw but with a different colour. didnt want to do more math for the colour.
        def draw(self):
            pygame.draw.rect(screen,GREEN,(self.pos1[0],self.pos1[1],self.sizex,self.sizey))


    class button(wall):

        def __init__(self, pos1, pos2):
            super().__init__(pos1,pos2)
            self.type = 2
        def collision(self, point):
            #special 5 in the return.
            if point[0] >= self.pos1[0] and point[0] <= self.pos2[0] and point[1] >= self.pos1[1] and point[1] <= self.pos2[1]:
                return(True, 6)
            else:
                return(False,0)
        #same draw but with a different colour. didnt want to do more math for the colour.
        def draw(self):
            pygame.draw.rect(screen,GREEN,(self.pos1[0],self.pos1[1],self.sizex,self.sizey))


    #this is a class to draw the lines that appear when the projectile moves forwards. doing this so they linger.
    class line():
        def __init__(self,pos1,pos2):
            self.pos1 = pos1
            self.pos2 = pos2
            #this changes how long the lines linger after being created.
            self.timer = 40
        #call this every frame. fades the line by x amount, aswell as makes the line less thick. also rounds the end off the back of the line.

        #TO BE DONE: BLOOM AND SPECIAL NUMPY THINGS
        def update(self):
            #normalize the fade variable
            fade = self.timer/40
            #print(fade)

            #draw them with the normalized fade
            pygame.draw.line(screen, [255*fade,255*fade,255*fade], self.pos1, self.pos2, int(7*fade))
            pygame.draw.circle(screen,[255*fade,255*fade,255*fade], (self.pos1[0]+int(2*fade),self.pos1[1]+int(2*fade)) ,int(4*fade))

            #return if timer == 0 and line needs to be ended.
            if self.timer == 0:
                return True
            else:
                self.timer -= 1
                return False

    #the class that creates and updates the main thing in the game: the bullet. does a whole lot of things.
    class projectile():
        #define the regular variable. stuff like where it is and where its pointing too. direction is angle position is pos.
        #ticker is how long till the next move and timer is how long the bullet will live
        def __init__(self,pos,angle):
            self.pos = pos
            self.angle = angle
            self.ticker = 0
            self.timer = 2000

        #call this every frame.
        def update(self,distance, walls, iteration):
            #take the global lines and port it.
            global lines
            #tick the ticker
            if self.ticker != 0:
                self.ticker -= 1
            #get the next position to check. does this by using sin and cos rules in triangles. basically soh cah toa i use soh and cah lol
            x1 = distance * math.sin(self.angle)
            y1 = distance * math.cos(self.angle)

            #save a temporary position. use this later for math
            pos1 = self.pos
            #if the ticker is done ticking, start moving
            if self.ticker <= 0:
                #set collided back to false. this is a local variable so it actually just creates it lol
                collided = False
                #for every wall do a collision check of the new position( the last position of the bullet plus the distances we just calculated.)
                for obj in walls:
                    #this is the collision check here. outputs a touple with (ifhit , sidehit)
                    this = obj.collision([self.pos[0]+x1,self.pos[1]+y1])
                    #if hit
                    if this[0]:
                        #this is asking: is the block hit a "winnermode"object? if so, return winner
                        if this[1] == 5:
                            return "lol"
                        elif this[1] == 6:
                            return "button"
                        #if not winnermode set collided to true, find the collision pos, and the object hit and break the for loop. dont need to break it but it feels nicer
                        collided = True
                        collisionpos = [self.pos[0]+x1,self.pos[1]+y1]
                        collidedObj = obj
                        break

                #now if you broke the loop do some math to find the new angle. this took so long to implement lol
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

                    """ this doesnt work in python 3.9.10 =(  switch statements my beloved
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
                    #
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



    def load(level):
        global playerobj
        with open(level, 'r', newline='') as infile:
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
                elif peram[2] == 3:

                    playerobj = player(peram[0])


    playerobj = None

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


    def calculation1(n, pos1, xdeviance, ydeviance,sample):
                    return abs(math.ceil(pos1[0] + xdeviance*(n/(sample*2)))), abs(math.ceil(pos1[1] + (ydeviance*(n/(sample*2)))))

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

    r1,g1,b1 = 255,255,255
    pixeltotal = 8
    margin = 1
    brush = 2
    grid = []
    for x in range(math.ceil(size[0]/pixeltotal)+math.ceil(brush/2)+1):
        grid.append([])
        for y in range(math.ceil(size[1]/pixeltotal)+math.ceil(brush/2)+1):
            #change this to [0,0,0] for a black background
            grid[x].append([255,255,255])

    array = np.zeros(shape=(len(grid), len(grid[0]),3), dtype="uint8" )


    angle = 0

    buttonson = False

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
    levels = ["level1.csv","level2.csv","level3.csv","level4.csv"]
    levelcounter = 0

    load(levels[levelcounter])




    """
    with load('level1.csv', 'r', newline='') as infile:
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
    """






    # -------- Main Program Loop -------------------------------------------------------------------------------------------------------------------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(BLACK)

        drawline1((random.randint(0,len(grid[1])),random.randint(0,len(grid[0]))),(random.randint(0,len(grid[1])),random.randint(0,len(grid[0]))),r1,g1,b1)
        array = blur(array)

        ycounter = 0
        for y in range(math.ceil(size[0]/pixeltotal)):
            xcounter = 0
            for x in range(math.ceil(size[1]/pixeltotal)):
                pygame.draw.rect(screen,array[ycounter][xcounter],(1+(pixeltotal*y),(1+(x*pixeltotal)),pixeltotal-margin,pixeltotal-margin))
                xcounter += 1
            ycounter += 1

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

        if keyboard.is_pressed("esc"):
            bullets = []

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
                    levelcounter += 1
                    buttonson = False
                    load(levels[levelcounter])
                elif winner == "button":
                    bullers.remove(obj)
                    buttonson = True
                elif winner:
                    bullets.remove(obj)


        pygame.display.flip()
        # --- Limit to 60 frames per second

        clock.tick(60)



    # Close the window and quit.
    pygame.quit()
