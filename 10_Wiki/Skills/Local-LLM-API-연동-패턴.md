---
id: skill-local-llm-001
category: "[[10_Wiki/Skills]]"
confidence_score: 0.95
tags: [ollama, local-llm, api, gemma4, curl, openai-compatible]
last_reinforced: 2026-06-24
github_commit: ""
---

# [[Local LLM API 연동 패턴 (Ollama + OpenAI Compatible)]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> `http://localhost:11434/v1`은 OpenAI API와 호환되는 로컬 Ollama 엔드포인트이며, `curl` 하나로 프롬프트를 로컬 LLM에 투입하고 결과를 즉시 받아올 수 있다.

## 📖 구조화된 지식 (Synthesized Content)

### 환경 설정 (`antigravity.config.json`)
```json
{
  "models": {
    "local": {
      "provider": "openai-compatible",
      "baseUrl": "http://localhost:11434/v1",
      "model": "gemma4:e4b",
      "apiKey": "ollama",
      "temperature": 0.1,
      "maxTokens": 4096,
      "contextWindow": 128000
    }
  },
  "defaultModel": "local",
  "fallback": {
    "enabled": true,
    "model": "gemini-3-pro-preview",
    "trigger": "context_exceeded"
  }
}
```

### 현재 로드된 모델 목록 조회
```bash
curl -i http://localhost:11434/v1/models
```
- **확인된 모델**: `gemma4:e4b` (기본), `gemma:latest`, `gemma:2b`

### 프롬프트 투입 패턴 (Chat Completions)
```bash
curl -s -X POST http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma4:e4b",
    "messages": [
      {"role": "user", "content": "{{프롬프트}}"}
    ],
    "temperature": 0.1
  }'
```

### 복잡한 프롬프트 처리 패턴 (파일 분리)
긴 컨텍스트나 멀티라인 프롬프트의 경우, JSON 파일을 별도 생성 후 `@` 플래그로 전달한다.
```bash
# 1단계: 프롬프트 페이로드 파일 생성
cat > /tmp/prompt.json << 'EOF'
{ "model": "gemma4:e4b", "messages": [...] }
EOF

# 2단계: 파일로 요청 전송
curl -s -X POST http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d @/tmp/prompt.json
```

### 추출된 패턴
- **`@local` 키워드**: 대표님이 특정 프롬프트를 로컬 모델로 라우팅하고자 할 때 사용하는 규칙
- **백그라운드 실행**: `curl` 응답이 긴 경우(특히 추론 모드) 백그라운드 태스크로 처리 후 로그 파일 폴링
- **gemma4:e4b 특성**: `reasoning` 필드를 별도로 반환 (내부 사고 과정 공개)

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- 최초 테스트 시 모델 자기소개가 "Gemma 2"와 "Gemma 4" 두 가지로 달라진 케이스 발생 → 모델이 자신의 버전을 항상 정확히 인식하지는 않음 (hallucination 가능성 주의)

## 🔗 지식 연결 (Graph)
- **Parent:** [[10_Wiki/Skills]]
- **Related:** [[antigravity.config.json]], [[Local-LLM-글쓰기-스타일-분석-실험]]
- **Raw Source:** [[00_Raw]] (이 대화 세션 기반)
