---
sidebar_position: 2
---

import ContentActions from '@site/src/components/ContentActions';

# Chapter 3.1: Isaac Sim Setup

<ContentActions chapterId="module-3-isaac-setup" />

NVIDIA Isaac Sim is a powerful robotics simulation platform built on Omniverse. Let's get it installed and running.

## 🛠️ System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Ubuntu 22.04 | Ubuntu 22.04 |
| **GPU** | RTX 2070 | RTX 4070+ |
| **VRAM** | 8 GB | 12+ GB |
| **RAM** | 32 GB | 64 GB |
| **Storage** | 50 GB SSD | 100 GB NVMe |

## 📥 Installation Steps

### 1. Install NVIDIA Drivers

```bash
# Check current driver
nvidia-smi

# Install latest driver (if needed)
sudo apt install nvidia-driver-535
```

### 2. Install Omniverse Launcher

1. Download from [NVIDIA Omniverse](https://www.nvidia.com/en-us/omniverse/)
2. Run the AppImage:
   ```bash
   chmod +x omniverse-launcher-linux.AppImage
   ./omniverse-launcher-linux.AppImage
   ```

### 3. Install Isaac Sim

1. Open Omniverse Launcher
2. Go to **Exchange** tab
3. Search for "Isaac Sim"
4. Click **Install**

## 🚀 First Launch

```bash
# Launch Isaac Sim from terminal
~/.local/share/ov/pkg/isaac_sim-*/isaac-sim.sh
```

Or use the Omniverse Launcher GUI.

## 🖥️ Interface Overview

```
┌─────────────────────────────────────────────────────────┐
│  Isaac Sim                                              │
├─────────────────────────────────────────────────────────┤
│ ┌─────────┐ ┌─────────────────────────────────────────┐ │
│ │ Stage   │ │                                         │ │
│ │         │ │         Viewport                        │ │
│ │ /World  │ │                                         │ │
│ │  /Robot │ │    [Photorealistic rendering]          │ │
│ │  /Env   │ │                                         │ │
│ └─────────┘ └─────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Property Panel | Timeline | Console                 │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## 🤖 Loading a Sample Robot

1. Go to **Isaac Examples** → **Robots**
2. Select **Carter** or **Jetbot**
3. Click **Load**
4. Press **Play** to start simulation

## 🔗 ROS 2 Bridge

Enable ROS 2 communication:

```python
# In Isaac Sim Python console
from omni.isaac.ros2_bridge import ROS2Bridge
bridge = ROS2Bridge()
bridge.create_clock_publisher()
```

## ✅ Key Takeaways

- Isaac Sim requires a powerful NVIDIA GPU
- Installation is via Omniverse Launcher
- Built-in ROS 2 bridge for integration
- Photorealistic rendering for synthetic data

## ➡️ Next Chapter

Continue to [Chapter 3.2: Isaac ROS Integration](./ros-integration) to connect with ROS 2!

