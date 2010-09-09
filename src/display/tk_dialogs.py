import Tkinter as tk
import tkFileDialog
import threading
import logging
from _event import event, Event

logger = logging.getLogger('display.tk_dialogs')

__dialog_thread = None
__root = None
def __run_dialog(fun):
    def result():
        global __dialog_thread, __root
        if __root is None:
            __root = tk.Tk()
        __root.withdraw()
        if __dialog_thread and __dialog_thread.is_alive():
            logger.warn('Attempted to open dialog when dialog was already active.')
        __dialog_thread = threading.Thread(target=fun, name=fun.__name__)
        __dialog_thread.start()
    return result

@__run_dialog
def file_open():
    event.put(Event('file_open', 
                    filename=tkFileDialog.askopenfilename()))
    global __root
    __root = None
    