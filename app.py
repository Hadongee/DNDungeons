from tkinter import *  # pylint: disable=unused-wildcard-import
import spritemap
import dungeon_generation
from PIL import Image, ImageTk
import math

# VARIABLES TO EDIT (In the future these will be GUI options)

# Number of tiles
grid_count = 30

canvas_size = 800
canvas_border_size = 0

# Spritemap info
sprites_filepath = 'spritemap/0/'
sprites_count = 37

# Other helpful variables to have stored (DO NOT EDIT)
grid_size = (canvas_size-1)/grid_count
spritemap = spritemap.SpriteMap(sprites_filepath, sprites_count)
tilemap = None


def main():
    print("Running...")

    # Application Setup
    root = Tk()
    root.geometry("820x890")
    root.winfo_toplevel().title("DNDungeonWorldGenerator")

    # Title label
    title = Label(root, anchor=CENTER, text="DNDungeonWorldGenerator",
                  pady=5, font=("Helvetica", 30))
    title.pack()

    # Map canvas
    canvas = Canvas(root, height=canvas_size, width=canvas_size,
                    bg="white", relief="solid", borderwidth=canvas_border_size)
    canvas.pack()
    canvas.update()

    # Button to generate a new tilemap
    generate_button = Button(root, text="Generate",
                             command=lambda: generate_map(canvas))
    generate_button.pack()

    init_grid(canvas)

    mainloop()


def init_grid(canvas):
    # Initialize the grid lines

    # Instantiate the underlying grid lines
    for y in range(grid_count):
        for x in range(grid_count):
            canvas.create_rectangle(x*grid_size+2,
                                    y*grid_size+2,
                                    (x+1)*grid_size+2,
                                    (y+1)*grid_size+2,
                                    outline="black", width=1, tags="gridline")


def reset_grid(canvas):
    # Call this after you add anything to the canvas to raise the grid lines back to the top
    canvas.tag_raise("gridline")


def generate_map(canvas):
    # Generates a tilemap from the spritemap
    global tilemap
    tilemap = dungeon_generation.generate_tilemap(grid_count, spritemap)
    display_tilemap(canvas, tilemap)
    reset_grid(canvas)


def display_tilemap(canvas, tilemap):
    # Displays the tilemap on the canvas

    # Loop through every tile
    for y in range(grid_count):
        for x in range(grid_count):
            # Open the sprite we are going to load to the canvas
            image = Image.open(
                tilemap.spritemap.sprites[tilemap.tiles[y * grid_count + x].sprite].filepath)
            # Resize the sprite to the grid size
            image = image.resize(
                (math.ceil(grid_size), math.ceil(grid_size)), Image.NEAREST)
            # Create a copy of the PhotoImage on the tile so that it does not get garbage collected. Without this the image will not show on the canvas
            tilemap.tiles[y * grid_count +
                          x].photoimg = ImageTk.PhotoImage(image)

            # Place the image onto the canvas
            canvas.create_image(x*grid_size+2+grid_size/2,
                                y*grid_size+2+grid_size/2,
                                image=tilemap.tiles[y *
                                                    grid_count + x].photoimg
                                )


main()
