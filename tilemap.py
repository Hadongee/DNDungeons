import tile

class Tilemap:
    def __init__ (self, width, height, initially_solid):
        self.tiles = list(())
        self.width = width
        self.height = height

        for y in range(height):
            for x in range(width):
                self.tiles.append(tile.Tile(x, y, y * width + x, initially_solid))

    def get_tile (self, x, y):
        return self.tiles[y * self.width + x]