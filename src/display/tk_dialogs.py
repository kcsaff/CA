import tkFileDialog
import threading
import logging
from _event import event, Event

logger = logging.getLogger('display.tk_dialogs')

__dialog_thread = None
def __run_dialog(fun):
    def result():
        global __dialog_thread
        if __dialog_thread and __dialog_thread.is_alive():
            logger.warn('Attempted to open dialog when dialog was already active.')
        threading.Thread(target=fun, name=fun.__name__).start()
    return result

@__run_dialog
def file_open():
    event.put(Event('file_open', 
                    filename=tkFileDialog.askopenfilename()))
    