# oakd-ros2-mutlicam

Light weight code based on the library from Luxonis for OAK-D cameras. ROS2 video streaming based on OAK-D cameras.

### Feature additions
- Publishing of RGB Camera stream over ROS2 topics
- Support for Multiple Cameras
- Support for multithreaded streaming on ROS2 topics

Tested with four simultaneous OAK-D lite RGB cameras.

## How to use the library
Install the ROS2 (Tested on ROS2 Humble)

Install the required tools with the given script.
```
python3 install_requirements.py
```

Test the code by running the demo code
```
python3 depthai_demo.py
```
This should output the camera stream with RGB and depth camera windows.

Now run the supported code
```
python3 depthai_ros2_multicam.py
```

You should be able to see `/videoX` topics when you run `ros2 topic list` in a new terminal.

