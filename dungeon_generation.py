import spritemap
import random

class Tile:
    def __init__ (self, x, y):
        self.x = x
        self.y = y
        self.decided = False
        self.sprite = None

class TileMap:
    def __init__ (self, tile_count, spritemap):
        self.width = tile_count
        self.height = tile_count
        self.tiles = list(())
        self.spritemap = spritemap

        for y in range(tile_count):
            for x in range(tile_count):
                self.tiles.append(Tile(x, y))
    
    def get_tile (self, x, y):
        if(x < self.width and x >= 0 and y < self.width and y >= 0):
            return self.tiles[y * self.width + x]
        else:
            return None

def get_decided (value, tiles):
    output = list(())

    for tile in tiles:
        if tile.decided == value:
            output.append(tile)

    return output

def get_possible_placements (tilemap):
    possible_placements = list(())

    for tile in get_decided(False, tilemap.tiles):
        #Check each side
        right_tile = tilemap.get_tile(tile.x+1, tile.y)
        left_tile = tilemap.get_tile(tile.x-1, tile.y)
        up_tile = tilemap.get_tile(tile.x, tile.y+1)
        down_tile = tilemap.get_tile(tile.x, tile.y-1)

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

        possible_placements_tile = list(set(right_possibilities) & set(left_possibilities) & set(up_possibilities) & set(down_possibilities))

        if len(possible_placements_tile) > 0:
            possible_placements.append([tile, possible_placements_tile])
    
    return possible_placements

def set_tile_neighbors_undecided (tilemap, tile):
    for x in range(-1, 2):
        for y in range(-1, 2):
            temp_tile = tilemap.get_tile(tile.x + x, tile.y + y)
            if temp_tile != None:
                temp_tile.decided = False

def generate_tilemap(size, spritemap):
    tilemap = TileMap(size, spritemap)
    while len(get_decided(False, tilemap.tiles)) != 0:
        #Check if valid tile can be placed
        possible = get_possible_placements(tilemap)
        if len(possible) > 0:
            #If it can select a random one
            tile_chosen = random.randint(0, len(possible))-1
            sprite_index = random.randint(0, len(possible[tile_chosen][1]))-1
            sprite_chosen = possible[tile_chosen][1][sprite_index]
            
            #place it
            possible[tile_chosen][0].sprite = sprite_chosen
            possible[tile_chosen][0].decided = True
        #OTHERWISE we select a random undecided tile and set its neighbors to undecided
        else:
            undecided_tiles = get_decided(False, tilemap.tiles)
            undecided_index = random.randint(0, len(undecided_tiles))-1
            set_tile_neighbors_undecided(tilemap, undecided_tiles[undecided_index])

    return tilemap
