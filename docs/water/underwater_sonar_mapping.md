# 水域载具 - 水下声呐三维测深与避障 ROS 2 封装模块

## 作业概述与背景
本模块基于水下声呐探测原理，在 ROS 2 环境下实现了一个水下三维地形测绘与避障仿真节点。节点模拟了声呐探测海底起伏以及识别障碍物的过程，实时生成包含障碍物信息的三维海底地形图，为水下航行器的自主避障提供环境感知基础。

## 二、运行环境
* 操作系统：Ubuntu 22.04（虚拟机）
* ROS 2 版本：Humble
* 依赖库：rclpy, matplotlib, numpy

## 核心代码文件
* `src/underwater_sonar_mapping/underwater_sonar_mapping.py`：三维声呐测绘与障碍物可视化节点。

## 运行步骤
```bash
cd ~/my_ws
source /opt/ros/humble/setup.bash
python3 src/underwater_sonar_mapping/underwater_sonar_mapping.py
```
## 五、运行效果（截图）
https://github.com/123ycx123/ros2/blob/123ycx123-patch-2/docs/img/capture_4.png

效果说明：节点成功启动，基于模拟声呐数据生成了三维海底地形，并清晰标注了水下沉船/暗礁等障碍物位置，验证了声呐三维测绘与避障感知算法的可行性。

## 提交信息（Commit Message / PR 描述）
text
feat(water): 新增水下声呐三维测深与避障 ROS 2 封装模块

基于 ROS 2 实现了声呐三维地形测绘与障碍物可视化。

已验证：
1. 程序运行正常
2. 3D 海底地形与障碍物绘制成功
3. 声呐波束模拟正确

---
