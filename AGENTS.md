# AGENTS.md

## Scope

Codex is used in this repository only for documentation and dependency metadata maintenance.

Do not modify application source code, ROS node logic, launch behavior, algorithms, tests, or runtime behavior unless explicitly requested.

Allowed files include:
- `README.md`
- `pyproject.toml`
- `package.xml`
- documentation files
- comments/docstrings only when explicitly requested

## Documentation workflow

Before changing documentation:

1. Inspect the repository structure.
2. Inspect the current ROS nodes and executable entry points.
3. Inspect launch files.
4. Inspect imports and dependencies.
5. Compare the repository state with the existing documentation.

Update documentation only when the repository supports the change.

Do not invent features, commands, topics, frames, executables, dependencies, or future functionality.

## README

Keep `README.md` synchronized with the actual project.

Verify:
- project purpose
- current architecture
- package structure
- node names
- executable names
- launch commands
- ROS topics
- TF frames
- build instructions
- run instructions
- current limitations

Do not describe planned functionality as implemented.

Do not describe the mapper as full SLAM unless pose correction / localization is actually implemented.

## Dependencies

ROS dependencies belong in `package.xml`.

Examples:
- `rclpy`
- `nav_msgs`
- `sensor_msgs`
- `geometry_msgs`
- `tf2_ros`
- `visualization_msgs`

Regular Python dependencies belong in `pyproject.toml`.

Examples:
- `numpy`
- `scipy`

Only add dependencies that are actually required by the repository.

Do not infer dependencies from packages installed on the developer machine.

## Project context

This is a ROS 2 Jazzy SLAM learning project.

The intended TF hierarchy is:

`map -> odom -> base_link -> laser_frame`

The current mapper may still use odometry directly and should be described as occupancy mapping with an odometry/known pose until pose correction is implemented.

## Safety for repository changes

Do not:
- modify `.py` application files
- rewrite algorithms
- change ROS behavior
- rename nodes or executables
- alter launch behavior
- perform broad refactors

If documentation appears inconsistent because source code may be wrong, report the inconsistency instead of changing the source code.

## Validation

Before finishing:

1. Review `git diff`.
2. Confirm that only documentation or dependency metadata files were changed.
3. Verify documented commands and names against the repository.
4. Summarize what was updated.
5. Mention anything that could not be verified.
