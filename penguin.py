import pygame
import math
import time

pygame.init()

##declaring our perameters

#canvas
screenWidth = 1280
screenHeight = 720

#forces
ballbearingResistance = 0.00005
gravity=0.00025
l = 4000 #inverse factor of the platforms velocity that relates to the change in torque

#platform params
platformRange = 500
platformFriction = 0.5
platformSpeed = 0.75

#pendulumn params
pendulumnMass=3
pendulumnLen = 100


screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Penguins and Pendulumns')
clock = pygame.time.Clock()
running = True


class pendulumn:
    def __init__(self, mass, pendulumnLen) -> None:
        self.angle = math.radians(90)
        self.colour = (15, 66, 51)
        self.radius = 7
        self.width = 0
        self.angularAcc = 0
        self.netTorque = 0
        self.mass = mass
        self.pendulumnLen = pendulumnLen

    def draw(self, point):
        pygame.draw.line(surface=screen, color=(247, 152, 98),
                         start_pos=point, end_pos=myPendulumn.getPos(point), width=3)
        pygame.draw.circle(surface=screen, color=self.colour,
                           width=self.width, radius=self.radius, center=self.getPos(point=point))
        

    def getPos(self, point):
        x = int(self.pendulumnLen * math.cos(self.angle) + point[0])
        y = int(point[1]-self.pendulumnLen * math.sin(self.angle))
        return x, y

    # def shiftDist(self, x, y):
    #     self.x = self.x+x
    #     self.y = self.y+y

    def setAngle(self, angle):
        self.angle = angle

    def getAngle(self):
        return self.angle

    def applyForce(self, magnitude, direction):
        self.netTorque += pendulumnLen * \
            magnitude * math.sin(direction-self.angle)

    def getTorque(self):
        return self.netTorque

    def applyTorque(self, magnitude):
        self.netTorque += magnitude

    def move(self):

        self.angle = self.netTorque / self.mass + self.angle


class platform:
    def __init__(self, range,friction) -> None:
        self.velocity = 0
        self.acceleration = 0
        self.friction= friction
        self.colour = (136, 8, 8)
        self.length = 50
        self.height = 10
        self.x = 0
        self.y = 0
        self.borderWidth = 10
        self.range = range
        self.rangeColour = (172, 131, 247)

    def draw(self):
        #draw outer rang box
        pygame.draw.rect(surface=screen, color=self.rangeColour, rect=pygame.Rect(
            int(screenWidth/2 - self.range/2), screenHeight/2+int(self.y), self.range, self.height), border_radius=self.borderWidth)
        #draw platform
        pygame.draw.rect(surface=screen, color=self.colour, rect=pygame.Rect(
            int(screenWidth/2 - self.length/2+self.x), screenHeight/2+int(self.y), self.length, self.height), border_radius=self.borderWidth)

    def getPos(self):
        centerX = self.x + screenWidth/2 
        centerY = self.y + self.height/2 + screenHeight/2
        return centerX, centerY
    
    def accelerate(self,force):
        self.acceleration=force

    def move(self):
        self.velocity += self.acceleration
        
        if abs(self.velocity)<self.friction:#not going with a greater force than friction
            self.velocity=0
        if self.velocity>0:#going forwards
            self.velocity-=self.friction
        if self.velocity<0:#going backwards
            self.velocity+=self.friction

        #if within range
        if (abs(self.x+self.velocity)+self.length/2)>self.range/2:
            if (self.x+self.velocity)>0:
                self.x=self.range/2-self.length/2
            else:
                self.x=self.length/2-self.range/2
            self.velocity=0
        else:
            self.x += self.velocity 
    
        self.acceleration=0

    def getVelocity(self):
        return self.velocity
    
    def getAcceleration(self):
        return self.acceleration


myPendulumn = pendulumn(mass=pendulumnMass, pendulumnLen=pendulumnLen)
myPlat = platform(range=platformRange, friction=platformFriction)
timeStart = time.time()



def drawAll(time,score):
    backgroundColour = (93, 63, 211)
    #create blank screen
    screen.fill(backgroundColour)

    #draw pendulumn and platform 
    myPendulumn.draw(point=myPlat.getPos())
    myPlat.draw()

    #render time
    font = pygame.font.Font('freesansbold.ttf', 24)
    text = font.render(f'Time (s): {time}', True, (0, 0, 128),backgroundColour)
    textRect = text.get_rect()
    textRect.bottomleft = (0,screenHeight)
    screen.blit(text, textRect)

    #render score
    font = pygame.font.Font('freesansbold.ttf', 24)
    text = font.render(f'Score: {score}%', True, (0, 0, 128),backgroundColour)
    textRect = text.get_rect()
    textRect.bottomleft = (0,screenHeight-30)
    screen.blit(text, textRect)

def playerMove(direction,speed):
    if direction == 'left':
        speed = -speed
    myPlat.accelerate(speed)
    
    #if going left the pendulumn is going to want to turn clockwise resulting in a negative torque which will be roughly proportional to the platforms velocity
    myPendulumn.applyTorque((myPlat.getVelocity()+myPlat.getAcceleration())/l)     #dont need an if here because the platforms Vf wioll be negative if we're going left
    
    


myPendulumn.setAngle(math.radians(85))
cycles=0
cyclesAbove=0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame

    # gravity
    myPendulumn.applyForce(gravity, math.radians(270))

    # resistance of bearing
    netTangentileForce = myPendulumn.getTorque()

    if netTangentileForce < 0:
        resistance = ballbearingResistance
    else:
        resistance = -ballbearingResistance

    if abs(netTangentileForce) < abs(resistance):
        myPendulumn.applyTorque(-netTangentileForce)
        if 269<math.radians(myPendulumn.getAngle())<271 or -89>math.radians(myPendulumn.getAngle())>-91:
            myPendulumn.setAngle(math.radians(270))
    else:
        myPendulumn.applyTorque(resistance)


    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        playerMove('left',platformSpeed)
    if keys[pygame.K_RIGHT]:
        playerMove('right',platformSpeed)

    #now we have calculated everything since the previous cycle we want to change to our new values
    myPlat.move()
    myPendulumn.move()
    
    cycles+=1
    if myPendulumn.getPos(myPlat.getPos())[1]<myPlat.getPos()[1]: #if pendulumnabove platform (remember y axis is inverted on the canvas)
        cyclesAbove+=1
    
    drawAll(time=round(float(time.time())-timeStart,2),score=round(100*cyclesAbove/cycles))

    #pygame draws wierdly so we want to flip it
    pygame.display.flip()


    clock.tick(60)  # limits FPS to 60

#time.sleep(0.001)

pygame.quit()
