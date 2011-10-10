#!/usr/bin/env python

"""test_menu_non_blocking.py - A non-blocking popup menu demo.

This mode of operation allows the main loop to keep processing. Drawing the menu
and using its events is the responsibility of the calling loop.

High-level steps for a non-blocking menu:

1.  Fashion a nested list of strings for the NonBlockingPopupMenu constructor.
2.  Store the menu object in a variable.
3.  Construct the NonBlockingPopupMenu object.
4.  Detect the condition that triggers the menu to post, and call menu.show()
    (or set menu.visible=True).
5.  Call menu.draw() to draw the menu. If it is visible, it will be drawn.
6.  Pass pygame events to menu.handle_events() and process the unhandled events
    that are returned as you would pygame's events. If the menu is not visible
    the method will immediately return the list passed in, unchanged.
7.  Upon menu exit, one or two USEREVENTs are posted via pygame. Retrieve them
    and recognize they are menu events (i.e., event.code=='MENU').
    a.  A menu-exit event signals the menu has detected an exit condition, which
        may or many not be accompanied by a menu selection. Recognize this by
        event.name==None or event.menu_id==-1. Upon receiving this event the
        main loop should call menu.hide() (or set menu.visible=False).
    b.  A menu-selection event signals the main loop that a menu item was
        selected. Recognize this by event.name=='your menu title'. event.menu_id
        holds the selected item number, and event.text holds the item label.
8.  Destroying the menu is optional.
9.  Assigning to menu.init_data, or changing its contents or that of the
    original list variable, will result in a modified menu the next time
    menu.show() is called (or menu.visible is set to True).
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

from popup_menu import NonBlockingPopupMenu


screen = pygame.display.set_mode((600,600))
pygame.display.set_caption('Click for menu. Press keys at any time. Watch stdout.')
screen_rect = screen.get_rect()
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

menu = NonBlockingPopupMenu(menu_data)

def handle_menu(e):
    global menu
    print 'Menu event: %s.%d: %s' % (e.name,e.item_id,e.text)
    if e.name is None:
        print 'Hide menu'
        menu.hide()
    elif e.name == 'Main':
        if e.text == 'Quit':
            quit()
    elif e.name == 'Things':
        pass
    elif e.name == 'More Things':
        pass

## Motion ball to demonstrate main loop still runs while menu is posted.

class Ball(object):
    def __init__(self):
        self.image = pygame.surface.Surface((20,20))
        self.image.fill(Color('white'))
        self.rect = self.image.get_rect(topleft=(303,204))
        self.dx,self.dy = 2,-2
    def update(self, bounds):
        ball_rect = self.rect
        ball_rect.x += self.dx
        ball_rect.y += self.dy
        if ball_rect.x < bounds.left or ball_rect.right > bounds.right:
            self.dx *= -1
        if ball_rect.y < bounds.top or ball_rect.bottom > bounds.bottom:
            self.dy *= -1
    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect)
ball = Ball()

## Sprite cursor also runs while menu is posted.

class Cursor(object):
    def __init__(self):
        self.image = pygame.surface.Surface((13,13))
        pygame.draw.line(self.image, Color('yellow'), (6,0), (6,12), 5)
        pygame.draw.line(self.image, Color('yellow'), (0,6), (12,6), 5)
        pygame.draw.line(self.image, Color(0,0,99), (6,0), (6,12), 3)
        pygame.draw.line(self.image, Color(0,0,99), (0,6), (12,6), 3)
        pygame.draw.line(self.image, Color('black'), (6,0), (6,120), 1)
        pygame.draw.line(self.image, Color('black'), (0,6), (12,6), 1)
        self.image.set_colorkey(Color('black'))
        self.rect = self.image.get_rect(center=(0,0))
        pygame.mouse.set_visible(False)
    def draw(self):
        pygame.display.get_surface().blit(self.image, self.rect)
cursor = Cursor()

## Main loop.

while 1:
    
    # update and draw ball
    screen.fill(Color('darkblue'))
    ball.update(screen_rect)
    ball.draw()
    
    # If the menu is visible it will be drawn.
    menu.draw()
    
    cursor.draw()
    pygame.display.flip()
    
    # Pass them through the menu. If the menu is visible it will consume mouse
    # events and return any unhandled events; else it will return them all.
    # Process the unhandled events returned by the menu. Function handle_menu()
    # processes only events posted by the menu.
    for e in menu.handle_events(pygame.event.get()):
        if e.type == KEYDOWN:
            print 'Key pressed:',pygame.key.name(e.key)
        elif e.type == MOUSEBUTTONUP:
            print 'Show menu'
            menu.show()
        elif e.type == MOUSEMOTION:
            cursor.rect.center = e.pos
        elif e.type == USEREVENT:
            if e.code == 'MENU':
                handle_menu(e)
    
    clock.tick(60)
