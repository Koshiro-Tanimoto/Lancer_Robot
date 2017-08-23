#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Combat Creatures Control System (C3s) for Raspberry Pi(python)

# wkey:Forword , skey:Back , dkey:Right turn
# akey:Left Turn , qkey:Pitch UP , ekey:Pitch Down
# gkey:Servo ON , fkey:Servo OFF , ikey:Servo Initial
# ENTERkey:NERF Shot

import serial
import io
from Tkinter import *
import sys

#Tkinter config
root = Tk()
root.option_add('*font',('FixedSys',14))
root.geometry("140x50")
root.title(u"C3s")
comment = StringVar()
comment.set('')
commentb = StringVar()
commentb.set('')

#Serial config (to mbed)
#ser = serial.Serial('/dev/ttyACM0',9600)

#key event
def forword(event):
    #ser.write('w')
    comment.set( '<<Forword>>')

def back(event):
    #ser.write('s')
    comment.set( '<<Back>>')

def right(event):
    #ser.write('d')
    comment.set( '<<Right Turn>>')

def left(event):
    #ser.write('a')
    comment.set( '<<Left Turn>>')

def shot(event):
    #ser.write('z')
    comment.set('<< Fire!! >>')

def pitchup(event):
    #ser.write('q')
    comment.set('<<Pitch Up>>')

def pitchdown(event):
    #ser.write('e')
    comment.set('<<Pitch Down>>')

def servoon(event):
    #ser.write('g')
    comment.set('<<Servo ON>>')

def servooff(event):
    #ser.write('f')
    comment.set('<<Servo OFF>>')

def servoi(event):
    #ser.write('i')
    comment.set('<<Servo Initial>>')

def dcon(event):
    #ser.write('k')
    comment.set('<<Shot DC ON>>')

def dcoff(event):
    #ser.write('l')
    comment.set('<<Shot DC OFF>>')

def notmove(event):
    #ser.write('0')
    comment.set('<<Stop>>')

#main
if __name__ == '__main__':

    Label(root,text = 'Main Control').pack()
    a = Label(root, textvariable = comment)
    a.pack()
    a.bind('<Key-w>',forword)
    a.bind('<Key-s>',back)
    a.bind('<Key-d>',right)
    a.bind('<Key-a>',left)
    a.bind('<Return>',shot) # Use Enter key
    a.bind('<Key-q>',pitchup)
    a.bind('<Key-e>',pitchdown)
    a.bind('<Key-g>',servoon)
    a.bind('<Key-f>',servooff)
    a.bind('<Key-i>',servoi)
    a.bind('<Key-k>',dcon)
    a.bind('<Key-l>',dcoff)
    a.bind('<Any-KeyRelease>',notmove)

    a.focus_set()
    root.mainloop()

#    ser.close

    print("End of c3s")

