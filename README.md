# SLAM Playground

`slam_playground` is a ROS 2 Jazzy learning project that simulates a robot,
a 2D laser scanner, and a simple occupancy-grid mapper. The robot follows a
known circular trajectory inside a square room, the simulated scanner measures
the room walls, and the mapper places scan endpoints into a persistent grid
using the simulated odometry pose.

Despite the repository name, this is **not a complete SLAM system**. There is
no scan matching, localization, loop closure, pose correction, or
`map -> odom` transform. Mapping currently relies directly on known odometry.

## Current system

The main demo consists of three nodes started by
`moving_robot.launch.py`:

```text
robot_motion_node
  |-- /odom ----------------> laser_simulator
  |       |                         |-- /scan
  |       +-------------------------+-------> simple_mapper
  |-- odom -> base_link TF                 |-- /map
  +-- base_link -> laser_frame static TF

laser_simulator
  +-- /scan_rays
```

| Executable | ROS node name | Role |
| --- | --- | --- |
| `robot_motion` | `robot_motion_node` | Moves the robot around a circle of radius 1.5 m and publishes its known pose at 5 Hz. |
| `laser_simulator` | `laser_simulator` | Casts 360 rays against the walls of an 8 m x 8 m square room and publishes scans and visualization markers at 5 Hz. |
| `simple_mapper_new` | `simple_mapper` | Transforms scan endpoints with the odometry pose and accumulates them in an occupancy grid. |
| `system_check` | `system_check` | Standalone heartbeat node that logs once per second; it is not part of the demo launch. |

The executable name `simple_mapper_new` is retained in the package metadata,
although the node itself is named `simple_mapper`.

## ROS interfaces

| Topic | Type | Publisher | Subscriber | Description |
| --- | --- | --- | --- | --- |
| `/odom` | `nav_msgs/msg/Odometry` | `robot_motion_node` | `laser_simulator`, `simple_mapper` | Simulated robot pose in `odom`. |
| `/scan` | `sensor_msgs/msg/LaserScan` | `laser_simulator` | `simple_mapper` | 360-degree scan in `laser_frame`, with a 0.1-8.0 m range. |
| `/scan_rays` | `visualization_msgs/msg/Marker` | `laser_simulator` | None | A `LINE_LIST` marker containing every tenth simulated ray. |
| `/map` | `nav_msgs/msg/OccupancyGrid` | `simple_mapper` | None | 12 m x 12 m grid at 0.05 m/cell, expressed in `odom`. |

The implemented TF tree is:

```text
odom -> base_link -> laser_frame
```

`odom -> base_link` changes with the simulated motion.
`base_link -> laser_frame` is static and currently has zero translation and
rotation. No `map` frame is published; the occupancy grid uses `odom` as its
header frame.

## Requirements

- Ubuntu 24.04 with ROS 2 Jazzy
- `colcon` and `rosdep`
- Python 3.12, as provided by the standard ROS 2 Jazzy platform
- NumPy

The ROS package declares `rclpy`, `sensor_msgs`, `nav_msgs`, `geometry_msgs`,
and `tf2_ros`. The current code also imports `visualization_msgs`, and the
mapper imports NumPy, but those two runtime dependencies are not yet declared
in the repository metadata. They must already be available in the environment
for the complete demo to run.

## Build

Run the following commands from the repository root:

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src --rosdistro jazzy -y
colcon build --symlink-install --packages-select slam_playground
source install/setup.bash
```

The setup file installs the launch file with the package, so the demo can be
started after sourcing the workspace.

## Run

Start all three simulation and mapping nodes:

```bash
ros2 launch slam_playground moving_robot.launch.py
```

Alternatively, run them in separate terminals after sourcing ROS 2 and the
workspace in each terminal:

```bash
ros2 run slam_playground robot_motion
ros2 run slam_playground laser_simulator
ros2 run slam_playground simple_mapper_new
```

The laser simulator and mapper wait for the first odometry message before
producing useful output. Start `robot_motion` first when launching the nodes
manually.

The standalone heartbeat can be run with:

```bash
ros2 run slam_playground system_check
```

## Inspect the demo

Useful ROS 2 checks include:

```bash
ros2 node list
ros2 topic list
ros2 topic echo /odom --once
ros2 topic echo /scan --once
ros2 topic echo /map --once
ros2 run tf2_ros tf2_echo odom base_link
```

If RViz 2 is installed, use `odom` as the fixed frame and add displays for the
occupancy grid (`/map`), laser scan (`/scan`), marker (`/scan_rays`), and TF.
The repository does not currently include an RViz configuration.

## Tests

The package contains the standard ament Flake8, PEP 257, and copyright test
wrappers:

```bash
colcon test --packages-select slam_playground
colcon test-result --verbose
```

The copyright test is currently skipped by its test file.
The current test suite does not pass: the Flake8 test reports existing style
violations in the package sources, launch file, and `setup.py`.

## Current limitations

- Robot motion is scripted and odometry is exact; no motion model or odometry
  noise is simulated.
- The world contains only the four walls of a fixed square room.
- The laser model has no noise, missed returns, or dynamic obstacles.
- The mapper uses odometry directly and performs no pose estimation or
  correction.
- Only valid scan endpoints are marked occupied (`100`). Free space along each
  ray is not cleared, and untouched cells remain unknown (`-1`).
- The map is published in `odom`; the intended future SLAM hierarchy
  `map -> odom -> base_link -> laser_frame` is not implemented.
- `setup.py` still registers `fake_laser`, `scan_analyzer`, and `simple_mapper`
  console scripts whose referenced modules are absent. Use the moving-robot
  executables documented above.
- `start_slam.sh` only changes directory and sources environments. It uses a
  hard-coded workspace path and does not launch any nodes.

## Repository layout

```text
.
|-- README.md
|-- pyproject.toml
|-- start_slam.sh
+-- src/slam_playground/
    |-- launch/moving_robot.launch.py
    |-- package.xml
    |-- setup.cfg
    |-- setup.py
    |-- slam_playground/
    |   |-- system_check.py
    |   +-- moving_robot/
    |       |-- robot_motion_node.py
    |       |-- laser_simulator_node.py
    |       +-- simple_mapper_node.py
    +-- test/
```

## License

Apache License 2.0. See
[`src/slam_playground/LICENSE`](src/slam_playground/LICENSE).
