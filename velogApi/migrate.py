#!/usr/bin/env python3
"""
Velog GraphQL API 포스트 마이그레이션 스크립트
작성자: 벌컵 하온 자동화 개발 부장
목적: Velog API로부터 특정 사용자의 전체 블로그 게시글을 추출하여 마크다운(.md) 파일로 백업합니다.

[백엔드 아키텍처 학습 포인트]
1. GraphQL API 통신: REST와 달리 단일 엔드포인트(/graphql)에 POST 요청을 보내며, 필요한 필드만 쿼리(Query)로 정의하여 Over-fetching을 방지합니다.
2. Cursor 기반 페이지네이션 (Cursor Pagination): 
   - 전통적인 Offset 기반 페이징(Page, Size)은 데이터가 빈번히 추가/삭제될 때 중복 조회 또는 누락 문제가 발생하며, 대용량 데이터 조회 시 성능 저하(Offset이 커질수록 느려짐)가 발생합니다.
   - Cursor 기반 페이징은 마지막으로 조회한 데이터의 고유 식별자(ID 등)를 Cursor로 삼아 다음 데이터를 조회하므로 매우 안정적이고 빠릅니다.
3. 방어적 프로그래밍 (Defensive Programming):
   - 외부 네트워크 통신, 환경 변수 파일 탐색, 파일 시스템 I/O 등 에러 발생 확률이 높은 구간에 철저한 예외 처리(Try-Except)를 구현하여 비정상 종료를 방지합니다.
"""

import os
import re
import sys
import requests
from dotenv import load_dotenv
from datetime import datetime

# 1. 환경 변수 설정 파일 (.env) 로드
# 현재 스크립트가 실행되는 디렉토리 기준으로 .env 파일을 로드합니다.
# 이로써 민감한 토큰 정보가 코드에 하드코딩되는 것을 원천 차단합니다.
ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(ENV_PATH)

# ==========================================
# [설정 변수 정의]
# ==========================================
VELOG_API_URL = "https://v2.velog.io/graphql"
TARGET_USERNAME = "trendsetter"
SAVE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../00_Raw"))
VELOG_ACCESS_TOKEN = os.getenv("VELOG_ACCESS_TOKEN", "").strip()

# ==========================================
# [방어적 프로그래밍: 환경 및 파일 시스템 검증]
# ==========================================
try:
    # 저장 디렉토리가 없는 경우 자동 생성 (Spring의 mkdirs와 동일한 원리)
    if not os.path.exists(SAVE_DIR):
        print(f"[⚙️ 시스템] 저장 디렉토리({SAVE_DIR})가 존재하지 않아 자동 생성을 진행합니다.")
        os.makedirs(SAVE_DIR, exist_ok=True)
        print(f"[⚙️ 시스템] 디렉토리 생성 완료: {SAVE_DIR}")
except OSError as e:
    print(f"[❌ 파일 I/O 오류] 저장 디렉토리를 생성할 수 없습니다: {e}", file=sys.stderr)
    print("[⚙️ 시스템] 권한 부족 또는 잘못된 경로 설정으로 인해 마이그레이션이 안전하게 종료됩니다.", file=sys.stderr)
    sys.exit(1)

# ==========================================
# [유틸리티 함수: 파일명 안전 변환]
# ==========================================
def sanitize_filename(title: str) -> str:
    """
    OS 파일 시스템에서 에러를 유발하는 특수문자 및 공백을 정제합니다.
    - 대상 특수문자: \\ / : * ? " < > |
    - 위 문자는 정규표현식(re)을 사용해 언더바(_)로 치환됩니다.
    - 줄바꿈이나 여러 개의 공백도 단일 공백으로 치환합니다.
    """
    if not title:
        return "untitled"
    # 1. OS 제한 특수 문자 제거
    cleaned = re.sub(r'[\\/:*?"<>|]', "_", title)
    # 2. 줄바꿈 및 불필요한 연속 공백 정제
    cleaned = re.sub(r'\s+', " ", cleaned).strip()
    return cleaned

