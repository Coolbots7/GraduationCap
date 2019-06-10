import numpy as np

class GameOfLife:
    ON = 255
    OFF = 0
    STATES = [ON, OFF]

    def __init__(self, width, height, density=0.2):
        self.WIDTH = width
        self.HEIGHT = height
        self.grid = np.random.choice(self.STATES, self.WIDTH*self.HEIGHT, p=[density, 1-density]).reshape(self.WIDTH, self.HEIGHT)

    def Reset(self, density=0.2):
        self.grid = np.random.choice(self.STATES, self.WIDTH*self.HEIGHT, p=[density, 1-density]).reshape(self.WIDTH, self.HEIGHT)
        return self.grid

    def Step(self):
        nextGrid = self.grid.copy()
        for i in range(self.WIDTH):
            for j in range(self.HEIGHT):
                total = int((self.grid[i, (j-1)%self.HEIGHT] + self.grid[i, (j+1)%self.HEIGHT] +
                         self.grid[(i-1)%self.WIDTH, j] + self.grid[(i+1)%self.WIDTH, j] +
                         self.grid[(i-1)%self.WIDTH, (j-1)%self.HEIGHT] + self.grid[(i-1)%self.WIDTH, (j+1)%self.HEIGHT] +
                         self.grid[(i+1)%self.WIDTH, (j-1)%self.HEIGHT] + self.grid[(i+1)%self.WIDTH, (j+1)%self.HEIGHT])/255)

                if self.grid[i, j] == self.ON:
                    if(total < 2) or (total > 3):
                        nextGrid[i, j] = self.OFF
                else:
                    if total == 3:
                        nextGrid[i, j] = self.ON

        self.grid[:] = nextGrid[:]
        return self.grid
