# Morning Briefing - Hermes Agent Skill

Hermes Agent를 처음부터 설치하고, **Gmail + Google Calendar + Notion + Slack**을 연동하여 매일 아침 자동 브리핑을 받는 완전한 셋업 가이드입니다.

## What It Does

```
Gmail API ─────┐
Calendar API ──┼──▶ Hermes Agent Gateway ──▶ Slack 채널/DM
Notion API ────┘     (cron + skills)
```

- **매일 아침 10시** — Gmail 이메일 요약 + 오늘의 캘린더 일정을 Slack으로 전달
- **수동 요청** — Slack에서 Notion 회의록의 액션 아이템을 즉시 정리

## Prerequisites

- Python 3.10+
- Google 계정 (Gmail & Calendar)
- Notion 계정
- Slack 워크스페이스 (앱 설치 권한)
- Anthropic API 키

## Quick Start

1. [Hermes Agent](https://github.com/NousResearch/hermes-agent) 설치
2. `SKILL.md`의 Phase 0~5를 순서대로 따라가기
3. 끝!

자세한 설정 방법은 **[SKILL.md](./SKILL.md)** 를 참조하세요.

## Setup Phases

| Phase | 내용 |
|-------|------|
| Phase 0 | Hermes Agent 설치 |
| Phase 1 | Anthropic API 키 설정 |
| Phase 2 | Slack 앱 생성 및 연동 |
| Phase 3 | Google Workspace (Gmail + Calendar) 연동 |
| Phase 4 | Notion 연동 |
| Phase 5 | Gateway 재시작 및 크론잡 생성 |

## License

MIT
