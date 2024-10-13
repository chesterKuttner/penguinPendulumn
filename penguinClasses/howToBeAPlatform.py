

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

    def getPos(self):
        return self.x, self.y

    def getPosOnScreen(self, screenWidth,screenHeight):
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



