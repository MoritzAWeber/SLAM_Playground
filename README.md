# SLAM Playground

`slam_playground` is a ROS 2 Jazzy learning project for simulating a moving
robot, generating idealized 2D laser scans, and building an occupancy grid.

The current implementation is an odometry-based mapper, not a complete SLAM
system. It uses the robot pose from simulated odometry to place laser endpoints
in a grid. It does not estimate or correct the pose from sensor observations.

## What is built

The `moving_robot.launch.py` launch file starts three nodes:

| Executable | Node name | Responsibility |
| --- | --- | --- |
| `robot_motion` | `robot_motion_node` | Publishes exact odometry for a robot following a circle and broadcasts the robot TF frames. |
| `laser_simulator` | `laser_simulator` | Casts 360 idealized rays against the walls of a square room. |
| `simple_mapper` | `simple_mapper` | Uses odometry and scan endpoints to accumulate occupied cells in an occupancy grid. |

The simulated robot moves on a circle with a radius of 1.5 m. The laser scans
an 8 m by 8 m square room at 5 Hz with a range of 0.1 m to 8.0 m. The mapper
publishes a 12 m by 12 m grid at 0.05 m per cell.

### ROS interfaces

| Topic | Type | Publisher | Subscriber | Purpose |
| --- | --- | --- | --- | --- |
| `/odom` | `nav_msgs/msg/Odometry` | `robot_motion_node` | `laser_simulator`, `simple_mapper` | Exact simulated robot pose. |
| `/scan` | `sensor_msgs/msg/LaserScan` | `laser_simulator` | `simple_mapper` | Simulated 360-degree laser scan. |
| `/scan_rays` | `visualization_msgs/msg/Marker` | `laser_simulator` | — | Visualization of every tenth laser ray. |
| `/map` | `nav_msgs/msg/OccupancyGrid` | `simple_mapper` | — | Accumulated occupied scan endpoints. |

The implemented TF tree is:

```text
odom -> base_link -> laser_frame
```

`odom -> base_link` follows the simulated motion. `base_link -> laser_frame`
is static with zero translation and rotation. The occupancy grid is expressed
in `odom`; there is no `map` TF frame.

The mapper marks valid scan endpoints as occupied (`100`). Unobserved cells
remain unknown (`-1`). It does not mark free space along a ray.

## Build

Requirements:

- Ubuntu 24.04 and ROS 2 Jazzy
- `colcon` and `rosdep`
- Python 3.12
- NumPy

From the repository root:

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src --rosdistro jazzy -y
colcon build --symlink-install --packages-select slam_playground
source install/setup.bash
```

ROS dependencies are declared in `src/slam_playground/package.xml`. The NumPy
dependency is declared in `pyproject.toml`.

## Run

After sourcing ROS 2 and the built workspace:

```bash
ros2 launch slam_playground moving_robot.launch.py
```

To run the nodes separately, source the environment in each terminal and start
the odometry publisher first:

```bash
ros2 run slam_playground robot_motion
ros2 run slam_playground laser_simulator
ros2 run slam_playground simple_mapper
```

For RViz 2, use `odom` as the fixed frame and add `/map`, `/scan`,
`/scan_rays`, and TF displays. No RViz configuration is included.

Useful inspection commands:

```bash
ros2 node list
ros2 topic list
ros2 topic echo /odom --once
ros2 topic echo /scan --once
ros2 topic echo /map --once
ros2 run tf2_ros tf2_echo odom base_link
```

## Tests

The package includes the standard ament Flake8, PEP 257, and copyright test
wrappers:

```bash
colcon test --packages-select slam_playground
colcon test-result --verbose
```

The copyright test is explicitly skipped. No functional tests currently
exercise the simulation or mapper. Test results have not been verified as part
of this documentation update.

## What remains to do

The tracked project work is maintained in [TODO.md](TODO.md). The main gaps are
functional tests, a less idealized sensor and motion model, free-space mapping,
and the pose-estimation and correction components required for actual 2D SLAM.

## Repository layout

```text
.
|-- README.md
|-- TODO.md
|-- pyproject.toml
|-- start_slam.sh
+-- src/slam_playground/
    |-- package.xml
    |-- setup.py
    |-- launch/moving_robot.launch.py
    |-- slam_playground/moving_robot/
    |   |-- robot_motion_node.py
    |   |-- laser_simulator_node.py
    |   +-- simple_mapper_node.py
    +-- test/
```

`start_slam.sh` is a local convenience script with a hard-coded workspace
path. It only sources the ROS 2 and workspace environments; it does not build
the workspace or launch nodes.

## License

Apache License 2.0. See
[`src/slam_playground/LICENSE`](src/slam_playground/LICENSE).
