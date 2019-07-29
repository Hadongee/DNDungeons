from PIL import Image, ImageTk

class Sprite:
    def __init__ (self, index, filepath):
        self.index = index
        self.filepath = filepath
        self.image = Image.open(filepath)
        self.width, self.height = self.image.size

        self.right = list(())
        self.left = list(())
        self.up = list(())
        self.down = list(())

    def compare (self, other):
        self_pixels = self.image.load()
        other_pixels = other.image.load()

        # Check each side against other
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
    def __init__ (self, filepath, sprite_count):
        self.sprites = list(())
        self.sprite_count = sprite_count
        for i in range(sprite_count):
            self.sprites.append(Sprite(i, filepath+str(i)+".png"))
            for j in range(i+1):
                self.sprites[i].compare(self.sprites[j])
                if i != j:
                    self.sprites[j].compare(self.sprites[i])