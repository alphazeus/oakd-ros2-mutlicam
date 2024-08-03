# oakd-ros2-mutlicam

Light weight code based on the library from Luxonis for OAK-D cameras. ROS2 video streaming based on OAK-D cameras.

### Feature additions
- Publishing of RGB Camera stream over ROS2 topics
- Support for Multiple Cameras
- Support for multithreaded streaming on ROS2 topics
Tested with four simultaneous OAK-D lite RGB cameras.

## Dependencies
- ROS2
- Python: >3.9
  
## How to use the library
Install the ROS2 (Tested on ROS2 Humble)

Install the required tools with the given script.
```
python3 install_requirements.py
```
Change the USB rules by running the command
```
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
```
Test the code by running the demo code
```
python3 depthai_demo.py
```
This should output the camera stream with RGB and depth camera windows.
Install cv-bridge to support the multicam code
```
sudo apt-get install ros-(ROS version name)-cv-bridge
```
Now run the supported code
```
python3 depthai_ros2_multicam.py
```
You should be able to see `/videoX` topics when you run `ros2 topic list` in a new terminal.
