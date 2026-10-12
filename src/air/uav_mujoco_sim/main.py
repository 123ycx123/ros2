#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""uav_mujoco_sim 统一入口（main 开头）：薄封装，逻辑在 ``uav_mujoco_sim/cli.py``。

源码目录 ``python main.py …`` 与安装后 ``ros2 run uav_mujoco_sim main …`` 走同一份代码。
"""
import os
import sys

# 源码目录直接运行时保证包可 import（安装后为 no-op）
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from uav_mujoco_sim.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
