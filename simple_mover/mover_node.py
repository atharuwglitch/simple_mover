import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MoverNode(Node):
    def __init__(self):
        super().__init__('mover_node')
        
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.02, self.timer_callback)
        
        # Menggunakan jam internal ROS 2 agar gerakan sinkron dan mulus
        self.start_time = self.get_clock().now()
        
    def timer_callback(self):
        msg = Twist()
        current_time = self.get_clock().now()
        elapsed_time = (current_time - self.start_time).nanoseconds / 1e9
                
        # 1. SISI PANJANG 1 (Maju selama 6 detik)
        if elapsed_time < 6.0:
            msg.linear.x = 0.4
            msg.angular.z = 0.0
            self.get_logger().info('Sisi Panjang 1: Maju...')
            
        # Belok 1 (Putar 90 derajat selama 2 detik)
        elif elapsed_time < 8.0:
            msg.linear.x = 0.0
            msg.angular.z = 0.785 # Kecepatan putar disesuaikan agar pas 90 derajat
            self.get_logger().info('Belok 1...')
            
        # 2. SISI LEBAR 1 (Maju selama 3 detik)
        elif elapsed_time < 11.0:
            msg.linear.x = 0.4
            msg.angular.z = 0.0
            self.get_logger().info('Sisi Lebar 1: Maju...')
            
        # Belok 2 (Putar 90 derajat)
        elif elapsed_time < 13.0:
            msg.linear.x = 0.0
            msg.angular.z = 0.785
            self.get_logger().info('Belok 2...')
            
        # 3. SISI PANJANG 2 (Maju selama 6 detik)
        elif elapsed_time < 19.0:
            msg.linear.x = 0.4
            msg.angular.z = 0.0
            self.get_logger().info('Sisi Panjang 2: Maju...')
            
        # Belok 3 (Putar 90 derajat)
        elif elapsed_time < 21.0:
            msg.linear.x = 0.0
            msg.angular.z = 0.785
            self.get_logger().info('Belok 3...')
            
        # 4. SISI LEBAR 2 (Maju selama 3 detik)
        elif elapsed_time < 24.0:
            msg.linear.x = 0.4
            msg.angular.z = 0.0
            self.get_logger().info('Sisi Lebar 2: Maju...')
            
        # Belok 4 (Putar 90 derajat untuk kembali ke hadapan semula)
        elif elapsed_time < 26.0:
            msg.linear.x = 0.0
            msg.angular.z = 0.785
            self.get_logger().info('Belok 4...')
            
        # SELESAI DAN BERHENTI
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info('Misi Selesai: Robot Berhenti!')
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
    main()import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MoverNode(Node):
    def __init__(self):
        super().__init__('mover_node')
        
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.02, self.timer_callback)
        
        # Menggunakan jam internal ROS 2 agar gerakan sinkron dan mulus
        self.start_time = self.get_clock().now()
        
    def timer_callback(self):
        msg = Twist()
        current_time = self.get_clock().now()
        elapsed_time = (current_time - self.start_time).nanoseconds / 1e9
                
        # 1. SISI PANJANG 1 (Maju selama 6 detik)
        if elapsed_time < 6.0:
            msg.linear.x = 0.4
            msg.angular.z = 0.0
            self.get_logger().info('Sisi Panjang 1: Maju...')
            
        # Belok 1 (Putar 90 derajat selama 2 detik)
        elif elapsed_time < 8.0:
            msg.linear.x = 0.0
            msg.angular.z = 0.785 # Kecepatan putar disesuaikan agar pas 90 derajat
            self.get_logger().info('Belok 1...')
            
        # 2. SISI LEBAR 1 (Maju selama 3 detik)
        elif elapsed_time < 11.0:
            msg.linear.x = 0.4
            msg.angular.z = 0.0
            self.get_logger().info('Sisi Lebar 1: Maju...')
            
        # Belok 2 (Putar 90 derajat)
        elif elapsed_time < 13.0:
            msg.linear.x = 0.0
            msg.angular.z = 0.785
            self.get_logger().info('Belok 2...')
            
        # 3. SISI PANJANG 2 (Maju selama 6 detik)
        elif elapsed_time < 19.0:
            msg.linear.x = 0.4
            msg.angular.z = 0.0
            self.get_logger().info('Sisi Panjang 2: Maju...')
            
        # Belok 3 (Putar 90 derajat)
        elif elapsed_time < 21.0:
            msg.linear.x = 0.0
            msg.angular.z = 0.785
            self.get_logger().info('Belok 3...')
            
        # 4. SISI LEBAR 2 (Maju selama 3 detik)
        elif elapsed_time < 24.0:
            msg.linear.x = 0.4
            msg.angular.z = 0.0
            self.get_logger().info('Sisi Lebar 2: Maju...')
            
        # Belok 4 (Putar 90 derajat untuk kembali ke hadapan semula)
        elif elapsed_time < 26.0:
            msg.linear.x = 0.0
            msg.angular.z = 0.785
            self.get_logger().info('Belok 4...')
            
        # SELESAI DAN BERHENTI
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info('Misi Selesai: Robot Berhenti!')
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
    main()import rclpy
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
