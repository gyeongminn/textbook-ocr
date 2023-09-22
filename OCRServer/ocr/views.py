from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from .ocr import do_ocr  # ocr.py에서 do_ocr 함수 import
from .gpt_api import gpt_sum, gpt_pro
import re
import json
import difflib

@csrf_exempt
def genQuiz(request):
    if request.method == 'POST':
        # POST 데이터를 JSON으로 파싱
        data = json.loads(request.body.decode('utf-8'))
        
        # gpt_pro 함수에 전달하고 결과를 받음
        result = gpt_pro(data['content'])
        
        # 결과를 JsonResponse로 반환
        response_data = {
            "quiz": result
        }
        return JsonResponse(response_data)
    else:
        # POST 요청이 아닐 경우의 처리 (예: 에러 메시지 반환)
        return JsonResponse({"error": "Only POST method is supported."})


@csrf_exempt
def imageToText(request):
    # 이미지로 불러오는데 실패할 경우, fail이라는 값을 가져오게 끔 기본값을 fail로 설정
    response_data = {
        'text': "fail",
        'title' : "fail",
        'summary' : "fail",
        'sum_result' : "fail"
    }
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        try:
            # 디렉토리에 book.jpg이름으로 저장
            with open('media/book.jpg', 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            print("image saved!")  # 저장 성공 로그 확인용

            # 이미지에서 추출한 텍스트 받아오기
            result = do_ocr('media/book.jpg')
            print("result = ", result)
            # get_sum에 요약할 내용 입력
            sum_result = gpt_sum(result)

            # 정규 표현식을 사용하여 제목과 요약 추출
            title_match = re.search(r'\[(.*?)\]', sum_result)
    
            # title 추출
            title = title_match.group(1) if title_match else ""
    
            # title 부분을 제거하고 나머지를 summary에 저장
            summary = re.sub(r'\[.*?\]', '', sum_result).strip()
    
            # 결과 출력
            print("Title:", title)
            print("Summary:", summary)
    
            # 분류 결과를 스마트폰으로 반환 (JSON 형태로 반환)
            response_data = {
                'text': result,
                'title' : title,
                'summary' : summary,
                'sum_result' : sum_result
            }
            
            return JsonResponse(response_data)
        
        except Exception as e:
            print(f"Error saving image: {e}")
            JsonResponse(response_data)

    # 이미지를 저장하지 못했다면 => 앞서 저장한 fail이 Json으로 반환될 것임
    return JsonResponse(response_data)


# ocr코드 완성 전 테스트용 api => 이미지를 전달받아 저장한후, 사전에 작성해둔 더미데이터로 gpt요약을 시도한다.
@csrf_exempt
def imageToTextTest(request):
    # 이미지로 불러오는데 실패할 경우, fail이라는 값을 가져오게 끔 기본값을 fail로 설정
    response_data = {
        'text': "fail",
        'title' : "fail",
        'summary' : "fail",
        'sum_result' : "fail"
    }
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        # 디렉토리에 book.jpg이름으로 저장
        with open('media/book.jpg', 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)
        print("image saved!(test)")  # 저장 성공 로그 확인용

        # get_sum에 요약할 내용 입력
        sum_result = gpt_sum("""
8장 알고리롬 설계 기법 이 장에서는 고급 알고리롬 설계 기법올 몇 가지 살펴마다 .
8.1절에서는 비트 연산을 이용하여 데이터지 효율적으로 처리하는 비트 병렬 알 고리증올 살펴분다.
반복문올 비트 연산으로 치환하는 방법올 주로 살펴보며, 그렇 게 함으로새 알고리증의 수행 시간올 크게 개선할 수 있다.
8.2절에서는 분할 상환 분석올 다루며, 이는 알고리증에서 일런의 연산을 수행하 논 데 드는 시간올 추정할 때 사용된다 .
이 기법올 이용하여 보다 작으면서 가장 가 까운 원소와 슬라이당 원도의 최솟값올 구하는 알고리증올 분석한다.
8.3절에서는 특정한 함수의 최솟값을 효율적으로 구하는 삼진 탄색과 몇 가지 다 른 기법올 살펴본다 .
8.1 비트 병렬 알고리좀 비트 병력 알고리롬 (bit-parallel algorithm) 은 어떤 수에 대한 비트 연산을 수행할 때, 그 수름 구성하고 있는 각 비트률 병렬적으로 처리할 수 있다는 사실에 입각한 알고리롬이다.
즉, 어떤 알고리증의 수행 과정올 비트 연산을 이용하여 효율적으로 구현할 수 있도록 표현한다면, 이는 효율적인 알고리롬올 설계하는 한 가지 방법이 된다.
8.1.1 해망 거리 길이가 같은 두 문자열 @와 b 사이의 해망 거리(Hamming distance) hammingta, b논 두 문자열이 일치하지 않는 위치의 개수이다.
예틀 들면 다음과 같다.
8.1 비트 병렬 알고리롬 133 
""",['비트 병렬 알고리롬', '해망 거리('])
        
        # 정규 표현식을 사용하여 제목과 요약 추출
        title_match = re.search(r'\[(.*?)\]', sum_result)

        # title 추출
        title = title_match.group(1) if title_match else ""

        # title 부분을 제거하고 나머지를 summary에 저장
        summary = re.sub(r'\[.*?\]', '', sum_result).strip()

        # 결과 출력
        print("Title:", title)
        print("Summary:", summary)

        # 분류 결과를 스마트폰으로 반환 (JSON 형태로 반환)
        response_data = {
            'text': "08008는 동시에 사용할 수 있는 사용자의 수에 따라 단일사용자 08545와 다중사용\n자 28045로 나눌 수 있다. 실제 <ㅠㄴ는 하나이지만 여러 사용자가 동시에 사용할 수 있\n: 는것은 다중 프로그래밍의 개념을 이용하기 때문이다. 예를 들어 은행 업무 시스템이\n. 항공기 예약 시스템 등은 여러 명의 사용자가 동시에 이용하게 되므로 다중사용자\n_ 08)45에 속하게 된다.\n\n： 로잔의 간섭으로 인해 일관성이 파괴될 수 있다. 이와 같이 상황이 발생되지 않도록\n: 드란잭션의 실행 순서를 제어할 필요가 있는데 이러한 기법을 통시성 제어(000010500/\n000008라고 한다. 동시성 제어는 다중사용자 08148에서는 매우 중요한 문제이다.\n\n. 2-1 트랜잭션에서의 연산\n\n동시성 제어를 위한 방법을 설명하기 위해서 우선 트랜잭션에서의 연산들을 정의한다.\n용자 관점에서 데이터베이스에 대한 연산은 대부분 901문을 사용하는데 50[을 실행\n하기 위해서는 내부적으로 데이터베이스에 대한 읽기와 쓰기 연산이 요구된다. 예를 들\n이 90Ｌ의 5860문은 읽기 연산을 필요로 하고 40000문은 읽기와 쓰기 연산을 필요로\n다. 이처럼 데이터베이스에서 실행되는 연산들은 다음과 같이 읽기 연산과 쓰기 연산\n으로 단순화하여 표현할 수 있다.\n\n。 ,=4460:이름이 ×인 데이터베이스 항목을 트랜잭션의 지역변수 <로 읽어 들인다.\n\n。 ㅠ00660:지역변수 ×에 저장된 값을 데이터베이스 항목 *에 저장한다.\n\n여기서 ×는 테이블, 레코드, 필드 등 데이터베이스를 구성하는 임의의 구성 요소가 될\n수 있다. 이때 뚜의했야 할 점은 01000 연산을 수행했을 때 그 결과가 디스크에 즉시\n저장될 수도 있고 그렇지 않을 수도 있는 점이다. 대부분의 21805에서는 주기억상치에\n버퍼0>4007)를 두고 디스크에 저장해야 할 데이터들을 일시적으로 보관하였나가 나중\n\n에 블록(11000) 단위로 기록한다.  ：\n\n196 15900( 4    녕 605 00 (\n「   \"   0 +\n\n^ 시 210  '거  !   라  여류\n생 ! 12  9 0후그라 |\n\n371\n",
            'title' : title,
            'summary' : summary,
            'sum_result' : sum_result
        }
        return JsonResponse(response_data)
    # 이미지를 저장하지 못했다면 => 앞서 저장한 fail이 Json으로 반환될 것임
    return JsonResponse(response_data)


# 유사도 가장 높은 번호 찾기
def closest_answer(answer, selections):
    max_ratio = -1
    index = -1
    
    for i, sel in enumerate(selections):
        s = difflib.SequenceMatcher(None, answer, sel)
        ratio = s.ratio()
        
        if ratio > max_ratio:
            max_ratio = ratio
            index = i + 1
            
    return str(index)


@csrf_exempt
def generateProblem(request):
    # 이미지로 불러오는데 실패할 경우, fail이라는 값을 가져오게 끔 기본값을 fail로 설정
    quiz = {
        "question": "[fail]",
        "selections": "[fail][fail][fail][fail]",
        "answer": "[fail]",
        "commentary" : "[fail]"
    }

    if request.method == 'POST':
        
        content = json.loads(request.body)
        print(f'content : {content}')
        problem_result = gpt_pro(content)

        # 각 질문을 분리하기 위한 패턴 (두 개 이상의 연속된 개행으로 분리)
        problems = re.split(r'\n{2,}', problem_result)
        ques, selec, ans, comment = "", "", "", ""

        for i, problem in enumerate(problems):
            print(f"problem #{i + 1} : {problem}")
            pattern = r'&([^&]+)&([\s\S]*?)%([^%]+)%([^@]+)@([\s\S]*)'
            match = re.search(pattern, problem)

            if match:
                question = match.group(1).strip()
                selections = [sel.strip() for sel in match.group(2).split('#') if sel.strip()]
                answer = match.group(3).strip()

                # answer가 숫자만 포함하고 있지 않으면 selections에서 해당 내용의 인덱스 찾기
                if not answer.isdigit():
                    answer = closest_answer(answer, selections)
                else:
                    answer = re.search(r'(\d+)', answer).group(1)

                commentary = match.group(5).replace('@', '').strip()
                ques += f"[{question}]"
                selec += "[" + "][".join(selections) + "]"
                ans += f"[{answer}]"
                comment += f"[{commentary}]"

        json_data = {
            "question": ques,
            "selections": selec,
            "answer": ans,
            "commentary": comment
        }

        print(json_data)
        return JsonResponse(json_data)

    return JsonResponse(quiz)
