import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  textbookSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: ROS 2',
      link: {
        type: 'generated-index',
        description: 'Learn the Robot Operating System 2 - the foundation of modern robotics',
      },
      items: [
        'module-1-ros2/intro',
        'module-1-ros2/fundamentals',
        'module-1-ros2/first-node',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: Gazebo & Unity',
      link: {
        type: 'generated-index',
        description: 'Master physics simulation and digital twins for robotics',
      },
      items: [
        'module-2-gazebo/intro',
        'module-2-gazebo/setup',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: NVIDIA Isaac',
      link: {
        type: 'generated-index',
        description: 'Explore NVIDIA\'s AI-powered robotics platform',
      },
      items: [
        'module-3-isaac/intro',
        'module-3-isaac/setup',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: VLA Models',
      link: {
        type: 'generated-index',
        description: 'Vision-Language-Action models for intelligent robotics',
      },
      items: [
        'module-4-vla/intro',
        'module-4-vla/fundamentals',
      ],
    },
  ],
};

export default sidebars;
