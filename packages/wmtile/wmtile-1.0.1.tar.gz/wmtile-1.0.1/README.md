```
usage: wmtile [-h] [-H] [-Y PDF_BROWSER] [-V] [-L] [-S] [-m] [-t] [-p] [-l]
              [-s] [-b] [-c]

WMTile - a window tiler for XFCE desktop environment

WMTile is a pure-Python Linux/BSD free and open-source utility to be used with
XFCE  4.18/4.20  desktop  environment  to  reshape  in  seven ways the visible
windows  in  current  workspace, while minimized windows remain hidden. But if
there  are no visible windows, WMTile makes visible and reshapes all minimized
windows.

Before installing WMTile, for instance on a Debian-derived Linux type:

    $ sudo apt update
    $ sudo apt upgrade
    $ sudo apt install wmctrl xdotool pipx
    $ sudo apt install x11-utils

On  other  platforms  you will use the specific installer instead. If you have
trouble with x11-utils, install xwininfo instead.

Then install WMTile by typing (without sudo):

    $ pipx install wmtile
    $ pipx ensurepath

Now you can close the terminal, open another one, and run WMTile. For example,
to tile all visible windows in current workspace, type:

    $ wmtile -t

As a CLI program, always give to WMTile one and only one argument, only -H and
-Y can go together.

Later you can type:

    $ pipx upgrade wmtile

in order to upgrade WMTile to a later version.

WMTile is a CLI program, but it's more convenient to use it either by mouse or
by keyboard.

To use WMTile by mouse you'll create seven panel launchers by:

    $ wmtile -L
    Creating 7 panel launchers...
        panel launcher 'wmtile -m' not found, created
        panel launcher 'wmtile -t' not found, created
        panel launcher 'wmtile -p' not found, created
        panel launcher 'wmtile -l' not found, created
        panel launcher 'wmtile -s' not found, created
        panel launcher 'wmtile -b' not found, created
        panel launcher 'wmtile -c' not found, created

To use WMTile by keyboard you'll create seven keyboard shortcuts by:

    $ wmtile -S'
    Creating 7 keyboard shortcuts...
        keyboard shortcut Alt+Shift+M --> 'wmtile -m' created
        keyboard shortcut Alt+Shift+T --> 'wmtile -t' created
        keyboard shortcut Alt+Shift+P --> 'wmtile -p' created
        keyboard shortcut Alt+Shift+L --> 'wmtile -l' created
        keyboard shortcut Alt+Shift+S --> 'wmtile -s' created
        keyboard shortcut Alt+Shift+B --> 'wmtile -b' created
        keyboard shortcut Alt+Shift+C --> 'wmtile -c' created
    Please reboot in order to make the keyboard shortcuts effective.

You can fine-tune WMTile's behavior using four parameters in file:

    ~/.config/wmtile/wmtile.cfg

For further details, see the WMTile User Manual by:

    $ wmtile -H

options:
  -h, --help            show this help message and exit
  -H, --user-manual     browse the User Manual in PDF format and exit
  -Y PDF_BROWSER, --pdf-browser PDF_BROWSER
                        PDF browser used by -H, default: 'xdg-open' = system
                        default PDF browser
  -V, --version         show program's version number and exit
  -L, --launchers       create 7 panel launchers
  -S, --shortcuts       create 7 keyboard shortcuts
  -m, --minimize        minimize visible windows
  -t, --tile            reshape visible windows as tiles
  -p, --portrait        reshape visible windows as portraits
  -l, --landscape       reshape visible windows as landscapes
  -s, --stack           reshape visible windows as a stack
  -b, --maximize        maximize visible windows
  -c, --close           gracefully close visible windows
```
