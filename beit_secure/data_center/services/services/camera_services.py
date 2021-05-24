import os
from datetime import datetime
from data_center.services.settings import IMAGE_COUNT_LIMIT, UNPROCESSED_IMAGES_DIRECTORY, UNPROCESSED_VIDEOS_DIRECTORY
import cv2
from data_center.services.settings import FACE_CASCADE_PATH


def valid_video_capture_devices():
    potential_device_range = 10
    available_capture_devices = []
    for devices_index in range(potential_device_range):
        cap = cv2.VideoCapture(devices_index)
        cap_is_opened = cap.isOpened()
        if cap and cap_is_opened:
            available_capture_devices.append(devices_index)
            cap.release()
    return available_capture_devices


def generate_name(file_type='image'):
    file_date_time_taken = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = datetime.now().strftime(f'{file_date_time_taken}')
    if file_type == 'image':
        os.makedirs(UNPROCESSED_IMAGES_DIRECTORY, exist_ok=True)
        file_location = os.path.join(UNPROCESSED_IMAGES_DIRECTORY, file_name + '.jpg')
    else:
        os.makedirs(UNPROCESSED_VIDEOS_DIRECTORY, exist_ok=True)
        file_location = os.path.join(UNPROCESSED_VIDEOS_DIRECTORY, file_name + '.avi')
    return file_location


def capture_image(image_frame):
    img_name = generate_name('image')
    imwrite_result = cv2.imwrite(img_name, image_frame)
    print("imwrite_result:", imwrite_result)
    if imwrite_result:
        print("Image {} saved.".format(img_name))
        return img_name
    else:
        print("Image {} failed to save.".format(img_name))
        return imwrite_result


def run_image_capture(valid_image_capture_device, window_name='Image Capture'):
    cam = cv2.VideoCapture(valid_image_capture_device)
    cv2.namedWindow(window_name)

    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow(window_name, frame)

        wait_key = cv2.waitKey(1)
        if wait_key % 256 == 27:
            # ESC pressed
            print("Closing...")
            break
        elif wait_key % 256 == 32:
            # SPACE pressed
            capture_image(frame)
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()


def run_face_detecting_camera(valid_image_capture_device, window_name='Image Capture', display_grey=False):
    cam = cv2.VideoCapture(valid_image_capture_device)
    cv2.namedWindow(window_name)
    img_counter = 0
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        wait_key = cv2.waitKey(1)
        if display_grey:
            frame = gray
        write_text_on_frame(frame, text=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        if wait_key % 256 == 27:
            # ESC pressed
            print("Closing...")
            break
        elif wait_key % 256 == 32:
            # SPACE pressed
            if len(faces) > 0:
                # Draw a rectangle around the faces
                if len(faces) > 1:
                    print("Capturing multiple faces...")
                else:
                    print("Capturing single faces...")
            capture_image(frame)
            img_counter += 1
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow(window_name, frame)
    cam.release()
    cv2.destroyAllWindows()


def run_automated_face_image_capture(valid_image_capture_device, window_name='Image Capture', display_grey=False):
    cam = cv2.VideoCapture(valid_image_capture_device)
    cv2.namedWindow(window_name)
    img_counter = 0
    face_cascade_path = FACE_CASCADE_PATH
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        if display_grey:
            frame = gray
        write_text_on_frame(frame, text=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Closing...")
            break
        if len(faces) > 0:
            # Draw a rectangle around the faces
            if len(faces) > 1:
                print("Multiple faces detected...")
            else:
                print("Single face detected...")
            if img_counter < IMAGE_COUNT_LIMIT:
                capture_image(frame)
                img_counter += 1
            else:
                print("IMAGE COUNT LIMIT:", IMAGE_COUNT_LIMIT)
                break
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow(window_name, frame)
    cam.release()
    cv2.destroyAllWindows()


def run_face_triggered_video_capture(valid_image_capture_device, window_name='Image Capture', display_grey=True):
    cam = cv2.VideoCapture(valid_image_capture_device)
    cv2.namedWindow(window_name)
    file_locations = []
    face_cascade_path = FACE_CASCADE_PATH
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    recording = False
    video_output = None
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        if display_grey:
            frame = gray
        k = cv2.waitKey(1)
        if k % 256 == 27:
            # ESC pressed
            print("Closing...")
            break
        if len(faces) > 0:
            recording_name = generate_name('video')
            if not recording:
                recording = True
                video_output = cv2.VideoWriter(recording_name, fourcc, 20.0, (640, 480))
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                if len(faces) > 1:
                    print("Multiple faces detected...")
                else:
                    print("Single face detected...")
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            write_text_on_frame(frame, text=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            video_output.write(frame)
        else:
            if recording:
                recording = False
                video_output.release()
        cv2.imshow(window_name, frame)
    cam.release()
    cv2.destroyAllWindows()
    return file_locations


def write_text_on_frame(img, text=datetime.now().strftime("%Y/%m/%d %H:%M:%S")):
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.putText(img, text, (10, 450), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
