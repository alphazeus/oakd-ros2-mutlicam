#!/usr/bin/env python3

import cv2
import depthai as dai
import contextlib
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import threading  #For running the nodes in paralled for each cameras
import time

class ImagePublisher(Node):

    def __init__(self, q_rgb, stream_name, cam_count):
        super().__init__('camera'+cam_count)
        self.publisher_ = self.create_publisher(Image, 'video'+cam_count, 10)
        timer_period = 0.2
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.br = CvBridge()
        self.q_rgb = q_rgb
        self.stream_name = stream_name
    
    def timer_callback(self):
        if self.q_rgb.has():
            self.publisher_.publish(self.br.cv2_to_imgmsg(self.q_rgb.get().getCvFrame()))
            self.get_logger().info('Publishing video frame')


def createPipeline():
    # Start defining a pipeline
    pipeline = dai.Pipeline()
    # Define a source - color camera
    camRgb = pipeline.create(dai.node.ColorCamera)

    camRgb.setPreviewSize(300, 300)
    camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    camRgb.setInterleaved(False)

    # Create output
    xoutRgb = pipeline.create(dai.node.XLinkOut)
    xoutRgb.setStreamName("rgb")
    camRgb.preview.link(xoutRgb.input)

    return pipeline


def main(args=None):
    #initialize the rclpy library
    rclpy.init(args=args)
    executor = rclpy.executors.MultiThreadedExecutor()

    with contextlib.ExitStack() as stack:
        deviceInfos = dai.Device.getAllAvailableDevices()
        usbSpeed = dai.UsbSpeed.SUPER
        openVinoVersion = dai.OpenVINO.Version.VERSION_2021_4

        qRgbMap = []
        devices = []
        cam_nodes = []

        for deviceInfo in deviceInfos:
            deviceInfo: dai.DeviceInfo
            device: dai.Device = stack.enter_context(dai.Device(openVinoVersion, deviceInfo, usbSpeed))
            devices.append(device)
            print("===Connected to ", deviceInfo.getMxId())
            mxId = device.getMxId()
            cameras = device.getConnectedCameras()
            usbSpeed = device.getUsbSpeed()
            eepromData = device.readCalibration2().getEepromData()
            print("   >>> MXID:", mxId)
            print("   >>> Num of cameras:", len(cameras))
            print("   >>> USB speed:", usbSpeed)
            if eepromData.boardName != "":
                print("   >>> Board name:", eepromData.boardName)
            if eepromData.productName != "":
                print("   >>> Product name:", eepromData.productName)

            pipeline = createPipeline()
            device.startPipeline(pipeline)

            # Output queue will be used to get the rgb frames from the output defined above
            q_rgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
            stream_name = "rgb-" + mxId + "-" + eepromData.productName
            qRgbMap.append((q_rgb, stream_name))

            #Creating Nodes for each camera detected
            cam_nodes.append(ImagePublisher(q_rgb, stream_name, str(len(cam_nodes))))
            print('Camera Node Created')
            executor.add_node(cam_nodes[len(cam_nodes)-1])

        executor_thread = threading.Thread(target=executor.spin, daemon=True)
        executor_thread.start()
        rate = cam_nodes[0].create_rate(2)
        try:
            while rclpy.ok():
                print('check')
                time.sleep(2)
        except KeyboardInterrupt:
            pass

        for node in cam_nodes:
            node.destroy_node()

        rclpy.shutdown()
        executor_thread.join()


if __name__=='__main__':
    main()
