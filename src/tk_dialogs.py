import Tkinter as tk
import tkFileDialog
import logging
import events
import comm
from events import Event

logger = logging.getLogger('display.tk_dialogs')


def open_process(ip, port, fun):
    def new_events_put(event):
        comm.client(ip, port, event)
    events.put = new_events_put
    
    fun()

def external_command(fun):
    def do_spawn(*args):
        import multiprocessing
        p = multiprocessing.Process(target=open_process, 
                                    args=comm.server() + (fun,))
        p.start()
        
    return do_spawn

def _use_tkinter():
    root = tk.Tk()
    root.withdraw()

def _file_open_dialog(*args):
    _use_tkinter()
    filename = tkFileDialog.askopenfilename()
    if filename:
        events.put(Event('file_open', filename=filename))
    
file_open_dialog = external_command(_file_open_dialog)


