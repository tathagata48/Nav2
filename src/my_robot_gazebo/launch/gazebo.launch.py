import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    ExecuteProcess,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_robot_desc = get_package_share_directory('my_robot_description')
    pkg_robot_gazebo = get_package_share_directory('my_robot_gazebo')

    urdf_file = os.path.join(pkg_robot_desc, 'urdf', 'my_robot.urdf.xacro')

    # Launch arguments
    use_sim_time   = LaunchConfiguration('use_sim_time',   default='true')
    world          = LaunchConfiguration('world',          default='navigation_world')
    x_pose         = LaunchConfiguration('x_pose',         default='0.0')
    y_pose         = LaunchConfiguration('y_pose',         default='0.0')
    z_pose         = LaunchConfiguration('z_pose',         default='0.05')
    gui            = LaunchConfiguration('gui',            default='true')
    headless       = LaunchConfiguration('headless',       default='false')

    world_file = PythonExpression([
        '"', pkg_robot_gazebo, '/worlds/', world, '.world"'
    ])

    robot_description = Command(['xacro ', urdf_file])

    # Gazebo server
    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world_file}.items(),
    )

    # Gazebo client (GUI)
    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        ),
        condition=IfCondition(gui),
    )

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': robot_description,
        }],
    )

    # Spawn robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'my_robot',
            '-x', x_pose,
            '-y', y_pose,
            '-z', z_pose,
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time',   default_value='true',              description='Use simulation clock'),
        DeclareLaunchArgument('world',          default_value='navigation_world',  description='World file name (without .world)'),
        DeclareLaunchArgument('x_pose',         default_value='0.0',               description='Initial X position of robot'),
        DeclareLaunchArgument('y_pose',         default_value='0.0',               description='Initial Y position of robot'),
        DeclareLaunchArgument('z_pose',         default_value='0.05',              description='Initial Z position of robot'),
        DeclareLaunchArgument('gui',            default_value='true',              description='Launch Gazebo GUI'),
        DeclareLaunchArgument('headless',       default_value='false',             description='Run headless (no GUI)'),
        gzserver,
        gzclient,
        robot_state_publisher,
        spawn_entity,
    ])
