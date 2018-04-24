import subprocess
from tkinter import Tk
from window_switcher.window import Window
import gi
import timeit
import sys

start = timeit.default_timer()

gi.require_version('Gdk', '3.0') 
from gi.repository import Gdk

screen = Gdk.Screen.get_default()
monitor = screen.get_monitor_at_window(screen.get_active_window())
monitor = screen.get_monitor_geometry(monitor)

ws = monitor.width
hs = monitor.height - 200
w = int(ws / 2)
h = 40

root = Tk()
window = Window(root, w, h)
print(f'Time to start {timeit.default_timer() - start:.3f}')

root.mainloop()
