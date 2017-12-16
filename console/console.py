# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/12/16
Description:
    console.py
----------------------------------------------------------------------------"""

import asyncio

from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.filters import IsDone, HasFocus, RendererHeightIsKnown, to_simple_filter, to_cli_filter, Condition
from prompt_toolkit.layout.screen import Char
from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer, AcceptAction
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import VSplit, HSplit, Window, FloatContainer, Float
from prompt_toolkit.layout.controls import BufferControl, FillControl, TokenListControl
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.shortcuts import create_asyncio_eventloop
from prompt_toolkit.token import Token
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.filters import Always
from prompt_toolkit.document import Document


class Console(object):
    def __init__(self, title="", commands={}, get_left_buffer=None, get_right_buffer=None):
        self._title = title
        self._toolbar_tips = ""
        self._commands = commands
        self._get_left_buffer = get_left_buffer if get_left_buffer else lambda: ""
        self._get_right_buffer = get_right_buffer if get_right_buffer else lambda: ""
        self._init_word_completer()
        self._init_buffers()
        self._init_layouts()
        self._init_style()
        self._init_application()

        self._stop = False

    def _get_title_tokens(self, cli):
        return [
            (Token.Title, ' %s ' % self._title),
            (Token.Title, ' (Press [Ctrl-Q] to quit.)'),
        ]

    def _get_bottom_toolbar_tokens(self, cli):
        return [(Token.Toolbar, " -- %s -- " % self._toolbar_tips if self._toolbar_tips else "")]

    def _init_layouts(self):
        self._layout = HSplit([
            # title
            Window(height=D.exact(1), content=TokenListControl(self._get_title_tokens, align_center=True)),
            # separator
            Window(height=D.exact(1), content=FillControl('-', token=Token.Line)),
            # body
            VSplit([
                # left buffer
                Window(content=BufferControl(buffer_name='LEFT')),
                # separator
                Window(width=D.exact(1), content=FillControl('|', token=Token.Line)),
                # right buffer
                Window(content=BufferControl(buffer_name='RIGHT')),
            ]),
            # separator
            Window(height=D.exact(1), content=FillControl('-', token=Token.Line)),
            FloatContainer(
                # input field
                Window(height=D.exact(3), content=BufferControl(buffer_name=DEFAULT_BUFFER)),
                # completion menus
                [Float(xcursor=True, ycursor=True,
                       content=CompletionsMenu(max_height=5, scroll_offset=-1, extra_filter=Always())), ]
            ),
            # bottom toolbar
            ConditionalContainer(
                Window(
                    TokenListControl(self._get_bottom_toolbar_tokens, default_char=Char(' ', Token.Toolbar)),
                    height=D.exact(1)), filter=~IsDone() & RendererHeightIsKnown())
        ])

        return self._layout

    registry = load_key_bindings()

    @staticmethod
    @registry.add_binding(Keys.ControlC, eager=True)
    @registry.add_binding(Keys.ControlQ, eager=True)
    def _quit_event_handler(event):
        event.cli.set_return_value(None)

    def _init_word_completer(self):
        self._word_completer = WordCompleter(self._commands.keys(), ignore_case=True)
        return self._word_completer

    def _accept_handler(self, cli, buffer):
        splits = buffer.text.split()
        if splits:
            command = splits[0]
            args = splits[1:]
            self._run_command(command, args)
        buffer.reset(None, True)

    def _init_buffers(self):
        self._buffers = {
            DEFAULT_BUFFER: Buffer(is_multiline=False, history=InMemoryHistory(), enable_history_search=True,
                                   completer=self._word_completer, complete_while_typing=True,
                                   accept_action=AcceptAction(handler=self._accept_handler)),
            'LEFT': Buffer(is_multiline=True, read_only=True),
            'RIGHT': Buffer(is_multiline=True, read_only=True),
        }

    def _init_style(self):
        self._style = style_from_dict({
            Token.Toolbar: '#ffffff bg:#ff0000',
            Token.Title: '#ffffff bg:#ff0000',
        })
        return self._style

    def _init_application(self):
        self._application = Application(
            style=self._style,
            layout=self._layout,
            buffers=self._buffers,
            key_bindings_registry=self.registry,
            mouse_support=True,
            use_alternate_screen=True,
        )
        return self._application

    def _force_render(self):
        self._cli.renderer.render(self._cli, self._layout)

    def _run_command(self, command, args):
        if command not in self._commands:
            self.set_toolbar_tips("command %s is not exist." % command)
            return

        try:
            func = self._commands.get(command)
            func(*args)
            self.set_toolbar_tips("%s success." % command)
        except Exception as ex:
            self.set_toolbar_tips(str(ex))

    async def _refresh_buffers(self):
        while True:
            if self._stop:
                return
            await asyncio.sleep(0.3)
            self._buffers["LEFT"].set_document(Document(self._get_left_buffer(), -1), True)
            self._buffers["RIGHT"].set_document(Document(self._get_right_buffer(), -1), True)
            self._force_render()

    async def run(self):
        eventloop = create_asyncio_eventloop()

        try:
            self._cli = CommandLineInterface(application=self._application, eventloop=eventloop)
            await asyncio.wait((self._refresh_buffers(), self._cli.run_async(),))

        finally:
            eventloop.close()

    def set_title(self, title):
        self._title = title

    def set_toolbar_tips(self, toolbar_tips):
        self._toolbar_tips = toolbar_tips


if __name__ == '__main__':
    import time

    cmd = ""


    def l():
        return "cmd: %s\n %f" % (cmd, time.time())


    def set_cmd(x):
        global cmd
        cmd = x


    commands = {
        "set_cmd": set_cmd,
        "clear_cmd": lambda: set_cmd("")
    }

    c = Console(title="TEST", commands=commands, get_left_buffer=l, get_right_buffer=l)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(c.run())


def start():
    pass
