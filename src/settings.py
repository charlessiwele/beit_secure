import os
from pathlib import Path
import yaml


BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = os.path.join(str(BASE_DIR), "src")
CONFIG_ROOT = os.path.join(SRC_DIR, "config.yaml")
print(CONFIG_ROOT)
file = open(CONFIG_ROOT)
app_config = yaml.load(file, Loader=yaml.FullLoader)

ORGANISATION_LOGO_DIRECTORY = os.path.join(SRC_DIR, 'public/images/logos/')
ORGANISATION_LOGO = os.path.join(ORGANISATION_LOGO_DIRECTORY, app_config.get('organisation_logo'))
QUOTATION_ITEMS_PER_PAGE = os.path.join(ORGANISATION_LOGO_DIRECTORY, app_config.get('organisation_logo'))
ORGANISATION_LOGO = os.path.join(ORGANISATION_LOGO_DIRECTORY, app_config.get('organisation_logo'))

PDF_FILES_DIRECTORY = os.path.join(SRC_DIR, 'public/pdf')

INVOICES_DIRECTORY = os.path.join(PDF_FILES_DIRECTORY, 'invoices')

QUOTATIONS_DIRECTORY = os.path.join(PDF_FILES_DIRECTORY, 'quotations')

FACE_SEC_KNOWN_FACES_DIRECTORY = os.path.join(SRC_DIR, "face_sec/face_collection/known/")

FACE_SEC_UNKNOWN_FACES_DIRECTORY = os.path.join(SRC_DIR, "face_sec/face_collection/unknown/")

UNPROCESSED_IMAGES_DIRECTORY = os.path.join(SRC_DIR, "face_sec/unprocessed/images")
UNPROCESSED_VIDEOS_DIRECTORY = os.path.join(SRC_DIR, "face_sec/unprocessed/videos")

EXCEL_IN_FILE_SOURCE = os.path.join(SRC_DIR, 'excel_files/in_files_source')

EXCEL_OUT_FILE_SOURCE = os.path.join(SRC_DIR, 'excel_files/out_files_source')

FACE_CASCADE_PATH = os.path.join(SRC_DIR, "haarcascade_frontalface.xml")

FOLDER_COLLECTION = [
    ORGANISATION_LOGO_DIRECTORY,
    PDF_FILES_DIRECTORY,
    INVOICES_DIRECTORY,
    QUOTATIONS_DIRECTORY,
    FACE_SEC_KNOWN_FACES_DIRECTORY,
    FACE_SEC_UNKNOWN_FACES_DIRECTORY,
    UNPROCESSED_IMAGES_DIRECTORY,
    UNPROCESSED_VIDEOS_DIRECTORY,
    EXCEL_IN_FILE_SOURCE,
    EXCEL_OUT_FILE_SOURCE,
]
EMAIL_SMTP_SERVER = app_config.get('email_smtp_server')

SENDER_EMAIL = app_config.get('sender_email')

SENDER_EMAIL_PASSWORD = app_config.get('sender_email_password')

BCC_EMAIL_RECIPIENTS = app_config.get('bcc_sender_email')

EMAIL_RETRIES_COUNT = app_config.get('email_retries_count')

INVOICE_ITEMS_PER_PAGE = app_config.get('invoices_items_per_page')

BANK_DETAILS = app_config.get('bank_details')

IMAGE_COUNT_LIMIT = app_config.get('image_count_limit')

DEFAULT_FILE_WRITE_NAME = 'out_files_source.xls'
DEFAULT_FILE_READ_NAME = 'in_files_source.xls'