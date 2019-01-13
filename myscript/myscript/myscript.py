#!/usr/bin/env python3.7

import iterm2
import objc
from AppKit import *
# To install packages from PyPI, use this command, changing package_name to the package you
# wish to install:
#   "/Users/huangyingw/Library/ApplicationSupport/iTerm2/Scripts/myscript/iterm2env/versions/3.7.1/bin/pip3" install package_name


async def main(connection):
    app = await iterm2.async_get_app(connection)

    async def move_current_tab_by_n_windows(delta):
        tab_to_move = app.current_terminal_window.current_tab
        window_with_tab_to_move = app.get_window_for_tab(tab_to_move.tab_id)
        i = app.terminal_windows.index(window_with_tab_to_move)
        n = len(app.terminal_windows)
        j = (i + delta) % n

        if i == j:
            window = await iterm2.Window.async_create(connection)
            await window.async_set_fullscreen(False)
            await window.async_set_tabs([tab_to_move])

            screenFrame = NSScreen.screens()[0].frame()
            new_window_frame = iterm2.Frame(iterm2.Point(screenFrame.origin.x, screenFrame.origin.y), iterm2.Size(screenFrame.size.width, screenFrame.size.height))
            await window.async_set_frame(new_window_frame)
        else:
            window = app.terminal_windows[j]
            await window.async_set_tabs(window.tabs + [tab_to_move])

    @iterm2.RPC
    async def move_current_tab_to_next_window():
        await move_current_tab_by_n_windows(1)
    await move_current_tab_to_next_window.async_register(connection)

    @iterm2.RPC
    async def move_current_tab_to_previous_window():
        n = len(app.terminal_windows)
        if n > 0:
            await move_current_tab_by_n_windows(n - 1)
    await move_current_tab_to_previous_window.async_register(connection)

iterm2.run_forever(main)
