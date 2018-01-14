# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/12/16
Description:
    watcher_console.py
----------------------------------------------------------------------------"""

import time

from threading import Thread

from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.filters import IsDone, RendererHeightIsKnown
from prompt_toolkit.layout.screen import Char
from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer, AcceptAction
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import VSplit, HSplit, Window, FloatContainer, Float
from prompt_toolkit.layout.controls import BufferControl, FillControl, TokenListControl
from prompt_toolkit.layout.dimension import LayoutDimension as Dim
from prompt_toolkit.shortcuts import create_eventloop
from prompt_toolkit.token import Token
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.filters import Condition
from prompt_toolkit.document import Document

from core.watcher import WatcherClient


class Console(object):
    def __init__(self, title="", commands={}, get_left_top_buffer=None, get_left_bottom_buffer=None,
                 get_right_buffer=None):
        self._title = title
        self._left_top_buffer_title = ""
        self._left_bottom_buffer_title = ""
        self._right_buffer_title = ""
        self._toolbar_tips = ""
        self._commands = commands
        self._get_left_top_buffer = get_left_top_buffer if get_left_top_buffer else lambda: ""
        self._get_left_bottom_buffer = get_left_bottom_buffer if get_left_bottom_buffer else lambda: ""
        self._get_right_buffer = get_right_buffer if get_right_buffer else lambda: ""
        self._registry_key()
        self._init_word_completer()
        self._init_buffers()
        self._init_layouts()
        self._init_style()
        self._init_application()

        self._cli = None
        self._thread_cli = None
        self._thread_data = None
        self._stop = False

    def _get_title_tokens(self, cli):
        return [
            (Token.Title, ' %s ' % self._title.upper()),
        ]

    def _get_left_top_buffer_title(self, cli):
        return [
            (Token.Category, ' %s ' % self._left_top_buffer_title),
        ]

    def _get_left_bottom_buffer_title(self, cli):
        return [
            (Token.Category, ' %s ' % self._left_bottom_buffer_title),
        ]

    def _get_right_buffer_title(self, cli):
        return [
            (Token.Category, ' %s ' % self._right_buffer_title),
        ]

    def _get_bottom_toolbar_tokens(self, cli):
        return [(Token.Toolbar, " -- %s -- " % self._toolbar_tips if self._toolbar_tips else "")]

    def _show_completions(self, cli):
        return " " not in self._buffers[DEFAULT_BUFFER].text

    def _init_layouts(self):
        self._layout = HSplit([
            # title
            Window(height=Dim.exact(1),
                   content=TokenListControl(self._get_title_tokens, default_char=Char(' ', Token.Title),
                                            align_center=True)),
            # separator
            Window(height=Dim.exact(1), content=FillControl('-', token=Token.Line)),
            # body
            VSplit([
                # left buffer
                HSplit([
                    Window(height=Dim.exact(1),
                           content=TokenListControl(self._get_left_top_buffer_title,
                                                    default_char=Char(' ', Token.Category), )),
                    Window(content=BufferControl(buffer_name='LEFT_TOP')),
                    Window(height=Dim.exact(1), content=FillControl('-', token=Token.Line)),
                    Window(height=Dim.exact(1),
                           content=TokenListControl(self._get_left_bottom_buffer_title,
                                                    default_char=Char(' ', Token.Category), )),
                    Window(content=BufferControl(buffer_name='LEFT_BOTTOM')),
                ]),
                # separator
                Window(width=Dim.exact(1), content=FillControl('|', token=Token.Line)),
                # right buffer
                HSplit([
                    Window(height=Dim.exact(1),
                           content=TokenListControl(self._get_right_buffer_title,
                                                    default_char=Char(' ', Token.Category), )),
                    Window(content=BufferControl(buffer_name='RIGHT')),
                ]),
            ]),
            # separator
            Window(height=Dim.exact(1), content=FillControl('-', token=Token.Line)),
            FloatContainer(
                # input field
                Window(height=Dim.exact(3), content=BufferControl(buffer_name=DEFAULT_BUFFER)),
                # completion menus
                [Float(xcursor=True, ycursor=True,
                       content=CompletionsMenu(max_height=5,
                                               scroll_offset=-1,
                                               extra_filter=Condition(self._show_completions))), ]
            ),
            # bottom toolbar
            ConditionalContainer(
                Window(
                    TokenListControl(self._get_bottom_toolbar_tokens, default_char=Char(' ', Token.Toolbar)),
                    height=Dim.exact(1)), filter=~IsDone() & RendererHeightIsKnown())
        ])

        return self._layout

    def _registry_key(self):
        self._key_bindings = load_key_bindings()

        @self._key_bindings.add_binding(Keys.ControlC, eager=True)
        def _quit_event_handler(event):
            self._stop = True
            self._cli.set_return_value(None)

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
            'LEFT_TOP': Buffer(is_multiline=True, read_only=True),
            'LEFT_BOTTOM': Buffer(is_multiline=True, read_only=True),
            'RIGHT': Buffer(is_multiline=True, read_only=True),
        }

    def _init_style(self):
        self._style = style_from_dict({
            Token.Title: '#000000 bg:#ffffff',
            Token.Category: '#000000 bg:#00ff00',
            Token.Toolbar: '#ffffff bg:#ff0000',
        })
        return self._style

    def _init_application(self):
        self._application = Application(
            style=self._style,
            layout=self._layout,
            buffers=self._buffers,
            key_bindings_registry=self._key_bindings,
            mouse_support=True,
            use_alternate_screen=True,
        )
        return self._application

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

    def _refresh_buffers(self):
        while True:
            if self._stop:
                return

            time.sleep(0.3)

            self._left_top_buffer_title, left_top_buffer = self._get_left_top_buffer()
            self._left_bottom_buffer_title, left_bottom_buffer = self._get_left_bottom_buffer()
            self._right_buffer_title, right_buffer = self._get_right_buffer()

            self._buffers["LEFT_TOP"].set_document(Document(left_top_buffer, -1), True)
            self._buffers["LEFT_BOTTOM"].set_document(Document(left_bottom_buffer, -1), True)
            self._buffers["RIGHT"].set_document(Document(right_buffer, -1), True)
            self._cli.invalidate()

    def _run_cli(self):
        self._cli.run()

    def run(self):
        event_loop = create_eventloop()

        try:
            self._cli = CommandLineInterface(application=self._application, eventloop=event_loop)
            self._thread_cli = Thread(target=self._run_cli)
            self._thread_data = Thread(target=self._refresh_buffers)

            self._thread_cli.start()
            self._thread_data.start()

            self._thread_cli.join()
            self._thread_data.join()

        finally:
            event_loop.close()

    def set_title(self, title):
        self._title = title

    def set_toolbar_tips(self, toolbar_tips):
        self._toolbar_tips = toolbar_tips


def start(watcher_key="grabber"):
    watcher_key = watcher_key
    watcher_client = WatcherClient(watcher_key)
    watcher_commands = watcher_client.get_commands()
    commands = {}
    buffers = {"left_top": "", "left_bottom": "", "right": ""}

    for command in watcher_commands:
        def func(*args, cmd=command):
            buffers["left_bottom"] = str(watcher_client.run_command(cmd, *args))

        commands[command] = func

    def get_left_top_buffer():
        status = watcher_client.get_status()
        lines = []
        for k, v in status.items():
            line = "    %s: %s" % (str(k), str(v))
            lines.append(line)
        buffers["left_top"] = "\n%s" % "\n".join(lines)
        return "status: ", buffers["left_top"]

    def get_right_buffer():
        lines = []
        logs = watcher_client.get_logs(10)
        for log in logs:
            lines.append(log)
        buffers["right"] = "\n".join(lines)
        return "log:", buffers["right"]

    def get_left_bottom_buffer():
        return "command result:", buffers["left_bottom"]

    console = Console(title="watcher_%s" % watcher_key, commands=commands,
                      get_left_top_buffer=get_left_top_buffer,
                      get_left_bottom_buffer=get_left_bottom_buffer,
                      get_right_buffer=get_right_buffer)

    console.run()
