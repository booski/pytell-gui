#!/usr/bin/env python3

from tellcore.telldus import TelldusCore
from tkinter.tix import *
from tkinter.font import Font
from tkinter import messagebox
from subprocess import call
import os
from PIL import Image, ImageTk

def makeaction(device, action):
    def offaction():
        device.turn_off()
    
    def onaction():
        device.turn_on()

    if action == 'off':
        return offaction
    elif action == 'on':
        return onaction
    else:
        raise IllegalArgumentException()


def getshutdown():
    def shutdown():
        if messagebox.askyesno("Really shut down?", "Are you sure you want to shut down the remote?"):
            call(["sudo", "poweroff"])

    return shutdown


tk = Tk()
tell = TelldusCore()

font = Font(size=16)

root = Canvas(tk)
win = Frame(root)

winid = root.create_window(0, 0, anchor=NW, window=win)

def scroll_start(event):
    if event.widget != vsb:
        root.scan_mark(0, event.y)
    
def scroll_move(event):
    if event.widget != vsb:
        root.scan_dragto(0, event.y, gain=1)
    
win.bind_all("<ButtonPress-1>", scroll_start)
win.bind_all("<B1-Motion>", scroll_move)

col = 0
row = 0

devices = tell.devices()
devices.sort(key=(lambda device: device.name))

for device in devices:
    
    container = Frame(win)
    label = Label(container, text=device.name, font=font)
    label.pack(side=TOP)
    
    buttonframe = Frame(container)

    onbutton = Button(buttonframe, 
                      text="ON", 
                      command=makeaction(device, 'on'),
                      font=font, 
                      activebackground='#00FF00',
                      bg='#00AA00')
    onbutton.pack(side=LEFT)

    offbutton = Button(buttonframe, 
                       text="OFF", 
                       command=makeaction(device, 'off'), 
                       font=font, 
                       activebackground='#FF0000',
                       bg='#AA0000')
    offbutton.pack(side=RIGHT)

    buttonframe.pack(side=TOP)
    container.grid(row=row, column=col)

    col += 1
    if col > 1:
        col = 0
        row += 1
    

filepath = os.path.dirname(os.path.realpath(__file__)) + '/power.png'
image = Image.open(filepath).resize((26,30), Image.ANTIALIAS)
power = ImageTk.PhotoImage(image)

exitframe = Frame(tk)
exitbutton = Button(exitframe, 
                    image=power,
                    width=28,
                    height=32,
                    command=getshutdown())
exitbutton.image = power
exitbutton.pack(side=LEFT)

exitframe.pack(side=BOTTOM, fill=X)

vsb = Scrollbar(tk, orient=VERTICAL)
vsb.config(width=28)
vsb.pack(side=RIGHT, fill=Y)

root.configure(yscrollcommand=vsb.set)
vsb.config(command=root.yview)

root.pack(fill=BOTH, expand=1)
root.update()
region = (0, 0, win.winfo_reqwidth(), win.winfo_reqheight())
root.configure(scrollregion=region)
tk.mainloop()
