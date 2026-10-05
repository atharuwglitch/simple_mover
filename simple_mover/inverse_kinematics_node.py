import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class InverseKinematicsNode(Node):
    def __init__(self):
        super().__init__('inverse_kinematics_node')

        # Panjang lengan robot (meter)
        self.L1 = 0.30
        self.L2 = 0.20

        # Target posisi end-effector (meter)
        self.x = 0.30
        self.y = 0.20

        # Publisher hasil sudut joint
        self.joint_publisher = self.create_publisher(
            Float64MultiArray,
            'joint_angles',
            10
        )

        # Hitung dan publish setiap 1 detik
        self.timer = self.create_timer(
            1.0,
            self.calculate_inverse_kinematics
        )

    def calculate_inverse_kinematics(self):
        x = self.x
        y = self.y
        L1 = self.L1
        L2 = self.L2

        # Rumus inverse kinematics
        cos_theta2 = (
            x**2 + y**2 - L1**2 - L2**2
        ) / (2 * L1 * L2)

        # Cek apakah target dapat dijangkau
        if cos_theta2 < -1.0 or cos_theta2 > 1.0:
            self.get_logger().error(
                'Target tidak dapat dijangkau oleh robot.'
            )
            return

        # Hitung theta 2
        theta2 = math.acos(cos_theta2)

        # Hitung theta 1
        theta1 = math.atan2(y, x) - math.atan2(
            L2 * math.sin(theta2),
            L1 + L2 * math.cos(theta2)
        )

        # Konversi radian ke derajat
        theta1_deg = math.degrees(theta1)
        theta2_deg = math.degrees(theta2)

        # Buat pesan
        msg = Float64MultiArray()
        msg.data = [theta1_deg, theta2_deg]

        # Publish hasil
        self.joint_publisher.publish(msg)

        # Tampilkan hasil di terminal
        self.get_logger().info(
            f'Target: x={x:.2f} m, y={y:.2f} m | '
            f'Theta1={theta1_deg:.2f}°, '
            f'Theta2={theta2_deg:.2f}°'
        )


def main(args=None):
    rclpy.init(args=args)

    node = InverseKinematicsNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
