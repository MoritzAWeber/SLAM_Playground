# AGENTS.md

## Purpose

This repository contains a ROS 2 Jazzy project for implementing and evaluating 2D SLAM components.

Codex is used in this repository only for documentation and dependency metadata maintenance.

Codex must not modify runtime behavior, application logic, algorithms, ROS node implementations, or launch behavior unless explicitly instructed.

## Allowed files

Codex may modify:

- `README.md`
- `TODO.md`
- `pyproject.toml`
- `package.xml`
- other documentation files
- comments or docstrings only when explicitly requested

Application source files must not be modified as part of routine documentation maintenance.

## Repository inspection

Before updating documentation or metadata, inspect the repository and derive facts from the actual implementation.

Relevant sources include:

- ROS package manifests
- Python package configuration
- launch files
- executable entry points
- node implementations
- imports
- topic names
- TF frame names
- existing documentation

Do not assume filenames, executable names, topics, frames, dependencies, or implemented features without verifying them.

## Documentation requirements

Keep the project documentation synchronized with the repository.

Documentation should accurately describe:

- project purpose
- repository structure
- ROS packages
- nodes and their responsibilities
- executable names
- launch files
- ROS topics
- message types
- TF frames and frame relationships
- configuration and dependencies
- build instructions
- run instructions
- implemented functionality
- known limitations

Do not document planned functionality as implemented functionality.

When implementation details are unclear or cannot be verified from the repository, state that explicitly instead of guessing.

## Technical terminology

Use ROS terminology consistently.

Distinguish between:

- mapping
- localization
- odometry
- scan matching
- SLAM
- loop closure
- pose graph optimization

Do not describe a mapping implementation as full SLAM unless the repository contains pose estimation or correction based on sensor observations.

Use frame names exactly as implemented.

Typical frame responsibilities may include:

- `map`: global corrected reference frame
- `odom`: locally continuous odometry reference frame
- `base_link`: robot-fixed base frame
- `laser_frame`: sensor-fixed frame

Only document frames that are actually present in the repository.

## Dependency management

ROS dependencies must be declared in `package.xml`.

Examples include:

- `rclpy`
- `nav_msgs`
- `sensor_msgs`
- `geometry_msgs`
- `tf2_ros`
- `visualization_msgs`

ROS packages must not be added as ordinary PyPI dependencies.

Non-ROS Python dependencies should be declared in `pyproject.toml`.

Examples include:

- `numpy`
- `scipy`

Only declare dependencies that are actually required by the project.

Do not derive project dependencies from packages installed globally on the development system.

## Python packaging

When maintaining `pyproject.toml`:

1. inspect imports used by the project
2. separate ROS dependencies from ordinary Python dependencies
3. preserve compatibility with the existing ROS packaging approach
4. avoid replacing or restructuring package configuration unless explicitly requested
5. do not add unused dependencies

## README maintenance

When updating `README.md`, verify that documented commands match the repository.

In particular, verify:

- workspace layout
- package names
- executable names
- launch filenames
- build commands
- source commands
- run commands
- topic names
- frame names
- dependency installation instructions

Prefer concise, reproducible commands over machine-specific assumptions.

Avoid documenting local absolute paths unless they are required.

## TODO maintenance

Maintain `TODO.md` as the source of project-level open work.

A TODO entry should represent a concrete, verifiable task.

Appropriate TODOs include:

- missing functionality
- incomplete documentation
- unresolved technical limitations
- known inconsistencies
- missing tests
- unimplemented interfaces
- dependency or packaging issues

Do not add speculative tasks without evidence from the repository.

Do not duplicate existing TODO items.

Do not resolve TODOs by modifying application source code unless explicitly instructed.

A TODO may be marked complete or removed only when the repository clearly shows that the task has been resolved.

## Source code protection

During documentation maintenance, do not:

- modify Python application logic
- change ROS node behavior
- change algorithms
- rename topics
- rename frames
- rename executables
- change launch behavior
- perform refactors
- alter tests
- change runtime configuration

If documentation reveals a likely source-code issue, document or report the inconsistency rather than changing the implementation.

## Validation

Before completing a documentation task:

1. inspect the relevant repository files
2. review all changes with `git diff`
3. confirm that only permitted files were modified
4. verify documented executable names
5. verify documented launch files
6. verify documented topics and frames
7. verify dependency declarations against actual usage
8. review `TODO.md` for duplicates and obsolete entries

Do not claim that a command, build, test, or runtime behavior was verified unless it was actually executed.

## Final report

At the end of a documentation task, provide a concise summary containing:

- files changed
- documentation or metadata updated
- inconsistencies found
- unresolved items
- checks that were performed