#!/usr/bin/env python3

from tellcore.telldus import TelldusCore
#from tkinter import tix
from tkinter.tix import *
from tkinter.font import Font


tk = Tk()
tell = TelldusCore()

font = Font(size=16)

root = ScrolledWindow(tk, scrollbar=Y)
root.vsb.config(width=28)

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

col = 0
row = 0

devices = tell.devices()
devices.sort(key=(lambda device: device.name))
for device in devices:
    
    container = Frame(root.window)
    label = Label(container, text=device.name, font=font)
    label.pack(side=TOP)
    
    buttonframe = Frame(container)

    onbutton = Button(buttonframe, 
                      text="ON", 
                      command=makeaction(device, 'on'),
                      font=font, 
                      bg='#00AA00')
    onbutton.pack(side=LEFT)

    offbutton = Button(buttonframe, 
                       text="OFF", 
                       command=makeaction(device, 'off'), 
                       font=font, 
                       bg='#AA0000')
    offbutton.pack(side=RIGHT)

    buttonframe.pack(side=TOP)
    container.grid(row=row, column=col)

    col += 1
    if col > 1:
        col = 0
        row += 1
    

exitframe = Frame(tk)
exitbutton = Button(exitframe, text='EXIT', command=exit, font=font)
exitbutton.pack(side=RIGHT)
exitframe.pack(side=BOTTOM, fill=X)
root.pack(fill=BOTH, expand=1)
tk.mainloop()
