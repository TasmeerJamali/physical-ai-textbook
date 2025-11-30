---
type: implement
mode: frontend
---

# Feature: Interactive 3D Digital Twin (Robot Viewer)

## Context
To elevate the textbook from static content to an interactive "Physical AI" lab, we are adding a "Digital Twin" viewer. This aligns with Module 2 (Gazebo/Simulation) and Module 1 (Kinematics).

## Requirements
1.  **3D Rendering**: Use `react-three-fiber` (Three.js) to render a 3D scene in the browser.
2.  **Robot Model**: Create a simplified "Robot Arm" using geometric primitives (Box, Cylinder) representing links and joints.
    *   Base
    *   Shoulder (Joint 1)
    *   Elbow (Joint 2)
    *   Wrist (Joint 3)
3.  **Interactive Controls**: Provide sliders to control the angle of each joint in real-time.
4.  **Educational Value**: Demonstrate "Forward Kinematics" — how changing joint angles affects the robot's pose.

## Technical Implementation
- **Component**: `src/components/RobotViewer/index.tsx`
- **Libraries**: `three`, `@react-three/fiber`, `@react-three/drei`
- **Integration**: Embed in a MDX file in the `docs` section.

## Goal
Provide a "Wow" factor that lets users interact with a robot simulation directly in the textbook, proving the "Digital Twin" concept.
