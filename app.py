from flask import Flask, request, jsonify
from main import analyze_text_with_gemini, save_to_notion
import os

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json
    
    # 1. 슬랙 URL 검증 (Challenge 대응 핵심 로직)
    if data and "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # 2. 메시지 이벤트 처리
    if "event" in data:
        event = data["event"]
        # 봇이 보낸 메시지는 무시 (무한 루프 방지)
        if event.get("type") == "message" and not event.get("bot_id"):
            user_text = event.get("text")
            print(f"📩 슬랙 메시지 수신: {user_text}")
            
            # AI 분석 및 노션 저장 실행
            analyzed = analyze_text_with_gemini(user_text)
            if analyzed:
                save_to_notion(analyzed)
                
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=5000)