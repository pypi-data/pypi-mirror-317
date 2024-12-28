import zipfile
import os
from docx import Document
from io import BytesIO
from PIL import Image


def extract_images(docx_path, output_dir):
    with zipfile.ZipFile(docx_path, 'r') as docx:
        image_files = [file for file in docx.namelist() if file.startswith('word/media/')]

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for image_file in image_files:
            img_data = docx.read(image_file)
            image_stream = BytesIO(img_data)

            try:
                img = Image.open(image_stream)
                image_format = img.format.lower()

                image_name = os.path.basename(image_file)
                img_path = os.path.join(output_dir, image_name)
                img.save(img_path, format=image_format.upper())

            except Exception as e:
                pass


def read_word_docx(docx_path):
    result_text = ''
    result_image = []
    doc = Document(docx_path)

    # 遍历所有段落，寻找内嵌式图片
    for idx, paragraph in enumerate(doc.paragraphs):
        result_text += paragraph.text+'\n'

        char_count = 0  # 记录段落中字符的累计计数

        # 遍历段落中的每个 run（字符、文本或图片）
        for run_idx, run in enumerate(paragraph.runs):
            run_text_length = len(run.text)  # 获取当前run中的文本长度

            # 检查是否有嵌入的图形元素（图像）
            if 'graphic' in run._r.xml:
                result_image.append((idx+1,char_count+1,char_count + run_text_length))
            # 更新累计字符数
            char_count += run_text_length
    return result_text,result_image


def main():
    docx_path = "TST.docx"  # 替换为你的文件路径
    output_dir = "extracted_images"

    # 提取图片
    extract_images(docx_path, output_dir)

    # 阅读文档并检查图片位置
    read_word_docx(docx_path)



if __name__ == "__main__":
    main()

def read_word_file(file_path,path):
    extract_images(file_path, path)
    return read_word_docx(file_path)
