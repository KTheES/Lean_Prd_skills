# 과제 명세 재점검 체크리스트

점검 기준: `00_과제명세서.md`, `01_채점루브릭.md`, `02_제출가이드_FAQ.md`, `CODEX_HANDOFF_lean_prd.md`

점검일: 2026-10-28

## Part A — Skill 설계

- [x] `.claude/skills/lean-prd/SKILL.md`와 올바른 frontmatter
- [x] 기능과 자연어 트리거 5종 이상, cycle 진입 조건
- [x] 본문 500줄 이하: 183줄
- [x] 최대 5개 질문과 미응답 기본 가정
- [x] Learn→Measure→Build 역산과 `00-overview` 마지막 작성 이유
- [x] H#/M#/E#/MS#/P#/T# 교차 참조 규칙
- [x] 결정별 갱신 파일이 있는 cycle 모드
- [x] 참조 문서 읽는 시점 안내
- [x] 이미지 유사도·권리 위험 탐지 도메인 보강과 변경 이력
- [x] 사용자 검증 규칙 3개 추가
- [x] 세 규칙의 실제 오류 탐지 증빙
- [x] Skill Creator `quick_validate.py`: `Skill is valid!`
- [x] 특정 제품명을 SKILL.md에 하드코딩하지 않음

## Part B — PRD 12종

- [x] 정확한 파일명으로 12개 문서 생성
- [x] 제품·버전·수정일·관련 가설 메타데이터
- [x] 필수 헤딩과 템플릿 자리표시자 제거
- [x] 가치 가설 2개와 성장 가설 1개, 위험도 순위
- [x] 모든 H#에 M#·E#·MS# 연결
- [x] Actionable/Vanity 구분
- [x] MVP 유형, In/Out, 모든 In의 H# 또는 측정 예외, 10영업일 범위
- [x] 역할·기술·FTE·담당 MS·충원 조건·결정 규칙
- [x] 기술 스택 6열, Mermaid, 분석/Feature Flag, ADR, 지금 하지 않을 것
- [x] GitHub Pages·Actions·PostHog 공식 출처와 2026-10-28 확인일
- [x] MS0~MS3의 H#·산출물·숫자 종료 조건·Go/No-Go·P#
- [x] GitHub 매핑과 Mermaid 일정
- [x] `VALIDATION.txt`: FAIL 0, WARN 1, ok 14
- [ ] 학생이 AI 초안을 직접 읽고 수정한 별도 커밋
- [ ] `11-bml-log.md` 검토 메모에 학생의 실제 수정 이유 기록
- [ ] 첫 10명 접근 채널을 실제 연락 가능한 집단으로 확정
- [ ] ArtGuard를 제출 아이디어로 최종 확정

## Part C — BML Cycle 1

- [x] 최고 위험 가설 H1과 E1 선정 이유
- [x] H1 검증용 정적 랜딩 MVP
- [x] 동의문·인터뷰·CSV·분석 양식
- [x] 사전 통과/실패/회색 지대 기준
- [ ] 실제 잠재고객 5명 이상 모집
- [ ] 정량 M1과 비식별 정성 데이터 수집
- [ ] 증빙을 `experiments/cycle-1/`에 저장
- [ ] `/lean-prd cycle`로 임계값 비교
- [ ] 학생이 Pivot/Persevere/Kill/재실험 최종 결정 승인
- [ ] 결정에 따라 PRD 갱신 후 재검증

실제 데이터가 없으므로 Part C 완료로 표시하지 않는다. 가상 데이터를 실제 결과로 만들지 않는다.

## Part D — 회고·제출

- [x] `RETROSPECTIVE.md` 1~2쪽 분량 초안
- [x] 구체적인 검증기 Before/After
- [x] 실제 팀 확장 방향
- [x] `docs/skill-session.md`에 Codex 실행 환경과 질문·가정 기록
- [x] 민감정보 패턴 검사와 `.gitignore`
- [x] PR마다 검증하는 GitHub Actions 구성
- [x] 파이프라인에 `set -o pipefail`을 적용해 검증 실패가 CI 실패로 전파됨
- [ ] 학생 표현으로 회고의 사람 검토 항목 확정
- [ ] Claude Code에서 자연어 트리거와 `/lean-prd cycle` 재현
- [ ] 최종 CI 성공 확인
- [ ] 실제 Cycle 1까지 마친 뒤 `v1.0` 태그 생성
- [ ] 저장소 URL과 `v1.0` 태그 URL 제출

## 현재 판정

- Part A: 구현·로컬 검증 완료
- Part B: 문서·자동 검증 완료, 사람 검토 증빙 대기
- Part C: Build와 수집 준비 완료, Measure/Learn은 실제 데이터 대기
- Part D: 초안 완료, 사람 회고·최종 태그 대기

따라서 현재 브랜치는 **중간 점검 제출 가능** 상태이며, 최종 제출 완료 상태는 아니다.

