---
name: morning-briefing
description: "Zero-to-hero: install Hermes Agent, connect Slack/Gmail/Calendar/Notion, set up daily morning briefing (email + calendar) and on-demand meeting note summaries."
version: 2.1.0
author: community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Gmail, Calendar, Notion, Slack, Cron, Digest, Productivity, OAuth, Morning-Briefing, Setup, Install]
    related_skills: [google-workspace, notion, hermes-agent]
---

# Morning Briefing

Hermes Agent를 처음부터 설치하고, Gmail + Google Calendar + Notion + Slack을 연동하여 매일 아침 자동 브리핑을 받는 완전한 셋업 가이드.

## 최종 결과물

- 매일 아침 10시, Hermes Agent가 Gmail 이메일 요약 + 오늘의 캘린더 일정을 Slack으로 전달
- Slack에서 요청하면 Notion 회의록의 액션 아이템을 즉시 정리

```
Gmail API ─────┐
Calendar API ──┼──▶ Hermes Agent Gateway ──▶ Slack 채널/DM
Notion API ────┘     (cron + skills)
```

## 사전 준비

- Python 3.10+ 설치됨
- Google 계정 (Gmail)
- Notion 계정
- Slack 워크스페이스 (앱 설치 권한)
- Anthropic API 키 (https://console.anthropic.com)

---

## Phase 0: Hermes Agent 설치

### Linux / macOS / WSL2

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc
```

### Windows (PowerShell)

```powershell
iex (irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1)
```

인스톨러가 uv, Python, Node.js, ripgrep, ffmpeg, Git Bash를 자동 설치합니다.

### 설치 확인

```bash
hermes --version
hermes doctor        # 상태 점검
```

---

## Phase 1: Anthropic API 키 설정

```bash
hermes setup         # 대화형 설정 위자드
```

또는 수동으로 `~/.hermes/.env`를 생성:

```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

`~/.hermes/config.yaml`에서 모델 설정:

```yaml
model:
  default: "anthropic/claude-sonnet-4"    # 또는 claude-opus-4
  provider: "anthropic"
```

테스트:

```bash
hermes chat -q "안녕하세요, 테스트입니다"
```

---

## Phase 2: Slack 앱 생성 및 연동

### Step 1. Slack 앱 생성

1. https://api.slack.com/apps 접속
2. **Create New App** → **From scratch**
3. 앱 이름: `Manus` (또는 원하는 이름), 워크스페이스 선택

### Step 2. Bot Token Scopes 설정

**OAuth & Permissions** 페이지에서 Bot Token Scopes 추가:

| Scope | 용도 |
|-------|------|
| `chat:write` | 메시지 전송 |
| `channels:read` | 채널 목록 읽기 |
| `channels:history` | 채널 메시지 읽기 |
| `groups:read` | 비공개 채널 읽기 |
| `groups:history` | 비공개 채널 메시지 읽기 |
| `im:read` | DM 읽기 |
| `im:history` | DM 메시지 읽기 |
| `im:write` | DM 전송 |
| `users:read` | 사용자 정보 읽기 |
| `files:read` | 파일 읽기 |
| `files:write` | 파일 업로드 |
| `reactions:read` | 리액션 읽기 |
| `reactions:write` | 리액션 추가 |

### Step 3. Socket Mode 활성화

1. **Settings > Socket Mode** → Enable Socket Mode
2. App-Level Token 생성: 이름 `hermes-socket`, scope `connections:write`
3. 생성된 `xapp-` 토큰 복사

### Step 4. Event Subscriptions 설정

**Event Subscriptions** → Enable Events → Subscribe to bot events:

- `message.channels`
- `message.groups`
- `message.im`
- `app_mention`

### Step 5. 앱 설치

**Install App** → **Install to Workspace** → 권한 허용
`xoxb-` 로 시작하는 Bot User OAuth Token 복사

### Step 6. Hermes에 토큰 등록

`~/.hermes/.env`에 추가:

```env
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-level-token
```

### Step 7. Gateway 시작 및 테스트

```bash
hermes gateway run
```

Windows에서 자동 시작 (스케줄러):

```powershell
# Gateway 시작 스크립트 생성 후 작업 스케줄러에 등록
hermes gateway start
```

Slack에서 봇에게 DM으로 "안녕" 전송 → 응답 확인

---

## Phase 3: Google Workspace (Gmail + Calendar) 연동

### Step 1. Google Cloud 프로젝트 설정

1. https://console.cloud.google.com 접속
2. 새 프로젝트 생성 (예: `hermes-agent`)
3. **API 및 서비스 > 라이브러리**에서:
   - `Gmail API` 검색 → **사용** 클릭
   - `Google Calendar API` 검색 → **사용** 클릭
4. (선택) `Google Drive API`도 활성화하면 추가 기능 사용 가능

### Step 2. OAuth 동의 화면 설정

1. **Google 인증 플랫폼 > 브랜딩** 이동
2. 앱 이름: `Hermes Agent`
3. 사용자 지원 이메일: 본인 이메일
4. 개발자 연락처: 본인 이메일
5. 저장

### Step 3. OAuth 클라이언트 생성

1. **Google 인증 플랫폼 > 클라이언트** 이동
2. **+ 클라이언트 만들기** 클릭
3. 애플리케이션 유형: **데스크톱 앱**
4. 이름: `Hermes Agent`
5. **만들기** 클릭
6. 클라이언트 상세 페이지에서 **JSON 다운로드** (client_secret 파일)

### Step 4. 테스트 사용자 추가

1. **Google 인증 플랫폼 > 대상** 이동
2. "테스트 사용자" 섹션에서 **+ Add users** 클릭
3. 본인 Gmail 주소 입력 → 저장

> 앱이 "테스트 중" 상태일 때는 등록된 테스트 사용자만 OAuth 인증 가능

### Step 5. Client Secret 설치

```bash
GSETUP="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py"

$GSETUP --client-secret <다운로드한_client_secret_json_경로>
# → OK: Client secret saved to ~/.hermes/google_client_secret.json
```

Windows PowerShell:

```powershell
$env:HERMES_HOME = "$env:USERPROFILE\.hermes"
python "$env:HERMES_HOME\skills\productivity\google-workspace\scripts\setup.py" --client-secret "<다운로드_경로>\client_secret_xxx.json"
```

### Step 6. OAuth 인증 수행

```bash
# 1. 인증 URL 생성
$GSETUP --auth-url
# → https://accounts.google.com/o/oauth2/auth?... URL 출력

# 2. 위 URL을 브라우저에서 열기
#    → Google 계정 선택
#    → "Google에서 확인하지 않은 앱" 경고 → "계속" 클릭 (본인 앱이므로 안전)
#    → 모든 권한 체크 → "계속" 클릭
#    → localhost로 리다이렉트 → 에러 페이지 표시 (정상!)
#    → 주소창 URL에서 code= 파라미터 값 복사

# 3. 인증 코드로 토큰 교환
$GSETUP --auth-code "<복사한_code_값>"
# → OK: Authenticated. Token saved to ~/.hermes/google_token.json

# 4. 인증 확인
$GSETUP --check
# → AUTHENTICATED: Token valid
```

### Step 7. Gmail & Calendar API 테스트

```bash
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"

# Gmail 테스트
$GAPI gmail search "is:unread" --max 5

# Calendar 테스트
$GAPI calendar list --from today --to tomorrow
```

Windows에서 인코딩 에러 시:

```powershell
$env:PYTHONIOENCODING = "utf-8"
```

---

## Phase 4: Notion 연동

### Step 1. Notion Integration 생성

1. https://www.notion.so/my-integrations 접속
2. **+ 새 API 통합** 클릭
3. 이름: `Hermes Agent`, 유형: **내부**
4. 생성 후 **시크릿 키** 복사 (`ntn_` 또는 `secret_`로 시작)

### Step 2. 환경 변수 설정

`~/.hermes/.env`에 추가:

```env
NOTION_API_KEY=ntn_your_key_here
```

### Step 3. Notion 페이지에 Integration 연결

접근할 Notion 페이지마다:
1. 페이지 우측 상단 `...` 메뉴 클릭
2. **연결 추가** → `Hermes Agent` 선택

> Integration이 연결되지 않은 페이지는 API에서 404를 반환합니다.

### Step 4. API 테스트

```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "회의록"}'
```

Windows PowerShell:

```powershell
$headers = @{
  "Authorization" = "Bearer $env:NOTION_API_KEY"
  "Notion-Version" = "2025-09-03"
  "Content-Type" = "application/json"
}
Invoke-RestMethod -Uri "https://api.notion.com/v1/search" -Method POST -Headers $headers -Body '{"query": "test"}'
```

---

## Phase 5: Gateway 재시작 및 크론잡 생성

### Step 1. Gateway 재시작

새 credential이 반영되도록 Gateway를 재시작합니다:

```bash
hermes gateway run --replace
```

Windows 작업 스케줄러 사용 시:

```powershell
schtasks /End /TN "Hermes_Gateway"
schtasks /Run /TN "Hermes_Gateway"
```

상태 확인:

```bash
hermes status
# 또는
cat ~/.hermes/gateway_state.json
# → "gateway_state":"running", "platforms":{"slack":{"state":"connected"}}
```

### Step 2. 아침 브리핑 크론잡 생성

```bash
hermes cron create "0 10 * * *" \
  "아침 브리핑을 해줘. 두 가지를 확인해서 한국어로 정리해줘: 1) Gmail 받은편지함에서 지난 24시간 내 수신된 이메일을 google-workspace 스킬의 gmail search 기능으로 검색하고 발신자/제목/간단한 내용을 요약해줘. 메일이 없으면 '새로운 메일이 없습니다'라고 알려줘. 2) Google Calendar에서 오늘 일정을 google-workspace 스킬의 calendar list 기능으로 확인하고 시간/제목/장소를 정리해줘. 일정이 없으면 '오늘 일정이 없습니다'라고 알려줘." \
  --name "morning-briefing" \
  --deliver slack \
  --skill google-workspace
```

### 크론잡 커스터마이징

| 파라미터 | 설명 | 예시 |
|---------|------|------|
| `schedule` | cron 표현식 | `0 10 * * *` (매일 10시), `0 9 * * 1-5` (평일 9시) |
| `prompt` | 에이전트에게 줄 지시 | 자유롭게 수정 가능 |
| `--name` | 작업 이름 | `daily-gmail-digest` |
| `--deliver` | 전달 대상 | `slack`, `telegram`, `discord` |
| `--skill` | 사용할 스킬 | `google-workspace` |
| `--repeat` | 반복 횟수 | 생략 시 무한 반복 |

### 크론잡 관리

```bash
hermes cron list              # 목록 확인
hermes cron pause <job_id>    # 일시 중지
hermes cron resume <job_id>   # 재개
hermes cron run <job_id>      # 즉시 실행 (테스트용)
hermes cron remove <job_id>   # 삭제
```

---

## 사용법

### 자동: 매일 아침 브리핑

크론잡이 매일 설정 시간에 자동 실행됩니다. Slack에서 브리핑 메시지를 받게 됩니다:

> **📬 Gmail 요약**
> 1. Google — 보안 알림
> 2. 플렉스웍 — 맞춤 채용공고 추천
> 3. 티로 — 새로운 기능 소개
>
> **📅 오늘 일정**
> - 10:00 주간 팀 미팅 (회의실 A)
> - 14:00 디자인 리뷰 (온라인)
> - 16:30 1:1 면담 (매니저)

### 수동: Notion 회의록 액션 아이템

Slack에서 마누스에게 직접 요청:

```
오늘 노션에 작성한 회의록에서 액션 아이템을 정리해줘
```

```
노션 "주간 회의" 페이지 읽고 다음 할 일 정리해줘
```

```
노션에서 최근 회의록 찾아서 담당자별로 할 일 정리해줘
```

별도 설정 없이, Notion API + Slack이 연결된 상태에서 바로 사용 가능합니다.

---

## 전체 .env 템플릿

`~/.hermes/.env`:

```env
# =============================================================================
# HERMES AGENT CORE
# =============================================================================
ANTHROPIC_API_KEY=sk-ant-your-key-here

# =============================================================================
# SLACK (Socket Mode)
# =============================================================================
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-level-token

# =============================================================================
# NOTION
# =============================================================================
NOTION_API_KEY=ntn_your-notion-key

# =============================================================================
# GOOGLE (OAuth 토큰은 파일로 관리 — 수동 설정 불필요)
# google_token.json, google_client_secret.json → ~/.hermes/
# =============================================================================
```

## 설정 파일 위치

| 파일 | 경로 | 용도 |
|------|------|------|
| 환경변수 | `~/.hermes/.env` | API 키 저장 |
| 메인 설정 | `~/.hermes/config.yaml` | Hermes 전체 설정 |
| Google 토큰 | `~/.hermes/google_token.json` | OAuth 액세스/리프레시 토큰 |
| Google 클라이언트 | `~/.hermes/google_client_secret.json` | OAuth 클라이언트 정보 |
| Gateway 상태 | `~/.hermes/gateway_state.json` | 실행 상태 확인 |

---

## 트러블슈팅

### Hermes 설치 실패

```bash
hermes doctor                 # 의존성 점검
hermes update                 # 최신 버전 업데이트
```

### Gateway가 "already running" 에러

```bash
hermes gateway run --replace  # 기존 프로세스 교체
```

### Slack 연결이 안 될 때

1. `SLACK_BOT_TOKEN`과 `SLACK_APP_TOKEN`이 올바른지 확인
2. Socket Mode가 활성화되어 있는지 확인
3. Event Subscriptions에 `message.im` 등이 등록되어 있는지 확인

### OAuth "Google에서 확인하지 않은 앱" 경고

- 정상입니다. 본인이 만든 테스트 앱이므로 "계속" 클릭
- 테스트 사용자로 등록된 계정만 사용 가능

### `setup.py --auth-url` 후 localhost 에러 페이지

- 정상 동작. 주소창 URL에서 `code=` 이후 `&scope=` 이전까지의 값을 복사

### Notion 404 에러

- 해당 페이지에 Integration이 연결되었는지 확인
- 페이지 `...` → 연결 추가 → Hermes Agent

### Windows 인코딩 에러

```powershell
$env:PYTHONIOENCODING = "utf-8"
```

`~/.hermes/.env`에 영구 설정:

```env
PYTHONIOENCODING=utf-8
```

### 크론잡이 실행되지 않을 때

```bash
hermes cron list              # 상태 확인 (active인지)
hermes cron run <job_id>      # 수동 실행으로 테스트
hermes status                 # Gateway 연결 상태 확인
```
