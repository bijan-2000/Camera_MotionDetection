# Authentication for pyrogram is not good.
# Change the recording format to .mp4
# Frame per second is not accurate for recording

def motion_detector(stream, fps_motion, fps_record, recording_time):
    import cv2
    import numpy as np
    import time
    from datetime import datetime
    from pyrogram import Client

    recorded_files = []

    delay_motion = np.rint(1000 / fps_motion).astype(int)  # Time delay between each frame for motion detection

    cap = cv2.VideoCapture(stream)

    while True:
        ret1, frame1 = cap.read()
        cv2.waitKey(delay_motion)
        ret2, frame2 = cap.read()
        gray_scale1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray_scale1 = cv2.GaussianBlur(gray_scale1, (21, 21), 0)

        gray_scale2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray_scale2 = cv2.GaussianBlur(gray_scale2, (21, 21), 0)

        diff = cv2.absdiff(gray_scale2, gray_scale1)
        thresh = np.sum(diff)

        if thresh > 1000000:  # Should be in percentage
            timer = recording_time
            tic = time.time()
            toc = time.time()
            print("Motion!")
            w, h = int(cap.get(3)), int(cap.get(4))
            filename = datetime.now().strftime("%H_%M_%S_%d_%m_%Y.avi")
            recorded_files.append(filename)
            writer = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'MJPG'), fps=fps_record,
                                     frameSize=(w, h))
            while timer > (toc-tic):
                ret, frame = cap.read()
                writer.write(frame)
                toc = time.time()

        elif len(recorded_files) > 0 & thresh < 1000000:  # Meanwhile it is not working on motion detection
            for i in recorded_files:
                path = i
                app = Client("IOT Project")
                app.start()
                app.send_document("me", path)
                app.send_message("me", "Motion is detected on {}".format(datetime.now()))  # given time is not precise!
                app.stop()
                recorded_files.remove(i)


motion_detector(0, 2, 40, 60)
