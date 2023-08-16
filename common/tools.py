
def get_list_line_from_file(file: str) -> list[str]:
    split_list = file.split('\n')
    split_list = split_list[:-1]
    return split_list


def get_dict_lines_from_file(file: str) -> dict:
    split_list = file.split('\n')
    split_list = split_list[:-1]
    return {i: LineFile(line=elem) for i, elem in enumerate(split_list)}
