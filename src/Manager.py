import win32gui
from win32gui import GetWindowText, GetForegroundWindow
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Lock
import uuid

from Corrector import Prometheus
from Utils import Config
from Utils import WindowsHelper

from time import sleep

class Manager:
    def __init__(self):
        self.global_lock = Lock()
        self.instances: dict[str, Prometheus] = {}
        self.activeInstance = None

    def init_prometheus(self, window: str):
        """ Inserts a prometheus instance to the manager. DOES NOT start the instance."""
        existing = self.instances.get(window)
        if existing:
            return existing
        id = uuid.uuid4()
        instance = Prometheus(id, window, self.global_lock)
        self.instances[window] = instance
        # self.threadPool.submit(instance.hook)
        return instance

    def _prep(self):
        """Receives the currently running apps, and creates prometheus instances."""
        for app_name in dict.fromkeys(WindowsHelper.get_open_applications()):
            if app_name not in self.instances:
                print("Init : " + app_name)
                self.init_prometheus(app_name)

        # Hook a prometheus instance only if the window is active.
        active = WindowsHelper.get_active_window()
        instance = self.instances.get(active)
        if instance and not instance.is_hooked():
            instance.hook()
            self.activeInstance = instance

        print("_prepVerbose | instances : \n")
        print(self.instances)

        print("\n\n")

    
    def start(self):

        self._prep() # Necessary for the activeInstance to be set.

        while 1:
            """ active = WindowsHelper.get_active_window()
            instance = self.instances.get(active)

            if instance and active != instance.get_window() and instance.is_hooked():
                print("Case 1")
                self.activeInstance.unhook()

            if not instance: # Ran if an active window is not registered in the manager
                print("Case 2")
                new_prometheus_instance = self.init_prometheus(active)
                new_prometheus_instance.hook()
                self.activeInstance = new_prometheus_instance
                

            elif instance and instance.get_window() == active and not instance.is_hooked() : # Ran if there is an unhooked instance which matches the active window
                print("Case 3")
                instance.hook()
                self.activeInstance = instance """
            

            active = WindowsHelper.get_active_window()

            if self.activeInstance and self.activeInstance.get_window() != active \
            and self.activeInstance.is_hooked():
                print("Case 1")
                self.activeInstance.unhook()

            instance = self.instances.get(active)
            if not instance:
                print("Case 2")
                instance = self.init_prometheus(active)

            if not instance.is_hooked():
                print("Case 3")
                instance.hook()

            self.activeInstance = instance
            
            
            sleep(0.3)


