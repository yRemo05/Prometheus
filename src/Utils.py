from json import load, dump
from os.path import abspath

import win32gui
from win32gui import GetWindowText, GetForegroundWindow

configFile = abspath("config.json")


class Config:
    
    @staticmethod
    def getKey(key:str):
        f = open(configFile,"r+")
        obj = load(f)
        f.close()
        return obj[key]
    
    @staticmethod
    def editKey(key:str, value:str) -> bool:
        try:
            fr = open(configFile,"r+")
            obj = load(fr)
            fr.close()
            fw = open(configFile, "w+")
            obj[key] = value
            dump(obj,fw,indent=4,sort_keys=False)
            return True
        except: 
            return False
        


class WindowsHelper:


    @staticmethod
    def get_active_window() -> str:
        return GetWindowText(GetForegroundWindow())

    @staticmethod
    def get_open_applications() -> list:
        open_apps = []

        # This is the callback function that Windows will run for every open window
        def enum_windows_proc(hwnd, extra_data):
            # 1. Check if the window is actually visible on screen
            if win32gui.IsWindowVisible(hwnd):
                # 2. Get the text (title) of the window
                window_title = win32gui.GetWindowText(hwnd)
                
                # 3. If the window has a title, add it to our list
                if window_title:
                    open_apps.append(window_title)

        # Tell Windows to iterate through all top-level windows and apply our function
        win32gui.EnumWindows(enum_windows_proc, None)
        
        return open_apps

