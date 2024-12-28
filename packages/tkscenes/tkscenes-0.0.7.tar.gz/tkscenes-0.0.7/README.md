A simple package for adding different scenes to TKinter and CustomTKinter

You can view the source code on the [Main Page](https://github.com/TonyLovesCoding/tkscenes)

> [!WARNING]\
> This project is in very early development.\
> Proceed with caution!

# Setup
Run `pip install tkscene` in the terminal to download the package

## Create a scene
To create a scene, use `tkscene.Scene()`

## Adding child to a scene

## Setting pack, grid and place

## Loading and unloading scenes
`scene.load()`
`scene.unload()`

# Example:
```python
# import modules
import tkinter as tk
import tkscenes

# make window
root = tk.Tk()
root.geometry("850x450")
root.title("Window")


# commands
def load_scene1() -> None:
    scene2.unload()
    scene1.load()


def load_scene2() -> None:
    scene1.unload()
    scene2.load()


# create scene
scene1 = tkscenes.Scene()
scene1["label"] = tk.Label(root, text="Scene1")
scene1["button"] = tk.Button(
    root, text="Next", command=load_scene2
)

scene2 = tkscenes.Scene()
scene2["label"] = tk.Label(root, text="Scene2")
scene2["button"] = tk.Button(
    root, text="Back",
    command=load_scene1
)

# define packing
scene1["label"].set_mode(
    "pack",
    fill="x"
)
scene1["button"].set_mode(
    "pack",
    anchor="center",
    expand=True
)

scene2["label"].set_mode(
    "pack",
    fill="x"
)
scene2["button"].set_mode(
    "pack",
    anchor="center",
    expand=True
)

# load scene 1
scene1.load()

# mainloop
root.mainloop()

```