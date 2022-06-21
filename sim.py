from types import NoneType
import numpy as np
import sys
import pygame
from pygame.locals import *


width = 50
height = width

class Pixel:
    color = pygame.Color(0,0,0)
    def neighbor_coords(coord):
        if coord[0] > width-2 or coord[1] > height-2:
            return []
        coords = [] 
        for i in np.array(range(3))-1:
            for j in np.array(range(3))-1:
                if i == j == 0:
                    continue
                coords.append((coord[0]+i, coord[1]+j))
        return coords
        
    def compute(grid, coord):
        pass

class Dirt(Pixel):
    color = pygame.Color(0,0,255) #pygame.Color(155,118,83)
    #def compute(coord):
    #    pass

class Food(Pixel):
    color = pygame.Color(0,255,0)
    pass

class Cell(Pixel):
    color = pygame.Color(255,0,0)
    ret = {'status': 0, 'data': []}
    def compute(grid,coord):
        coords = Pixel.neighbor_coords(coord)
        
        dirt_neighboors = []
        food_neighboors = []
        cell_neighboors = 0
        for location in coords:
            type = grid[location[0],location[1]]
            if d[type] == Cell:
                cell_neighboors+=1
                continue
            if d[type] == Food:
                food_neighboors.append(location)
                continue
            if d[type] == Dirt:
                dirt_neighboors.append(location)
                continue

        if cell_neighboors > 4:
            return {"status":1,"data":None}
        
        if len(food_neighboors) < 2:
            return {"status":1,"data":None}
        
        if len(dirt_neighboors) > 1:
            #print(dirt_neighboors)
            return {"status":2,"data":{'dirt':dirt_neighboors,'food':food_neighboors}}

        return Cell.ret
    pass

d = {
    0: Dirt,
    1: Food,
    2: Cell
}

class Game:
    def __init__(self) -> None:
        pass

#grid = np.random.random_integers(low= 0, high=len(d), size=(width, height))
fps = 20
FramePerSec = pygame.time.Clock()
quit = 0
scale = 10

def main():
    pygame.init()
    DISPLAY_SURF = pygame.display.set_mode((width*scale,height*scale))
    grid = np.random.randint(len(d), size=(width,height))

    while not quit:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        nugrid = grid.copy()
        for x in range(width):
            for y in range(height):
                ret = d[grid[x][y]].compute(grid,(x,y))
                if not type(ret) == NoneType:
                    if ret['status'] == 2:
                        cloc = ret['data']['dirt'][np.random.randint(len(ret['data']['dirt']))]
                        floc = ret['data']['food'][np.random.randint(len(ret['data']['food']))]
                        nugrid[cloc[0],cloc[1]] = 2
                        nugrid[floc[0],floc[1]] = 0
                    if ret['status'] == 1:
                        nugrid[x][y] = 1
                r = pygame.Rect([x*scale,y*scale],[scale,scale])
                pygame.draw.rect(DISPLAY_SURF, color=d[grid[x][y]].color, rect=r)
        grid = nugrid
        FramePerSec.tick(fps)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()