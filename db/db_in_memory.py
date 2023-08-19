import copy
from datetime import datetime

from .db_interface import DbInterface
from dto.file import FileData, LineFile
from common.exceptions import NoFilenameInDb, FilenameAlreadyExists
from common.exceptions import ErrorNumLine, NoDateForUpdate
import tests.constants as c


class DbInMemory(DbInterface):
    def __init__(self) -> None:
        self.db = {}

    def seed(self):
        self.db = {}
        self.db[c.filename1] = copy.deepcopy(c.file1)

    def read_files(self):
        return list(self.db)

    def read_file(self, filename):
        if filename not in self.db:
            raise NoFilenameInDb(f'no {filename} in db')
        return self.db[filename]

    def create_file(self, file: FileData):
        if file.name in self.db:
            raise FilenameAlreadyExists(f'{file.name} is already exists')
        self.db[file.name] = file
        return file.name

    def read_line(self, filename: str, num_line: int):
        if filename not in self.db:
            raise NoFilenameInDb(f'no {filename} in db')
        if len(self.db[filename].data) < num_line:
            raise ErrorNumLine(f'no {num_line} line in {filename}')
        return self.db[filename].data[num_line]

    def add_line(self, filename: str, line: LineFile):
        if filename not in self.db:
            raise NoFilenameInDb(f'no {filename} in db')
        self.db[filename].data.append(line)
        return len(self.db[filename].data) - 1

    def update_line(self, filename: str, num_line: int, new_line: LineFile):
        if filename not in self.db:
            raise NoFilenameInDb(f'no {filename} in db')
        if len(self.db[filename].data) < num_line:
            raise ErrorNumLine(f'no {num_line} line in {filename}')
        if self.db[filename].data[num_line] == new_line:
            raise NoDateForUpdate
        self.db[filename].data[num_line] = new_line
        self.db[filename].data[num_line].released_at = datetime.now()

    def lock_line(self, filename: str, num_line: int):
        if filename not in self.db:
            raise NoFilenameInDb(f'no {filename} in db')
        if len(self.db[filename].data) < num_line:
            raise ErrorNumLine(f'no {num_line} line in {filename}')
        if self.db[filename].data[num_line].is_locked_by:
            raise NoDateForUpdate
        self.db[filename].data[num_line].is_locked_by = True
        self.db[filename].data[num_line].released_at = datetime.now()

    def unlock_line(self, filename: str, num_line: int):
        if filename not in self.db:
            raise NoFilenameInDb(f'no {filename} in db')
        if len(self.db[filename].data) < num_line:
            raise ErrorNumLine(f'no {num_line} line in {filename}')
        if not self.db[filename].data[num_line].is_locked_by:
            raise NoDateForUpdate
        self.db[filename].data[num_line].is_locked_by = True
        self.db[filename].data[num_line].released_at = datetime.now()

    def delete_line(self, filename: str, num_line: int):
        if filename not in self.db:
            raise NoFilenameInDb(f'no {filename} in db')
        if len(self.db[filename].data) < num_line:
            raise ErrorNumLine(f'no {num_line} line in {filename}')
        del self.db[filename].data[num_line]

    def delete_file(self, filename: str):
        try:
            del self.db[filename]
        except KeyError:
            raise NoFilenameInDb(f'no {filename} in db')
