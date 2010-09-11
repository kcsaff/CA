# Copyright (C) 2010 by Kevin Saff

# This file is part of the CA scanner.

# The CA scanner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# The CA scanner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with the CA scanner.  If not, see <http://www.gnu.org/licenses/>.

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
    return root

def _file_open_dialog(last_filename = ''):
    filename = tkFileDialog.askopenfilename(parent=_use_tkinter(),
                                            initialdir=os.path.dirname(last_filename))
    if filename:
        events.put(Event('file_open', filename=filename))
file_open_dialog = external_command(_file_open_dialog)

def _file_save_dialog(last_filename = ''):
    filename = tkFileDialog.asksaveasfilename(parent=_use_tkinter(),
                                              initialdir=os.path.dirname(last_filename),
                                              filetypes=[('CA scanner native',
                                                          '*.ca.zip')])
    if filename:
        events.put(Event('file_save', filename=filename))
file_save_dialog = external_command(_file_save_dialog)


