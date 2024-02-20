from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

from ros2_package.exp_params import *


def generate_launch_description():

    # my own launch arguments
    free_drive_parameter_name = 'free_drive'
    mapping_ratio_parameter_name = 'mapping_ratio'
    use_depth_parameter_name = 'use_depth'
    participant_parameter_name = 'part_id'
    alpha_parameter_name = 'alpha_id'
    trajectory_parameter_name = 'traj_id'

    free_drive = LaunchConfiguration(free_drive_parameter_name)
    mapping_ratio = LaunchConfiguration(mapping_ratio_parameter_name)
    use_depth = LaunchConfiguration(use_depth_parameter_name)
    participant = LaunchConfiguration(participant_parameter_name)
    alpha = LaunchConfiguration(alpha_parameter_name)
    trajectory = LaunchConfiguration(trajectory_parameter_name)


    return LaunchDescription([

        DeclareLaunchArgument(
            free_drive_parameter_name,
            default_value=my_free_drive,  
            description='Free drive parameter'),
        DeclareLaunchArgument(
            mapping_ratio_parameter_name,
            default_value=my_mapping_ratio,  
            description='Mapping ratio parameter'),
        DeclareLaunchArgument(
            use_depth_parameter_name,
            default_value=my_use_depth,  
            description='Use depth parameter'),
        DeclareLaunchArgument(
            participant_parameter_name,
            default_value=my_part_id,  
            description='Participant ID parameter'),
        DeclareLaunchArgument(
            alpha_parameter_name,
            default_value=my_alpha_id,
            description='Alpha ID parameter'),
        DeclareLaunchArgument(
            trajectory_parameter_name,
            default_value=my_traj_id,
            description='Trajectory ID parameter'),


        # real robot controller node [need position_talker to be running]
        Node(
            package='ros2_package',
            executable='real_controller',
            parameters=[
                {free_drive_parameter_name: free_drive},
                {mapping_ratio_parameter_name: mapping_ratio},
                {use_depth_parameter_name: use_depth},
                {participant_parameter_name: participant},
                {alpha_parameter_name: alpha},
                {trajectory_parameter_name: trajectory}
            ],
            output='screen',
            emulate_tty=True,
            name='real_controller'
        ),

    ])
