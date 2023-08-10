from django.urls import path
from ocr.views import imageToText

urlpatterns = [
    # last : 127.0.0.1:8000/
    # + path
    # post방식으로 http-body의 이미지 내부에 저장
    path('image-to-text', imageToText, name='imageToText'),
]
