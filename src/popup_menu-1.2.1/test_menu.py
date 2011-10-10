#!/usr/bin/env python

"""test_menu.py - A no-fuss popup menu demo.

High-level steps for a blocking menu:

1.  Fashion a nested list of strings for the PopupMenu constructor.
2.  Upon creation, the menu runs its own loop.
3.  Upon exit, control is returned to the caller.
4.  Handle the resulting USEREVENT event in the caller where
    event.name=='your menu title', event.item_id holds the selected item
    number, and event.text holds the item label.
"""

# PopupMenu
# Version:  v1.2.1
# Description: A low-fuss, infinitely nested popup menu for pygame.
# Author: Gummbum
# Home: http://code.google.com/p/simple-pygame-menu/
# Source: See home.


import os
import sys

import pygame
from pygame.locals import *

progname = sys.argv[0]
progdir = os.path.dirname(progname)
sys.path.append(os.path.join(progdir,'gamelib'))

from popup_menu import PopupMenu


screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

## Menu data and functions.

menu_data = (
    'Main',
    'Item 0',
    'Item 1',
    (
        'Things',
        'Item 0',
        'Item 1',
        'Item 2',
        (
            'More Things',
            'Item 0',
            'Item 1',
        ),
    ),
    'Quit',
)
def handle_menu(e):
    print 'Menu event: %s.%d: %s' % (e.name,e.item_id,e.text)
    if e.name == 'Main':
        if e.text == 'Quit':
            quit()
    elif e.name == 'Things':
        pass
    elif e.name == 'More Things':
        pass

## Main loop.

while 1:
    screen.fill(Color('darkblue'))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == MOUSEBUTTONUP:
            ## Blocking popup menu.
            PopupMenu(menu_data)
        elif e.type == USEREVENT:
            if e.code == 'MENU':
                handle_menu(e)
    clock.tick(30)
