from PIL import ImageFont, ImageDraw, Image
from time import time
import matplotlib.pyplot as plt
import easyocr
import cv2

# Load easyocr reader 
reader = easyocr.Reader(['ko', 'en'], gpu=True)


def show_image(image):
    print('call show_image')
    
    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(image)
    plt.show()
    
    return


def detect_annotation_object(image):
    print('call detect_annotation_object')
    
    # Extract Red image
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (160, 200, 0), (179, 255, 255)) 
    red_image = cv2.bitwise_and(image, image, mask=mask)

    # Convert red image to gray image
    gray = cv2.cvtColor(red_image, cv2.COLOR_BGR2GRAY)

    # Dilation
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    dilate = cv2.morphologyEx(gray, cv2.MORPH_DILATE, k)

    # Connection
    _, src_bin = cv2.threshold(dilate, 0, 255, cv2.THRESH_OTSU)
    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(src_bin)

    # Get annotation data
    annotation_data = []
    for x, y, width, height, area in stats:
        if area > 100000: continue  # Remove Outliers
        annotation_data.append((x, y, width, height, area))
        
    return annotation_data


def draw_ocr_result(image, ocr_data, annotation_data):
    print('call draw_ocr_result')
    
    image = Image.fromarray(image)
    draw = ImageDraw.Draw(image)

    # Draw boxes from data
    for pos, string, score in ocr_data:
        draw.rectangle((*pos[0], *pos[2]), outline=(0, 255, 0), width=2)
    for x, y, width, height, area in annotation_data:
        draw.rectangle((x, y, x + width, y + height), outline=(255, 0, 0), width=3)

    return image


def detect_main_text_using_pitch(text_data):
    print("call detect_main_text_using_pitch")
    
    def get_y_pos(data):
        pos, string, score = data
        return pos[0][1], pos[2][1]

    # Calc pitchs from near object
    pitch = [0]
    for i in range(1, len(text_data)):
        cur_y1, cur_y2 = get_y_pos(text_data[i])
        
        prev_y1, prev_y2 = get_y_pos(text_data[i - 1])
        top_pitch = cur_y1 - prev_y2
        
        if (i == len(text_data) - 1):
            pitch.append(top_pitch)
            break
        
        next_y1, next_y2 = get_y_pos(text_data[i + 1])
        bottom_pitch = next_y1 - cur_y2 
        
        pitch.append(min(top_pitch, bottom_pitch))

    # Threshold = Mean. 
    # Assum main text's pitch is always less than mean pitch.
    threshold = sum(pitch) / len(pitch) 

    # Get main text data
    main_text_data = []
    for i in range(len(text_data)):
        if pitch[i] < threshold:
            main_text_data.append(text_data[i])

    return main_text_data

  
def do_ocr(image_path, pyramid_level=1, remove_text=(), debug=False):
    print("call do_ocr")
    
    total_time_start = time()
    
    # Load image
    image = cv2.imread(image_path)
    print("image roaded")
    
    # Resize image (Gaussian Filter)
    ocr_image = image[:]
    for _ in range(1, pyramid_level):
        ocr_image = cv2.pyrDown(ocr_image)
    
    # Read text
    ocr_time_start = time()
    text_data = reader.readtext(ocr_image)
    print(f'OCR Time : {time() - ocr_time_start:.2f}s')
    
    if len(text_data) == 0:
        print('OCR failed')
        return

    # Detect main text (Rule-Based Method) **This is not perfect yet**
    main_text_data = detect_main_text_using_pitch(text_data)

    # Detect annotation (Rule-Based Method)
    annotation_data = detect_annotation_object(image)
    
    # Get height of textbox
    height_mean = 0
    for pos, string, score in main_text_data:
        height_mean += pos[2][1] - pos[0][1]
    height_mean //= len(main_text_data)
    
    # Read text using annotation data
    ocr_time_start = time()
    for x, y, w, h, _ in annotation_data:
        anno_img = image[max(0, int(y - height_mean * 1.7)): y + h, x: x + w]
        anno_text = reader.readtext(anno_img)
        print(f'important word : {anno_text[0][1]}')
        if debug:
            show_image(anno_img)
    print(f'Annotation OCR Time : {time() - ocr_time_start:.2f}s')
    
    # Text post-processing
    text = ''
    for pos, string, score in main_text_data:
        for item in remove_text:
            if item in string:
                break
        else:
            text += string + ' '
    text = '.\n'.join(text.split('. '))

    if debug:
        show_image(draw_ocr_result(image, main_text_data, annotation_data))

    print(f'Total time : {time() - total_time_start:.2f}s')

    return text


# Example Code
image_path = '/Users/gyeongmin/Work/Github/DjangoServer/OCRServer/ocr/img.jpg'
result = do_ocr(
    image_path,
    pyramid_level=2,
    remove_text=('Competitive Programming',), 
    debug=False
)
print(result)