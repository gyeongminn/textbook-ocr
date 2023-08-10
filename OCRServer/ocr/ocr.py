# import easyocr

# reader = easyocr.Reader(['ko', 'en'])
# result = reader.readtext('img.jpg')


# brew install tesseract
# brew install tesseract-lang
# pip install pytesseract

import pytesseract as pt
from PIL import Image


def do_ocr(image):
    image = Image.open('media/book.jpg')
    text = pt.image_to_string(image, lang='kor')
    return text