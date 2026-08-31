#!/usr/bin/env python3

import rclpy
from rclpy.node import Node


class SystemCheckNode(Node):
    def __init__(self) -> None:
        super().__init__("system_check")

        self.counter = 0
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info("SLAM-Projekt wurde gestartet.")

    def timer_callback(self) -> None:
        self.counter += 1
        self.get_logger().info(
            f"System läuft. Zyklus: {self.counter}"
        )


def main(args=None) -> None:
    rclpy.init(args=args)

    node = SystemCheckNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
