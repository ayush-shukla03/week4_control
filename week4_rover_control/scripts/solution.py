#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray
import math

class DoubleAckermannSolution(Node):
    def __init__(self):
        super().__init__('double_ackermann_solution')
        
        self.cmd_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)
        self.steer_pub = self.create_publisher(Float64MultiArray, '/steering_controller/commands', 10)
        self.drive_pub = self.create_publisher(Float64MultiArray, '/drive_controller/commands', 10)

        # Rover Physical Constants
        self.wheelbase = 0.4 
        self.track_width = 0.6
        self.wheel_radius = 0.12

        self.get_logger().info("Solution Node Active. Ready for /cmd_vel inputs.")

    def cmd_callback(self, msg):
        v = msg.linear.x       # Forward velocity (m/s)
        omega = msg.angular.z  # Rotational velocity (rad/s)
        
        # Wheel coordinates (x, y) relative to the center of the rover
        # Standard ROS coordinate frame: X is forward, Y is left
        x_f = self.wheelbase / 2.0
        x_r = -self.wheelbase / 2.0
        y_l = self.track_width / 2.0
        y_r = -self.track_width / 2.0

        # Dictionary to maintain the strict YAML order: [FL, FR, RL, RR]
        wheels = [
            {'name': 'fl', 'x': x_f, 'y': y_l},
            {'name': 'fr', 'x': x_f, 'y': y_r},
            {'name': 'rl', 'x': x_r, 'y': y_l},
            {'name': 'rr', 'x': x_r, 'y': y_r}
        ]

        angles = []
        velocities = []

        for wheel in wheels:
            # 1. Calculate the velocity vector (vx, vy) for this specific wheel
            # Formula: V_wheel = V_chassis + (Omega x R_wheel)
            vx = v - (omega * wheel['y'])
            vy = omega * wheel['x']

            # 2. Convert vector to steering angle and linear speed
            speed = math.hypot(vx, vy)
            angle = math.atan2(vy, vx)

            # 3. Angle Wrapping (The Trick)
            # We set URDF joint limits to +/- 1.57 rads (90 degrees). 
            # If the math demands a wheel point backwards (e.g., > 90 deg), 
            # we must flip the wheel 180 degrees forward and spin the motor in reverse.
            if angle > math.pi / 2.0:
                angle -= math.pi
                speed = -speed
            elif angle < -math.pi / 2.0:
                angle += math.pi
                speed = -speed

            # 4. Convert linear speed (m/s) to wheel rotation speed (rad/s)
            wheel_omega = speed / self.wheel_radius

            angles.append(angle)
            velocities.append(wheel_omega)

        # Publish Steering Commands
        steer_msg = Float64MultiArray()
        steer_msg.data = angles
        self.steer_pub.publish(steer_msg)

        # Publish Drive Commands
        drive_msg = Float64MultiArray()
        drive_msg.data = velocities
        self.drive_pub.publish(drive_msg)

def main(args=None):
    rclpy.init(args=args)
    node = DoubleAckermannSolution()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
