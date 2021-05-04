import os
from datetime import datetime
from excel_handlers.services import ENV
from excel_handlers.services.ExcelHandler import ExcelHandler
from excel_handlers.services.FileSystemHandler import FileSystemHandler


class FileHandler:
    @staticmethod
    def generate_excel_file_data(multi_row_data=(['row 1, col 1', 'row 1, col 2'], ['row 2, col 1', 'row 2, col 2']),
                                 read_file_name: str = 'in_files_source.xls',
                                 write_file_name: str = 'out_files_source.xls',
                                 write_worksheet_name: str = 'Earnings Statement',
                                 out_files_source: str = ENV.out_files_source
                                 ):

        write_workbook = ExcelHandler.write_worksheet(read_file_name, write_worksheet_name, multi_row_data)

        now = datetime.now()  # current date and time
        date_time = now.strftime("%Y%m%d%H%M%S")
        new_file_name = f"{date_time}_{write_file_name}.xls"
        new_file_name = new_file_name.replace('.xls.xls', '.xls')
        FileSystemHandler.generate_file_directories(out_files_source)
        new_file_name_path = os.path.join(out_files_source, new_file_name)
        write_workbook.save(new_file_name_path)
        print(f'File "{new_file_name}" saved to folder "{out_files_source}"')
        return new_file_name_path

    @staticmethod
    def read_excel_file_data(read_file_name: str,
                             write_worksheet_name: str = 'Earnings Statement',
                             ):

        read_workbook = ExcelHandler.open_workbook(read_file_name)
        worksheet = ExcelHandler.get_sheet_by_name(read_workbook, write_worksheet_name)
        sheet_row_count = ExcelHandler.get_sheet_row_count(worksheet)
        excel_file_data = []
        for sheet_row in range(0, sheet_row_count):
            sheet_row_as_array = ExcelHandler.get_sheet_row_as_array(worksheet, sheet_row)
            excel_file_data.append(sheet_row_as_array)
        print(excel_file_data)
        return excel_file_data

