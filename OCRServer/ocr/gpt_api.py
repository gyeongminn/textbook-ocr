import openai
import time
import json
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured


# Load your API key from an environment variable or secret management service
BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = BASE_DIR / 'secrets.json'
with open(secret_file) as file:
    secrets = json.loads(file.read())

def get_secret(setting, secrets_dict=secrets):
    try:
        return secrets_dict[setting]
    except KeyError:
        error_msg = f'Set the {setting} environment variable'
        raise ImproperlyConfigured(error_msg)
    
openai.api_key = get_secret('GPT_SECRET_KEY')


# $데이터 베이스$, 줄여서 DB 특정 다수의 이용자들에게 필요한 정보를 제공한다든지 조직 내에서 필요로 하는 정보를 체계적으로 축적하여 그 조직 내의 이용자에게 필요한 정보를 제공하는 정보 서비스 기관의 심장부에 해당된다.
#    일반적으로 응용 프로그램과는 별개의 미들웨어[1]를 통해서 관리된다. 데이터베이스 자체만으로는 거의 아무 것도 못하기 때문에 그걸 관리하는 시스템과 통합돼 제공되며 따라서 정확한 명칭은 $데이터베이스 관리 시스템$(DBMS)[2]이 된다. 데이터베이스만 제공되는 건 CSV같이 아주 단순한 데이터에 국한되는데 이걸 직접 사용하는 경우는 많지 않고 이런 데이터를 RAW데이터로 간주해 다른 DBMS시스템에 적재하고 사용하는 게 일반적이다.
def gpt_sum(data):

        # 역할 부여
    messages = [
        {"role" : "system",
        "content" : """
        당신은 노트를 필기하는 학생입니다. 
        제공하는 글을 대상으로 제목을 포함하여 노트를 필기하세요. 
        요구사항은 아래와 같습니다. 
        1. 7줄 필기노트를 작성하세요. 
        2. 핵심 키워드 혹은 핵심 문장은 $사과$와 같이 $로 처음과 끝을 감싸서 제공합니다. 
        3. 노트의 제목은 []로 표현해야 하고, 마지막 문장을 제외한 각 문장의 끝은 \n\n으로 표기합니다.

        입력 예시 : 
        데이터베이스는 다양한 정보를 저장, 관리하고, 검색하는데 사용되는 중요한 시스템입니다. 이러한 데이터베이스를 효율적으로 설계하고 운영하기 위한 몇 가지 주요 개념들을 살펴보겠습니다.
        $정규화$는 데이터베이스 설계의 핵심 원칙 중 하나입니다. 이것은 데이터 중복을 최소화하고, 데이터의 무결성을 유지하는 설계 방법입니다. 정규화를 통해 여러 테이블에 중복으로 저장되는 정보를 줄이고, 데이터의 일관성을 확보할 수 있습니다.
        데이터베이스 내에서, $엔터티$는 정보의 기본 단위로서 흔히 테이블로 표현됩니다. 각 테이블은 그 자체로 하나의 엔터티를 나타냅니다. 테이블 간의 $관계$는 엔터티 간의 연결을 나타내며, $일대일, 일대다, 다대다$ 등의 관계 유형으로 표현됩니다.
        데이터를 빠르게 검색하기 위해 $인덱스$라는 구조를 사용합니다. 인덱스는 특정 테이블의 한 또는 여러 필드에 대해 생성될 수 있으며, 데이터의 검색 속도를 크게 향상시킬 수 있습니다.
        데이터베이스에서 $뷰$는 특정 목적을 위해 여러 테이블의 정보를 조합한 가상의 테이블을 의미합니다. 뷰는 실제 데이터를 저장하지 않지만, 사용자에게 필요한 정보를 제공하는데 유용하게 사용됩니다.
        마지막으로, $무결성$은 데이터베이스의 데이터가 정확하고 일관되게 유지되도록 하는 규칙입니다. 무결성은 주로 제약 조건을 통해 데이터베이스에 적용되며, 데이터의 품질과 신뢰도를 보장하는데 중요한 역할을 합니다.
        이렇게 데이터베이스 설계는 다양한 원칙과 규칙을 통해 정보를 체계적이고 효율적으로 관리할 수 있게 돕습니다.

        출력 예시 :
        [데이터베이스 설계]
        정규화 : 데이터 중복을 최소화하는 설계 방법\n\n
        엔터티 : 정보의 기본 단위, 테이블로 표현\n\n
        관계 : 테이블 간의 연결\n\n
        인덱스 : 데이터 검색 속도 향상을 위한 구조\n\n
        일대일, 일대다, 다대다 : 엔터티 간 관계 유형\n\n
        뷰 : 하나 이상의 테이블로부터 파생된 가상 테이블\n\n
        무결성 : 데이터의 정확성과 일관성을 유지하는 규칙

        위 출력 예시를 보면 \n\n으로 분리된 노트의 줄이 총 7줄임을 확인 할 수 있습니다. 위와 같이 7줄로 필기해주세요

        [노트 생성 요청]

        """},
    ]

    # user_content = input("user : ")
    messages.append({"role": "user", "content": f"{data}"})

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    result = completion.choices[0].message["content"].strip()

    print(f"GPT : {result}")
    return result



