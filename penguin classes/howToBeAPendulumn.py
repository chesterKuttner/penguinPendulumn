import math


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
      

    def getPos(self, point):
        x = int(self.pendulumnLen * math.cos(self.angle) + point[0])
        y = int(point[1]-self.pendulumnLen * math.sin(self.angle))
        return x, y


    def setAngle(self, angle):
        self.angle = angle

    def getAngle(self):
        return self.angle

    def applyForce(self, magnitude, direction):
        self.netTorque += self.pendulumnLen * \
            magnitude * math.sin(direction-self.angle)

    def getTorque(self):
        return self.netTorque

    def applyTorque(self, magnitude):
        self.netTorque += magnitude

    def move(self):

        self.angle = self.netTorque / self.mass + self.angle