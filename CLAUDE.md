# Morning Briefing 프로젝트 규칙

## 절대 규칙: 기존 기능 보존

**수정 시 기존 기능을 절대 삭제하거나 변경하지 않는다.**

- 사용자가 명시적으로 요청하지 않는 한, 기존 기능/로직/설정을 제거하지 않음
- 수정 전에 영향받는 기능 목록을 먼저 알려주고 확인받음
- 새 기능 추가 시에도 기존 기능이 깨지지 않는지 확인

## 프로젝트 구조

```
morning-briefing/
├── CLAUDE.md              # 프로젝트 규칙 (이 파일)
├── SKILL.md               # Hermes Agent 스킬 정의 (Phase 0~5 셋업 가이드)
├── README.md              # 프로젝트 소개
├── .gitignore             # 시크릿/캐시 제외
├── app/                   # Railway 클라우드 브리핑 서비스
│   ├── __init__.py
│   ├── main.py            # 엔트리포인트 (cron → Gmail → Calendar → Claude → Slack)
│   ├── gmail_client.py    # Gmail API (OAuth refresh token)
│   ├── calendar_client.py # Google Calendar API
│   ├── summarizer.py      # Claude API 요약 생성
│   └── slack_sender.py    # Slack 메시지 전송
├── Dockerfile             # Railway 빌드용
├── railway.toml           # Railway 크론잡 설정 (매일 10시 KST)
├── requirements.txt       # Python 의존성
├── docs/
│   ├── 00-INDEX.md        # 요청→문서 라우팅
│   ├── agent-workflow.md  # 에이전트 파이프라인
│   ├── code-review-checklist.md
│   ├── features/          # 개별 기능 사양
│   └── operations/        # 운영·점검
└── .claude/
    └── settings.local.json
```

## 외부 의존 파일 (이 레포 밖)

| 파일 | 경로 | 용도 |
|------|------|------|
| Hermes 환경변수 | `~/.hermes/.env` | API 키 (Anthropic, Slack, Notion) |
| Hermes 설정 | `~/.hermes/config.yaml` | 모델·프로바이더 설정 |
| Google 토큰 | `~/.hermes/google_token.json` | OAuth 토큰 |
| Google 클라이언트 | `~/.hermes/google_client_secret.json` | OAuth 클라이언트 |
| Gateway 상태 | `~/.hermes/gateway_state.json` | 실행 상태 |
| 캐치업 스크립트 | `%LOCALAPPDATA%\hermes\gateway-service\MorningBriefing_Catchup.ps1` | PC 부팅 시 놓친 브리핑 실행 |
| 마커 스크립트 | `%LOCALAPPDATA%\hermes\gateway-service\MorningBriefing_Marker.ps1` | 크론잡 실행 마커 |
| Gateway 시작 | `%LOCALAPPDATA%\hermes\gateway-service\Hermes_Gateway.cmd` | Gateway 자동 시작 |
| Startup VBS | `%APPDATA%\...\Startup\MorningBriefing_Catchup.vbs` | 부팅 시 캐치업 트리거 |
| Startup VBS | `%APPDATA%\...\Startup\Hermes_Gateway.vbs` | 부팅 시 Gateway 트리거 |

## 주요 기능 목록 (삭제 금지)

1. **매일 아침 Gmail 요약** — 크론잡(`0 10 * * *`)으로 지난 24시간 이메일 요약
2. **매일 아침 Calendar 일정** — 오늘 일정 시간/제목/장소 정리
3. **Slack 전송** — 위 브리핑을 Slack 채널/DM으로 자동 전달
4. **PC 부팅 캐치업** — PC가 꺼져 있어서 놓친 브리핑을 부팅 시 자동 실행 (레거시)
5. **Railway 클라우드 브리핑** — PC 상태 무관, Railway 크론잡으로 매일 10시 KST 자동 실행 (`app/`)

## 기술 스택

| 구분 | 기술 |
|------|------|
| Agent 프레임워크 | Hermes Agent (Python) |
| LLM | Anthropic Claude (claude-sonnet-4) |
| 이메일 | Gmail API (OAuth 2.0) |
| 캘린더 | Google Calendar API (OAuth 2.0) |
| 노트 | Notion API |
| 메시징 | Slack (Socket Mode, Bot Token) |
| 스케줄링 | Hermes cron + Windows Task Scheduler (레거시) |
| OS 자동화 | PowerShell + VBScript (Windows Startup, 레거시) |
| 클라우드 배포 | Railway (Docker + cron, 매일 01:00 UTC = 10:00 KST) |

## 보안 규칙

