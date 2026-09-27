# Simple Mover - Robot Industri

Program ROS 2 untuk menggerakkan robot pada simulasi dengan pola berbentuk persegi panjang.

## Environment

- **Operating System:** Ubuntu 24.04 LTS
- **ROS 2:** Jazzy Jalisco
- **Programming Language:** Python 3
- **Simulation:** Gazebo

## Package

`simple_mover`

## Program

Node `mover_node` mengendalikan gerakan robot menggunakan pesan `geometry_msgs/Twist` melalui topic:

```text
/cmd_vel
