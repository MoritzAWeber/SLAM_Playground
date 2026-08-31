#!/usr/bin/env python3

import math
from typing import Optional

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class ScanAnalyzerNode(Node):
    def __init__(self) -> None:
        super().__init__("scan_analyzer")

        self.subscription = self.create_subscription(
            LaserScan,
            "/scan",
            self.scan_callback,
            10,
        )

        self.get_logger().info(
            "Warte auf LaserScan-Nachrichten auf /scan."
        )

    def scan_callback(self, scan: LaserScan) -> None:
        valid_ranges = [
            distance
            for distance in scan.ranges
            if math.isfinite(distance)
            and scan.range_min <= distance <= scan.range_max
        ]

        if not valid_ranges:
            self.get_logger().warning(
                "Scan enthält keine gültigen Messungen."
            )
            return

        minimum_distance = min(valid_ranges)
        average_distance = sum(valid_ranges) / len(valid_ranges)

        closest_index = self.find_closest_index(scan)

        if closest_index is None:
            return

        closest_angle = (
            scan.angle_min
            + closest_index * scan.angle_increment
        )

        closest_angle_degrees = math.degrees(closest_angle)

        self.get_logger().info(
            f"Messungen: {len(scan.ranges)} | "
            f"Gültig: {len(valid_ranges)} | "
            f"Nächster Punkt: {minimum_distance:.2f} m | "
            f"Winkel: {closest_angle_degrees:.1f}° | "
            f"Mittelwert: {average_distance:.2f} m"
        )

    @staticmethod
    def find_closest_index(scan: LaserScan) -> Optional[int]:
        best_index: Optional[int] = None
        best_distance = math.inf

        for index, distance in enumerate(scan.ranges):
            if not math.isfinite(distance):
                continue

            if not scan.range_min <= distance <= scan.range_max:
                continue

            if distance < best_distance:
                best_distance = distance
                best_index = index

        return best_index


def main(args=None) -> None:
    rclpy.init(args=args)

    node = ScanAnalyzerNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
