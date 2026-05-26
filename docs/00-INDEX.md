# Morning Briefing 문서 인덱스

> 요청을 받으면 아래 매핑을 확인하여 해당 md를 읽고 작업을 시작하세요.

**최종 정리일:** 2026-05-22

## 0. 가장 먼저 읽는 것

| 파일 | 역할 | 언제 |
|------|------|------|
| /CLAUDE.md | 프로젝트 규칙·기능 보존·기술 스택 | 모든 작업 시작 전 |
| /SKILL.md | Hermes 스킬 정의 (Phase 0~5 셋업) | 설정 변경·트러블슈팅 시 |

## 1. 카테고리 트리

```
docs/
├── 00-INDEX.md              # 이 파일 (라우팅)
├── agent-workflow.md        # 에이전트 파이프라인
├── code-review-checklist.md # 리뷰 피드백 루프
├── features/                # 개별 기능 사양
│   └── (향후 추가)
└── operations/              # 운영·점검
    └── (향후 추가)
```

## 2. 요청 → 참고 문서 매핑

### 설정·설치

| 키워드 | 참고 문서 | 설명 |
|--------|----------|------|
| Hermes 설치, setup | /SKILL.md Phase 0~1 | Agent 설치 + API 키 |
| Slack 연동, 봇 | /SKILL.md Phase 2 | Slack 앱 생성·토큰 |
| Gmail, Calendar, Google | /SKILL.md Phase 3 | OAuth 설정 |
| Notion | /SKILL.md Phase 4 | Integration 생성 |
| 크론잡, cron, 스케줄 | /SKILL.md Phase 5 | 크론잡 생성·관리 |

### 기능

| 키워드 | 참고 문서 | 설명 |
|--------|----------|------|
| 아침 브리핑, 이메일 요약 | /SKILL.md "사용법" 섹션 | 자동 브리핑 동작 |
| Railway, 클라우드 배포 | app/main.py, Dockerfile, railway.toml | Railway 크론잡 기반 클라우드 브리핑 |
| Notion 회의록, 액션아이템 | /SKILL.md "수동 요청" 섹션 | Slack에서 수동 요청 |
| PC 부팅 캐치업 | /CLAUDE.md Gotchas | 부팅 시 놓친 브리핑 자동 실행 (레거시) |

### 운영

| 키워드 | 참고 문서 | 설명 |
|--------|----------|------|
| 트러블슈팅, 에러 | /SKILL.md "트러블슈팅" 섹션 | 일반적인 에러 해결 |
| Gateway 상태, 실행 | /CLAUDE.md 외부 의존 파일 | gateway_state.json 위치 |
| 환경변수, API 키 | /SKILL.md ".env 템플릿" | 전체 환경변수 목록 |

### 개발 프로세스

| 키워드 | 참고 문서 | 설명 |
|--------|----------|------|
| 에이전트 워크플로우 | docs/agent-workflow.md | 7단계 파이프라인 |
| 코드 리뷰 | docs/code-review-checklist.md | 리뷰 체크리스트 |

## 3. 작업 시작 표준 절차

1. CLAUDE.md (자동 로드) — 규칙 확인
2. 이 파일 — 어떤 카테고리인지 매핑
3. 해당 md — 기존 의도·동작 파악
4. 관련 코드/스크립트 — Read 또는 Grep
5. 변경 계획 보고 후 작업 시작

> 금지: 매핑 없이 코드부터 수정하지 말 것.

## 4. 새 문서 추가 시

새 md를 추가하면 이 INDEX의 "2. 매핑"에 행을 추가해야 함.

## 5. 치트시트

```
설치/설정     → SKILL.md
기능 동작     → SKILL.md 사용법
트러블슈팅    → SKILL.md 하단
외부 파일     → CLAUDE.md 외부 의존 파일 테이블
개발 프로세스 → docs/agent-workflow.md
리뷰         → docs/code-review-checklist.md
```
