# Textbook OCR
This is the OCR part of the 'SumNote' project submitted to the Hansung University Engineering Competitive Exhibition.

## Used Library
- Opencv
- EasyOCR

## Algorithm
- First, convert the given image to Gray-Scale.
- Apply Otsu's Threshold operation to binarize the image.
- Dilate the image, then use the Connected Component operation to separate the regions.
- Crop the image using each ROI.
- Apply OCR to obtain the main body text.
- Convert the given image to HSV, then detect the red areas.
- Crop the vicinity of the red regions, and apply OCR to extract important words.
- Combine the results.

# Poaster
![판넬](https://github.com/SumNote/.github/assets/98332877/0b2e4e5c-8cb5-4ceb-8d55-b7564c5fb81c)
