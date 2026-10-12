#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""终端原始按键读取：纯标准库实现（不依赖 ROS 与第三方库），供 ROS 键盘节点与独立演示共用。
"""
from __future__ import annotations

import os
import select
import sys
from typing import List


class RawKeyReader:
    """把终端切成非规范、非回显模式，逐个读出按键；用完需 ``restore()``。

    stdin 非终端（重定向或 launch 接管）时 ``is_tty`` 为 False，``read()`` 恒返回空列表。
    """

    def __init__(self, warn=None):
        self.is_tty = sys.stdin.isatty()
        self._termios = None
        self._old = None
        if self.is_tty:
            try:
                import termios
                import tty
                self._termios = termios
                self._old = termios.tcgetattr(sys.stdin.fileno())
                tty.setcbreak(sys.stdin.fileno())
            except Exception as e:                    # noqa: BLE001
                self.is_tty = False
                if warn:
                    warn("无法进入原始终端模式：%s" % e)

    def read(self) -> List[str]:
        """非阻塞读出当前已到达的按键。"""
        if not self.is_tty:
            return []
        out: List[str] = []
        try:
            while select.select([sys.stdin], [], [], 0)[0]:
                ch = os.read(sys.stdin.fileno(), 1).decode("utf-8", "replace")
                if not ch:
                    break
                out.append(ch)
        except (OSError, ValueError):
            self.is_tty = False
        return out

    def restore(self) -> None:
        if self._old is not None and self._termios is not None:
            try:
                self._termios.tcsetattr(sys.stdin.fileno(),
                                        self._termios.TCSADRAIN, self._old)
            except Exception:                          # noqa: BLE001
                pass
            self._old = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.restore()
        return False
