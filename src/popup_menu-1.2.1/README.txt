# PopupMenu
# Version:  v1.2.1
# Description: A low-fuss, infinitely nested popup menu for pygame.
# Author: Gummbum
# Home: http://code.google.com/p/simple-pygame-menu/
# Source: See home.


Changes since v1.2
==================
*   PopupMenu.handle_events() now returns MOUSEMOTION events. It would be kinda
    useful to get them if your mouse pointer is a sprite.
*   Added a visible property to NonBlockingPopupMenu, which wraps the show() and
    hide() methods.
*   Tweaked demos.

Changes since v1.1
==================
*   Added class NonBlockingPopupMenu to simplify use.
*   Added exception handlers around "import data" and font initialization. If
    the data.py cannot be imported, or the preferred font cannot be loaded from
    file, the default system font is quietly used. This supports less
    restrictive inclusion in other libraries.
*   Added pos=None parameter to constructors to provide the option of explicit
    positioning.
*   Added class SubmenuLabel for strong-typing of submenu text in menus. This
    allows PopupMenu.handle_events() to accurately detect submenus as opposed to
    endswith('...'). It also lifts the restriction implied by depending on
    endswith('...'), so coders are free to put any text they want in labels
    without side-effects.
*   Tweaked demos.
