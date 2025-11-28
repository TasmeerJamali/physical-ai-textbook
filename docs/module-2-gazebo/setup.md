---
sidebar_position: 2
---

import ContentActions from '@site/src/components/ContentActions';

# Chapter 2.1: Gazebo Setup and Basics

<ContentActions chapterId="module-2-gazebo-setup" />

Let's install Gazebo and explore its interface. Gazebo is the most popular open-source robotics simulator.

## 🛠️ Installation

### Ubuntu 22.04 with ROS 2 Humble

```bash
# Install Gazebo Harmonic with ROS 2 integration
sudo apt update
sudo apt install ros-humble-ros-gz

# Verify installation
gz sim --version
```

### Verify ROS 2 Bridge

```bash
# Check if the bridge is installed
ros2 pkg list | grep ros_gz
```

## 🖥️ Launching Gazebo

Start Gazebo with a sample world:

```bash
# Launch empty world
gz sim empty.sdf

# Launch with a robot
gz sim shapes.sdf
```

## 🎮 Interface Overview

```
┌─────────────────────────────────────────────────────────┐
│  File  Edit  View  Help                    [Gazebo]     │
├─────────────────────────────────────────────────────────┤
│ ┌─────────┐ ┌─────────────────────────────────────────┐ │
│ │ World   │ │                                         │ │
│ │ Tree    │ │         3D Viewport                     │ │
│ │         │ │                                         │ │
│ │ - World │ │    [Your robot and world here]         │ │
│ │   - Sun │ │                                         │ │
│ │   - Gnd │ │                                         │ │
│ └─────────┘ └─────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Component Inspector                                 │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Key Controls

| Action | Control |
|--------|---------|
| **Rotate View** | Right-click + drag |
| **Pan View** | Middle-click + drag |
| **Zoom** | Scroll wheel |
| **Select Object** | Left-click |
| **Move Object** | T key, then drag |

## 📝 Your First World

Create `my_world.sdf`:

```xml
<?xml version="1.0" ?>
<sdf version="1.8">
  <world name="my_world">
    <!-- Sun light -->
    <light type="directional" name="sun">
      <pose>0 0 10 0 0 0</pose>
    </light>
    
    <!-- Ground plane -->
    <model name="ground">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane><size>100 100</size></plane>
          </geometry>
        </collision>
      </link>
    </model>
  </world>
</sdf>
```

Launch it:
```bash
gz sim my_world.sdf
```

## ✅ Key Takeaways

- Gazebo uses SDF (Simulation Description Format) for worlds
- The interface has a world tree, 3D viewport, and inspector
- ROS 2 integration is via the `ros_gz` bridge

## ➡️ Next Chapter

Continue to [Chapter 2.2: Building Robot Worlds](./worlds) to create custom environments!

