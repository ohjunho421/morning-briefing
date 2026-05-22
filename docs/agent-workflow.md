# 에이전트 활용 워크플로우

## 파이프라인

```
요청 접수 → 1.탐색 → 2.계획 → 3.구현 → 4.리뷰 → 5.검증 → 6.문서 업데이트
```

> 커밋/푸시는 사용자가 직접 수행

### 1단계: 탐색

| 목적 | 도구 | 설명 |
|------|------|------|
| 레포 내 파일 | Explore 에이전트 | SKILL.md, 스크립트 위치 |
| 외부 파일 | Read | `~/.hermes/`, `%LOCALAPPDATA%\hermes\` 경로 |
| 문서 확인 | docs/00-INDEX.md Read | 규칙·히스토리 파악 |
| Hermes 상태 | PowerShell | `hermes status`, `hermes cron list` |

### 2단계: 계획

| 조건 | 도구 |
|------|------|
| 복잡한 변경 (3파일+) | planner 에이전트 |
| 단순 변경 (1~2파일) | 직접 진행 |

### 3단계: 구현

| 작업 유형 | 도구 |
|----------|------|
| SKILL.md 수정 | 직접 Edit |
| PowerShell 스크립트 | 직접 Write/Edit |
| Hermes 크론잡 | PowerShell (hermes cron CLI) |
| Slack 메시지 | Slack MCP 도구 |
| Notion 조회 | Notion MCP 도구 |

### 4단계: 리뷰 (필수)

| 도구 | 설명 |
|------|------|
| code-reviewer | 로직, 보안, 경로 정확성 |
| security-reviewer | API 키 노출, 토큰 하드코딩 검사 |
| code-review-checklist.md | 과거 피드백 반복 방지 |

### 5단계: 검증

| 도구 | 설명 |
|------|------|
| PowerShell | 스크립트 실행 테스트 |
| hermes cron run | 크론잡 수동 실행 테스트 |
| Slack MCP | 메시지 전송 확인 |

### 6단계: 문서 업데이트

| 대상 | 조건 |
|------|------|
| CLAUDE.md | 기능·스택·Gotchas 변경 시 |
| SKILL.md | 스킬 정의·셋업 과정 변경 시 |
| docs/00-INDEX.md | 새 md 추가 시 |
| code-review-checklist.md | 교훈 발견 시 |

---

## 요청 유형별 빠른 매핑

| 유형 | 파이프라인 | 핵심 도구 |
|------|-----------|-----------|
| 크론잡 변경 | 탐색 → hermes cron CLI → 검증 → 문서 | PowerShell |
| Slack 연동 | 탐색 → 구현 → 리뷰 → 검증 → 문서 | Slack MCP |
| 스크립트 수정 | 탐색 → Edit → 리뷰 → 검증 → 문서 | Read/Edit + PowerShell |
| 새 기능 추가 | 탐색 → plan → 구현 → 리뷰 → 검증 → 문서 | planner → 구현 |
| 트러블슈팅 | SKILL.md 참조 → 진단 → 수정 → 검증 | PowerShell + Read |

---

## 에이전틱 전략

1. **Explore 우선** — 파일 위치 모를 때 토큰 절약
2. **병렬 에이전트** — 독립 작업은 동시 실행
3. **Grep > Read** — 패턴 검색은 Grep, 정확한 위치일 때만 Read
4. **외부 파일 주의** — `~/.hermes/` 경로 파일은 항상 존재 확인 후 수정
5. **Hermes CLI 활용** — `hermes cron`, `hermes status`, `hermes gateway` 명령 우선 사용
