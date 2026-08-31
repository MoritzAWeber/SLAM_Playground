#!/usr/bin/env python3

import math
from typing import Optional

import rclpy
from geometry_msgs.msg import TransformStamped
from nav_msgs.msg import OccupancyGrid
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster


class SimpleMapperNode(Node):
    def __init__(self) -> None:
        super().__init__("simple_mapper")

        self.resolution = 0.05
        self.width = 200
        self.height = 200

        self.origin_x = -(self.width * self.resolution) / 2.0
        self.origin_y = -(self.height * self.resolution) / 2.0

        self.grid = [-1] * (self.width * self.height)

        self.subscription = self.create_subscription(
            LaserScan,
            "/scan",
            self.scan_callback,
            10,
        )

        self.map_publisher = self.create_publisher(
            OccupancyGrid,
            "/map",
            10,
        )

        self.tf_broadcaster = StaticTransformBroadcaster(self)
        self.publish_static_transform()

        self.get_logger().info(
            "Simple Mapper wartet auf LaserScan-Daten."
        )

    def publish_static_transform(self) -> None:
        transform = TransformStamped()

        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = "map"
        transform.child_frame_id = "laser_frame"

        transform.transform.translation.x = 0.0
        transform.transform.translation.y = 0.0
        transform.transform.translation.z = 0.0

        transform.transform.rotation.x = 0.0
        transform.transform.rotation.y = 0.0
        transform.transform.rotation.z = 0.0
        transform.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(transform)

    def scan_callback(self, scan: LaserScan) -> None:

        robot_cell = self.world_to_grid(0.0, 0.0)

        if robot_cell is None:
            self.get_logger().error(
                "Roboter liegt außerhalb der Karte."
            )
            return

        robot_grid_x, robot_grid_y = robot_cell
        valid_points = 0

        for index, distance in enumerate(scan.ranges):
            if not math.isfinite(distance):
                continue

            if distance < scan.range_min or distance > scan.range_max:
                continue

            angle = scan.angle_min + index * scan.angle_increment

            point_x = distance * math.cos(angle)
            point_y = distance * math.sin(angle)

            obstacle_cell = self.world_to_grid(
                point_x,
                point_y,
            )

            if obstacle_cell is None:
                continue

            obstacle_grid_x, obstacle_grid_y = obstacle_cell

            ray_cells = self.bresenham(
                robot_grid_x,
                robot_grid_y,
                obstacle_grid_x,
                obstacle_grid_y,
            )

            for free_x, free_y in ray_cells[:-1]:
                self.set_grid_value(
                    self.grid,
                    free_x,
                    free_y,
                    0,
                )

            self.set_grid_value(
                self.grid,
                obstacle_grid_x,
                obstacle_grid_y,
                100,
            )

            valid_points += 1

        message = self.create_map_message(
            grid=self.grid,
            stamp=scan.header.stamp,
        )

        self.map_publisher.publish(message)

        self.get_logger().info(
            f"Karte veröffentlicht: "
            f"{valid_points} Scanpunkte verarbeitet.",
            throttle_duration_sec=2.0,
        )

    def world_to_grid(
        self,
        world_x: float,
        world_y: float,
    ) -> Optional[tuple[int, int]]:
        grid_x = int(
            math.floor(
                (world_x - self.origin_x) / self.resolution
            )
        )

        grid_y = int(
            math.floor(
                (world_y - self.origin_y) / self.resolution
            )
        )

        if not self.is_inside_grid(grid_x, grid_y):
            return None

        return grid_x, grid_y

    def set_grid_value(
        self,
        grid: list[int],
        grid_x: int,
        grid_y: int,
        value: int,
    ) -> None:
        if not self.is_inside_grid(grid_x, grid_y):
            return

        flat_index = grid_y * self.width + grid_x

        if self.grid[flat_index] == 100 and value == 0:
            return

        self.grid[flat_index] = value

    def is_inside_grid(
        self,
        grid_x: int,
        grid_y: int,
    ) -> bool:
        return (
            0 <= grid_x < self.width
            and 0 <= grid_y < self.height
        )

    @staticmethod
    def bresenham(
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
    ) -> list[tuple[int, int]]:
        cells: list[tuple[int, int]] = []

        current_x = start_x
        current_y = start_y

        delta_x = abs(end_x - start_x)
        delta_y = abs(end_y - start_y)

        step_x = 1 if start_x < end_x else -1
        step_y = 1 if start_y < end_y else -1

        error = delta_x - delta_y

        while True:
            cells.append((current_x, current_y))

            if current_x == end_x and current_y == end_y:
                break

            doubled_error = 2 * error

            if doubled_error > -delta_y:
                error -= delta_y
                current_x += step_x

            if doubled_error < delta_x:
                error += delta_x
                current_y += step_y

        return cells

    def create_map_message(
        self,
        grid: list[int],
        stamp,
    ) -> OccupancyGrid:
        message = OccupancyGrid()

        message.header.stamp = stamp
        message.header.frame_id = "map"

        message.info.resolution = self.resolution
        message.info.width = self.width
        message.info.height = self.height

        message.info.origin.position.x = self.origin_x
        message.info.origin.position.y = self.origin_y
        message.info.origin.position.z = 0.0

        message.info.origin.orientation.x = 0.0
        message.info.origin.orientation.y = 0.0
        message.info.origin.orientation.z = 0.0
        message.info.origin.orientation.w = 1.0

        message.data = self.grid

        return message


def main(args=None) -> None:
    rclpy.init(args=args)

    node = SimpleMapperNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
