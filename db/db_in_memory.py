from .db_interface import DbInterface
from dto.file import FileData
from common.exceptions import NoFilenameInDb, FilenameAlreadyExists, ErrorNumLine
import tests.constants as c


class DbInMemory(DbInterface):
    def __init__(self) -> None:
        self.db = {}

    def seed(self):
        self.db = {}
        self.db[c.filename1] = c.file1

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

    def add_line(self, filename: str, line: str):
        if filename not in self.db:
            raise NoFilenameInDb(f'no {filename} in db')
        self.db[filename].data.append(line)

    def read_line(self, filename: str, num_line: int):
        if filename not in self.db:
            raise NoFilenameInDb(f'no {filename} in db')
        if len(self.db[filename].data) < num_line - 1:
            raise ErrorNumLine(f'no {num_line} line in {filename}')
        return self.db[filename][num_line]

    def update_line(self, filename: str, num_line: int, new_line: str):
        if filename not in self.db:
            raise NoFilenameInDb(f'no {filename} in db')
        if len(self.db[filename].data) < num_line - 1:
            raise ErrorNumLine(f'no {num_line} line in {filename}')
        self.db[filename][num_line] = new_line

    def delete_line(self, filename: str, num_line: int):
        if filename not in self.db:
            raise NoFilenameInDb(f'no {filename} in db')
        if len(self.db[filename].data) < num_line - 1:
            raise ErrorNumLine(f'no {num_line} line in {filename}')
        del self.db[filename][num_line]

    def delete_file(self, filename: str):
        try:
            del self.db[filename]
        except KeyError:
            raise NoFilenameInDb(f'no {filename} in db')
