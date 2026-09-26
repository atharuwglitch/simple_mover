import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class MoverNode(Node):
    def __init__(self):
        super().__init__('mover_node')

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        self.timer = self.create_timer(0.1, self.timer_callback)
        self.start_time = time.time()

    def timer_callback(self):
        msg = Twist()
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        if elapsed_time < 5.0:
            msg.linear.x = 0.5
            msg.angular.z = 0.0
            self.get_logger().info('Gerak Maju...')

        elif elapsed_time < 10.0:
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.get_logger().info('Rotasi...')

        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info('Berhenti.')

            self.publisher_.publish(msg)

            self.timer.cancel()
            rclpy.shutdown()
            return

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = MoverNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time


class MoverNode(Node):
    def __init__(self):
        super().__init__('mover_node')

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        self.timer = self.create_timer(0.1, self.timer_callback)
        self.start_time = time.time()

    def timer_callback(self):
        msg = Twist()

        elapsed_time = time.time() - self.start_time

        # 1. Maju sisi panjang
        if elapsed_time < 4.0:
            msg.linear.x = 0.5
            msg.angular.z = 0.0
            self.get_logger().info('Maju sisi panjang 1')

        # 2. Rotasi 90 derajat
        elif elapsed_time < 7.2:
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.get_logger().info('Rotasi 90 derajat')

        # 3. Maju sisi pendek
        elif elapsed_time < 9.2:
            msg.linear.x = 0.5
            msg.angular.z = 0.0
            self.get_logger().info('Maju sisi pendek 1')

        # 4. Rotasi 90 derajat
        elif elapsed_time < 12.4:
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.get_logger().info('Rotasi 90 derajat')

        # 5. Maju sisi panjang
        elif elapsed_time < 16.4:
            msg.linear.x = 0.5
            msg.angular.z = 0.0
            self.get_logger().info('Maju sisi panjang 2')

        # 6. Rotasi 90 derajat
        elif elapsed_time < 19.6:
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.get_logger().info('Rotasi 90 derajat')

        # 7. Maju sisi pendek
        elif elapsed_time < 21.6:
            msg.linear.x = 0.5
            msg.angular.z = 0.0
            self.get_logger().info('Maju sisi pendek 2')

        # 8. Rotasi terakhir
        elif elapsed_time < 24.8:
            msg.linear.x = 0.0
            msg.angular.z = 0.5
            self.get_logger().info('Rotasi 90 derajat terakhir')

        # 9. Berhenti
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info('Gerak persegi panjang selesai')

            self.publisher_.publish(msg)

            self.timer.cancel()
            rclpy.shutdown()
            return

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = MoverNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
