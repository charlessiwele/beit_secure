import os


class FileSystemHandler:

    def __init__(self):
        pass

    @staticmethod
    def generate_file_directories(files_directory):
        print(f"Creating folders...")
        if type(files_directory) in (tuple, list):
            for file in files_directory:
                try:
                    if not os.path.isdir(file):
                        os.makedirs(file)
                        print(f"Created folder  {file}")
                    else:
                        print(f"Folder {file} already exists")
                except OSError as e:
                    print(e)
        else:
            try:
                if not os.path.isdir(files_directory):
                    os.makedirs(files_directory)
                    print(f"Created folder  {files_directory}")
                else:
                    print(f"Folder {files_directory} already exists")
            except OSError as e:
                print(e)
