#!/usr/bin/env python3

import math
import random

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class FakeLaserNode(Node):
    def __init__(self) -> None:
        super().__init__("fake_laser")

        self.publisher = self.create_publisher(
            LaserScan,
            "/scan",
            10,
        )

        self.timer = self.create_timer(0.2, self.publish_scan)

        self.get_logger().info(
            "Künstlicher LiDAR veröffentlicht auf /scan."
        )

    def publish_scan(self) -> None:
        scan = LaserScan()

        # Zeitpunkt und Koordinatenframe des Sensors
        scan.header.stamp = self.get_clock().now().to_msg()
        scan.header.frame_id = "laser_frame"

        # 360 Messungen von -180 bis +180 Grad
        number_of_measurements = 360

        scan.angle_min = -math.pi
        scan.angle_max = math.pi
        scan.angle_increment = (
            scan.angle_max - scan.angle_min
        ) / number_of_measurements

        scan.time_increment = 0.0
        scan.scan_time = 0.2

        scan.range_min = 0.10
        scan.range_max = 10.0

        # Standardmäßig befindet sich überall eine Wand in 5 m Entfernung.
        ranges = [5.0] * number_of_measurements

        # Simuliertes Hindernis direkt vor dem Roboter.
        # Die Indizes um 180 entsprechen ungefähr 0 Grad.
        for index in range(165, 196):
            noise = random.uniform(-0.03, 0.03)
            ranges[index] = 1.5 + noise

        # Zweites Hindernis links vom Roboter.
        for index in range(255, 276):
            noise = random.uniform(-0.03, 0.03)
            ranges[index] = 2.5 + noise

        scan.ranges = ranges

        # Intensitätswerte verwenden wir zunächst nicht.
        scan.intensities = []

        self.publisher.publish(scan)


def main(args=None) -> None:
    rclpy.init(args=args)

    node = FakeLaserNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
