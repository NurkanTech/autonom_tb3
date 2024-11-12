# Installation
If you have not installed ros, follow the steps this => https://wiki.ros.org/noetic/Installation/Ubuntu

## Overview
![tb3](https://github.com/user-attachments/assets/8e589269-32f9-4715-b498-4f2aa448fb52)

## Dependencies
-Open the terminal
```
roscore
```
```
roslaunch turtlebot3_gazebo turtlebot3_house.launch  #in the new terminal
```
```
roslaunch turtlebot3_navigation turtlebot3_navigation.launch
```

```
rosrun navigate_goal.py
```


If it doesn't work you should try these steps;
```
sudo apt-get update
source /<yoursworkspace>/devel/setup.bash
source /opt/ros/<distro>/setup.sh

