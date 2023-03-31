import pygame
import math

pygame.init()

screenWidth = 1280
screenHeight = 720
pendulumnLen = 100

screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()
running = True


class circle:
    def __init__(self) -> None:
        self.x = screenWidth/2
        self.y = screenHeight/2 - pendulumnLen
        self.colour = (15, 66, 51)
        self.radius = 10
        self.width = 4

    def draw(self):
        pygame.draw.circle(surface=screen, color=self.colour,
                           width=self.width, radius=self.radius, center=(int(self.x), int(self.y)))

    def setPos(self, newX, newY):
        self.x = newX
        self.y = newY

    def getPos(self):
        return self.x, self.y

    def shiftDist(self, x, y):
        self.x = self.x+x
        self.y = self.y+y

    def shiftAngle(self, point, rad):
        # necessary to get xy co-ordibnatesaround the origin
        tempX = self.x - screenWidth/2
        tempY = self.y - screenHeight/2

        print(tempX, tempY)

        if tempX == 0:
            ACO = math.radians(90)
        else:
            ACO = math.asin(tempY/tempX)
        BCO = ACO-rad

        print('ACO', math.degrees(ACO))
        print('BCO', math.degrees(BCO))

        self.x = 100*math.sin(BCO)+point[0]
        self.y = 100*math.cos(BCO)+point[1]


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


myCirc = circle()
myPlat = platform()


def drawAll():
    screen.fill((93, 63, 211))
    myCirc.draw()
    myPlat.draw()
    pygame.draw.line(surface=screen, color=(247, 152, 98),
                     start_pos=myPlat.getPos(), end_pos=myCirc.getPos(), width=5)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    drawAll()

    myCirc.shiftAngle(point=myPlat.getPos(), rad=math.radians(1))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(30)  # limits FPS to 60

pygame.quit()
