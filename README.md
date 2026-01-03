# 📧 Gmail 일정 분석 AI 에이전트

Gmail에 수신된 이메일의 본문을 AI(Google Gemini)가 가져오는 파이썬 기반 AI 에이전트입니다. (향후 Google Calendar 등록 기능 추가 예정)

## ✨ 주요 기능

-   **자동 이메일 감지**: '약속', '예약' 등 특정 키워드가 포함된 읽지 않은 이메일을 자동으로 검색합니다.
-   **AI 기반 정보 추출**: Google Gemini API를 사용하여 이메일 본문을 가져옵니다. (향후 **일정 제목, 날짜, 시간, 장소** 추출하도록 업데이트 예정)
-   **간편한 실행**: 로컬 환경에서 간단한 설정만으로 바로 실행할 수 있습니다.

## ⚙️ 아키텍처

`새 이메일 도착` → `Python 스크립트 실행` → `Gmail API로 이메일 검색 및 본문 로드` → `Gemini API로 본문 분석 및 정보 추출` → `터미널에 결과 출력`

## 🛠️ 설치 및 사용법

### 1. 사전 준비 (최초 1회)

**1-1. Python 설치**
-   [python.org](https://www.python.org/) 에 접속하여 **Python 3.11 또는 3.12** 버전을 다운로드하여 설치합니다.
-   **(중요!)** 설치 첫 화면에서 **`Add Python to PATH`** 체크박스를 **반드시 체크**해 주세요.

**1-2. Google Cloud & API 설정**
-   **Gmail API**와 **Google Calendar API**를 사용할 수 있도록 [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트를 생성하고 각 API를 '사용 설정'해야 합니다.
-   [사용자 인증 정보 페이지](https://console.cloud.google.com/apis/credentials)에서 **'OAuth 2.0 클라이언트 ID'**를 생성합니다.
    -   **'애플리케이션 유형'**은 **'데스크톱 앱'**으로 선택합니다.
    -   생성이 완료되면 **JSON 다운로드(↓)** 아이콘을 클릭하여 파일을 다운로드하고, 파일 이름을 **`credentials.json`**으로 변경한 뒤, 이 프로젝트 폴더 안에 넣어주세요.
-   **Gemini API 키**를 [Google AI Studio](https://aistudio.google.com/)에서 발급받으세요.

### 2. 프로젝트 설정

**2-1. 프로젝트 파일 다운로드**
1. gmail-ai-agent.zip 파일을 다운로드합니다.
2. 다운로드한 ZIP 파일의 압축을 풉니다.

**2-2. 터미널 열기 및 폴더 이동**
1.  `Win` + `R` 키를 누르고 `cmd`를 입력하여 **명령 프롬프트(터미널)**를 엽니다.
2.  터미널에 `cd`를 입력하고 한 칸 띈 다음, 압축 푼 폴더의 경로를 복사하여 붙여넣습니다.
    ```bash
    # 예시: 다운로드 폴더에 압축을 푼 경우
    cd C:\Users\"YourName"\Downloads\gmail-ai-agent 
    ```

**2-3. 가상 환경 생성 및 활성화**
-   이 프로젝트만을 위한 격리된 파이썬 환경을 만듭니다.
    ```bash
    python -m venv venv
    ```
-   만들어진 가상 환경을 활성화합니다.
    ```bash
    venv\Scripts\activate
    ```
    (터미널 맨 앞에 `(venv)` 표시가 나타나면 성공입니다.)

**2-4. 필요 라이브러리 설치**
-   `requirements.txt` 파일을 사용하여 프로젝트에 필요한 모든 라이브러리를 자동으로 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```

**2-5. Gemini API 키 설정**
-   프로젝트 폴더에 `.env`라는 이름의 새 파일을 만듭니다.
-   파일을 열어 아래와 같이 발급받은 Gemini API 키를 입력하고 저장합니다. (이 파일은 `.gitignore`에 의해 깃허브에 올라가지 않습니다.)
    ```
    GEMINI_API_KEY='여기에_발급받은_API_키를_붙여넣으세요'
    ```
-   `main.py` 파일의 Gemini API 설정 부분을 아래와 같이 수정하여, `.env` 파일에서 키를 읽어오도록 변경합니다. (이 방식이 키를 직접 코드에 넣는 것보다 훨씬 안전합니다.)
    -   `pip install python-dotenv`로 라이브러리 설치가 필요합니다. (`requirements.txt`에 추가해두는 것이 좋습니다.)
    -   `main.py` 상단에 `from dotenv import load_dotenv` 추가
    -   `load_dotenv()` 호출
    -   `GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')`

### 3. 실행

**3-1. 테스트 이메일 보내기**
-   본인 Gmail 계정으로, **제목**에 '약속' 또는 '예약'이라는 단어를 포함하고 **본문**에 날짜, 시간, 장소 정보를 담은 이메일을 보냅니다.

**3-2. 프로그램 실행**
```bash
python main.py
```
-   **(최초 실행 시)** 웹 브라우저가 열리며 Google 계정 로그인을 요청합니다. 화면의 안내에 따라 계정을 선택하고 **'허용'** 버튼을 눌러 인증을 완료해 주세요.
-   인증이 완료되면, 터미널에 AI가 분석한 일정 정보가 출력됩니다.

## ⚠️ 주의사항
-   이 프로젝트는 학습 및 개인용으로 제작되었습니다.
-   `credentials.json`과 `.env` 파일은 민감한 정보를 담고 있으므로, 절대로 공개된 장소(특히 Public 깃허브 저장소)에 직접 업로드해서는 안 됩니다.
