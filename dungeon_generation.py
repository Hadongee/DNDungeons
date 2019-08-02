import tilemap
import random

class Room:
    def __init__ (self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
    
    def inside (self, x, y):
        if self.top >= y and self.bottom <= y and self.left <= x and self.right >= x:
            return True
        else:
            return False

def generate (width, height, rooms, max_room_attempts):
    print("Generating dungeon...")
    map = tilemap.Tilemap(width, height, True)
    rooms = list(())

    # Generate map in here
    trial = 0
    for i in range(rooms):
        x = random.randrange(width)
        y = random.randrange(height)

    return map