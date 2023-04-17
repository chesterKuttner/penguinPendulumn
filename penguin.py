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
        self.radius = 10
        self.width = 4
        self.angularAcc = 0
        self.netTorque = 0
        self.mass = mass
        self.pendulumnLen = pendulumnLen

    def draw(self, point):
        pygame.draw.circle(surface=screen, color=self.colour,
                           width=self.width, radius=self.radius, center=self.getPos(point=point))
        pygame.draw.line(surface=screen, color=(247, 152, 98),
                         start_pos=point, end_pos=myPendulumn.getPos(point), width=3)

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
        self.colour = (136, 8, 8)
        self.length = 50
        self.height = 10
        self.x = screenWidth/2 - self.length/2
        self.y = screenHeight/2
        self.borderWidth = 10

    def draw(self):
        pygame.draw.rect(surface=screen, color=self.colour, rect=pygame.Rect(
            int(self.x), int(self.y), self.length, self.height), border_radius=self.borderWidth)

    def getPos(self):
        centerX = self.x + self.length/2
        centerY = self.y + self.height/2
        return centerX, centerY

    def move(self, speed):
        self.x += speed


myPendulumn = pendulumn(mass=2, pendulumnLen=100)
myPlat = platform()


def drawAll():
    screen.fill((93, 63, 211))
    myPendulumn.draw(point=myPlat.getPos())
    myPlat.draw()


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
    else:
        myPendulumn.applyTorque(resistance)

    myPendulumn.move()
    drawAll()

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

    time.sleep(0.001)

pygame.quit()
