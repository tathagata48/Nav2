import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_nav  = get_package_share_directory('my_robot_navigation')
    pkg_nav2 = get_package_share_directory('nav2_bringup')

    nav2_params_file = os.path.join(pkg_nav, 'config', 'nav2_params.yaml')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    map_yaml     = LaunchConfiguration('map')
    params_file  = LaunchConfiguration('params_file', default=nav2_params_file)
    autostart    = LaunchConfiguration('autostart', default='true')

    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2, 'launch', 'localization_launch.py')
        ),
        launch_arguments={
            'map': map_yaml,
            'use_sim_time': use_sim_time,
            'params_file': params_file,
            'autostart': autostart,
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time',  default_value='true',           description='Use simulation clock'),
        DeclareLaunchArgument('map',           description='Full path to map yaml file to load'),
        DeclareLaunchArgument('params_file',   default_value=nav2_params_file, description='Nav2 params file'),
        DeclareLaunchArgument('autostart',     default_value='true',           description='Auto-start lifecycle nodes'),
        localization,
    ])
