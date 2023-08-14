from dto.file import FileData
from common.tools import get_list_line_from_file


line1 = '123'
line2 = '456'
line3 = '789'

tmp_lines1 = f'{line1}\n{line2}\n'
lines1 = get_list_line_from_file(tmp_lines1)
filename1 = 'file1'
file1 = FileData(name=filename1, data=lines1)

tmp_lines2 = f'{line3}\n{line1}\n'
lines2 = get_list_line_from_file(tmp_lines2)
filename2 = 'file2'
file2 = FileData(name=filename2, data=lines2)

num_line1 = 0
num_line_not_exists = 3
