# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 18:45:41 2018

@author: Hatlab_3
"""
import h5py
import numpy as np
import tkinter as tk
from tkinter import filedialog as tkFileDialog
import datetime
import os
from instrumentserver.client import Client


def advanced_input_label(window_name, keys, units, row_init=0, column_init=0, grid=None, entry_init=None, width=20):
    '''
    window_name: Tk window name
    keys: list of all the input entry name
    units: the units of the input
    '''
    label_set = []
    entry_set = []
    unit_set = []
    if grid == None:
        for i in range(len(keys)):
            '''
            There are three parts you need to combine:
            1. name of parameter (list)
            2. input entry of parameter
            3. units (list)
            '''
            label_temp = tk.Label(window_name, text=keys[i])
            label_temp.grid(row=i + row_init, column=column_init)
            label_set.append(label_temp)
            entry_temp = tk.Entry(window_name, width=width)
            entry_temp.grid(row=i + row_init, column=column_init + 1)
            if entry_init != None:
                entry_temp.insert(0, str(entry_init[i]))
            entry_set.append(entry_temp)
            unit_temp = tk.Label(window_name, text=units[i])
            unit_temp.grid(row=i + row_init, column=column_init + 2)
            unit_set.append(unit_temp)
    else:
        num = 0
        for row in range(int(grid[0])):
            for column in range(int(grid[1])):
                label_temp = tk.Label(window_name, text=keys[num])
                label_temp.grid(row=row + row_init, column=3 * column + column_init)
                label_set.append(label_temp)
                entry_temp = tk.Entry(window_name, width=width)
                entry_temp.grid(row=row + row_init, column=3 * column + column_init + 1)
                if entry_init != None:
                    entry_temp.insert(0, str(entry_init[num]))
                entry_set.append(entry_temp)
                unit_temp = tk.Label(window_name, text=units[num])
                unit_temp.grid(row=row + row_init, column=3 * column + column_init + 2)
                unit_set.append(unit_temp)
                num += 1
    return label_set, entry_set, unit_set


def wrong_window(Output):
    temp = tk.Toplevel()
    temp.title("Something Wrong, mortal!!!")
    temp.geometry('300x100+500+300')

    def trick_window():
        temp = tk.Toplevel()
        temp.title("Something Wrong, mortal!!!")
        temp.geometry('300x100+500+300')
        label = tk.Label(temp, text="You're so bad!")
        label.grid(row=0)
        button2 = tk.Button(temp, text="Close", command=temp.destroy)
        button2.grid(row=1)

    label = tk.Label(temp, text=Output, wraplength=300)
    label.grid(row=0)
    button1 = tk.Button(temp, text="Ha?", command=trick_window)
    button1.grid(row=1)
    button2 = tk.Button(temp, text="Fine, I got it", command=temp.destroy)
    button2.grid(row=2)
    return


def SigCore_window(params, cli:Client):
    fridge_date = params.get('fridge_date', "20XXXXXX")
    save_date = params.get('save_date', datetime.date.today().strftime('%Y%m%d'))
    directory = r"M:\code\project\tree\InstrumentControl\GeneratorSettings\\" + save_date + "\Pump_condition\\"
    instr_list = cli.list_instruments()
    allGens = {}
    for instr_name, instr_type in instr_list.items():
        driver_cls_name = instr_type.__name__
        if driver_cls_name in ['SignalCore_SC5511A', 'SignalCore_SC5506A', 'Keysight_N5183B', 'N51x1']:
            allGens[instr_name] = cli.get_instrument(instr_name)

    try:
        os.makedirs(directory)
    except WindowsError:
        pass
    except:
        raise
    print(directory)
    window_h = len(allGens) * 20 + 100
    temp = tk.Tk()
    temp.geometry(f'1100x{int(window_h)}+500+300')
    temp.title('Generator Control')

    def get_all_value():
        i = 0
        for gen_name, gen in allGens.items():
            SC_entry_set[i].delete(0, tk.END)
            SC_entry_set[i].insert(0, gen.output_status())
            SC_entry_set[i + 1].delete(0, tk.END)
            SC_entry_set[i + 1].insert(0, np.round(gen.frequency() * 1e-9, 9))
            SC_entry_set[i + 2].delete(0, tk.END)
            SC_entry_set[i + 2].insert(0, gen.power())
            SC_entry_set[i + 3].delete(0, tk.END)
            SC_entry_set[i + 3].insert(0, gen.reference_source())
            i += 4
        return

    def set_all_value():
        i = 0
        for gen_name, gen in allGens.items():
            gen.output_status(int(SC_entry_set[i].get()))
            gen.frequency(np.round(float(SC_entry_set[i + 1].get()) * 1e9))
            gen.power(float(SC_entry_set[i + 2].get()))
            gen.reference_source(int(SC_entry_set[i + 3].get()))
            i += 4
        return



    def save_window():
        def save_data():
            data = h5py.File(directory + save_name.get(), 'w-')

            for keys, values in setting.items():
                data.create_dataset(keys, data=values)
            data.close()
            save_win.destroy()
            return None

        setting = {}
        i=0
        for gen_name, gen in allGens.items():
            setting.update({gen_name + ' status': SC_entry_set[i * 4].get()})
            setting.update({gen_name + ' frequency': SC_entry_set[i * 4 + 1].get()})
            setting.update({gen_name + ' power': SC_entry_set[i * 4 + 2].get()})
            setting.update({gen_name + ' refernce': SC_entry_set[i * 4 + 3].get()})
            i+=1


        save_win = tk.Toplevel()
        save_win.geometry('250x100+500+300')
        save_win.title('Filename')

        tk.Label(save_win, text='Dear Hatlab, what is the filename?').grid(row=0, column=0, columnspan=5)
        save_name = tk.Entry(save_win, width=20)
        save_name.grid(row=1, column=0, columnspan=5)
        tk.Button(save_win, text='Save', command=save_data, bg='white').grid(row=2, column=2)
        return

    def save_setting():
        save_window()
        return

    def load_window():
        def load_data():
            filename = tkFileDialog.askopenfilename(initialdir=directory, title="Select file",
                                                    filetypes=(("All files", "*.*"), ("all files", "*.*")))
            load_name.delete(0, tk.END)
            load_name.insert(0, filename)
            setting = {}
            i=0
            for gen_name, gen in allGens.items():
                setting.update({gen_name + ' status': SC_entry_set[i * 4]})
                setting.update({gen_name + ' frequency': SC_entry_set[i * 4 + 1]})
                setting.update({gen_name + ' power': SC_entry_set[i * 4 + 2]})
                setting.update({gen_name + ' refernce': SC_entry_set[i * 4 + 3]})
                i += 1

            try:
                data = h5py.File(load_name.get(), 'r')
                for keys in data.keys():
                    try:
                        setting[keys].delete(0, tk.END)
                        setting[keys].insert(0, data[keys].value)
                    except:
                        pass
            except IOError:
                wrong_window("Sorry, there is no original setting")
            data.close()
            set_all_value()
            load_win.destroy()
            return

        load_win = tk.Toplevel()
        load_win.geometry('300x100+500+300')
        load_win.title('Load File')

        tk.Label(load_win, text='Dear Hatlab, what setting you want to load?').grid(row=0, column=0, columnspan=5)
        load_name = tk.Entry(load_win, width=20)
        load_name.grid(row=1, column=0, columnspan=5)
        tk.Button(load_win, text='Browse and Load', command=load_data, bg='white').grid(row=2, column=2)
        return

    def load_setting():
        load_window()
        return

    row_num = 0
    Cooldown_date_label = tk.Label(temp,
                                   text=' Cooldown Date(YYYYMMDD)  :')
    Cooldown_date_label.grid(row=row_num, column=0, columnspan=2)

    tk.Label(temp, text=fridge_date, width=20).grid(row=row_num, column=2, columnspan=2)

    Save_date_label = tk.Label(temp,
                               text='  Save Date  :  ')
    Save_date_label.grid(row=row_num, column=4, columnspan=2)

    tk.Label(temp, text=save_date, width=20).grid(row=row_num, column=6, columnspan=2)
    row_num += 1

    SigCore_keys = []
    SigCore_units = []
    for i, gen_name in enumerate(allGens.keys()):
        temp_list1 = [gen_name + ' status: ', 'Frequency', 'Power: ', 'Ref: ']
        SigCore_keys += temp_list1
        temp_units1 = ['0/1', 'GHz', 'dBm', '0/1 (0:Internal, 1:External)']
        SigCore_units += temp_units1
    SC_label_set, SC_entry_set, SC_unit_set = advanced_input_label(temp, SigCore_keys, SigCore_units, row_init=row_num,
                                                                   grid=(len(allGens), 4), width=20)




    row_num += len(allGens)



    tk.Button(temp, text='Get All', command=get_all_value, width=15, bg='purple').grid(row=row_num, column=2,
                                                                                       columnspan=2)
    tk.Button(temp, text='Set All', command=set_all_value, width=15, bg='grey').grid(row=row_num, column=6,
                                                                                     columnspan=2)
    row_num += 1

    tk.Button(temp, text='Save Setting', command=save_setting, width=15, bg='salmon').grid(row=row_num, column=2,
                                                                                           columnspan=2)
    tk.Button(temp, text='Load Setting', command=load_setting, width=15, bg='yellow').grid(row=row_num, column=6,
                                                                                           columnspan=2)
    row_num += 1
    temp.mainloop()
    # _thread.start_new_thread(temp.mainloop, ())


if __name__ == '__main__':
    params = {'fridge_date': '20201224',
              'save_date': datetime.date.today().strftime('%Y%m%d')}
    cli = Client()
    SigCore_window(params, cli)
