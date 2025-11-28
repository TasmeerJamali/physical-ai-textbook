---
sidebar_position: 3
---

import ContentActions from '@site/src/components/ContentActions';

# Chapter 1.2: Your First ROS 2 Node

<ContentActions chapterId="module-1-ros2-first-node" />

Now that you understand the fundamentals, let's write your first ROS 2 node! We'll create a simple publisher that sends messages.

## 🎯 What We'll Build

A Python node that:
1. Publishes "Hello, Robot!" messages
2. Runs at 1 Hz (once per second)
3. Uses the standard `String` message type

## 📁 Project Setup

First, create a ROS 2 workspace:

```bash
# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Create package
ros2 pkg create --build-type ament_python my_first_robot
```

## 💻 The Code

Create `my_first_robot/my_first_robot/hello_publisher.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class HelloPublisher(Node):
    """A simple node that publishes greeting messages."""
    
    def __init__(self):
        super().__init__('hello_publisher')
        
        # Create publisher
        self.publisher = self.create_publisher(
            String,           # Message type
            'greetings',      # Topic name
            10                # Queue size
        )
        
        # Create timer (1 Hz)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0
        
        self.get_logger().info('Hello Publisher started!')
    
    def timer_callback(self):
        """Called every second to publish a message."""
        msg = String()
        msg.data = f'Hello, Robot! Count: {self.count}'
        
        self.publisher.publish(msg)
        self.get_logger().info(f'Published: "{msg.data}"')
        
        self.count += 1

def main(args=None):
    rclpy.init(args=args)
    node = HelloPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 🔧 Understanding the Code

| Component | Purpose |
|-----------|---------|
| `Node` | Base class for all ROS 2 nodes |
| `create_publisher()` | Creates a publisher for a topic |
| `create_timer()` | Schedules periodic callbacks |
| `rclpy.spin()` | Keeps the node running |

## 🚀 Running Your Node

```bash
# Build the workspace
cd ~/ros2_ws
colcon build

# Source the workspace
source install/setup.bash

# Run the node
ros2 run my_first_robot hello_publisher
```

## 📝 Exercise

1. Modify the message to include your name
2. Change the publishing rate to 2 Hz
3. Add a subscriber in another terminal: `ros2 topic echo /greetings`

## ✅ Key Takeaways

- Nodes inherit from `rclpy.node.Node`
- Publishers send messages to topics
- Timers enable periodic execution
- Always call `rclpy.shutdown()` when done

## ➡️ Next Chapter

Continue to [Chapter 1.3: Publishers and Subscribers](./pub-sub) to build a complete communication system!

