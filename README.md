# 🚀 Quick-Capture AI (QCA)
> **"슬랙 메시지 한 줄로 끝내는 AI 지식 큐레이션 자동화"**

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Notion](https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white)
![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)
![Render](https://img.shields.io/badge/Render-%2346E3B7.svg?style=for-the-badge&logo=render&logoColor=white)

일상 속에서 접하는 방대한 IT/금융 지식을 슬랙(Slack)을 통해 즉시 수집하고, **Gemini AI**를 활용해 분석 및 요약하여 **Notion 데이터베이스**에 체계적으로 저장하는 자동화 파이프라인입니다.

---

## 📌 개요 (Project Overview)
- **개발 기간**: 2026.01.10 ~ 2026.01.19
- **개발자**: **신은욱** (우리 FISA AI 엔지니어 부트캠프 6기)
- **주요 기술 스택**:
  - **Language**: `Python 3.11`
  - **Framework**: `Flask` (Server), `Gemini 2.0 Flash` (AI Analysis)
  - **Infrastructure**: `Render` (Cloud Deployment), `Slack Event API`
  - **Storage**: `Notion API` (Database)

---

## 🛠 주요 기능 (Key Features)
- **24/7 Cloud Service**: Render 클라우드 배포를 통해 로컬 PC 구동 없이 모바일 슬랙으로 언제 어디서든 사용 가능.
- **Real-time Event Listening**: Slack Event API를 통해 지정된 채널의 메시지를 실시간으로 감지.
- **AI-Powered Analysis (Gemini)**: 수집된 텍스트를 분석하여 아래 항목을 생성.
  - **Category**: AI, 개발, 비즈니스, 일반 중 자동 분류
  - **Tags**: 관련 핵심 키워드 3개 자동 생성 (# 포함)
  - **Summary**: 내용 전체를 관통하는 1~2문장 요약
  - **Glossary**: 주요 용어 정의 추출 (최대 2개)
- **Automated Archiving**: 분석된 정형 데이터를 Notion 데이터베이스 속성에 맞춰 자동으로 레코드 생성.

---

## 🏗 시스템 아키텍처 (System Architecture)



1. **User**: 슬랙 채널에 메모/지식 메시지 전송
2. **Slack Event API**: **Render Cloud**에 등록된 Webhook Endpoint로 JSON 데이터 전송
3. **Flask Server**: 데이터 수신 및 슬랙 `challenge` 파라미터 인증 처리
4. **Gemini API**: 프롬프트 엔지니어링을 통한 텍스트 구조화 및 분석
5. **Notion API**: 최종 분석 데이터를 노션 데이터베이스에 삽입

---

## 💻 실행 및 배포 (Deployment)

### 1. 환경 변수 설정
배포 환경(Render Settings > Environment)에 아래 정보를 입력해야 합니다.
- `GEMINI_API_KEY`, `NOTION_TOKEN`, `NOTION_DB_ID`

### 2. 클라우드 배포 설정 (Render)
- **Runtime**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

---

## 🔍 프로젝트 회고 (Retrospective)

### 💡 도전 과제 및 해결 (Troubleshooting)

#### 1. Slack API 'Challenge' 인증 처리
- **문제**: 슬랙 Event Subscriptions 설정 시 서버가 `challenge` 파라미터에 응답하지 않아 연결이 거부되는 현상 발생.
- **해결**: Flask 라우터 내에서 슬랙이 보낸 JSON 데이터의 `challenge` 키 존재 여부를 확인하고, 해당 값을 즉시 반환하는 로직을 최우선적으로 배치하여 인증 통과.

#### 2. Notion API 데이터 타입 및 필드 매핑
- **문제**: API 호출 시 노션 데이터베이스의 Property 이름(`이름`, `카테고리`, `태그`, `용어 설명`)과 Python 딕셔너리 키 값이 일치하지 않아 데이터 유실 및 400 에러 발생.
- **해결**: 노션 데이터베이스의 각 필드 유형(Title, Select, Multi-select, Rich Text)에 맞게 Python 데이터 구조를 정형화하고, 필드 이름을 코드와 1:1로 매칭하여 안정적인 데이터 적재 구현.

#### 3. 보안 환경 변수(.env) 노출 및 서버 배포 오류
- **문제**: 초기 Git 커밋 시 `.env` 파일을 `.gitignore`에 등록하지 않아 API 키와 토큰이 노출됨. 또한, 배포 환경에서 환경 변수 미설정으로 인한 서버 크래시 발생.
- **해결**: 
  - **보안 조치**: 즉시 `.gitignore` 적용 및 `git rm --cached .env`를 통해 노출된 파일 기록 제거. 
  - **배포 설정**: Render 대시보드의 `Environment Variables` 설정을 활용하여 서버 측에 환경 변수를 직접 주입함. 
  - **학습 포인트**: 민감한 정보는 소스코드와 철저히 분리해야 함을 깊이 체감하고 관리 프로세스를 확립함.

---

### 📈 향후 계획
- **금융 도메인 분석 고도화**: **우리 FISA 부트캠프** 학습 내용과 연계하여 금융 뉴스 특화 이상탐지(Anomaly Detection) 관련 프롬프트 강화.
- **URL 콘텐츠 분석 기능**: 메시지에 포함된 외부 링크(URL)의 내용을 크롤링하여 요약해주는 기능 추가 예정.

---

## 📄 License
This project is licensed under the **MIT License**.