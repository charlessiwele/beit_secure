import os
import random
import string
from shutil import copyfile

import face_recognition
import requests
from settings import FACE_SEC_KNOWN_FACES_DIRECTORY, FACE_SEC_UNKNOWN_FACES_DIRECTORY

known_faces_directory_list = os.listdir(FACE_SEC_KNOWN_FACES_DIRECTORY)


def compare_unknown_face_to_known_faces(unknown_face_path):
    # Load the jpg files into numpy arrays
    potential_matches = []
    for known_face_directory in known_faces_directory_list:
        known_faces_path = os.path.join(FACE_SEC_KNOWN_FACES_DIRECTORY, known_face_directory)
        known_faces_collection = os.listdir(known_faces_path)
        known_faces_encoded = []
        for face in known_faces_collection:
            face_path = os.path.join(known_faces_path, face)
            known_face = face_recognition.load_image_file(face_path)
            # Get the face encodings for each face in each image file
            # Since there could be more than one face in each image, it returns a list of encodings.
            known_face_encoding = face_recognition.face_encodings(known_face)[0]
            known_faces_encoded.append(known_face_encoding)
        unknown_face = face_recognition.load_image_file(unknown_face_path)
        unknown_face_encoded = face_recognition.face_encodings(unknown_face)[0]
        # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
        results = face_recognition.compare_faces(known_faces_encoded, unknown_face_encoded, tolerance=0.5)
        if True in results:
            potential_matches.append(os.path.join(FACE_SEC_KNOWN_FACES_DIRECTORY, known_face_directory))
    return potential_matches


def create_known_faces_directory(known_face_directory):
    known_faces_path = os.path.join(FACE_SEC_KNOWN_FACES_DIRECTORY, known_face_directory)
    os.makedirs(known_faces_path, exist_ok=True)
    return known_faces_path


def copy_face_to_known_faces_directory(new_known_face_path, known_faces_directory):
    known_faces_directory_path = os.path.join(FACE_SEC_KNOWN_FACES_DIRECTORY, known_faces_directory)
    filename = os.path.basename(new_known_face_path)
    copyfile(new_known_face_path, os.path.join(known_faces_directory_path, filename))


def remove_known_faces_directory(known_faces_directory):
    os.rmdir(known_faces_directory)


def remove_known_faces_file(known_faces_file_path):
    os.remove(known_faces_file_path)


def generate_random_file_and_directory_names(how_long=25):
    # https://www.educative.io/edpresso/how-to-generate-a-random-string-in-python
    # printing lowercase
    # letters = string.ascii_lowercase
    # print(''.join(random.choice(letters) for i in range(10)))
    #
    # # printing uppercase
    # letters = string.ascii_uppercase
    # print(''.join(random.choice(letters) for i in range(10)))
    #
    # # printing digits
    # letters = string.digits
    # print(''.join(random.choice(letters) for i in range(10)))
    #
    # # printing punctuation
    # letters = string.punctuation
    # print(''.join(random.choice(letters) for i in range(10)))

    # # printing letters
    letters = string.ascii_letters
    letters_result = ''.join(random.choice(letters) for i in range(how_long))
    print(letters_result)
    return letters_result


def save_unkown_image(img_path_io):
    name_img = generate_random_file_and_directory_names(how_long=25) + '.jpeg'
    image_destination = os.path.join(FACE_SEC_UNKNOWN_FACES_DIRECTORY, name_img)
    outfile = open(image_destination, 'wb')
    outfile.write(img_path_io)
    outfile.flush()
    outfile.close()
    return image_destination


def post_kown_image_for_save(img_path, destination_path):
    url = 'http://127.0.0.1:8000/face_sec/store_image/'
    with open(img_path, 'rb') as img:
        name_img = os.path.basename(img_path)
        files = {
            'image': (name_img, img, 'multipart/form-data', {'Expires': '0'})
        }
        data = {
            'destination_path': destination_path
        }

        with requests.Session() as s:
            r = s.post(url, files=files, data=data)
            print(r.status_code)
