import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_nav    = get_package_share_directory('my_robot_navigation')
    pkg_nav2   = get_package_share_directory('nav2_bringup')

    nav2_params_file = os.path.join(pkg_nav, 'config', 'nav2_params.yaml')
    rviz_config_file = os.path.join(pkg_nav, 'rviz', 'nav2_default_view.rviz')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    map_yaml     = LaunchConfiguration('map', default='')
    params_file  = LaunchConfiguration('params_file', default=nav2_params_file)
    autostart    = LaunchConfiguration('autostart', default='true')
    use_rviz     = LaunchConfiguration('use_rviz', default='true')

    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_yaml,
            'use_sim_time': use_sim_time,
            'params_file': params_file,
            'autostart': autostart,
        }.items(),
    )

    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': use_sim_time}],
        condition=__import__('launch.conditions', fromlist=['IfCondition']).IfCondition(use_rviz),
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time',  default_value='true',           description='Use simulation clock'),
        DeclareLaunchArgument('map',           default_value='',               description='Full path to map yaml file'),
        DeclareLaunchArgument('params_file',   default_value=nav2_params_file, description='Nav2 params file'),
        DeclareLaunchArgument('autostart',     default_value='true',           description='Auto-start Nav2 lifecycle nodes'),
        DeclareLaunchArgument('use_rviz',      default_value='true',           description='Launch RViz2'),
        nav2_bringup,
        rviz2,
    ])
