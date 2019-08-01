from PIL import Image, ImageTk
import pickle

FILETYPE = ".sprm"

class Sprite:
    # Sprite class for holding image filepath and sprite index in a spritemap
    def __init__(self, index, filepath):
        self.index = index
        self.filepath = filepath
        self.image = Image.open(self.filepath)
        self.width, self.height = self.image.size

        # List of which sprite indexes can be connected to each side
        self.right = list(())
        self.left = list(())
        self.up = list(())
        self.down = list(())

    # Compare this sprite to another sprite to determine which side it can be connected to (if any)
    def compare(self, other):
        self_pixels = self.image.load()
        other_pixels = other.image.load()

        # Check each side against the other sprites opposite side
        # If the pixels match up on adjoining sides we add that sprite index to the correlated list
        for i in range(self.height):
            if self_pixels[0, i] != other_pixels[other.width-1, i]:
                break
        else:
            self.left.append(other.index)

        for i in range(self.height):
            if self_pixels[self.width-1, i] != other_pixels[0, i]:
                break
        else:
            self.right.append(other.index)

        for i in range(self.width):
            if self_pixels[i, self.height-1] != other_pixels[i, 0]:
                break
        else:
            self.up.append(other.index)

        for i in range(self.width):
            if self_pixels[i, 0] != other_pixels[i, other.height-1]:
                break
        else:
            self.down.append(other.index)


class SpriteMap:
    # This class handles a set of sprites from which the tilemap can be made out of
    # It holds data about sprites and which sprites they can connect to
    def __init__(self, filepath, sprite_count):
        self.sprites = list(())
        self.sprite_count = sprite_count

        # Loop through all sprites and add them to the sprites array
        for i in range(sprite_count):
            self.sprites.append(Sprite(i, filepath+str(i)+".png"))
            # Determine which sprites can connect to other sprites
            for j in range(i+1):
                # Compare the current sprite to the other sprites
                self.sprites[i].compare(self.sprites[j])
                # If the comparison is not between the same sprite then compare the other sprite to the current sprite as well
                if i != j:
                    self.sprites[j].compare(self.sprites[i])

def save_spritemap(spritemap, filename):
    with open(filename + FILETYPE, "wb") as spritemap_file:
        pickle.dump(spritemap, spritemap_file)

def load_spritemap(filename):
    with open(filename + FILETYPE, "rb") as spritemap_file:
        spritemap = pickle.load(spritemap_file)
        return spritemap