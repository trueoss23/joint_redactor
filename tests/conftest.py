import pytest

from db.db_in_memory import DbInMemory
from di_container import di


@pytest.fixture(scope='function')
def db_mem():
    # di.db = DbInMemory()
    # print('??di', di.db)
    di.db.seed()
    print('??di', di.db)

    yield di
