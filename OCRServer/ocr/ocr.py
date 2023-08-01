import easyocr

reader = easyocr.Reader(['ko', 'en'])
result = reader.readtext('img.jpg')

def do_ocr(image):
    pass