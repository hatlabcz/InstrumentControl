# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 18:45:41 2018

@author: Pinlei Lu
"""
import numpy as np
import tkinter as tk
from functools import partial

from instrumentserver.client import Client

cli = Client()
instr_list = cli.list_instruments()
SWT = cli.get_instrument("SWT")

gens = {}
KeysightGens = {}
for instr_name, instr_type in instr_list.items():
    driver_cls_name = instr_type.__name__
    if driver_cls_name in ['SignalCore_SC5511A', 'SignalCore_SC5506A', 'Keysight_N5183B', 'N51x1']:
        gens[instr_name] = cli.get_instrument(instr_name)

genCurrentStatusList = np.zeros(len(gens), dtype=int)

def recordGens():
    for i, gen_ in enumerate(gens.values()):
        genCurrentStatusList[i] = gen_.output_status()
    
def switchGens(status):
    for gen_ in gens.values():
        gen_.output_status(status)

def setGensBack():
    for i, gen_ in enumerate(gens.values()):
        gen_.output_status(genCurrentStatusList[i])

def labelFunction(windowName, textOutput, row_, column_, columnspan_, underline_=-1, font_="Times 24", fg_='black', bg_=None):
    tempLabel = tk.Label(windowName, text=textOutput, underline=underline_, font=font_, foreground=fg_, background=bg_)
    tempLabel.grid(row=row_, column=column_, columnspan=columnspan_)
    return tempLabel


def changeSwitch(mode_name):
    print(mode_name)
    recordGens()
    print('turn off all gens')
    switchGens(0)
    SWT.mode(mode_name)
    print('turn on gens')    
    setGensBack()
    return 0


def controlWindow(params):
    temp = tk.Tk()
    temp.geometry('500x300+200+100')
    temp.title('Control Window')

    rowNum = 0
    columnNum = 0
    labelFunction(temp, 'Switch Control', rowNum, columnNum, 40, bg_='Pink')
    allMode = SWT.get_mode_options()
    rowNum += 1
    backGround = 'Yellow'
    for i, mode_name in enumerate(allMode):
        tk.Button(temp, text=mode_name, command=partial(changeSwitch, mode_name), width=10, bg=backGround, font='Times 13').grid(row=rowNum, column=columnNum, columnspan=2)
        columnNum += 5
        if (i + 1) % 4 == 0:
            rowNum += 1
            columnNum = 0

    rowNum += 1
    columnNum = 0

    temp.mainloop()


controlWindow(0)