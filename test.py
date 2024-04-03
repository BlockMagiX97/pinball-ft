#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
import sys, os, random
from time import sleep
import ftrobopy                                              # Import the ftrobopy module
import threading
import multiprocessing
from pynput.keyboard import Key, Listener

lock_f = False
lock_j = False

txt: ftrobopy.ftrobopy
score=0
def _on_press(key):
    global txt, lock_f, lock_j
    if key.char == 'q':
        os._exit(0)
    if key.char == 'f':
        if not lock_f:
            lock_f = True
            txt.setPwm(1,512)

            while (txt.getCurrentInput(1) != 1):
                txt.updateWait()

            txt.setPwm(1,0)
            txt.setPwm(0, 512)
            while (txt.getCurrentInput(3) != 1):
                txt.updateWait()
            txt.setPwm(0,0)
            lock_f = False
        else:
            return
    if key.char == 'j':
        if not lock_j:
            lock_j = True
            txt.setPwm(2,512)

            while (txt.getCurrentInput(2) != 1):
                txt.updateWait()

            txt.setPwm(2,0)
            txt.setPwm(3, 512)
            while (txt.getCurrentInput(4) != 1):
                txt.updateWait()
            txt.setPwm(3,0)
            lock_j = False
        else:
            return
def on_press(key):
    t = threading.Thread(target=_on_press, args=(key,))

    t.start()
    


def on_release(key):
    global txt
    
def pararell(txt: ftrobopy.ftrobopy):
    score = 0
    while True:
        if txt.getCurrentInput(5) == 0:
            
            score+=1
            while txt.getCurrentInput(5) == 0:
                txt.updateWait()
            print(f'score: {score}', flush=True)
            sleep(0.01)

def pararell2(txt:ftrobopy.ftrobopy):
    txt.setPwm(7, 0)
    txt.setPwm(6, 512)
    while True:
        if (txt.getCurrentInput(0) == 1):
            txt.setPwm(7, 0)
            txt.setPwm(6, 512)
        if (txt.getCurrentInput(6) == 1):
            txt.setPwm(6, 0)
            txt.setPwm(7, 512)

def blower(txt:ftrobopy.ftrobopy):
    while True:
        i = random.randint(4,5)
        txt.setPwm(i, 512)
        sleep(random.uniform(0.1, 5.0))
        txt.setPwm(i, 0)
        sleep(random.uniform(0.1, 5.0))


txt = ftrobopy.ftrobopy("192.168.0.30", 65000) # connect to TXT's IO controller
# configure all TXT outputs to normal mode
M = [ txt.C_OUTPUT, txt.C_OUTPUT, txt.C_OUTPUT, txt.C_OUTPUT ]
I = [ (txt.C_SWITCH, txt.C_DIGITAL ),
      (txt.C_SWITCH, txt.C_DIGITAL ),
      (txt.C_SWITCH, txt.C_DIGITAL ),
      (txt.C_SWITCH, txt.C_DIGITAL ),
      (txt.C_SWITCH, txt.C_DIGITAL ),
      (txt.C_SWITCH, txt.C_DIGITAL ),
      (txt.C_SWITCH, txt.C_DIGITAL ),
      (txt.C_SWITCH, txt.C_DIGITAL ) ]
txt.setConfig(M, I)
txt.updateConfig()
t = threading.Thread(target=pararell, args=(txt,))
t.start()
t3 = threading.Thread(target=pararell2, args=(txt,))
t3.start()
t2 = threading.Thread(target=blower, args=(txt,))
t2.start()
with Listener(
    on_press=on_press,
    on_release=on_release) as listen:
        listen.join()
t.join()

