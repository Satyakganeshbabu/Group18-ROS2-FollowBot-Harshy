import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class Follow(Node):
    def __init__(self):
        super().__init__('follow')
        self.laser_sub = self.create_subscription(LaserScan, 'laser_scan', self.OnSensorMsg, 10)
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.min_dist = 1.0
        self.linear_k = 0.02
        self.angular_k = 0.08

    def OnSensorMsg(self, msg):
        min_range = msg.range_max + 1
        idx = -1
        for i in range(len(msg.ranges)):
            range = msg.ranges[i]
            if range > msg.range_min and range < msg.range_max and range < min_range:
                min_range = range
                idx = i

        turn = msg.angle_min + msg.angle_increment * idx

        cmd_msg = Twist()

        if idx < 0:
            cmd_msg.linear.x = 0
            cmd_msg.angular.z = 0
        elif min_range <= self.min_dist:
            cmd_msg.linear.x = 0
            cmd_msg.angular.z = turn * self.angular_k
        else:
            cmd_msg.linear.x = self.linear_k / abs(turn)
            cmd_msg.angular.z = turn * self.angular_k

        self.cmd_pub.publish(cmd_msg)

def main(args=None):
    rclpy.init(args=args)
    node = Follow()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
