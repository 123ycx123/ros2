#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""键盘遥控 ROS2 节点：发布 ``/uav/cmd_vel``（geometry_msgs/Twist），由 ``uav_sim_bridge`` 执行；按键映射集中在 ``core/teleop.py``。

用 ``termios`` 非规范、非回显模式读取单键；stdin 非终端（如被 ``ros2 launch`` 重定向）时退化为按行读取并在日志提示。
"""
from __future__ import annotations

import os
import select
import sys
import threading
import time

import rclpy
from rclpy.node import Node

import geometry_msgs.msg

try:
    from ..core.teleop import TeleopConfig, command_from_keys, key_help, EXIT_KEYS
    from ..core.terminal import RawKeyReader
    from .conversions import make_twist
except ImportError:  # pragma: no cover
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from uav_mujoco_sim.core.teleop import (TeleopConfig, command_from_keys,
                                            key_help, EXIT_KEYS)
    from uav_mujoco_sim.core.terminal import RawKeyReader
    from uav_mujoco_sim.ros.conversions import make_twist


class KeyboardNode(Node):
    def __init__(self):
        super().__init__("uav_keyboard_teleop")

        self.declare_parameter("speed/horiz", 1.0)
        self.declare_parameter("speed/vert", 0.6)
        self.declare_parameter("speed/yaw", 0.6)
        self.declare_parameter("publish_hz", 20.0)
        self.declare_parameter("topic/cmd_vel", "/uav/cmd_vel")
        self.declare_parameter("hold_timeout", 0.25)
        #: 终端无按键“抬起”事件，超时无新按键即视为松手。
        self.declare_parameter("key_ttl", 0.20)

        g = self.get_parameter
        self.cfg = TeleopConfig(
            horiz_speed=float(g("speed/horiz").value),
            vert_speed=float(g("speed/vert").value),
            yaw_rate=float(g("speed/yaw").value),
        )
        self.key_ttl = float(g("key_ttl").value)

        self.pub = self.create_publisher(
            geometry_msgs.msg.Twist, g("topic/cmd_vel").value, 10)

        self.keys = RawKeyReader(warn=lambda m: self.get_logger().warn(m))
        if not self.keys.is_tty:
            self.get_logger().warn(
                "stdin 不是终端，键盘节点收不到按键。请在本机终端直接运行 "
                "`python3 main.py --keyboard`，或改用不依赖 ROS 的 "
                "`python3 main.py --demo`。")
        self._pressed = set()
        self._last_key_t = -1e9
        self._stop = False

        hz = max(float(g("publish_hz").value), 1.0)
        self.timer = self.create_timer(1.0 / hz, self.on_timer)

        self.get_logger().info(
            "\n键盘遥控已启动（发布 %s）\n%s\n"
            "提示：按键后若无人机没反应，先确认 uav_sim_bridge 已启动。"
            % (g("topic/cmd_vel").value, key_help()))

        # 终端读取在单独线程，避免阻塞 ROS 执行器
        self._thread = threading.Thread(target=self._pump, daemon=True)
        self._thread.start()

    def _pump(self):
        while not self._stop and rclpy.ok():
            for ch in self.keys.read():
                if ch in EXIT_KEYS:
                    self.get_logger().info("收到退出键，正在关闭…")
                    self._stop = True
                    return
                if ch.lower() in "wasdrfqe":
                    self._pressed = {ch.lower()}     # 单键独占，避免多键残留
                    self._last_key_t = time.monotonic()
            time.sleep(0.01)

    def on_timer(self):
        if self._stop:
            raise KeyboardInterrupt
        now = time.monotonic()
        active = (now - self._last_key_t) < self.key_ttl
        keys = self._pressed if active else set()
        # 超时清空 → 松手即停
        if not active:
            self._pressed = set()
        vx, vy, vz, wz = command_from_keys(keys, self.cfg)
        self.pub.publish(make_twist(vx, vy, vz, wz))

    def destroy_node(self):
        self._stop = True
        try:
            self.pub.publish(make_twist(0.0, 0.0, 0.0, 0.0))   # 退出前发悬停
        except Exception:                                       # noqa: BLE001
            pass
        self.keys.restore()
        super().destroy_node()


def main(argv=None):
    rclpy.init(args=argv)
    node = None
    try:
        node = KeyboardNode()
        rclpy.spin(node)
    except (KeyboardInterrupt, Exception):        # noqa: BLE001
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    print("\n键盘遥控已退出。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
