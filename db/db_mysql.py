from sqlalchemy import create_engine
from sqlalchemy import update, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


from .db_interface import DbInterface
from dto.file import FileData
from common.exceptions import NoFilenameInDb, FilenameAlreadyExists
from common.exceptions import ErrorNumLine, NoDateForUpdate
from .table_mysql import create_tables, delete_tables, LinesFilesTable, FilesTable
from config import get_settings
import tests.constants as c

settings = get_settings()


class DbMysql(DbInterface):
    def __init__(self, user, password, host, db_name) -> None:
        self.engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{db_name}')
        create_tables(self.engine)

    def seed(self):
        delete_tables(self.engine)
        create_tables(self.engine)
        self.create_file(c.file1)

    def read_line(self, filename: str, num_line: int):
        with Session(self.engine) as session:
            file = session.query(FilesTable).filter(FilesTable.name == filename).first()
            if not file:
                raise NoFilenameInDb(f'no {filename} in db')
            line = session.query(LinesFilesTable)\
                .filter(LinesFilesTable.file_id == file.id,
                        LinesFilesTable.key == num_line).first()
            if not line:
                raise ErrorNumLine(f'no {num_line} line in {filename}')
            result = line
        return result

    def read_file(self, filename: str):
        with Session(self.engine) as session:
            file = session.query(FilesTable).filter(FilesTable.name == filename).first()
            if not file:
                raise NoFilenameInDb(f'no {filename} in db')
            lines = session.query(LinesFilesTable).filter(LinesFilesTable.file_id == file.id).all()
            result = {'name': filename, 'data': lines}
        return result

    def read_files(self):
        result = dict()
        names = []
        with Session(self.engine) as session:
            files = session.query(FilesTable).all()
            for file in files:
                names.append(file.name)
        for name in names:
            file = self.read_file(name)
            result[name] = file
        return result

    def add_line(self, filename: str, line: str):
        result = None
        with Session(self.engine) as session:
            file = session.query(FilesTable).filter(FilesTable.name == filename).first()
            if not file:
                raise NoFilenameInDb(f'no {filename} in db')
            max_key = session.query(func.max(LinesFilesTable.key))\
                .filter(LinesFilesTable.file_id == file.id).scalar()
            new_key = max_key + 1 if max_key is not None else 0
            try:
                new_line = LinesFilesTable(key=new_key,
                                            file_id=file.id,
                                            line=line,)
                session.add(new_line)
                session.commit()
                result = new_line.key
            except SQLAlchemyError as e: # pragma: no cover
                session.rollback() # pragma: no cover
                raise e # pragma: no cover
        return result

    def create_file(self, file: FileData):
        with Session(self.engine) as session:
            record = session.query(FilesTable).filter(FilesTable.name == file.name).first()
            if record:
                raise FilenameAlreadyExists(f'{file.name} is already exists')
            new_file = FilesTable(name=file.name)
            file_id = None
            try:
                session.add(new_file)
                session.commit()
                file_id = new_file.id
            except SQLAlchemyError as e: # pragma: no cover
                session.rollback() # pragma: no cover
                raise e # pragma: no cover
        for i, line in enumerate(file.data):
            self.add_line(file.name, line)
        return file_id

    def update_line(self, filename: str, num_line: int, new_line: str):
        with Session(self.engine) as session:
            try:
                file = session.query(FilesTable).filter(FilesTable.name == filename).first()
                if not file:
                    raise NoFilenameInDb(f'no {filename} in db')
                line = session.query(LinesFilesTable)\
                    .filter(LinesFilesTable.key == num_line,
                            LinesFilesTable.file_id == file.id).first()
                if not line:
                    raise NoFilenameInDb(f'no {num_line} line in {filename}')
                updated_data = {
                    'line': new_line,
                }
                if line.line == new_line:
                    raise NoDateForUpdate
                update_query = update(LinesFilesTable)\
                    .where(LinesFilesTable.key == num_line,
                           LinesFilesTable.file_id == file.id)\
                    .values(**updated_data)
                session.execute(update_query)
                session.commit()
            except SQLAlchemyError as e: # pragma: no cover
                session.rollback() # pragma: no cover
                raise e # pragma: no cover

    def lock_line(self, filename: str, num_line: int):
        with Session(self.engine) as session:
            try:
                file = session.query(FilesTable).filter(FilesTable.name == filename).first()
                if not file:
                    raise NoFilenameInDb(f'no {filename} in db')
                line = session.query(LinesFilesTable)\
                    .filter(LinesFilesTable.key == num_line,
                            LinesFilesTable.file_id == file.id).first()
                if not line:
                    raise NoFilenameInDb(f'no {num_line} line in {filename}')
                if line.is_locked:
                    raise NoDateForUpdate
                line.is_locked = True
                session.commit()
            except SQLAlchemyError as e:
                session.rollback() # pragma: no cover
                raise e # pragma: no cover

    def unlock_line(self, filename: str, num_line: int):
        with Session(self.engine) as session:
            try:
                file = session.query(FilesTable).filter(FilesTable.name == filename).first()
                if not file:
                    raise NoFilenameInDb(f'no {filename} in db')
                line = session.query(LinesFilesTable)\
                    .filter(LinesFilesTable.key == num_line,
                            LinesFilesTable.file_id == file.id).first()
                if not line:
                    raise NoFilenameInDb(f'no {num_line} line in {filename}')

                if not line.is_locked:
                    raise NoDateForUpdate
                line.is_locked = False
                session.commit()
            except SQLAlchemyError as e: # pragma: no cover
                session.rollback() # pragma: no cover
                raise e # pragma: no cover

    def delete_line(self, filename: str, num_line: int):
        with Session(self.engine) as session:
            try:
                file = session.query(FilesTable).filter(FilesTable.name == filename).first()
                if not file:
                    raise NoFilenameInDb(f'no {filename} in db')
                line = session.query(LinesFilesTable)\
                    .filter(LinesFilesTable.key == num_line,
                            LinesFilesTable.file_id == file.id).first()
                if not line:
                    raise NoFilenameInDb(f'no {num_line} line in db')
                result = line
                session.delete(line)
                session.commit()
            except SQLAlchemyError as e: # pragma: no cover
                session.rollback() # pragma: no cover
                raise e # pragma: no cover
        return result

    def delete_file(self, filename: str):
        with Session(self.engine) as session:
            try:
                file = session.query(FilesTable).filter(FilesTable.name == filename).first()
                if not file:
                    raise NoFilenameInDb(f'no {filename} in db')
                session.query(LinesFilesTable).filter(LinesFilesTable.file_id == file.id).delete()
                session.commit()
                session.delete(file)
                session.commit()
            except SQLAlchemyError as e: # pragma: no cover
                session.rollback() # pragma: no cover
                raise e # pragma: no cover