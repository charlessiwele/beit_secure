import os
import xlwt
import xlrd
from xlutils.copy import copy


class ExcelHandler:
    @staticmethod
    def create_workbook():
        return xlwt.Workbook(encoding='utf-8')

    @staticmethod
    def open_workbook(workbook_name_path: str):
        workbook = xlrd.open_workbook(workbook_name_path)
        return workbook

    @staticmethod
    def create_workbook_sheet(workbook: xlwt.Workbook, sheet_name: str, cell_overwrite: bool = True):
        return workbook.add_sheet(sheet_name, cell_overwrite_ok=cell_overwrite)

    @staticmethod
    def get_sheet_by_name(workbook: xlrd.Book, sheet_name: str):
        sheets = ExcelHandler.get_sheet_by_index_or_name(workbook, sheet_name)
        sheet = workbook.sheet_by_name(sheet_name)
        return sheet

    @staticmethod
    def get_sheet_by_index(workbook: xlrd.Book, sheet_index: int):
        return workbook.sheet_by_index(sheet_index)

    @staticmethod
    def get_sheet_by_index_or_name(workbook: xlrd.Book, sheet_name_or_index):
        if type(sheet_name_or_index) == int:
            sheet = workbook.sheet_by_index(sheet_name_or_index)
        else:
            sheet = workbook.sheet_by_name(sheet_name_or_index)
        return sheet

    @staticmethod
    def open_workbook_to_edit(workbook_name_path: str):
        read_workbook: xlrd.Book = ExcelHandler.open_workbook(workbook_name_path)
        write_workbook: xlwt.Workbook = copy(read_workbook)
        return write_workbook

    @staticmethod
    def get_sheet_row_count(workbook_sheet: xlrd.sheet):
        return workbook_sheet.nrows

    @staticmethod
    def get_sheet_column_count(workbook_sheet: xlrd.sheet):
        return workbook_sheet.ncols

    @staticmethod
    def get_sheet_row_as_array(workbook_sheet: xlrd.sheet, sheet_row_number: int = 1):
        worksheet_col_count = workbook_sheet.ncols
        row_as_array = []
        for each_col in range(0, worksheet_col_count):
            row_as_array.append(workbook_sheet.cell(sheet_row_number, each_col).value)
        return row_as_array

    @staticmethod
    def write_worksheet_row(write_worksheet: any, array_values: any, row_index: int):
        row: xlwt.Row = write_worksheet.row(row_index)
        for idx, item in enumerate(array_values):
            row.write(idx, item)
        return row

    @staticmethod
    def write_worksheet(file_name_path: any, sheet_name: str, multi_row_data: []):
        if not os.path.exists(file_name_path):
            write_workbook: xlwt.Workbook = ExcelHandler.create_workbook()
            write_workbook_sheet: xlwt.Worksheet = ExcelHandler.create_workbook_sheet(write_workbook, sheet_name)
        else:
            write_workbook: xlwt.Workbook = ExcelHandler.open_workbook_to_edit(file_name_path)
            sheet = write_workbook.get_sheet(sheet_name)
            if sheet:
                write_workbook_sheet: xlrd.sheet = sheet
            else:
                write_workbook_sheet: xlrd.sheet = write_workbook.add_sheet(sheet_name)

        row_index = 0
        for array_values in multi_row_data:
            ExcelHandler.write_worksheet_row(write_workbook_sheet, array_values, row_index)
            row_index += 1
        return write_workbook