def gpt_pro(data):

    # 역할 부여
    messages = [
        {"role" : "system",
        "content" : """
            당신의 역할은 4지선다 객관식 문제를 4문제 만드는 것입니다.
            아래 규칙을 따라 문제를 만들어주세요.
            1. 입력으로 문자열이 주어집니다. 이 문자열을 대상으로 문제를 만들면 됩니다.
            2. 문제의 시작과 끝은 &로 감쌉니다. 예를 들어 &다음중 사과의 색이 아닌것을 고르시오& 와 같습니다.
            3. 객관식은 #으로 시작하여 #으로 끝납니다. 예를 들어 
            #빨간색# 
            #노란색# 
            #초록색# 
            #보라색#
            와 같습니다.
            4. 문제에 대한 정답을 제공해야합니다. 예를들어 위 문제의 경우 정답은 보라색이므로 정답번호인 4를 리턴합니다.
            정답은 *로 감싸서 제공합니다. *4*
            5. 문제에 대한 해설을 제공해야합니다. 해설은 1줄에서 2줄 사이로 제공합니다. 해설은 @로 감싸서 제공합니다.
            @사과는 빨간색,노란색,초록색 등의 색상을 갖는데 보락색은 존재하지 않으므로 정답은 4번입니다.@

            최종 예시를 제공합니다.
            입력 : 
            [사과]
            과일의 하나이다. 과육은 기본적으로 노란색에서 연두색[2]이며, 맛은 품종마다 다르다. 아래 사과 품종 문단을 참고하자.

            일반적으로 한국에서 말하는 사과 맛은 달콤새콤 + 아삭아삭하게 씹히는 탄력이 있고 단단한 과육의 식감을 말한다. 종마다 다르지만 잘 익은 사과는 껍질이 벗겨지지 않은 상태에서도 청량감이 있는 좋은 냄새가 아주좋게 난다.

            너무 오래 두면 수분과 펙틱화합물(pectic compounds)이 감소하면서 과실의 경도가 낮아져 모래처럼 푸석푸석 해지는데, '사과(沙果, 모래열매)'라는 이름은 여기에서 유래한다.

            나이드신 기성세대 일부는 간혹 사과를 두고 능금이라 부르기도 한다. 능금은 Malus asiatica를 말하기 때문에 사과의 근연종일 뿐 서로 다른 종이라 구별해야 한다. 그러나, 능금 농사 풍년을 기원드린다고 쓰는 어른들이 간간히 있다.
            사과는 빨간색,노란색,초록색 등의 색상을 갖는다.

            출력:
            &다음중 사과의 색이 아닌것을 고르시오&
            #빨간색# 
            #노란색# 
            #초록색# 
            #보라색#
            *4*
            @사과는 빨간색,노란색,초록색 등의 색상을 갖는데 보락색은 존재하지 않으므로 정답은 4번입니다.@

        """},
    ]

    # user_content = input("user : ")
    messages.append({"role": "user", "content": f"{data}"})

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)


    result = completion.choices[0].message["content"].strip()

    print(f"GPT : {result}")
    return result