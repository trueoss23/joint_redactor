from common.singleton import Singleton
from db.db_interface import DbInterface
from db.db_in_memory import DbInMemory
from common.db_type import DataBaseType
from config import get_settings


setting = get_settings()


def init_db():
    if setting.db_type == DataBaseType.MEM:
        database = DbInMemory()
    else:
        raise Exception('No db')
    return database


class DiContainer(Singleton):
    db: DbInterface = init_db()


di = DiContainer()


def get_di_container():
    global di
    return di
