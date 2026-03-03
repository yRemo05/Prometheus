from pynput.keyboard import Controller,Key,Listener
from string import ascii_lowercase,ascii_uppercase
from textblob import Word
import win32console,win32gui
from win32gui import GetWindowText, GetForegroundWindow
from threading import Lock
from Utils import WindowsHelper


from time import sleep

## Made By Remo Under Apache-2.0 license


class Prometheus:
    def __init__(self, id, window, lock):
        
        self.id = id
        self.window = window
        self._is_hooked = False
        self.thread_lock = lock

        self.controller = Controller()
        self.upperLetters = [*ascii_uppercase]
        self.lowerLetters = [*ascii_lowercase]
        self.letters = []
        self.dismissable = False
        self.windows = {}


    # Getters and Setters
    def get_id(self):return self.id
    def get_window(self): return self.window
    def is_hooked(self):return self._is_hooked


    def on_press(self,key):
            # This try and except statement handles the filter that cleans 'Key' instances
            try:
                # This handles the filter that cleans 'KeyCode' instances
                if key.char in self.upperLetters or key.char in self.lowerLetters:
                    if not self.dismissable:
                        self.letters.append(key.char)
            except:pass

    def touch(self,key):
        self.controller.press(key)
        self.controller.release(key)

    def fix_word(self):
        pass

    def on_release(self,key):
        if self.dismissable:
            return
        if len(self.letters) != 0:
            if key == Key.space or key == Key.enter:
                word = "".join(letter for letter in self.letters)
                self.letters = []
                #print("[+] Found word while typing : "+word)
                wordL = Word(word).spellcheck()[0][0]
                if wordL != word:
                    for _ in range(len([*word]) + 1):
                        self.touch(Key.backspace)
                    self.dismissable = True
                    self.controller.type(wordL)
                    self.dismissable = False
                    self.touch(Key.space) if key == Key.space else self.touch(Key.enter)
            if key == Key.backspace:
                self.letters.pop()

    def hook(self):
        self.thread_lock.acquire()
        self.listener = Listener(self.on_press,self.on_release)
        self.listener.start()
        self._is_hooked = True
        self.thread_lock.release()

    def unhook(self):
        self.thread_lock.acquire()
        self.listener.stop()
        self._is_hooked = False
        self.thread_lock.release()

    

    """ def initialize(self):
        while 1:
            active = WindowsHelper.get_active_window()
            if active == self.window and not self._is_hooked:
                self.hook()
            elif active != self.window and self._is_hooked:
                self.unhook()
            sleep(0.3) """



""" 
if __name__ == "__main__":
    corrector = Prometheus()
    corrector.hook()
    win32gui.ShowWindow(win32console.GetConsoleWindow(),0)
    #print("[+] Hooks injected.")
    corrector.listener.join() 
"""