- API 키/토큰은 절대 코드에 하드코딩하지 않음 (`~/.hermes/.env` 또는 Railway 환경변수에서만 관리)
- `google_token.json`, `google_client_secret.json`은 `.gitignore`에 포함
- `.env` 파일은 절대 커밋하지 않음
- Slack Bot Token(`xoxb-`), App Token(`xapp-`)은 로그에 출력 금지
- Railway 환경변수: `GOOGLE_REFRESH_TOKEN`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `ANTHROPIC_API_KEY`, `SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`

## Gotchas (과거 교훈)

| 날짜 | 이슈 | 해결 |
|------|------|------|
| 2026-05-22 | PC 꺼져 있으면 10시 크론잡 미실행 | Startup 폴더에 캐치업 VBS 추가로 부팅 시 자동 보충 |
| 2026-05-22 | Hermes Gateway도 PC 재부팅 시 꺼짐 | Startup 폴더에 Gateway VBS 추가로 자동 시작 |
| 2026-05-23 | Gateway 재부팅 후 stale state로 캐치업 실패 | CMD에서 시작 전 state 초기화 + Catchup에서 PID 생존 검증 추가 |
| 2026-05-24 | VBS가 CMD를 직접 실행 시 "파일을 찾을 수 없습니다" 에러 + Task Scheduler와 충돌 | VBS에서 cmd.exe /c 명시 + 10초 딜레이 + CMD에 중복 실행 방지(tasklist) 추가 |
| 2026-05-24 | 브리핑 트리거 후 마커 즉시 기록 → Gateway 크래시 시 미전송+재시도 불가 | active_agents 모니터링으로 실제 완료 확인 후 마커 기록, 실패 시 마커 미생성(다음 부팅 재시도) |
| 2026-05-24 | tasklist가 모든 pythonw.exe 감지 → 다른 Python 프로세스 때문에 Gateway 미시작 | gateway_state.json PID 검증으로 교체 (특정 Gateway 프로세스만 확인) |
| 2026-05-24 | CMD 배치 파일 LF 줄바꿈 → CMD.exe 파싱 실패 | Claude Code Edit/Write 사용 금지, PowerShell WriteAllText로 CRLF+ASCII 강제 |
| 2026-05-27 | 로컬 VBS→CMD→PS1 체인 전체 불안정 (부팅 시 VBS 미실행 빈번) | Railway 클라우드 배포로 전환. PC 상태에 의존하지 않는 구조 |

## 수정 시 체크리스트

1. **CLAUDE.md 읽기** — 규칙과 기능 목록 확인
2. **docs/00-INDEX.md 라우팅** — 요청→카테고리 매핑, 해당 md 읽기
3. **영향 범위 파악** — 수정이 다른 기능에 영향 주는지 확인
4. **기존 기능 보존** — 삭제/변경은 명시적 요청 시에만
5. **SKILL.md 동기화** — 스킬 정의 변경 시 SKILL.md도 업데이트
6. **외부 파일 확인** — Hermes 설정/스크립트 변경 시 실제 파일 경로 확인
7. **코드 리뷰** — `code-reviewer` 에이전트 (code-review-checklist.md 참고)
8. **문서 업데이트** — 기능 변경 시: CLAUDE.md + docs/ + 00-INDEX.md 동기화
9. **커밋** — 사용자가 직접 커밋/푸시 (Claude는 코드 변경만)

## 에이전트 파이프라인

```
요청 접수 → 탐색 → 계획 → 구현 → 리뷰 → 검증 → 문서 업데이트
```

상세 가이드: [docs/agent-workflow.md](./docs/agent-workflow.md)

### 요청 유형별 스킬 자동 라우팅

| 요청 키워드 | 필수 스킬/플러그인 | 시점 |
|-------------|-------------------|------|
| 크론잡, 스케줄 | Hermes cron CLI 확인 | 구현 전 |
| Slack 연동 | Slack MCP 도구 | 구현 시 |
| Gmail, Calendar | Google Workspace API 확인 | 구현 시 |
| Notion | Notion MCP 도구 | 구현 시 |
| PowerShell 스크립트 | 외부 파일 경로 확인 | 구현 전 |
| 코드 수정 완료 후 | `ccpp:review` | 리뷰 단계 (필수) |
| 보안 민감 코드 | `security-review` | 리뷰 단계 |

### 에이전틱 코딩 원칙

- **병렬 실행**: 독립 작업은 Agent `run_in_background`로 동시 실행
- **Explore 우선**: 파일 위치 모를 때 Explore 에이전트로 탐색
- **Grep > Read**: 패턴 검색은 Grep, 정확한 위치일 때만 Read
- **외부 파일 주의**: `~/.hermes/` 및 `%LOCALAPPDATA%\hermes\` 경로의 파일 수정 시 경로 존재 확인 필수
