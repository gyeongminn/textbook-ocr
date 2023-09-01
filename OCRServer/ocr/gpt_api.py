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

# 역할 부여
messages = [
    {"role" : "system",
      "content" : """
      역할 : 당신은 이제부터 노트를 필기하는 학생입니다. 내가 제공하는 교과서 한페이지 분량의 문장들을 보고 노트를 필기하면 만들어주면 됩니다.

규칙 : 당신은 아래와 같은 규칙을 따릅니다.
1. 핵심 키워드 또는 핵심 문장을 중점적으로 필기노트를 만듭니다. 핵심 키워드, 또는 문장들은 $ $로 구별됩니다. 
예시) 나는 $사과$를 먹는다. 사과는 맛있기 때문이다. 라는 문장에서의 키워드는 '사과'입니다.
2. 제목을 함께 만들어야 합니다. 제목은 [ ] 로 표현합니다.
예시) 
입력 : 나는 오늘 마트에서 쇼핑을 했다. $사과$를 먹고 싶었기 때문이다. 
출력 : [사과] 사과 : 빨간색 과일
3. 노트는 최소 6줄이상 8줄 이하로 만들어야합니다. 각 줄이 끝날때마다 //로 구별합니다.
4. 별다른 미사여구 없이 노트만 생성해야 합니다.

예시)
입력 : 
$데이터 베이스$, 줄여서 DB 특정 다수의 이용자들에게 필요한 정보를 제공한다든지 조직 내에서 필요로 하는 정보를 체계적으로 축적하여 그 조직 내의 이용자에게 필요한 정보를 제공하는 정보 서비스 기관의 심장부에 해당된다.
일반적으로 응용 프로그램과는 별개의 미들웨어[1]를 통해서 관리된다. 데이터베이스 자체만으로는 거의 아무 것도 못하기 때문에 그걸 관리하는 시스템과 통합돼 제공되며 따라서 정확한 명칭은 $데이터베이스 관리 시스템$(DBMS)[2]이 된다. 데이터베이스만 제공되는 건 CSV같이 아주 단순한 데이터에 국한되는데 이걸 직접 사용하는 경우는 많지 않고 이런 데이터를 RAW데이터로 간주해 다른 DBMS시스템에 적재하고 사용하는 게 일반적이다.

출력: 
[데이터베이스] //
* 데이터 베이스(DB) //
: 조직 내의 이용자에게 필요한 정보를 제공함 //
: 정보기관내의 심장부 역할//
* DBMS //
: 데이터 베이스 관리 시스템
: 데이터 베이스를 관리하는 프로그램 또는 시스템을 의미 //

위의 조건을 지키며 아래 글로 노트를 필기하세요.  지금부터는 별다른 말이 없이 글을 입력으로 보내면 규칙을 지켜 노트를 필기해야 합니다. 6줄 이상 9줄 이상으로 작성해야 한다는 규칙을 반드시 지켜야 합니다.

$데이터 베이스$, 줄여서 DB 특정 다수의 이용자들에게 필요한 정보를 제공한다든지 조직 내에서 필요로 하는 정보를 체계적으로 축적하여 그 조직 내의 이용자에게 필요한 정보를 제공하는 정보 서비스 기관의 심장부에 해당된다.
일반적으로 응용 프로그램과는 별개의 미들웨어[1]를 통해서 관리된다. 데이터베이스 자체만으로는 거의 아무 것도 못하기 때문에 그걸 관리하는 시스템과 통합돼 제공되며 따라서 정확한 명칭은 $데이터베이스 관리 시스템$(DBMS)[2]이 된다. 데이터베이스만 제공되는 건 CSV같이 아주 단순한 데이터에 국한되는데 이걸 직접 사용하는 경우는 많지 않고 이런 데이터를 RAW데이터로 간주해 다른 DBMS시스템에 적재하고 사용하는 게 일반적이다.
      """},
]



def gpt_sum(data):

    # user_content = input("user : ")
    messages.append({"role": "user", "content": f"{data}"})

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    result = completion.choices[0].message["content"].strip()

    print(f"GPT : {result}")
    return result


