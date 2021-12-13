import time
import tkinter

text_pad: tkinter.Text


def write_text(output):
    global text_pad
    text_pad.config(state=tkinter.NORMAL)
    text_pad.delete('1.0', tkinter.END)
    text_pad.insert(tkinter.END, output)
    text_pad.see(tkinter.END)
    text_pad.config(state=tkinter.DISABLED)