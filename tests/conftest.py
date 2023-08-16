import pytest

from di_container import di
from db.table_mysql import delete_tables, create_tables


@pytest.fixture(scope='function')
def db_mem():
    di.db.seed()
    yield di
    di.db.seed()


@pytest.fixture(scope='function')
def db_mysql():
    di.db.seed()
    yield di
    # di.db.seed()
