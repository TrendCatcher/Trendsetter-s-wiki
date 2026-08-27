#!/usr/bin/env python3
"""
Velog 임시 글 추출 및 기발행 글 연계성 분석기
작성자: 벌컵 하온 자동화 개발 부장
"""

import os
import re
import sys
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(ENV_PATH, override=True)

VELOG_API_URL = "https://v2.velog.io/graphql"
TARGET_USERNAME = "trendsetter"
SAVE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../00_Raw"))
VELOG_ACCESS_TOKEN = os.getenv("VELOG_ACCESS_TOKEN", "").strip()

def fetch_posts(username: str, temp_only: bool = False, limit: int = 50) -> list:
    query = """
    query Posts($username: String, $limit: Int, $cursor: ID, $temp_only: Boolean) {
      posts(username: $username, limit: $limit, cursor: $cursor, temp_only: $temp_only) {
        id
        title
        body
        short_description
        thumbnail
        is_temp
        is_private
        url_slug
        likes
        comments_count
        created_at
        updated_at
        released_at
        tags
        series {
          id
          name
          url_slug
        }
      }
    }
    """
    
    headers = {
        "Content-Type": "application/json",
    }
    if VELOG_ACCESS_TOKEN:
        headers["Authorization"] = f"Bearer {VELOG_ACCESS_TOKEN}"
        headers["Cookie"] = f"access_token={VELOG_ACCESS_TOKEN}"
        
    all_posts = []
    cursor = None
    
    while True:
        variables = {
            "username": username,
            "limit": limit,
            "cursor": cursor,
            "temp_only": temp_only
        }
        try:
            res = requests.post(VELOG_API_URL, json={"query": query, "variables": variables}, headers=headers, timeout=15)
            res.raise_for_status()
            data = res.json()
            if "errors" in data:
                print(f"[Error in fetch_posts(temp_only={temp_only})]: {data['errors']}", file=sys.stderr)
                break
            posts = data.get("data", {}).get("posts") or []
            if not posts:
                break
            all_posts.extend(posts)
            if len(posts) < limit:
                break
            cursor = posts[-1]["id"]
        except Exception as e:
            print(f"[Exception in fetch_posts]: {e}", file=sys.stderr)
            break
            
    return all_posts

def main():
    if not VELOG_ACCESS_TOKEN:
        print("ERROR: VELOG_ACCESS_TOKEN_NOT_FOUND", file=sys.stderr)
        return

    print(f"[*] Access token found (length: {len(VELOG_ACCESS_TOKEN)})")
    print("[*] Fetching draft posts (temp_only=True)...")
    draft_posts = fetch_posts(TARGET_USERNAME, temp_only=True)
    print(f"[+] Retrieved {len(draft_posts)} draft posts.")

    print("[*] Fetching published posts (temp_only=False)...")
    published_posts = fetch_posts(TARGET_USERNAME, temp_only=False)
    print(f"[+] Retrieved {len(published_posts)} published posts.")

    output_data = {
        "drafts": draft_posts,
        "published": published_posts
    }
    
    out_file = os.path.join(os.path.dirname(__file__), "velog_posts_dump.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    print(f"[+] Successfully saved posts dump to {out_file}")

if __name__ == "__main__":
    main()
