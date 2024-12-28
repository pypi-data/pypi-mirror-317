wi = '''import os
from PIL import Image


os.remove(f'{__name__}.py')
temp_name = __name__
__name__ = '__main__'


class w_image():
    def __init__(self, img_name):
        Image.open(f'.\\\\{temp_name}\\\\{img_name}')


i_list = [file for file in os.listdir(f'.\\\\{temp_name}\\\\')]
i_list.sort()
w_image_list = [w_image(temp_name) for temp_name in i_list]

import shutil
shutil.rmtree(f'.\\\\{temp_name}\\\\')

class c_int():
    content: int

    def __init__(self, c_int_string: str):
        self.content = int(c_int_string[1:])
        if self.content > 2 ** 31 - 1:
            self.content = 2 ** 31
        if self.content < -2 ** 31:
            self.content = -2 ** 31

'''