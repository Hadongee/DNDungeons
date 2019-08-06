import tilemap
import random

class Room:
    def __init__ (self, map, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        
        for y in range(top, bottom+1):
            for x in range(left, right+1):
                map.get_tile(x, y).solid = False
    
    def inside (self, x, y):
        if self.top <= y and self.bottom >= y and self.left <= x and self.right >= x:
            return True
        else:
            return False
    
    def inside_including_walls (self, x, y):
        if self.top-1 <= y and self.bottom+1 >= y and self.left-1 <= x and self.right+1 >= x:
            return True
        else:
            return False

def generate (width, height, room_count, max_room_attempts, min_room_size, max_room_size):
    print("Generating dungeon...")
    map = tilemap.Tilemap(width, height, True)
    rooms = list(())

    # Generate map in here
    for i in range(room_count):
        trial = 0
        while trial < max_room_attempts:
            
            room_top = random.randint(0, height-2)
            room_bottom = min(height-2, room_top + random.randint(min_room_size, max_room_size))
            room_left = random.randint(0, width-2)
            room_right = min(width-2, room_left + random.randint(min_room_size, max_room_size))

            print(("Trying to place room " + str(i) + " with rect(" + str(room_top) + ", " + str(room_bottom) + ", " + str(room_left) + ", " + str(room_right) + "), Trial:" + str(trial)))

            if checkRoomAllowed(room_top, room_bottom, room_left, room_right, rooms):
                print("Placing Room")
                rooms.append(Room(map, room_top, room_bottom, room_left, room_right))
                break
            else:
                print("Placement didn't work")
                trial += 1

    return map

def checkRoomAllowed (room_top, room_bottom, room_left, room_right, rooms):
    for y in range(room_top, room_bottom+1):
        for x in range(room_left, room_right+1):
            for room in rooms:
                if room.inside_including_walls(x, y):
                    return False
    else:
        return True