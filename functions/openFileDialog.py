from tkinter import Tk
from tkinter import filedialog
from dearpygui import core
from src import main


def get_background_image():
    Tk().withdraw()
    print('in function')
    file = filedialog.askopenfilename(title="Search for Background Image",
                                      filetypes=[("JPEG (*.jpg, *.jpeg)", "*.jpg"), ("PNG (*.png)", "*.png")],
                                      defaultextension=[("JPEG (*.jpg, *.jpeg)", "*.jpg"), ("PNG (*.png)", "*.png")])
    core.set_value("##BgImage", file)
    main.save_font()
    return file
