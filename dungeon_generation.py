import spritemap
import random
import app
from tkinter import *  # pylint: disable=unused-wildcard-import


class Tile:
    # Class to store which sprite is held at a location on the tilemap specified by (x, y)
    # Also stores a decided variable which is used when generating the tilemap
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.decided = False
        self.sprite = None


class TileMap:
    # Tilemap class to store a list of tiles, this structure hold the data about a DNDUNGEON map
    def __init__(self, tile_count, spritemap):
        self.width = tile_count
        self.height = tile_count
        self.tiles = list(())
        # Spritemap defines the set of sprites that the tilemap is made from
        self.spritemap = spritemap

        # Add a grid of blank tiles
        for y in range(tile_count):
            for x in range(tile_count):
                self.tiles.append(Tile(x, y))

    # Get the tile at position (x, y)
    def get_tile(self, x, y):
        # Check to make sure the tile is valid
        if(x < self.width and x >= 0 and y < self.width and y >= 0):
            return self.tiles[y * self.width + x]
        else:
            return None


def get_decided(value, tiles):
    # Gets all tiles in a list with a decided value that is the same as value
    output = list(())

    for tile in tiles:
        if tile.decided == value:
            output.append(tile)

    return output


def get_possible_placements(tilemap):
    # List to store every possible sprite placement that could occur
    # Elements take the form of [<Tile>, <List of sprite indexes that can go on that tile>]
    possible_placements = list(())

    # Get every undecided tile
    for tile in get_decided(False, tilemap.tiles):
        tile_possibilities = get_tile_possibilities(tilemap, tile)
        if tile_possibilities != None:
            possible_placements.append(tile_possibilities)

    return possible_placements

def get_tile_possibilities (tilemap, tile):
    # Store each side in temporary variables
    right_tile = tilemap.get_tile(tile.x+1, tile.y)
    left_tile = tilemap.get_tile(tile.x-1, tile.y)
    up_tile = tilemap.get_tile(tile.x, tile.y+1)
    down_tile = tilemap.get_tile(tile.x, tile.y-1)

    # Check each side to see if the it has been decided
    # If said side has been decided already then we get the list of possibilities that the current tile can be
    # Otherwise that side has not been decided or doesn't exist which means the tile we are currently looking at can be any sprite
    if right_tile != None and right_tile.decided == True:
        right_possibilities = tilemap.spritemap.sprites[right_tile.sprite].left
    else:
        right_possibilities = range(0, tilemap.spritemap.sprite_count)

    if left_tile != None and left_tile.decided == True:
        left_possibilities = tilemap.spritemap.sprites[left_tile.sprite].right
    else:
        left_possibilities = range(0, tilemap.spritemap.sprite_count)

    if up_tile != None and up_tile.decided == True:
        up_possibilities = tilemap.spritemap.sprites[up_tile.sprite].down
    else:
        up_possibilities = range(0, tilemap.spritemap.sprite_count)

    if down_tile != None and down_tile.decided == True:
        down_possibilities = tilemap.spritemap.sprites[down_tile.sprite].up
    else:
        down_possibilities = range(0, tilemap.spritemap.sprite_count)

    # We then get the intersection of all the sides possibilities.
    # Eg.  if the right side can have sprites [0, 1, 2] but the left side will only allow sprites [0, 2]
    #      we return the intersection of these two sets [0, 2]
    possible_placements_tile = list(set(right_possibilities) & set(
        left_possibilities) & set(up_possibilities) & set(down_possibilities))

    # Finally only add this tile's possible sprites to the possible_placements list if it has at least one possible sprite
    if len(possible_placements_tile) > 0:
        return [tile, possible_placements_tile]
    else:
        return None

def set_tile_neighbors_undecided(tilemap, tile, canvas):
    # Loop through neightbors or tile and set them to be undecided
    for x in range(-1, 2):
        for y in range(-1, 2):
            if abs(x) != abs(y):
                temp_tile = tilemap.get_tile(tile.x + x, tile.y + y)
                if temp_tile != None:
                    temp_tile.decided = False
                canvas.delete(("tile(" + str(tile.x + x) + "," + str(tile.y + y) + ")"))
                


def generate_tilemap(size, spritemap, canvas):
    canvas.delete("tilemap_image")

    tilemap = TileMap(size, spritemap)

    # Get all undecided tiles
    undecided = get_decided(False, tilemap.tiles)

    # Keep going as long as there are undecided tiles
    while len(undecided) > 0:
        # Index of the chosen tile in the undecided list
        tile_chosen = random.randint(0, len(undecided))-1
        possible = get_tile_possibilities(tilemap, undecided[tile_chosen])

        # If there are possible sprites that can be placed at the chosen tile's position
        if possible != None:
            # Choose a random possible sprite
            sprite_index = random.randint(0, len(possible[1]))-1
            sprite_chosen = possible[1][sprite_index]

            # Place the tile's data into the tilemap
            possible[0].sprite = sprite_chosen
            possible[0].decided = True

            # Put sprite onto the canvas
            app.display_tile(
                canvas, tilemap, possible[0].x, possible[0].y)
            canvas.update()
        else:
            # otherwise we select a random undecided tile and set its neighbors to undecided
            set_tile_neighbors_undecided(tilemap, undecided[tile_chosen], canvas)

        # Recalculate the undecided array
        undecided = get_decided(False, tilemap.tiles)
            
    return tilemap
