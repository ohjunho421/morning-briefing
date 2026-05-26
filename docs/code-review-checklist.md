# 코드 리뷰 체크리스트

## 리뷰 시 확인사항

- [ ] 기존 기능이 깨지지 않았는가 (CLAUDE.md "절대 규칙")
- [ ] API 키/토큰이 코드에 하드코딩되지 않았는가
- [ ] 외부 파일 경로가 정확한가 (`~/.hermes/`, `%LOCALAPPDATA%\hermes\`)
- [ ] 크론잡 표현식이 의도한 스케줄과 일치하는가
- [ ] PowerShell 스크립트 인코딩이 UTF-8인가
- [ ] **CMD 배치 파일(.cmd/.bat)이 CRLF + ASCII 인코딩인가** (Claude Code Edit/Write는 LF로 저장 → CMD.exe 파싱 실패. 반드시 PowerShell `WriteAllText`로 CRLF 변환 필수)
- [ ] .gitignore에 시크릿 파일이 포함되어 있는가
- [ ] SKILL.md와 CLAUDE.md가 변경사항과 동기화되었는가

## 과거 피드백 (교훈 누적)

| 날짜 | 이슈 | 원인 | 교훈 |
|------|------|------|------|
| 2026-05-22 | PC 꺼져 있으면 크론잡 미실행 | Windows Task Scheduler는 PC 꺼지면 실행 불가 | Startup 폴더 VBS로 부팅 시 캐치업 보충 |
| 2026-05-22 | 프로젝트 초기 세팅 | - | 하네스 init 완료. 이후 교훈 여기에 누적할 것 |
| 2026-05-24 | CMD 배치 파일 LF 줄바꿈으로 파싱 실패 | Claude Code Edit/Write가 LF로 저장 | CMD 파일은 반드시 PowerShell WriteAllText로 CRLF 변환 |
| 2026-05-24 | 브리핑 트리거만 하고 마커 즉시 기록 → 미전송 | cron run은 비동기 트리거만 수행 | active_agents 모니터링으로 실제 완료 확인 후 마커 기록 |
| 2026-05-24 | tasklist가 모든 pythonw 감지 → Gateway 미시작 | imagename 필터가 프로세스 구분 불가 | gateway_state.json PID 검증으로 교체 |
| 2026-05-27 | 로컬 VBS→CMD→PS1 체인 불안정 (부팅 시 VBS 미실행) | Windows Startup 폴더 신뢰도 낮음 | Railway 클라우드 배포로 전환. PC 의존성 제거 |

> 리뷰 시 위 테이블의 패턴이 반복되지 않는지 확인한다.
