#!/usr/local/bin/python3
# coding: utf-8
import sys
import curses
import time
import numpy as np

debug = False
step = False
delay = 0

def main(stdscr):
    global toggle
    global debug
    global step
    global delay
    global points
    global constants
    
    if debug:        
        rows = 5
        cols = 5
    else:
        rows = curses.LINES - 1
        cols = curses.COLS
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.clear()

    points = np.zeros((rows, cols), dtype=complex)
    constants = np.zeros((rows, cols), dtype=complex)

    def initConstants():
        global constants
        for y in range(0, rows):
            for x in range(0, cols):
                constants[y,x] = complex(5*(x/(cols-1))-3.5,3*(y/(rows-1))-1.5)
        if debug:
            stdscr.getkey()
            print("Constants\r")
            print(str(constants).replace("\n","\n\r")+"\n\r")
            stdscr.getkey()

    def drawScreen():
        for y in range(0, rows):
            for x in range(0, cols):
                if points[ y, x ] != points[ y, x ]:
                    stdscr.addch(y, x, ' ', curses.A_REVERSE)
                else:
                    stdscr.addch(y, x, ' ', curses.A_NORMAL)

    def updatePoints():
        global points
        points = points**2 + constants

    g = 0
    initConstants()
    try:
        while True:
            if debug:
                print("Generation: {0}\n\r".format(g))
                print(str(points).replace("\n","\n\r")+"\n\r")
            else:
                drawScreen()
                stdscr.refresh()
            if step:
                stdscr.getkey()
            elif delay != 0:
                time.sleep(delay)
            updatePoints()
            g += 1
    except KeyboardInterrupt:
        pass

def help():
    print('^C : exit')
    print('-d : debug - output arrays instead of displaying points')
    print('-h : print this help and exit')
    print('-s : single step between generations with key press')
    print('-t : time in seconds between generations (default 0)')
    exit()
    
argc = 1
while argc < len(sys.argv):
    argv = sys.argv[argc]
    argc += 1
    if argv == '-h': help()
    if argv == '-d': debug = True
    if argv == '-s': step = True
    if argv == '-t':
        if argc < len(sys.argv):
            try:
                delay = float(sys.argv[argc])
            except ValueError:
                delay = 1
            else:
                argc += 1
        else:
            delay = 1
            
if debug:
    main(curses.initscr())
else:
    curses.wrapper(main)


