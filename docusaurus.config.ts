import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Master ROS 2, Gazebo, NVIDIA Isaac, and VLA Models',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  url: 'https://tasmeerjamali.github.io',
  baseUrl: '/physical-ai-textbook/',

  organizationName: 'TasmeerJamali',
  projectName: 'physical-ai-textbook',
  trailingSlash: false,

  onBrokenLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/TasmeerJamali/physical-ai-textbook/tree/main/',
        },
        blog: false, // Disable blog for textbook
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/physical-ai-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI Textbook',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'textbookSidebar',
          position: 'left',
          label: 'Textbook',
        },
        {
          href: 'https://github.com/TasmeerJamali/physical-ai-textbook',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Modules',
          items: [
            { label: 'ROS 2', to: '/docs/module-1-ros2/intro' },
            { label: 'Gazebo & Unity', to: '/docs/module-2-gazebo/intro' },
            { label: 'NVIDIA Isaac', to: '/docs/module-3-isaac/intro' },
            { label: 'VLA Models', to: '/docs/module-4-vla/intro' },
          ],
        },
        {
          title: 'Resources',
          items: [
            { label: 'ROS 2 Docs', href: 'https://docs.ros.org/en/humble/' },
            { label: 'Gazebo Docs', href: 'https://gazebosim.org/docs' },
            { label: 'NVIDIA Isaac', href: 'https://developer.nvidia.com/isaac-sim' },
          ],
        },
        {
          title: 'Community',
          items: [
            { label: 'Panaversity', href: 'https://panaversity.org' },
            { label: 'GitHub', href: 'https://github.com/TasmeerJamali' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook. Built for Panaversity Hackathon.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'bash', 'yaml', 'cpp'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
