import Tkinter as tk
import tkFileDialog
import logging
import events
import comm
from events import Event
import os.path

logger = logging.getLogger('display.tk_dialogs')


def open_process(ip, port, fun, *args):
    def new_events_put(event):
        comm.client(ip, port, event)
    events.put = new_events_put
    
    fun(*args)

def external_command(fun):
    def do_spawn(*args):
        import multiprocessing
        p = multiprocessing.Process(target=open_process, 
                                    args=comm.server() + (fun,) + args)
        p.start()
        
    return do_spawn

def _use_tkinter():
    root = tk.Tk()
    root.withdraw()

def _file_open_dialog(last_filename = ''):
    _use_tkinter()
    filename = tkFileDialog.askopenfilename(initialdir=os.path.dirname(last_filename))
    if filename:
        events.put(Event('file_open', filename=filename))
    
file_open_dialog = external_command(_file_open_dialog)


