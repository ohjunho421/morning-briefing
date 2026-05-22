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
4. **PC 부팅 캐치업** — PC가 꺼져 있어서 놓친 브리핑을 부팅 시 자동 실행

## 기술 스택

| 구분 | 기술 |
|------|------|
| Agent 프레임워크 | Hermes Agent (Python) |
| LLM | Anthropic Claude (claude-sonnet-4) |
| 이메일 | Gmail API (OAuth 2.0) |
| 캘린더 | Google Calendar API (OAuth 2.0) |
| 노트 | Notion API |
| 메시징 | Slack (Socket Mode, Bot Token) |
| 스케줄링 | Hermes cron + Windows Task Scheduler |
| OS 자동화 | PowerShell + VBScript (Windows Startup) |

## 보안 규칙

- API 키/토큰은 절대 코드에 하드코딩하지 않음 (`~/.hermes/.env`에서만 관리)
- `google_token.json`, `google_client_secret.json`은 `.gitignore`에 포함
- `.env` 파일은 절대 커밋하지 않음
- Slack Bot Token(`xoxb-`), App Token(`xapp-`)은 로그에 출력 금지

## Gotchas (과거 교훈)

| 날짜 | 이슈 | 해결 |
|------|------|------|
| 2026-05-22 | PC 꺼져 있으면 10시 크론잡 미실행 | Startup 폴더에 캐치업 VBS 추가로 부팅 시 자동 보충 |
| 2026-05-22 | Hermes Gateway도 PC 재부팅 시 꺼짐 | Startup 폴더에 Gateway VBS 추가로 자동 시작 |

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
