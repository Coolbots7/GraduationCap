import time
import board
import neopixel
from NeoMatrix import NeoMatrix
from game_of_life import GameOfLife
import numpy as np

PIXEL_PIN = board.D18
# The order of the pixel colors - RGB or GRB.
ORDER = neopixel.GRB
BRIGHTNESS = 1.0
AUTO_WRITE = False
MATRIX_WIDTH = 8
MATRIX_HEIGHT = 8
TILE_WIDTH = 3
TILE_HEIGHT = 3

matrix = NeoMatrix(MATRIX_WIDTH, MATRIX_HEIGHT, PIXEL_PIN, NeoMatrix.NEO_MATRIX_TOP | NeoMatrix.NEO_MATRIX_LEFT | NeoMatrix.NEO_MATRIX_COLUMNS | NeoMatrix.NEO_MATRIX_ZIGZAG | NeoMatrix.NEO_TILE_TOP | NeoMatrix.NEO_TILE_LEFT | NeoMatrix.NEO_TILE_ZIGZAG | NeoMatrix.NEO_TILE_COLUMNS,
    tile_w = TILE_WIDTH, tile_h = TILE_HEIGHT, brightness=BRIGHTNESS, auto_write=AUTO_WRITE, pixel_order=ORDER)

# matrix.fill((0,0,0))
# matrix.show()

color = (255,0,0)
wait = 1.0/5.0

# while True:
    # for i in range((MATRIX_HEIGHT*TILE_HEIGHT)-1):
    #     matrix.fill((0,0,0))
    #     matrix.drawPixel(0, i, color)
    #     matrix.show()
    #     time.sleep(wait)
    #
    # for i in range((MATRIX_WIDTH*TILE_WIDTH)-1):
    #     matrix.fill((0,0,0))
    #     matrix.drawPixel(i, (MATRIX_HEIGHT*TILE_HEIGHT)-1, color)
    #     matrix.show()
    #     time.sleep(wait)
    #
    #
    # for i in range((MATRIX_HEIGHT*TILE_HEIGHT)-1):
    #     matrix.fill((0,0,0))
    #     matrix.drawPixel((MATRIX_WIDTH*TILE_WIDTH)-1, (MATRIX_HEIGHT*TILE_HEIGHT)-1-i, color)
    #     matrix.show()
    #     time.sleep(wait)
    #
    # for i in range((MATRIX_WIDTH*TILE_WIDTH)-1):
    #     matrix.fill((0,0,0))
    #     matrix.drawPixel((MATRIX_WIDTH*TILE_WIDTH)-1-i, 0, color)
    #     matrix.show()
    #     time.sleep(wait)


GOL = GameOfLife(MATRIX_WIDTH*TILE_WIDTH, MATRIX_HEIGHT*TILE_HEIGHT)
while True:
    grid = GOL.Step()

    if (np.sum(grid)/GOL.ON) <= 70.0:
        matrix.fill((0,0,0))
        matrix.show()
        time.sleep(wait*2)
        grid = GOL.Reset()

    for i in range(GOL.WIDTH):
        for j in range(GOL.HEIGHT):
            if grid[i, j] == GOL.ON:
                matrix.drawPixel(i, j, color)
            else:
                matrix.drawPixel(i, j, (0,0,0))

    matrix.show()
    time.sleep(wait)
