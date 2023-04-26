import pygame
import math
import time

pygame.init()

screenWidth = 1280
screenHeight = 720
pendulumnLen = 100
pendulumnMass = 1

screen = pygame.display.set_mode((screenWidth, screenHeight))
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
    def __init__(self) -> None:
        self.velocity = 0
        self.acceleration = 0
        self.friction= 0.5
        self.colour = (136, 8, 8)
        self.length = 50
        self.height = 10
        self.x = 0
        self.y = 0
        self.borderWidth = 10

    def draw(self):
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

        self.x += self.velocity 
        self.acceleration=0

    def getVelocity(self):
        return self.velocity


myPendulumn = pendulumn(mass=2, pendulumnLen=100)
myPlat = platform()


def drawAll():
    screen.fill((93, 63, 211))
    myPendulumn.draw(point=myPlat.getPos())
    myPlat.draw()


def playerMove(direction,speed):
    if direction == 'left':
        speed = -speed
    myPlat.accelerate(speed)
    


myPendulumn.setAngle(math.radians(85))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame

    # myPlat.move(1)
    # myPendulumn.applyForce(0.0001, math.radians(0))

    # gravity
    myPendulumn.applyForce(0.0001, math.radians(270))

    # resistance of bearing
    netTangentileForce = myPendulumn.getTorque()
    if netTangentileForce < 0:
        resistance = 0.00005
    else:
        resistance = -0.00005

    if abs(netTangentileForce) < abs(resistance):
        myPendulumn.applyTorque(-netTangentileForce)
        myPendulumn.setAngle(math.radians(270))
    else:
        myPendulumn.applyTorque(resistance)


    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        playerMove('left',1)
    if keys[pygame.K_RIGHT]:
        playerMove('right',1)

    myPlat.move()
    myPendulumn.move()
    drawAll()

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

#time.sleep(0.001)

pygame.quit()
