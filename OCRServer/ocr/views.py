from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from .ocr import do_ocr  # ocr.py에서 do_ocr 함수 import
from .gpt_api import gpt_sum, gpt_pro
import re
import json

# 문제 생성 테스트
# @csrf_exempt
# def genQuiz(request):
#     # 이곳에 문제 생성을 희망하는 요약 노트 작성
#     result = gpt_pro("""
#     [데이터베이스의 정규화]
#         #1 제1정규형 : 각 행의 값이 원자 값이어야 하며, 중복된 행이 없어야 한다.
#         #2 제2정규형 : 제1정규형을 만족하고, 부분 함수 종속을 제거해야 한다.
#         #3 제3정규형 : 제2정규형을 만족하고, 이행성 종속을 제거해야 한다.
#         #4 BCNF : 제3정규형을 만족하고, 모든 결정자가 후보 키가 되어야 한다.
#     """)
#     # 생성한 문제 리턴
#     response_data = {
#         "quiz" : result
#     }
#     return JsonResponse(response_data)

@csrf_exempt
def genQuiz(request):
    if request.method == 'POST':
        # POST 데이터를 JSON으로 파싱
        data = json.loads(request.body.decode('utf-8'))
        
        # gpt_pro 함수에 전달하고 결과를 받음
        # 여기서 가정은 data에 "content"라는 키가 있고 그 값이 gpt_pro에 전달될 문자열이라는 것입니다.
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
    }
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']

        try:

            # 디렉토리에 book.jpg이름으로 저장
            with open('media/book.jpg', 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            print("image saved!")  # 저장 성공 로그 확인용

            # get_sum에 요약할 내용 입력
            sum_result = gpt_sum("""
            술이 없는(없었던) 문화권은 찾아보기 힘들다. 또한 지역과 문화의 특색에 따라 많고 많은 종류의 술이 존재한다. 그만큼 술은 인간의 문화와 밀접하게 엮여 있는 물건이다.

'술'이라는 낱말의 $어원$은 삼국시대부터 나타난다. 삼국사기〈지리지〉에서는 압록강 이북의 '풍부성(豐夫城)'이라는 고장이 원래 고구려의 소파홀(肖巴忽)이었다고 기록하고 있는데, 豐은 '술잔 받침'이라는 뜻도 있으므로 '소파(肖巴)'가 '술'의 고구려 어형이었음을 추정해볼 수 있다. 신라의 17관등 중 제일 높은 이벌찬은 '서발한(舒發翰)' 혹은 '서불한(舒弗邯)'이라고도 불렸는데, 이를 신라시대 때 훈차하여 '주다(酒多)'라고도 했다는 기록이 남아있다. '多'는 '많다'의 옛말 '하다'의 어간을 빌려 '한'~'간'을 표기한 것으로 보이므로, 술을 뜻하는 酒가 신라어 '서발' 혹은 '서불'에 대응됨을 알 수 있다.
            """)

            # 이미지에서 추출한 텍스트 받아오기
            result = do_ocr('media/book.jpg')

            # 분류 결과를 스마트폰으로 반환 (JSON 형태로 반환)
            response_data = {
                'text': result,
                'sum_result' : sum_result,
            }
            return JsonResponse(response_data)
        
        except Exception as e:
            print(f"Error saving image: {e}")
            JsonResponse(response_data)

    # 이미지를 저장하지 못했다면 => 앞서 저장한 fail이 Json으로 반환될 것임
    return JsonResponse(response_data)


@csrf_exempt
def imageToTextTest(request):
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
        print("image saved!(test)")  # 저장 성공 로그 확인용

        # get_sum에 요약할 내용 입력
        sum_result = gpt_sum("""
자동차(自動車, automobile) 또는 간단히 차(車, car)는 원동기의 힘을 통해 차체의 바퀴를 노면과 마찰시켜 그 반작용으로 움직이는 $교통 수단$을 말한다. 자동차는 20세기 이후 인류의 가장 보편적인 교통 수단이 되었으며, 다양한 과학 기술과 목적이 모여 만들어져 현대 문명에 빠질 수 없는 것 중 하나다. 현대의 자동차는 휘발유, 경유, 가스, 전기, 수소 등을 연료로 움직인다.
본래 원동기의 동력을 이용하는 탈것은 사전적인 의미의 자동차에 속한다. 대한민국 법령에서는 원동기장치자전거[2], 전기자전거나 전동휠체어 등은 제외한 자동차관리법 제3조와 대통령령으로 규정하는 탈것을 자동차라고 한다. 군용차의 경우 기술적 제원으로는 군용무기로 간주해 자동차관리법의 적용대상은 아니지만, 공도상에서는 장갑차, 표준차량, 민수차량 모두 도로교통법상의 자동차로 인정한다는 대법원 판례(94도1519)가 있다.
            """)
        
#         sum_result = gpt_sum("""
# 1. 개요[편집]
# 자동차(自動車, automobile) 또는 간단히 차(車, car)는 원동기의 힘을 통해 차체의 바퀴를 노면과 마찰시켜 그 반작용으로 움직이는 교통 수단을 말한다. 자동차는 20세기 이후 인류의 가장 보편적인 교통 수단이 되었으며, 다양한 과학 기술과 목적이 모여 만들어져 현대 문명에 빠질 수 없는 것 중 하나다. 현대의 자동차는 휘발유, 경유, 가스, 전기, 수소 등을 연료로 움직인다.
# 2. 정의[편집]
# 본래 원동기의 동력을 이용하는 탈것은 사전적인 의미의 자동차에 속한다. 대한민국 법령에서는 원동기장치자전거[2], 전기자전거나 전동휠체어 등은 제외한 자동차관리법 제3조와 대통령령으로 규정하는 탈것을 자동차라고 한다. 군용차의 경우 기술적 제원으로는 군용무기로 간주해 자동차관리법의 적용대상은 아니지만, 공도상에서는 장갑차, 표준차량, 민수차량 모두 도로교통법상의 자동차로 인정한다는 대법원 판례(94도1519)가 있다.
# """)
        
#         sum_result = gpt_sum("""
#             술이 없는(없었던) 문화권은 찾아보기 힘들다. 또한 지역과 문화의 특색에 따라 많고 많은 종류의 술이 존재한다. 그만큼 술은 인간의 문화와 밀접하게 엮여 있는 물건이다.

# '술'이라는 낱말의 $어원$은 삼국시대부터 나타난다. 삼국사기〈지리지〉에서는 압록강 이북의 '풍부성(豐夫城)'이라는 고장이 원래 고구려의 소파홀(肖巴忽)이었다고 기록하고 있는데, 豐은 '술잔 받침'이라는 뜻도 있으므로 '소파(肖巴)'가 '술'의 고구려 어형이었음을 추정해볼 수 있다. 신라의 17관등 중 제일 높은 이벌찬은 '서발한(舒發翰)' 혹은 '서불한(舒弗邯)'이라고도 불렸는데, 이를 신라시대 때 훈차하여 '주다(酒多)'라고도 했다는 기록이 남아있다. '多'는 '많다'의 옛말 '하다'의 어간을 빌려 '한'~'간'을 표기한 것으로 보이므로, 술을 뜻하는 酒가 신라어 '서발' 혹은 '서불'에 대응됨을 알 수 있다.
#             """)

#         sum_result = gpt_sum("""

# 3 .알고리즘 설계와 구현
#         알고리즘 설계
#         ［그림 1-3 에서 본 바와 같이 컴퓨터 비전을 응용할 수 있는 분야는 무척 다양하며, 시스템이 동
#         작하는 환경과 제약 조건에 따라 변화의 폭도 크다. 주어진 문제를 정확히 이해한 후 그 문제에 적
#         합한 알고리즘을 새로 개발하거나 기존 알고리즘 중에서 그 문제에 가장 우수한 성능을 보이는 것
#         을 선택하는 일은 아주 중요하다.
#         컴퓨터 비전의 처리 절차는 ［그림 1-6 에서 본 바와 같이 여러 단계를 거친다. 각각의 단계는 여
#         러 세부 문제로 구성되며, 이들 문제를 푸는 많은 종류의 알고리즘이 개발되어 있다. 사람의 손동
#         작을 인식하는 문제를 생각해 보자. 손을 찾아내는 단계에서는 손 모델을 이용하여 매칭 연산을 한
#         다. 에지나 영역을 사용해 연산하거나 SIFT와 같은 지역 특징을 사용할 수도 있다. 영역을 사용하
#         기로 결정했다면, 여러 영역 분할 알고리즘 중에 어떤 것을 사용할지 결정해야 한다. 이러한 방법
#         론적 다양성은 무엇을 뜻할까? 바로, 자신의 문제에 가장 적합한 알고리즘을 선별하는 작업이 어
#         려울 뿐 아니라 아주 중요하다는 점이다.
#         좋은 알고리즘을 찾기 위한 가장 확실하고 널리 사용하는 방법은 데이터베이스를 이용하여 실제
#         성능 실험을 수행하고, 그 결과에 따라 알고리즘을 선택하는 것이다. 보통 적절한 알고리즘을 찾
#         을 때까지 다양한 알고리즘을 적용해 보는 휴리스틱heuristic한 방식을 사용한다. 이때 주어진 문제
#         에 대한 통찰력과 공학적인 경험을 갖추고 있다면 시행착오를 줄일 수 있다. 이 책은 이러한 능력
#         을 갖추는 데 좋은 길잡이 노릇을 해 줄 것이다. 이 책은 주제별로 대표적인 알고리즘을 제시하는
#         데, 그것들의 기본 원리를 대비시켜 좀더 깊이 이해할 수 있도록 도울 것이며 실제 응용과 관련 지
#         어 장단점을 비교해 실용 시스템을 구축하는 데 필요한 통찰력을 길러줄 것이다.
#         좋은 알고리즘을 선별하는 데 크게 도움이 되는 길잡이가 또 있다. 요즘 두드러진 연구 방향 중
#         하나로, 표준 데이터베이스와 표준 성능 지표를 이용하여 여러 알고리즘의 성능을 객관적으로 비
#         교 분석하는 일이다. 컴퓨터 비전에 관련된 학술대회나 학술지에는 이러한 연구 결과를 담은 논문
#         이 많다. 알고리즘을 선별할 때 이들이 제시한 성능 비교 결과를 참조하는 것은 매우 현명한 자세
#         이다. 예를 들어, 지역 특징을 비교한 Schmid2000, Mikolajczyk2005a, Mikolajczyk2005bL
#         영 역 분할 알고리즘을 비교한 Estrada200이 등이 있다.

# """)

        # # 정규 표현식을 사용하여 제목과 요약 추출
        # title_match = re.search(r'\[(.*?)\]', sum_result)
        

        # # title과 summary 추출
        # title = title_match.group(1) if title_match else ""
        
        # # 제목을 제외한 나머지 줄을 summary에 저장
        # lines = sum_result.split('\n')
        # summary = '\n'.join(lines[1:]) if len(lines) > 1 else ""

        # # 결과 출력
        # print("Title:", title)
        # print("Summary:", summary)

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


@csrf_exempt
def generateProblem(request):
    # 이미지로 불러오는데 실패할 경우, fail이라는 값을 가져오게 끔 기본값을 fail로 설정
    quiz = {
            'text': "fail",
    }

    if request.method == 'POST':
        
        content = json.loads(request.body)
        
        print(f'content : {content}')

        # get_pro 에 해당 요약된 노트 내용 전달
        problem_result = gpt_pro(content)

        # 정규 표현식을 사용하여 문자열을 파싱
        query_match = re.search(r'&(.+)&', problem_result)
        answer_list_matches = re.findall(r'#(.+?)#', problem_result)
        answer_num_match = re.search(r'\*(.*?)\*', problem_result)
        commentary_match = re.findall(r'@(.*?)@', problem_result)

        # query, answerList, answerNum 추출
        question = query_match.group(1) if query_match else ""
        selections = answer_list_matches if answer_list_matches else []
        answer = answer_num_match.group(1) if answer_num_match else ""
        commentary = [match.strip() for match in commentary_match]
        
        # 결과를 []로 감싸기
        question = f"[{question}]"
        selections = "[" + "][".join(selections) + "]"
        answer = f"[{answer}]"
        commentary = "[" + "][".join(commentary) + "]"

        # 분류 결과를 스마트폰으로 반환 (JSON 형태로 반환)
        # Quiz 객체 생성
        quiz = {
            "question": question,
            "selections": selections,
            "answer": answer,
            "commentary" : commentary
        }

        # Quiz 객체를 출력
        print(quiz)
        
        return JsonResponse(quiz)
    # 이미지를 저장하지 못했다면 => 앞서 저장한 fail이 Json으로 반환될 것임
    return JsonResponse(quiz)