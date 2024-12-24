import cv2
import numpy as np
import pytesseract
import os

# 设置 Tesseract 的路径
if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
elif os.name == 'posix':  # Linux 或 macOS
    pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
def ocr2str(image_path):
    # 读取图像
    image = cv2.imread(image_path)

    # 将图像转换为灰度
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用 Tesseract 进行 OCR 识别
    text = pytesseract.image_to_string(gray_image)

    return text

def ocr2box(img):
    gray_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # 使用 Tesseract 进行 OCR 识别
    data = pytesseract.image_to_data(gray_image, output_type=pytesseract.Output.DICT)
    return data