import os
from services.camera_services import valid_video_capture_devices, run_face_detecting_camera
from services.face_sec_services import compare_unknown_face_to_known_faces, copy_face_to_known_faces_directory, \
    create_known_faces_directory, remove_faces_file
from settings import UNPROCESSED_IMAGES_DIRECTORY

capture_devices = valid_video_capture_devices()
run_face_detecting_camera(capture_devices[0], window_name='Image Capture', display_grey=False)

unprocessed_images = os.listdir(UNPROCESSED_IMAGES_DIRECTORY)
for image_name in unprocessed_images:
    image_path = os.path.join(UNPROCESSED_IMAGES_DIRECTORY, image_name)
    image_path_results = compare_unknown_face_to_known_faces(image_path)
    if len(image_path_results) > 0:
        known_faces_directory = image_path_results[0]
        # TODO: create sqlite db record for the captured images
    else:
        image_path_basename = os.path.basename(image_path).split('.')[0]
        known_faces_directory = create_known_faces_directory(image_path_basename)
    copy_face_to_known_faces_directory(image_path, known_faces_directory)
    remove_faces_file(image_path)
    # TODO: return sqlite db record for the captured images
    # TODO: Add record to sqlite db to reflect captured images transaction
