# 人形机器人 - 基于 ZMP 的步行轨迹规划 ROS 2 封装模块

## 作业概述与背景
本模块基于简化的人形机器人 ZMP（零力矩点）运动学模型，在 ROS 2 环境下实现了一个步行轨迹规划与可视化节点。节点模拟了人形机器人一个完整步态周期（支撑期与摆动期）的足部轨迹，并实时绘制出机器人的运动姿态，验证了双足行走的步态规划逻辑。

## 运行环境
* 操作系统：Ubuntu 22.04（虚拟机）
* ROS 2 版本：Humble
* 依赖库：rclpy, geometry_msgs, matplotlib, numpy

## 核心代码文件清单
本模块包含以下核心文件，均已提交至仓库：
* `src/humanoid_zmp_walk_planner/humanoid_zmp_walk_planner.py`：ZMP 步行轨迹规划与可视化节点。
* `src/humanoid_zmp_walk_planner/setup.py`：ROS 2 功能包配置文件。
* `src/humanoid_zmp_walk_planner/launch/main.launch.py`：一键启动文件。

## 运行步骤
在终端中执行以下命令运行该模块：
```bash
cd ~/my_ws
source /opt/ros/humble/setup.bash
python3 src/humanoid_zmp_walk_planner/humanoid_zmp_walk_planner.py
```
## 五、运行效果（截图）
![运行效果](img/capture_3.png)

效果说明：节点成功启动，实时计算并绘制出人形机器人的足部运动轨迹，图形界面成功展示了机器人的行走姿态，验证了 ZMP 步行规划算法的正确性。

## 提交信息（Commit Message / PR 描述）
text
feat(humanoid): 新增基于 ZMP 的人形机器人步行轨迹规划 ROS 2 封装模块

基于简化双足 ZMP 模型实现了人形机器人步行轨迹规划与可视化。

已验证：
1. 程序运行正常
2. 人形机器人步行轨迹绘制成功
3. 终端实时输出足部高度数据
text


