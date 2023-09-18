from PIL import ImageFont, ImageDraw, Image
import matplotlib.pyplot as plt
import easyocr
import cv2

# 전역환경에서 로드 => 시간 단축용
reader = easyocr.Reader(['ko', 'en'], gpu=True)

def show_image(image):
    plt.figure(figsize=(30, 20))
    plt.axis('off')
    plt.imshow(image)
    plt.show()
    return


def detect_annotation_object(image):
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

def do_ocr(image_path):
    print("call do_ocr")
    image = cv2.imread(image_path)
    print("image roaded")
    # OCR
    
    text_data = reader.readtext(image)

    # Detect main text (Rule-Based Method) **This is not perfect yet**
    main_text_data = detect_main_text_using_pitch(text_data)

    # Detect annotation (Rule-Based Method)
    annotation_data = detect_annotation_object(image)
    
    text = ''
    for pos, string, score in main_text_data:
        if score < 0.2:
            continue
        text += string + ' '
    
    return text
