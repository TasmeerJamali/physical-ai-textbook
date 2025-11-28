---
sidebar_position: 1
---

import ContentActions from '@site/src/components/ContentActions';

# Introduction to ROS 2

<ContentActions chapterId="module-1-ros2-intro" />

**ROS 2** (Robot Operating System 2) is the foundation of modern robotics software development. Think of it as the **nervous system** of a robot - it handles communication between different parts of the robot, just like your nervous system coordinates your body.

## 🎯 Learning Objectives

By the end of this module, you will:

- Understand the ROS 2 architecture and core concepts
- Create and run ROS 2 nodes
- Implement publisher-subscriber communication
- Use services and actions for robot control
- Define robot models with URDF

## 🤔 Why ROS 2?

| Feature | Benefit |
|---------|---------|
| **Modular Design** | Build complex robots from simple, reusable components |
| **Real-time Support** | Critical for safety and precision in robotics |
| **Cross-platform** | Works on Linux, Windows, and macOS |
| **Industry Standard** | Used by NASA, Amazon, BMW, and more |

## 📚 Chapter Overview

### Chapter 1.1: ROS 2 Fundamentals
Learn the core concepts: nodes, topics, messages, and the ROS 2 graph.

### Chapter 1.2: Your First ROS 2 Node
Write and run your first Python node that publishes messages.

### Chapter 1.3: Publishers and Subscribers
Build a complete pub-sub system for robot sensor data.

### Chapter 1.4: Services and Actions
Implement request-response patterns and long-running tasks.

### Chapter 1.5: Robot Modeling with URDF
Define your robot's physical structure for simulation.

## 🛠️ Setup Requirements

Before starting, ensure you have:

```bash
# Ubuntu 22.04 with ROS 2 Humble
sudo apt install ros-humble-desktop

# Source ROS 2
source /opt/ros/humble/setup.bash
```

## 🚀 Ready to Start?

Let's begin with [Chapter 1.1: ROS 2 Fundamentals](./fundamentals) to understand the building blocks of ROS 2!

