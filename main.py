import depthai as dai
import time
import cv2
import os

pipeline = dai.Pipeline()

cam_rgb = pipeline.createColorCamera()
cam_rgb.setPreviewSize(854, 480)
cam_rgb.setInterleaved(False)
cam_rgb.setFps(60)

xout_video = pipeline.createXLinkOut()
xout_video.setStreamName("video")
cam_rgb.preview.link(xout_video.input)

SCREENSHOT_INTERVAL = 1

with dai.Device(pipeline) as device:
    video_queue = device.getOutputQueue(name="video", maxSize=4, blocking=False)
    time_counter = time.time()

    while True:
        video_frame = video_queue.get()
        frame = video_frame.getCvFrame()

        delta_time_counter = time.time()

        if delta_time_counter - time_counter >= SCREENSHOT_INTERVAL:
            if not os.path.exists("images"):
                os.makedirs("images")

            cv2.imwrite(f'images/{time.strftime("%Y-%m-%d--%H-%M-%S")}.jpg', frame)
            time_counter = delta_time_counter

        cv2.imshow("Smart Traffic Camera Videostream", frame)

        if cv2.waitKey(1) == ord('q'):
            break

cv2.destroyAllWindows()
