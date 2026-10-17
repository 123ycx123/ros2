# 人形机器人 - 基于 ZMP 的步行轨迹规划 ROS 2 封装模块

基于简化的人形机器人 ZMP（零力矩点）运动学模型，实时绘制出机器人的运动姿态。

## 核心代码文件

* `main.py`：ZMP 步行轨迹规划与可视化节点。
* `setup.py`：配置文件。
* `launch/main.launch.py`：一键启动文件。
  
## 核心代码文件清单

本模块包含以下核心文件，均已提交至仓库：

```text
src/
└── humanoid_zmp_walk_planner/
    ├── main.py                 # ZMP 步行轨迹规划与可视化节点
    ├── setup.py                # ROS 2 功能包配置文件
    ├── package.xml             # ROS 2 依赖声明文件
    ├── README.md               # 模块说明文档
    └── launch/
        └── main.launch.py      # 一键启动文件
```
## 运行步骤

```bash
colcon build --packages-select humanoid_zmp_walk_planner
source install/setup.bash
ros2 launch humanoid_zmp_walk_planner main.launch.py
```
> 📖 **详细原理与实验步骤请参阅：** [点击查看主文档](../../docs/humanoid/zmp_walk_planner.md)
