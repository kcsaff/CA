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

import multiprocessing, Queue
import simple

__events = Queue.Queue()

class Event(simple.typed_object):
    def __repr__(self):
        return 'Event(%s)' % self.format_args()
        
def __handle_pygame_all(pygame):
    for event in pygame.event.get():
        __handle_pygame(pygame, event)
            
def __handle_pygame(pygame, event):
    if event.type is pygame.MOUSEBUTTONDOWN:
        assert event.pos
        __events.put(Event('M%d' % event.button,
                           pos = event.pos, 
                           pressed = True))
        __events.put(Event('M%d~' % event.button,
                           pos = event.pos, 
                           pressed = True))
    elif event.type is pygame.MOUSEBUTTONUP:
        assert event.pos
        __events.put(Event('M%d~' % event.button,
                           pos = event.pos, 
                           pressed = False))
    elif event.type is pygame.MOUSEMOTION:
        assert event.pos
        for button in range(1, 3+1):
            if event.buttons[button - 1]:
                __events.put(Event('M%d~' % button,
                                pos = event.pos, 
                                pressed = True))
    elif event.type is pygame.KEYDOWN:
        __events.put(Event(event.unicode))
    elif event.type is pygame.QUIT:
        __events.put(Event('Quit'))
    elif event.type is pygame.USEREVENT and event.code == 'MENU':
        print event.name, event.item_id, event.text
        __events.put(Event(e.name))
    else:
        __events.put(Event('Unknown'))

def __handle_events(lib):
    if lib.__name__ == 'pygame':
        __handle_pygame_all(lib)
    else:
        raise ValueError, 'Unimplemented event source: %s' % lib.__name__
        
def get(libs):
    for lib in libs:
        __handle_events(lib)
    result = []
    try:
        while 1:
            result.append(__events.get(False))
    except Queue.Empty:
        pass
    return result

def put(an_event):
    __events.put(an_event)
    
