from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def output_folder() -> Path:
    f = Path(__file__).parent.parent / "output"
    f.mkdir(parents=True, exist_ok=True)
    return f


@pytest.fixture(scope="session")
def fixtures_folder() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def small_box_xlsx_c1(fixtures_folder) -> Path:
    return fixtures_folder / "small_box_client1.xlsx"


@pytest.fixture(scope="session")
def sage_folder() -> Path:
    return Path.home() / "Downloads" / "sage"


@pytest.fixture(scope="session")
def mgi_template_folder(sage_folder) -> Path:
    return sage_folder / "mgi_templates"


@pytest.fixture(scope="session")
def check_template(mgi_template_folder) -> Path:
    return mgi_template_folder / "Registro de Cheques y Transferencias Bancarias Mensual.xlsx"


@pytest.fixture(scope="session")
def check_template_xls(mgi_template_folder) -> Path:
    return mgi_template_folder / "xls" / "Registro de Cheques y Transferencias Bancarias Mensual.xls"
