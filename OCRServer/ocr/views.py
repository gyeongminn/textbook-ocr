from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from .ocr import do_ocr  # ocr.py에서 do_ocr 함수 import

@csrf_exempt
def imageToText(request):
    # 이미지로 불러오는데 실패할 경우, fail이라는 값을 가져오게 끔 기본값을 fail로 설정
    response_data = {
            'text': "fail",
        }
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        # 디렉토리에 book.jpg이름으로 저장
        with open('media/book.jpg', 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        print("image saved!")  # 저장 성공 로그 확인용

        # 이미지에서 추출한 텍스트 받아오기
        result = do_ocr('media/book.jpg')

        # 분류 결과를 스마트폰으로 반환 (JSON 형태로 반환)
        response_data = {
            'text': result,
        }
        return JsonResponse(response_data)
    # 이미지를 저장하지 못했다면 => 앞서 저장한 fail이 Json으로 반환될 것임
    return JsonResponse(response_data)