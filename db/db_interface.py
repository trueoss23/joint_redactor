from abc import ABC, abstractclassmethod
from dto.file import FileData


class DbInterface(ABC):
    @abstractclassmethod
    def seed(self):
        pass

    @abstractclassmethod
    def read_files(self):
        pass

    @abstractclassmethod
    def create_file(self, file: FileData):
        pass

    @abstractclassmethod
    def add_line(self, filename: str, line: str):
        pass

    @abstractclassmethod
    def read_line(self, filename: str, num_line: int):
        pass

    @abstractclassmethod
    def update_line(self, filename: str, num_line: int, new_line: str):
        pass

    @abstractclassmethod
    def delete_line(self, filename: str, num_line: int):
        pass

    @abstractclassmethod
    def delete_file(self, filename: str):
        pass
