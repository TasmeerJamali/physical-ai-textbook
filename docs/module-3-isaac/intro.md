---
sidebar_position: 1
---

import ContentActions from '@site/src/components/ContentActions';

# Introduction to NVIDIA Isaac

<ContentActions chapterId="module-3-isaac-intro" />

**NVIDIA Isaac** is a comprehensive platform for developing and deploying AI-powered robots. It combines simulation, perception, and navigation into a unified ecosystem optimized for NVIDIA GPUs.

## 🎯 Learning Objectives

By the end of this module, you will:

- Understand the Isaac platform components
- Set up Isaac Sim for robot simulation
- Use Isaac ROS for GPU-accelerated perception
- Implement VSLAM for robot localization
- Deploy Nav2 for autonomous navigation

## 🧠 The Isaac Ecosystem

```
┌─────────────────────────────────────────────────────────┐
│                    NVIDIA Isaac Platform                 │
├─────────────────┬─────────────────┬─────────────────────┤
│   Isaac Sim     │   Isaac ROS     │   Isaac Perceptor   │
│   (Simulation)  │   (Perception)  │   (3D Understanding)│
├─────────────────┴─────────────────┴─────────────────────┤
│                    NVIDIA Jetson / RTX                   │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Key Components

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| **Isaac Sim** | Photorealistic simulation | Omniverse, synthetic data |
| **Isaac ROS** | GPU-accelerated ROS 2 | CUDA-optimized nodes |
| **cuVSLAM** | Visual SLAM | Real-time localization |
| **Nav2** | Navigation stack | Path planning, obstacle avoidance |

## 📚 Chapter Overview

### Chapter 3.1: Isaac Sim Setup
Install and configure Isaac Sim on your system.

### Chapter 3.2: Isaac ROS Integration
Connect Isaac Sim to ROS 2 with GPU acceleration.

### Chapter 3.3: Visual SLAM with cuVSLAM
Implement real-time robot localization.

### Chapter 3.4: Autonomous Navigation
Deploy Nav2 for path planning and obstacle avoidance.

## 🛠️ Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **GPU** | RTX 2070 | RTX 4070+ |
| **RAM** | 32 GB | 64 GB |
| **Storage** | 50 GB SSD | 100 GB NVMe |
| **OS** | Ubuntu 22.04 | Ubuntu 22.04 |

## 🚀 Ready to Start?

Begin with [Chapter 3.1: Isaac Sim Setup](./setup) to install the platform!

