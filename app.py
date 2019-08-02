from tkinter import *  # pylint: disable=unused-wildcard-import
from PIL import Image, ImageTk
import math

# VARIABLES TO EDIT (In the future these will be GUI options)
# Number of tiles
grid_count = 20

canvas_size = 800
canvas_border_size = 0

# Other helpful variables to have stored (DO NOT EDIT)
grid_size = (canvas_size-1)/grid_count

def main():
    print("Running...")

    # Application Setup
    root = Tk()
    root.geometry("920x880")
    root.winfo_toplevel().title("DNDungeonWorldGenerator")

    Init_Frames(root)

    mainloop()

class Init_Frames:
    def __init__(self,master):
        fm_top = Frame(master)
        
        # Title label
        title = Label(fm_top, anchor=CENTER, text="DNDungeonWorldGenerator",
                      pady=5, font=("Helvetica", 30))
        title.pack()

        fm_lft = Frame(master)

        # Map canvas
        canvas = Canvas(fm_lft, height=canvas_size, width=canvas_size,
                        bg="white", relief="solid", borderwidth=canvas_border_size)
        canvas.pack()

        init_grid(canvas)
        
        fm_rgt = Frame(master)

        # checkbox for grid overlay
        grid_bool = BooleanVar(value=False)
        grid_button = Checkbutton(fm_rgt, text="Grid Overlay", command=lambda: grid_on_off(grid_bool, canvas),
                                  variable=grid_bool, onvalue=True, offvalue=False)
        grid_button.pack()

        # Button to generate a new tilemap
        generate_button = Button(fm_rgt, text="Generate")
        generate_button.pack()

        fm_top.pack(side=TOP)
        fm_lft.pack(side=LEFT)
        fm_rgt.pack(side=RIGHT) 


def grid_on_off(grid_bool, canvas):
    # deletes or (re)initialises the grid depending on the value of grid_bool
    if grid_bool.get() == True:
        init_grid(canvas)
    if grid_bool.get() == False:
        canvas.delete("gridline")


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
