import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 1. 권한을 '읽기 전용'으로 단순화합니다.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def main():
    """
    Gmail에 인증하고, 조건에 맞는 이메일의 본문을 가져와 출력합니다.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        # token.json이 낡았거나, 권한(SCOPES)이 변경되었을 경우 새로 로그인합니다.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=8080)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Gmail API 서비스에 연결합니다.
        gmail_service = build("gmail", "v1", credentials=creds)
        print("\n✅ Gmail 서비스에 성공적으로 연결되었습니다.")

        # 이메일을 검색합니다.
        query = "is:unread subject:(약속 OR 예약)"
        print(f"\n🔍 '{query}' 조건으로 이메일을 검색합니다...")
        results = gmail_service.users().messages().list(userId="me", q=query).execute()
        messages = results.get("messages", [])

        if not messages:
            print("  -> 해당하는 새 이메일이 없습니다.")
        else:
            print(f"  -> {len(messages)}개의 이메일을 찾았습니다!")
            for message_info in messages:
                # 전체 이메일 내용을 가져옵니다.
                msg = gmail_service.users().messages().get(userId="me", id=message_info['id'], format='full').execute()
                payload = msg['payload']
                headers = payload['headers']
                
                subject = next(header['value'] for header in headers if header['name'] == 'Subject')

                # 본문 내용을 파싱(해독)합니다.
                body = ""
                if 'parts' in payload:
                    parts = payload['parts']
                    data = parts[0]['body']['data']
                else:
                    data = payload['body']['data']
                
                body = base64.urlsafe_b64decode(data).decode('utf-8')

                # 최종 결과를 출력합니다.
                print("\n" + "="*40)
                print(f"  제목: {subject}")
                print("-"*40)
                print("  [ 이메일 본문 ]")
                print(body)
                print("="*40)

    except HttpError as error:
        print(f"API 호출 중 에러가 발생했습니다: {error}")

if __name__ == "__main__":
    main()
