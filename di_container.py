from common.singleton import Singleton
from db.db_interface import DbInterface
# from db.db_in_memory import DbInMemory
from db.db_mysql import DbMysql
from common.db_type import DataBaseType
from config import get_settings


settings = get_settings()


def init_db():
    if settings.db_type == DataBaseType.MYSQL:
        database = DbMysql(
                        settings.db_user,
                        settings.db_password,
                        settings.db_host,
                        settings.db_name,)
    else:
        raise Exception('No db')
    return database


class DiContainer(Singleton):
    db: DbInterface = init_db()


di = DiContainer()


def get_di_container():
    global di
    return di
