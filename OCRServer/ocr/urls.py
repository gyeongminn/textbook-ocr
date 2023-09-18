from django.urls import path
from ocr.views import imageToText,imageToTextTest, generateProblem,genQuiz

urlpatterns = [
    # last : 127.0.0.1:8000/
    # + path
    # post방식으로 http-body의 이미지 내부에 저장
    path('image-to-text', imageToText, name='imageToText'),
    # 문제 생성
    path('gen-problem', generateProblem, name='generateProblem'),
    # 테스트용(안드로이드 스튜디오 카메라 화질 이슈)
    path('image-to-text-test',imageToTextTest,name='imageToTextTest'),
    # 문제 생성 테스트 - 최강
    path('gen-quiz',genQuiz,name='genQuiz')
]
