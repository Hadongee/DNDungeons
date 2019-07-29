from tkinter import * # pylint: disable=unused-wildcard-import
import spritemap
import dungeon_generation
from PIL import Image, ImageTk
import math

grid_count = 20
canvas_size = 800
canvas_border_size = 0
grid_size = (canvas_size-1)/grid_count

spritemap = spritemap.SpriteMap('spritemap/0/', 37)
tilemap = None

def main():
    print("Running...")

    # Application Setup
    root = Tk()
    root.geometry("820x890")
    root.winfo_toplevel().title("DNDungeonWorldGenerator")

    # Title label
    title = Label(root, anchor=CENTER, text="DNDungeonWorldGenerator", pady=5, font=("Helvetica", 30))
    title.pack()

    # Map canvas
    canvas = Canvas(root, height=canvas_size, width=canvas_size, bg="white", relief="solid", borderwidth=canvas_border_size)
    canvas.pack()
    canvas.update()

    generate_button = Button(root, text="Generate", command=lambda: generate_map(canvas))
    generate_button.pack()

    init_grid(canvas)

    mainloop()

# Initialize the grid lines
def init_grid(canvas):
    print("Initializing Grid...")

    # Instantiate the underlying grid lines
    for y in range(grid_count):
        for x in range(grid_count):
            canvas.create_rectangle(x*grid_size+2, 
                                    y*grid_size+2, 
                                    (x+1)*grid_size+2, 
                                    (y+1)*grid_size+2, 
                                    outline="black", width=1, tags="gridline")

# Call this after you add anything to the canvas to raise the grid lines back to the top
def reset_grid(canvas):
    canvas.tag_raise("gridline")

# Generates a tilemap from the spritemap
def generate_map(canvas):
    print("Generating map...")
    global tilemap
    tilemap = dungeon_generation.generate_tilemap(grid_count, spritemap)
    display_tilemap(canvas, tilemap)
    reset_grid(canvas)

# Displays the tilemap on the canvas
def display_tilemap(canvas, tilemap):
    print("Displaying map...")
    for y in range(grid_count):
        for x in range(grid_count):
            image = Image.open(tilemap.spritemap.sprites[tilemap.tiles[y * grid_count + x].sprite].filepath)
            image = image.resize((math.ceil(grid_size), math.ceil(grid_size)), Image.NEAREST)
            tilemap.tiles[y * grid_count + x].photoimg = ImageTk.PhotoImage(image)

            canvas.create_image(x*grid_size+2+grid_size/2, 
                                y*grid_size+2+grid_size/2,
                                image=tilemap.tiles[y * grid_count + x].photoimg
                                )

main()