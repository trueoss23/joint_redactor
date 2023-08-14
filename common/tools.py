from dto.file import LineFile


def get_list_line_from_file(file: str) -> list[LineFile]:
    split_list = file.split('\n')
    split_list = split_list[:-1]
    return [LineFile(line=elem) for elem in split_list]
