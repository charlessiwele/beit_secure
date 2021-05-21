import os
import random
import string
from shutil import copyfile
import cv2
import face_recognition
from settings import FACE_SEC_KNOWN_FACES_DIRECTORY, FACE_SEC_UNKNOWN_FACES_DIRECTORY, FACE_CASCADE_PATH

os.makedirs(FACE_SEC_KNOWN_FACES_DIRECTORY, exist_ok=True)


def run_potential_face_match_tolerance_increment(unknown_face, known_faces_encoded, known_face_directory):
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
    potential_match = None
    faces = face_cascade.detectMultiScale(
        unknown_face,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    unknown_face_encoded = face_recognition.face_encodings(unknown_face, known_face_locations=faces)
    if len(unknown_face_encoded) > 0:
        for tolerance in range(5, 9):
            # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
            tolerance = float(tolerance/10)
            results = face_recognition.compare_faces(known_faces_encoded, unknown_face_encoded[0], tolerance=tolerance)
            if True in results:
                potential_match = os.path.join(FACE_SEC_KNOWN_FACES_DIRECTORY, known_face_directory)
                break
    return potential_match

def compare_unknown_face_to_known_faces(unknown_face_path):
    # Load the jpg files into numpy arrays
    known_faces_directory_list = os.listdir(FACE_SEC_KNOWN_FACES_DIRECTORY)
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
            face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
            faces = face_cascade.detectMultiScale(
                known_face,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            known_face_encoding = face_recognition.face_encodings(known_face)
            if len(known_face_encoding) > 0:
                known_face_encoding = known_face_encoding[0]
                known_faces_encoded.append(known_face_encoding)
            else:
                known_face_encoding = face_recognition.face_encodings(known_face, known_face_locations=faces)
                if len(known_face_encoding) > 0:
                    known_face_encoding = known_face_encoding[0]
                    known_faces_encoded.append(known_face_encoding)
                else:
                    continue
        unknown_face = face_recognition.load_image_file(unknown_face_path)
        unknown_face_encoded = face_recognition.face_encodings(unknown_face)
        if len(unknown_face_encoded) > 0:
            # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
            results = face_recognition.compare_faces(known_faces_encoded, unknown_face_encoded[0], tolerance=0.5)
            if True in results:
                potential_match = os.path.join(FACE_SEC_KNOWN_FACES_DIRECTORY, known_face_directory)
                if potential_match not in potential_matches:
                    potential_matches.append(potential_match)
        else:
            potential_match = run_potential_face_match_tolerance_increment(unknown_face, known_faces_encoded, known_face_directory)
            if potential_match is not None and potential_match not in potential_matches:
                potential_matches.append(potential_match)
    return potential_matches


def create_known_faces_directory(known_face_directory):
    known_faces_path = os.path.join(FACE_SEC_KNOWN_FACES_DIRECTORY, known_face_directory)
    os.makedirs(known_faces_path, exist_ok=True)
    return known_faces_path


def copy_face_to_known_faces_directory(new_known_face_path, known_faces_directory):
    known_faces_directory_path = os.path.join(FACE_SEC_KNOWN_FACES_DIRECTORY, known_faces_directory)
    filename = os.path.basename(new_known_face_path)
    copyfile(new_known_face_path, os.path.join(known_faces_directory_path, filename))


def remove_faces_directory(known_faces_directory):
    os.rmdir(known_faces_directory)


def remove_faces_file(known_faces_file_path):
    os.remove(known_faces_file_path)


def generate_random_uppercase_name(how_long=25):
    ## printing uppercase
    letters = string.ascii_uppercase
    letters_result = ''.join(random.choice(letters) for i in range(how_long))
    return letters_result


def generate_random_lowercase_name(how_long=25):
    ## printing lowercase
    letters = string.ascii_lowercase
    letters_result = ''.join(random.choice(letters) for i in range(how_long))
    return letters_result


def generate_random_numbers(how_long=10):
    ## printing digits
    letters = string.digits
    letters_result = ''.join(random.choice(letters) for i in range(how_long))
    print(letters_result)
    return letters_result


def generate_random_file_system_name(how_long=25):
    letters = string.ascii_letters
    letters_result = ''.join(random.choice(letters) for i in range(how_long))
    print(letters_result)
    return letters_result


def save_unkown_image(img_path_io):
    name_img = generate_random_file_system_name(how_long=25) + '.jpeg'
    image_destination = os.path.join(FACE_SEC_UNKNOWN_FACES_DIRECTORY, name_img)
    outfile = open(image_destination, 'wb')
    outfile.write(img_path_io)
    outfile.flush()
    outfile.close()
    return image_destination

