from sage_templater.plugins.file_classifiers.excel_classifier import convert_xls_to_xlsx, copy_xls_to_xlsx


class TestConvertXlsToXlsx:

    def test_convert_xls_to_xlsx(self, check_template_xls, output_folder):
        xlsx_file = output_folder / "Registro de Cheques y Transferencias Bancarias Mensual.xlsx"

        convert_xls_to_xlsx(check_template_xls, xlsx_file)
        assert xlsx_file.exists()
        assert xlsx_file.stat().st_size > 0
        # xlsx_file.unlink()
        # assert not xlsx_file.exists()

    def test_copy_xls_to_xlsx(self, check_template_xls, output_folder):
        xlsx_file = output_folder / "Registro de Cheques y Transferencias Bancarias Mensual.xlsx"
        copy_xls_to_xlsx(check_template_xls, xlsx_file)
