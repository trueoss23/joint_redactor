from dto.file import FileData
from common.tools import get_list_line_from_file


tmp_lines = '123\n456\n'
lines1 = get_list_line_from_file(tmp_lines)
filename1 = 'file1'
file1 = FileData(name=filename1, data=lines1)