# ==========================================
# [핵심 로직: GraphQL API 호출 함수]
# ==========================================
def fetch_velog_posts(username: str, limit: int = 20, cursor: str = None) -> list:
    """
    Velog GraphQL API를 통해 포스트 목록을 조회합니다.
    
    [GraphQL Query 구조]
    - posts 쿼리에 username, limit, cursor 변수를 인자로 전달합니다.
    - 응답값으로 id, title, body, url_slug, released_at 정보를 정의하여 요청합니다.
    """
    query = """
    query Posts($username: String!, $limit: Int, $cursor: ID) {
      posts(username: $username, limit: $limit, cursor: $cursor) {
        id
        title
        body
        url_slug
        released_at
      }
    }
    """
    
    variables = {
        "username": username,
        "limit": limit,
        "cursor": cursor
    }
    
    # HTTP Request Headers 구성 (인증 토큰 유무 분기 처리)
    headers = {
        "Content-Type": "application/json",
    }
    
    # Velog API는 Authorization Header와 Cookie(access_token) 형식을 통해 인증을 인식합니다.
    # 토큰이 기입된 경우에만 안전하게 탑재하여 보냅니다.
    if VELOG_ACCESS_TOKEN:
        headers["Authorization"] = f"Bearer {VELOG_ACCESS_TOKEN}"
        headers["Cookie"] = f"access_token={VELOG_ACCESS_TOKEN}"
        
    try:
        # GraphQL은 항상 POST 메서드를 통해 JSON 바디에 query와 variables를 실어 보냅니다.
        response = requests.post(
            VELOG_API_URL, 
            json={"query": query, "variables": variables}, 
            headers=headers,
            timeout=15  # 네트워크 지연(Hang) 방지를 위한 타임아웃 15초 설정
        )
        
        # HTTP Status Code 검증 (2xx 성공 대역이 아닌 경우 예외 발생)
        response.raise_for_status()
        
        response_json = response.json()
        
        # GraphQL은 HTTP status가 200이더라도 내부 비즈니스 로직 에러(예: 쿼리 에러, 인자 형식 오류)가 
        # response body의 'errors' 필드에 담길 수 있으므로 이를 확인합니다.
        if "errors" in response_json:
            errors = response_json["errors"]
            print(f"[❌ GraphQL API 에러] 쿼리 실행 중 에러가 발생했습니다: {errors}", file=sys.stderr)
            return []
            
        return response_json.get("data", {}).get("posts", [])
        
    except requests.exceptions.Timeout:
        print("[❌ 네트워크 오류] Velog API 서버 응답 시간이 초과되었습니다 (Timeout).", file=sys.stderr)
        return []
    except requests.exceptions.ConnectionError:
        print("[❌ 네트워크 오류] Velog API 서버와의 인터넷 연결 상태를 확인해주십시오.", file=sys.stderr)
        return []
    except requests.exceptions.HTTPError as e:
        print(f"[❌ HTTP 오류] API 응답 에러 발생 (Status Code: {response.status_code}): {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"[❌ 예상치 못한 오류] API 조회 중 에러 발생: {e}", file=sys.stderr)
        return []

# ==========================================
# [핵심 로직: 마크다운 파일 저장 함수]
# ==========================================
def save_post_as_markdown(post: dict) -> bool:
    """
    단일 포스트 딕셔너리를 마크다운(.md) 형식의 파일로 저장합니다.
    
    [파일명 포맷] YYYY-MM-DD-제목.md
    - 작성일(released_at) 데이터 파싱 및 가공
    """
    title = post.get("title", "Untitled")
    body = post.get("body", "")
    released_at_raw = post.get("released_at", "")
    url_slug = post.get("url_slug", "")
    
    # 1. 날짜 데이터 정제 (ISO 8601 -> YYYY-MM-DD)
    # 예: '2023-10-24T12:34:56.789Z' -> '2023-10-24'
    date_prefix = "unknown-date"
    formatted_date_time = "unknown"
    if released_at_raw:
        try:
            # T 문자를 기준으로 스플릿하거나, datetime으로 정확하게 파싱
            dt = datetime.strptime(released_at_raw.split(".")[0].replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
            date_prefix = dt.strftime("%Y-%m-%d")
            formatted_date_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            # 파싱 실패 시 원본 문자열에서 날짜 패턴(YYYY-MM-DD)만 정규식으로 추출 시도
            match = re.match(r'(\d{4}-\d{2}-\d{2})', released_at_raw)
            if match:
                date_prefix = match.group(1)
                formatted_date_time = date_prefix
    
    # 2. 파일명 조합 및 특수문자 필터링
    safe_title = sanitize_filename(title)
    filename = f"{date_prefix}-{safe_title}.md"
    file_path = os.path.join(SAVE_DIR, filename)
    
    # 3. 마크다운 내용 구성 (YAML Front Matter 적용)
    # 블로그 게시글의 메타데이터를 표준 Front Matter 형식으로 포함하여 이식성을 높입니다.
    content = f"""---
title: "{title.replace('"', '\\"')}"
date: {formatted_date_time}
url_slug: "{url_slug}"
---

{body}
"""
    
    # 4. 파일 쓰기 실행 (I/O Exception 처리 포함)
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except IOError as e:
        print(f"[❌ 파일 쓰기 실패] 게시글 '{title}' 저장 중 I/O 에러 발생: {e}", file=sys.stderr)
        return False

# ==========================================
# [메인 실행 엔진 (Cursor Pagination Loop)]
# ==========================================
def main():
    print("==================================================")
    print("🚀 Velog 데이터 마이그레이션 작전 가동 (벌컵 하온 부장)")
    print(f"Target Username : {TARGET_USERNAME}")
    print(f"Save Path       : {SAVE_DIR}")
    print(f"Token Configured: {'YES' if VELOG_ACCESS_TOKEN else 'NO (공개 게시글만 수집)'}")
    print("==================================================")
    
    cursor = None
    total_processed = 0
    total_saved = 0
    page_count = 1
    
    # Cursor 기반 무한 루프 시작
    while True:
        print(f"[🔄 진행 중] {page_count}번째 페이지 호출 시도... (Cursor: {cursor})")
        
        # 1. API 호출
        posts = fetch_velog_posts(TARGET_USERNAME, limit=20, cursor=cursor)
        
        # 데이터가 아예 없는 경우 또는 에러로 빈 리스트가 리턴된 경우 루프 탈출
        if not posts:
            print(f"[📢 완료] 더 이상 조회할 포스트가 없거나 에러가 발생하여 조회를 종료합니다.")
            break
            
        print(f"[✅ 성공] {page_count}번째 페이지에서 {len(posts)}개의 포스트를 가져왔습니다.")
        
        # 2. 개별 포스트 마크다운 파일 저장 실행
        for post in posts:
            total_processed += 1
            if save_post_as_markdown(post):
                total_saved += 1
                
        # 3. 페이징 중단 조건 체크 (Velog API는 응답 크기가 limit 미만이면 마지막 페이지임)
        if len(posts) < 20:
            print("[📢 완료] 마지막 페이지에 도달했습니다.")
            break
            
        # 4. 다음 루프를 위한 Cursor 포인터 갱신
        # 이전 응답 데이터 리스트의 '가장 마지막(최신순 정렬 기준 과거글)' 게시글 ID를 커서로 설정합니다.
        cursor = posts[-1]["id"]
        page_count += 1
        
    print("==================================================")
    print("🎉 마이그레이션 수행 완료 보고서")
    print(f"총 조회된 게시글 수: {total_processed}개")
    print(f"성공적으로 저장됨 : {total_saved}개")
    print(f"저장 경로          : {SAVE_DIR}")
    print("==================================================")

if __name__ == "__main__":
    main()
