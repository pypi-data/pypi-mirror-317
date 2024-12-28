import argparse
import os
import time
from hashlib import sha256
from wython.read import read_word_file
from wython.transform import transform_code
from wython.writein import wi


def main():
    parser = argparse.ArgumentParser(description='接受一个word文件路径并转换为绝对路径')
    parser.add_argument('file_path', type=str, help='输入的word文件路径')
    args = parser.parse_args()
    abs_path = os.path.abspath(args.file_path)
    return abs_path


def generate_pyfile(content, file_name):
    with open(f'{file_name}.py', 'w', encoding='utf-8') as f:
        f.write(wi + content)


def generate_py_filename():
    return f'w{sha256(str(time.time()).encode()).hexdigest()}'


if __name__ == '__main__':
    path_rec = main()
    if os.path.exists(path_rec) and path_rec.endswith('.docx'):
        f_n = generate_py_filename()
        text, image = read_word_file(path_rec, f_n)
        to_be_write = transform_code(text, image)
        generate_pyfile(to_be_write, f_n)
        exec(f'import {f_n}')
    else:
        print(f"can't open file {path_rec}: [Errno 2] No such file or directory")
