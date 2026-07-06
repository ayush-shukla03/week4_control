# Kratos Rover: Double Ackermann Kinematics Assignment

Welcome! In this assignment, you will write a Kinematic Controller for a 4-wheel independent drive and steer rover named Kratos.

You will take standard joystick commands and convert them into the specific steering angles and wheel velocities required to drive the rover using Double Ackermann steering geometry.

---

## ⚙️ System Requirements
This assignment is built for **ROS 2 Humble** running on **Ubuntu 22.04**. 
You are expected to have the `ros-humble-desktop` environment installed.

## 🛠️ Step 1: Install System Dependencies
Before cloning this repository, you must install the standard simulation bridges and hardware interfaces required to run in Gazebo Classic.

Run the following command to install the required packages:

```bash
sudo apt update
sudo apt install ros-humble-gazebo-ros-pkgs \
                 ros-humble-gazebo-ros2-control \
                 ros-humble-ros2-control \
                 ros-humble-ros2-controllers \
                 ros-humble-teleop-twist-keyboard