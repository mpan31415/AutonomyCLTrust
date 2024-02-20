import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    use_rviz_parameter_name = 'use_rviz'

    use_rviz = LaunchConfiguration(use_rviz_parameter_name)

    rviz_file = os.path.join(get_package_share_directory('franka_description'), 'rviz',
                             'my_config.rviz')

    return LaunchDescription([

        DeclareLaunchArgument(
            use_rviz_parameter_name,
            default_value='true',          # this was "false" by default
            description='Visualize the robot in Rviz'),

        # launch Rviz2 with my custom config
        Node(package='rviz2',
             executable='rviz2',
             name='rviz2',
             arguments=['--display-config', rviz_file],
             condition=IfCondition(use_rviz)
             ),

        # publish {camera base frame, depth camera frame}
        Node(
            package='ros_package',
            executable='const_br',
            name='const_br'
        ),

    ])
