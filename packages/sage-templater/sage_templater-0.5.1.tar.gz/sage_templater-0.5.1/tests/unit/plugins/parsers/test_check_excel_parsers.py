from sage_templater.plugins.file_classifiers.excel_classifier import copy_xls_to_xlsx
from sage_templater.plugins.parsers.check_excel_parsers import get_start_and_end_row_numbers
from sage_templater.plugins.parsers.excel_parser import get_wb_and_sheets


class TestGetStartAndEndRowNumbers:

    def test_get_start_and_end_row_numbers(self, check_template):
        wb, sheet_names =  get_wb_and_sheets(check_template)
        start, end = get_start_and_end_row_numbers(wb, sheet_names[0])
        assert start == 8
        assert end == 326

    def test_get_start_end_row_numbers_with_data(self, fixtures_folder, output_folder):
        excel_file = fixtures_folder / "check_registry.xls"

        xlsx_file = output_folder / f"{excel_file.stem}.xlsx"
        copy_xls_to_xlsx(excel_file, xlsx_file)
        wb, sheet_names =  get_wb_and_sheets(xlsx_file)
        start, end = get_start_and_end_row_numbers(wb, sheet_names[0])
        assert start == 8
        assert end == 33
        assert len(sheet_names) == 1



