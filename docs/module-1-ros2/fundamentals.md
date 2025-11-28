---
sidebar_position: 2
---

import ContentActions from '@site/src/components/ContentActions';

# Chapter 1.1: ROS 2 Fundamentals

<ContentActions chapterId="module-1-ros2-fundamentals" />

Understanding the core concepts of ROS 2 is essential before building any robotic application. This chapter introduces the fundamental building blocks.

## 🧠 The ROS 2 Graph

ROS 2 organizes robot software as a **computational graph** - a network of processes (nodes) that communicate through well-defined channels.

```
┌─────────┐     /camera/image     ┌─────────────┐
│ Camera  │ ──────────────────────▶│   Vision    │
│  Node   │                        │  Processor  │
└─────────┘                        └─────────────┘
                                          │
                                          │ /detected_objects
                                          ▼
┌─────────┐     /cmd_vel           ┌─────────────┐
│ Motor   │ ◀──────────────────────│  Navigation │
│ Driver  │                        │   Planner   │
└─────────┘                        └─────────────┘
```

## 📦 Core Concepts

### 1. Nodes

A **node** is a single-purpose process that performs computation. Each node should do one thing well.

```python
import rclpy
from rclpy.node import Node

class MyRobotNode(Node):
    def __init__(self):
        super().__init__('my_robot_node')
        self.get_logger().info('Node started!')

def main():
    rclpy.init()
    node = MyRobotNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 2. Topics

**Topics** are named buses for streaming data. Nodes publish messages to topics, and other nodes subscribe to receive them.

- **Publisher**: Sends messages to a topic
- **Subscriber**: Receives messages from a topic
- **Message**: The data structure being sent

### 3. Services

**Services** implement request-response communication. A client sends a request and waits for a response.

```python
# Service definition (example)
# Request: goal_position (x, y, z)
# Response: success (bool), message (string)
```

### 4. Actions

**Actions** are for long-running tasks with feedback. They combine:
- **Goal**: What you want to achieve
- **Feedback**: Progress updates during execution
- **Result**: Final outcome when complete

## 🔧 ROS 2 CLI Tools

Essential commands for working with ROS 2:

```bash
# List all running nodes
ros2 node list

# List all topics
ros2 topic list

# Echo messages on a topic
ros2 topic echo /camera/image

# Get info about a topic
ros2 topic info /cmd_vel

# Call a service
ros2 service call /reset_robot std_srvs/srv/Empty
```

## 📝 Exercise: Explore ROS 2

1. Open a terminal and run:
   ```bash
   ros2 run demo_nodes_cpp talker
   ```

2. In another terminal:
   ```bash
   ros2 run demo_nodes_cpp listener
   ```

3. Use `ros2 topic list` to see the topic being used.

## ✅ Key Takeaways

- ROS 2 uses a **graph-based** architecture
- **Nodes** are single-purpose processes
- **Topics** enable publish-subscribe communication
- **Services** provide request-response patterns
- **Actions** handle long-running tasks with feedback

## ➡️ Next Chapter

Continue to [Chapter 1.2: Your First ROS 2 Node](./first-node) to write your own node!

