upload ini ke github ya


import math
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState

class RectangleOdomNode(Node):

    def __init__(self):
        super().__init__('rectangle_odom_node')

        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.create_subscription(JointState, 'joint_states', self.joint_callback, 10)

        # Parameter robot (dari plugin diff-drive)
        self.wheel_radius = 0.1        # m
        self.wheel_separation = 0.45   # m
        self.left_joint = 'base_left_wheel_joint'
        self.right_joint = 'base_right_wheel_joint'

        #Parameter gerakan
        self.linear_speed = 0.3        # m/s
        self.angular_speed = 0.5       # rad/s
        self.side_long_time = 4.0      # detik, sisi panjang
        self.side_short_time = 2.0     # detik, sisi pendek
        self.settle_time = 2.0         # detik menunggu robot benar-benar diam
        self.turn_time = (math.pi / 2) / self.angular_speed

        # (linear_x, angular_z, durasi, label)
        self.sequence = [
            (self.linear_speed, 0.0, self.side_long_time,  'Maju sisi panjang 1'),
            (0.0, self.angular_speed, self.turn_time,      'Belok 90 derajat'),
            (self.linear_speed, 0.0, self.side_short_time, 'Maju sisi pendek 1'),
            (0.0, self.angular_speed, self.turn_time,      'Belok 90 derajat'),
            (self.linear_speed, 0.0, self.side_long_time,  'Maju sisi panjang 2'),
            (0.0, self.angular_speed, self.turn_time,      'Belok 90 derajat'),
            (self.linear_speed, 0.0, self.side_short_time, 'Maju sisi pendek 2'),
            (0.0, self.angular_speed, self.turn_time,      'Belok 90 derajat'),
        ]
        self.state_index = 0
        self.state_start = time.time()
        self.label = 'Mulai'
        self.finish_time = None

        # State estimasi global
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        self.v_b = 0.0
        self.w_b = 0.0
        self.prev_left = None
        self.prev_right = None
        self.prev_time = None

        self.tick = 0
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('Mulai: gerak persegi panjang + estimasi koordinat global')

    # Estimasi dari sensor roda 
    def joint_callback(self, msg):
        if self.left_joint not in msg.name or self.right_joint not in msg.name:
            return

        left = msg.position[msg.name.index(self.left_joint)]
        right = msg.position[msg.name.index(self.right_joint)]
        now = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9

        if self.prev_left is None:
            self.prev_left, self.prev_right, self.prev_time = left, right, now
            return

        dt = now - self.prev_time
        if dt <= 0.0:
            return

        d_left = self.wheel_radius * (left - self.prev_left)
        d_right = self.wheel_radius * (right - self.prev_right)
        d_center = (d_left + d_right) / 2.0
        d_theta = (d_right - d_left) / self.wheel_separation

        self.v_b = d_center / dt
        self.w_b = d_theta / dt

        self.x += d_center * math.cos(self.theta + d_theta / 2.0)
        self.y += d_center * math.sin(self.theta + d_theta / 2.0)
        self.theta = math.atan2(math.sin(self.theta + d_theta),
                                math.cos(self.theta + d_theta))

        self.prev_left, self.prev_right, self.prev_time = left, right, now

    # Gerak persegi panjang + tampilan
    def publish_cmd(self, linear_x, angular_z):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.cmd_pub.publish(msg)

    def timer_callback(self):
        if self.state_index < len(self.sequence):
            lin, ang, dur, label = self.sequence[self.state_index]
            self.label = label
            if time.time() - self.state_start < dur:
                self.publish_cmd(lin, ang)
            else:
                self.state_index += 1
                self.state_start = time.time()
        else:
            # Lintasan selesai: robot berhenti, tunggu sebentar sampai diam
            self.publish_cmd(0.0, 0.0)
            self.label = 'Berhenti'
            if self.finish_time is None:
                self.finish_time = time.time()
            elif time.time() - self.finish_time >= self.settle_time:
                self.print_final()
                self.timer.cancel()
                rclpy.shutdown()
                return

        # Tampilkan estimasi tiap 0.5 detik
        self.tick += 1
        if self.tick % 5 == 0:
            self.print_pose()

    def print_pose(self):
        if self.prev_left is None:
            self.get_logger().info('Menunggu data /joint_states ...')
            return
        self.get_logger().info(
            f'[{self.label:<20}] x = {self.x:7.3f} m | y = {self.y:7.3f} m | '
            f'theta = {math.degrees(self.theta):7.2f} deg | '
            f'v_b = {self.v_b:5.2f} m/s'
        )

    def print_final(self):
        jarak = math.hypot(self.x, self.y)
        self.get_logger().info(' LINTASAN SELESAI ')
        self.get_logger().info(
            f'Posisi akhir: x = {self.x:.3f} m, y = {self.y:.3f} m, '
            f'theta = {math.degrees(self.theta):.2f} deg'
        )
        self.get_logger().info(f'Jarak dari titik awal (0, 0): {jarak:.3f} m')


def main(args=None):
    rclpy.init(args=args)
    node = RectangleOdomNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.publish_cmd(0.0, 0.0)
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
EOF
