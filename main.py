import os
import json
from dotenv import load_dotenv
from google import genai  # 최신 google-genai 라이브러리
from notion_client import Client

# .env 파일 로드
load_dotenv()

# 1. API 클라이언트 설정
# 환경 변수에 GEMINI_API_KEY, NOTION_TOKEN, NOTION_DB_ID가 정확히 있어야 합니다.
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
notion = Client(auth=os.getenv("NOTION_TOKEN"))
db_id = os.getenv("NOTION_DB_ID")

def analyze_text_with_gemini(text):
    """
    제미나이를 이용해 텍스트를 분석하고 정형화된 JSON 데이터를 반환합니다.
    """
    # 확인된 가용 모델 중 가장 안정적인 모델 선택
    model_id = "gemini-flash-lite-latest"
    # model_id = "gemini-2.0-flash" 
    
    prompt = f"""
    당신은 IT 전문 큐레이터입니다. 다음 텍스트를 분석하여 JSON 형식으로만 답변하세요.
    반드시 순수한 JSON만 반환하고, ```json 과 같은 마크다운 형식을 포함하지 마세요.
    
    분석 항목:
    1. category: [AI, 개발, 비즈니스, 일반] 중 하나 선택
    2. tags: 관련 핵심 키워드 3개 (# 포함)
    3. summary: 전체 내용을 관통하는 1~2문장 요약
    4. glossary: 주요 용어 설명 (최대 2개, 'term'과 'definition' 키 포함)

    분석할 텍스트:
    {text}
    """
    
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        
        # JSON 문자열 정제 (마크다운 코드 블록 제거)
        raw_text = response.text.strip()
        clean_json = raw_text.replace("```json", "").replace("```", "").strip()
        
        return json.loads(clean_json)
    
    except Exception as e:
        print(f"❌ AI 분석 중 에러: {e}")
        return None

def save_to_notion(data):
    """
    분석된 데이터를 노션 데이터베이스 형식에 맞춰 저장합니다.
    """
    if not data:
        return

    # 용어 사전 데이터를 한 줄씩 포맷팅
    glossary_list = [f"📌 {g['term']}: {g['definition']}" for g in data['glossary']]
    glossary_final = "\n".join(glossary_list)
    
    try:
        notion.pages.create(
            parent={"database_id": db_id},
            properties={
                "이름": {"title": [{"text": {"content": data['summary']}}]},
                "카테고리": {"select": {"name": data['category']}},
                "태그": {"multi_select": [{"name": t} for t in data['tags']]},
                "용어 설명": {"rich_text": [{"text": {"content": glossary_final}}]}
            }
        )
        print("✅ 노션 데이터베이스 저장 성공!")
    except Exception as e:
        print(f"❌ 노션 저장 중 에러: {e}")
        print("팁: 노션 DB 열 이름이 '이름', '카테고리', '태그', '용어 설명'과 일치하는지 확인하세요.")

# 메인 실행부
if __name__ == "__main__":
    # 테스트용 데이터
    test_memo = """
    ChatGPT 접근성 확대와 광고 도입 배경. 
    AI 발전으로 누구나 개인용 슈퍼 어시스턴트를 가질 수 있는 시대에 도달. 
    AI 접근성의 차이에 따라 기회 확대 또는 격차 심화가 발생할 수 있음.
    """
    
    print("🤖 AI 분석 시작...")
    analyzed_data = analyze_text_with_gemini(test_memo)
    
    if analyzed_data:
        print("📊 분석 결과:", json.dumps(analyzed_data, indent=2, ensure_ascii=False))
        save_to_notion(analyzed_data)