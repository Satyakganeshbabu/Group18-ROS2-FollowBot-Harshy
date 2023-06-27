
"""Launch Gazebo with a world that has harshy, as well as the follow node."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_harshy_gazebo = get_package_share_directory('harshy_gazebo')

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py'),
        )
    )

    # Follow node
    follow = Node(
        package='harshy_follow',
        executable='harshy_follow',
        output='screen',
        remappings=[
            ('cmd_vel', '/harshy/cmd_vel'),
            ('laser_scan', '/harshy/laser_scan')
        ]
    )

    # RViz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(pkg_harshy_gazebo, 'rviz', 'harshy_gazebo.rviz')],
        condition=IfCondition(LaunchConfiguration('rviz'))
    )

    return LaunchDescription([
        DeclareLaunchArgument(
          'world',
          default_value=[os.path.join(pkg_harshy_gazebo, 'worlds', 'harshy_empty.world'), ''],
          description='SDF world file'),
        DeclareLaunchArgument('rviz', default_value='true',
                              description='Open RViz.'),
        gazebo,
        follow,
        rviz
    ])
