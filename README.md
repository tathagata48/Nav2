# my_robot — Nav2 ROS2 Gazebo Project

A complete autonomous mobile robot navigation stack built with **ROS2 Humble**, **Nav2**, and **Gazebo Classic (Gazebo 11)**. Features a differential drive robot with 2D lidar, SLAM-based mapping, AMCL localization, and full Nav2 autonomous navigation.

---

## Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [1. Launch Gazebo Simulation](#1-launch-gazebo-simulation)
  - [2. SLAM Mapping](#2-slam-mapping)
  - [3. Save Map](#3-save-map)
  - [4. Autonomous Navigation](#4-autonomous-navigation)
- [Package Overview](#package-overview)
- [Robot Specifications](#robot-specifications)
- [Project Structure](#project-structure)

---

## Architecture

```
Gazebo (physics simulation)
    │
    ├── /scan       (LaserScan, 360° lidar @ 10Hz)
    ├── /odom       (Odometry from diff drive plugin)
    └── /cmd_vel    (Twist commands from Nav2 controller)
    
Nav2 Stack
    ├── SLAM Toolbox    → /map (occupancy grid)
    ├── AMCL            → localization on saved map
    ├── Planner Server  → NavFn (Dijkstra global planner)
    ├── Controller      → DWB (local trajectory planner)
    ├── Costmap 2D      → global + local costmaps
    └── BT Navigator    → behavior trees for goal execution
```

---

## Prerequisites

- **OS**: Ubuntu 22.04 (Jammy)
- **ROS2**: Humble Hawksbill ([install guide](https://docs.ros.org/en/humble/Installation.html))
- **Gazebo**: Classic 11.x

### Install ROS2 Dependencies

```bash
sudo apt update && sudo apt install -y \
  ros-humble-nav2-bringup \
  ros-humble-nav2-bt-navigator \
  ros-humble-nav2-controller \
  ros-humble-nav2-costmap-2d \
  ros-humble-nav2-map-server \
  ros-humble-nav2-planner \
  ros-humble-nav2-recoveries \
  ros-humble-nav2-smoother \
  ros-humble-slam-toolbox \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros \
  ros-humble-robot-state-publisher \
  ros-humble-joint-state-publisher-gui \
  ros-humble-xacro \
  ros-humble-rviz2 \
  ros-humble-dwb-core \
  ros-humble-dwb-critics \
  ros-humble-dwb-plugins
```

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/tathagata48/nav2.git ~/nav2_ws/src/nav2

# 2. Move packages to workspace src (or use as-is if already a workspace)
cd ~/nav2_ws

# 3. Install additional dependencies via rosdep
rosdep install --from-paths src --ignore-src -r -y

# 4. Build
colcon build --symlink-install

# 5. Source the workspace
source install/setup.bash
```

---

## Usage

Open multiple terminal tabs and source your workspace in each:

```bash
source ~/nav2_ws/install/setup.bash
```

### 1. Launch Gazebo Simulation

```bash
# Launch with the navigation world (enclosed room with obstacles)
ros2 launch my_robot_gazebo gazebo.launch.py

# Or launch with the empty world
ros2 launch my_robot_gazebo gazebo.launch.py world:=empty_world

# Headless (no Gazebo GUI)
ros2 launch my_robot_gazebo gazebo.launch.py gui:=false
```

### 2. SLAM Mapping

In a second terminal, start SLAM to build a map:

```bash
ros2 launch my_robot_navigation slam.launch.py
```

Drive the robot around to map the environment. Use `teleop_twist_keyboard`:

```bash
sudo apt install ros-humble-teleop-twist-keyboard
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

### 3. Save Map

Once the map looks complete:

```bash
ros2 run nav2_map_server map_saver_cli -f ~/my_map
```

This saves `~/my_map.yaml` and `~/my_map.pgm`.

### 4. Autonomous Navigation

Launch Nav2 with the saved map:

```bash
# First, make sure Gazebo is still running (step 1)
ros2 launch my_robot_navigation navigation.launch.py map:=/home/$USER/my_map.yaml
```

In RViz2:
1. Click **"2D Pose Estimate"** and click on the map to set the robot's initial position
2. Click **"Nav2 Goal"** (or **"2D Nav Goal"**) and click somewhere on the map
3. The robot will plan a path and navigate autonomously

---

## Package Overview

| Package | Description |
|---------|-------------|
| `my_robot_description` | URDF/xacro robot model — differential drive base, lidar, IMU |
| `my_robot_gazebo` | Gazebo worlds and robot spawning launch files |
| `my_robot_navigation` | Nav2 configuration, SLAM, localization and navigation launch files |

---

## Robot Specifications

| Parameter | Value |
|-----------|-------|
| Base shape | Cylinder, ⌀0.30m × 0.15m tall |
| Drive type | Differential drive |
| Wheel diameter | 0.10m |
| Wheel separation | 0.28m |
| Max linear velocity | 0.26 m/s |
| Max angular velocity | 1.0 rad/s |
| Lidar type | 2D, 360°, 8m range |
| Lidar frequency | 10 Hz |
| IMU frequency | 100 Hz |

---

## Project Structure

```
Nav2/
├── README.md
├── LICENSE
└── src/
    ├── my_robot_description/
    │   ├── CMakeLists.txt
    │   ├── package.xml
    │   ├── launch/
    │   │   └── display.launch.py          # RViz URDF viewer
    │   ├── rviz/
    │   │   └── urdf_view.rviz
    │   └── urdf/
    │       ├── my_robot.urdf.xacro        # Robot model (links, joints)
    │       └── my_robot_gazebo.xacro      # Gazebo plugins
    ├── my_robot_gazebo/
    │   ├── CMakeLists.txt
    │   ├── package.xml
    │   ├── launch/
    │   │   └── gazebo.launch.py           # Gazebo + robot spawn
    │   └── worlds/
    │       ├── empty_world.world          # Flat empty world
    │       └── navigation_world.world     # Room with obstacles
    └── my_robot_navigation/
        ├── CMakeLists.txt
        ├── package.xml
        ├── config/
        │   ├── nav2_params.yaml                    # Full Nav2 configuration
        │   └── mapper_params_online_async.yaml     # SLAM Toolbox config
        ├── launch/
        │   ├── navigation.launch.py       # Nav2 full stack
        │   ├── slam.launch.py             # SLAM mapping mode
        │   └── localization.launch.py     # AMCL localization only
        ├── maps/                          # Store saved maps here
        └── rviz/
            └── nav2_default_view.rviz     # RViz config with Nav2 panel
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.
