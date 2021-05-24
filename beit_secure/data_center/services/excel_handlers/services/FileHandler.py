import os
from datetime import datetime
from data_center.services.excel_handlers.services import ENV
from data_center.services.excel_handlers.services.ExcelHandler import ExcelHandler
from data_center.services.excel_handlers.services.FileSystemHandler import FileSystemHandler
from data_center.services.settings import DEFAULT_FILE_WRITE_NAME, DEFAULT_FILE_READ_NAME


class FileHandler:
    @staticmethod
    def generate_excel_file_data(multi_row_data=(['row 1, col 1', 'row 1, col 2'], ['row 2, col 1', 'row 2, col 2']),
                                 read_file_name: str = DEFAULT_FILE_READ_NAME,
                                 write_file_name: str = DEFAULT_FILE_WRITE_NAME,
                                 write_worksheet_name: str = 'Sheet 1',
                                 out_files_source: str = ENV.out_files_source,
                                 starting_row_index=0,
                                 file_prefix=datetime.now().strftime("%Y%m%d%H%M%S")
                                 ):

        write_workbook = ExcelHandler.write_worksheet(read_file_name,
                                                      write_worksheet_name,
                                                      multi_row_data,
                                                      starting_row_index=starting_row_index)
        if file_prefix:
            new_file_name = file_prefix + '_' + write_file_name
        else:
            new_file_name = write_file_name
        FileSystemHandler.generate_file_directories(out_files_source)
        file_name_path = os.path.join(out_files_source, new_file_name)
        write_workbook.save(file_name_path)
        print(f'File "{new_file_name}" saved to folder "{out_files_source}"')
        return new_file_name

    @staticmethod
    def read_excel_file_data(read_file_name: str, write_worksheet_name: str = 'Sheet 1'):

        read_workbook = ExcelHandler.open_workbook(read_file_name)
        worksheet = ExcelHandler.get_sheet_by_name(read_workbook, write_worksheet_name)
        sheet_row_count = ExcelHandler.get_sheet_row_count(worksheet)
        excel_file_data = []
        for sheet_row in range(0, sheet_row_count):
            sheet_row_as_array = ExcelHandler.get_sheet_row_as_array(worksheet, sheet_row)
            excel_file_data.append(sheet_row_as_array)
        print(excel_file_data)
        return excel_file_data

