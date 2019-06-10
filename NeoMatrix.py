import neopixel
import math

# declare NeoMatrix class, inherit NeoPixel library
class NeoMatrix(neopixel.NeoPixel):
    NEO_MATRIX_TOP = 0x00 # Pixel 0 is at top of matrix
    NEO_MATRIX_BOTTOM = 0x01 # Pixel 0 is at bottom of matrix
    NEO_MATRIX_LEFT = 0x00 # Pixel 0 is at left of matrix
    NEO_MATRIX_RIGHT = 0x02 # Pixel 0 is at right of matrix
    NEO_MATRIX_CORNER = 0x03 # Bitmask for pixel 0 matrix corner
    NEO_MATRIX_ROWS = 0x00 # Matrix is row major (horizontal)
    NEO_MATRIX_COLUMNS = 0x04 # Matrix is column major (vertical)
    NEO_MATRIX_AXIS = 0x04 # Bitmask for row/column layout
    NEO_MATRIX_PROGRESSIVE = 0x00 # Same pixel order across each line
    NEO_MATRIX_ZIGZAG = 0x08 # Pixel order reverses between lines
    NEO_MATRIX_SEQUENCE = 0x08 # Bitmask for pixel line order

    NEO_TILE_TOP = 0x00 # First tile is at top of matrix
    NEO_TILE_BOTTOM = 0x10 # First tile is at bottom of matrix
    NEO_TILE_LEFT = 0x00 # First tile is at left of matrix
    NEO_TILE_RIGHT = 0x20 # First tile is at right of matrix
    NEO_TILE_CORNER = 0x30 # Bitmask for first tile corner
    NEO_TILE_ROWS = 0x00 # Tiles ordered in rows
    NEO_TILE_COLUMNS = 0x40 # Tiles ordered in columns
    NEO_TILE_AXIS = 0x40 # Bitmask for tile H/V orientation
    NEO_TILE_PROGRESSIVE = 0x00 # Same tile order across each line
    NEO_TILE_ZIGZAG = 0x80 # Tile order reverses between lines
    NEO_TILE_SEQUENCE = 0x80 # Bitmask for tile line order

    # class constructor for a single matrix
    def __init__(self, matrix_w, matrix_h, pin, type, tile_w=1, tile_h=1, bpp=3, brightness=1.0, auto_write=True, pixel_order=None):
        neopixel.NeoPixel.__init__(self, pin, (tile_w*tile_h)*(matrix_w*matrix_h), bpp=bpp, brightness=brightness, auto_write=auto_write, pixel_order=pixel_order)
        self.matrixWidth = matrix_w
        self.matrixHeight = matrix_h
        self.type = type
        self.tileWidth = tile_w
        self.tileHeight = tile_h
        self._width = matrix_w*tile_w
        self._height = matrix_h*tile_h

    def drawPixel(self, x, y, color):
        # If x ot y coordinate is out of bounds, return
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            return

        tileOffset = 0
        corner = self.type & self.NEO_MATRIX_CORNER

        # multiple tiled matrices
        if self.tileWidth > 1 or self.tileHeight > 1:
            minor = math.floor(x / self.matrixWidth)
            major = math.floor(y / self.matrixHeight)

            x = x - (minor * self.matrixWidth)
            y = y - (major * self.matrixHeight)

            if self.type & self.NEO_TILE_RIGHT:
                minor = self.tileWidth - 1 - minor
            if self.type & self.NEO_TILE_BOTTOM:
                major = self.tileHeight -1 - major

            if (self.type & self.NEO_TILE_AXIS) == self.NEO_TILE_ROWS:
                majorScale = self.tileWidth
            else:
                minor, major = major, minor
                majorScale = self.tileHeight

            if (self.type & self.NEO_TILE_SEQUENCE) == self.NEO_TILE_PROGRESSIVE:
                tile = major * majorScale + minor
            else:
                if major & 1:
                    corner ^= self.NEO_MATRIX_CORNER
                    tile = (major + 1) * majorScale - 1 - minor
                else:
                    tile = major * majorScale + minor

            tileOffset = tile * (self.matrixWidth * self.matrixHeight)

        minor = x
        major = y

        if(corner & self.NEO_MATRIX_RIGHT):
            minor = self.matrixWidth - 1 - minor
        if(corner & self.NEO_MATRIX_BOTTOM):
            major = self.matrixHeight - 1 - major

        if (self.type & self.NEO_MATRIX_AXIS) == self.NEO_MATRIX_ROWS:
            majorScale = self.matrixWidth
        else:
            minor, major = major, minor
            majorScale = self.matrixHeight


        if(self.type & self.NEO_MATRIX_SEQUENCE) == self.NEO_MATRIX_PROGRESSIVE:
            pixelOffset = (major * majorScale) + minor
        else:
            if major & 1:
                pixelOffset = (major + 1) * majorScale - 1 - minor
            else:
                pixelOffset = major * majorScale + minor

        self.__setitem__(tileOffset + pixelOffset, color)
