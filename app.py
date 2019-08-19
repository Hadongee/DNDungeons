from tkinter import * # pylint: disable=unused-wildcard-import
from PIL import Image, ImageTk
import math
import dungeon_generation

# VARIABLES TO EDIT (In the future these will be GUI options)
# Number of tiles
grid_count = 100

canvas_size = 800
canvas_border_size = 0

# Other helpful variables to have stored (DO NOT EDIT)
grid_size = (canvas_size-1)/grid_count

frames = None

def main():
    print("Running...")

    # Application Setup
    root = Tk()
    root.geometry("1000x880")
    root.winfo_toplevel().title("DNDungeonWorldGenerator")

    global frames
    frames = Init_Frames(root)

    mainloop()

class Init_Frames:
    # create tkinter elements, place them in frames for origanisation and load them all into the window
    def __init__(self,master):
        self.fm_top = Frame(master)
        
        # Title label
        self.title = Label(self.fm_top, anchor=CENTER, text="DNDungeonWorldGenerator",
                      pady=5, font=("Helvetica", 30))
        self.title.pack()

        self.fm_lft = Frame(master)

        # Map canvas
        self.canvas = Canvas(self.fm_lft, height=canvas_size, width=canvas_size,
                        bg="white", relief="solid", borderwidth=canvas_border_size)
        self.canvas.pack()
        init_grid(self.canvas)

        self.fm_rgt = Frame(master)

        # entry boxes - holy fuck this code sucks immensely
        # this can be done cleaner using an array of results
        self.lbl_a = Label(self.fm_rgt, text="Number of Rooms")
        self.ent_a = Entry(self.fm_rgt)
        self.lbl_b = Label(self.fm_rgt, text="Minimum Room Size")
        self.ent_b = Entry(self.fm_rgt)
        self.lbl_c = Label(self.fm_rgt, text="Maximum Room Size")
        self.ent_c = Entry(self.fm_rgt)
        self.lbl_d = Label(self.fm_rgt, text="Maximum Connections")
        self.ent_d = Entry(self.fm_rgt)
        self.lbl_e = Label(self.fm_rgt, text="Maximum Trials")
        self.ent_e = Entry(self.fm_rgt)

        self.ent_a.insert(END,'10')
        self.ent_b.insert(END,'2')
        self.ent_c.insert(END,'10')
        self.ent_d.insert(END,'3')
        self.ent_e.insert(END,'100')

        self.lbl_a.pack()
        self.ent_a.pack()
        self.lbl_b.pack()
        self.ent_b.pack()
        self.lbl_c.pack()
        self.ent_c.pack()
        self.lbl_d.pack()
        self.ent_d.pack()
        self.lbl_e.pack()
        self.ent_e.pack()

        self.no_rooms = self.ent_a.get()
        self.min_size = self.ent_b.get()
        self.max_size = self.ent_c.get()
        self.max_conc = self.ent_d.get()
        self.max_tril = self.ent_e.get()

        # checkbox for grid overlay
        self.grid_bool = BooleanVar(value=True)
        self.grid_button = Checkbutton(self.fm_rgt, text="Grid Overlay", command=lambda: grid_on_off(self.grid_bool, self.canvas),
                                  variable=self.grid_bool, onvalue=True, offvalue=False)
        self.grid_button.pack()

        # Button to generate a new tilemap
        self.generate_button = Button(self.fm_rgt, text="Generate", command= lambda: generate_dungeon(self.no_rooms, self.max_tril, self.min_size, self.max_size, self.max_conc))
        self.generate_button.pack()

        self.fm_top.pack(side=TOP)
        self.fm_lft.pack(side=LEFT,padx=15)
        self.fm_rgt.pack(side=RIGHT,padx=15) 

def generate_dungeon (rooms, trials, min_room_size, max_room_size, max_connections):
    # generates the dungeon tilemap, many different functions can be added for generating overworld tilemaps and such
    frames.canvas.delete("tilemap")

    # Generate tilemap and show it on canvas here

    #tilemap = dungeon_generation.generate(grid_count, grid_count, rooms, trials, min_room_size, max_room_size)
    #show_tilemap(frames.canvas, tilemap)

def grid_on_off(grid_bool, canvas):
    # deletes or (re)initialises the grid depending on the value of grid_bool
    if grid_bool.get() == True:
        init_grid(canvas)
    if grid_bool.get() == False:
        canvas.delete("gridline")

def show_tilemap (canvas, tilemap):
    for y in range(tilemap.height):
        for x in range(tilemap.width):
            if tilemap.tiles[y * tilemap.width + x].solid:
                canvas.create_rectangle(x*grid_size+2,
                                        y*grid_size+2,
                                        (x+1)*grid_size+2,
                                        (y+1)*grid_size+2,
                                        outline="black", width=1, tags="tilemap", fill="black")

def init_grid(canvas):
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

if __name__ == "__main__":
    main()
