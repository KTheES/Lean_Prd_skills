# Lean PRD Skill

아이디어 한 줄을 **가설 → 지표 → MVP → 실험 → 팀·기술 스택 → 검증 마일스톤 → Pivot 안전장치**로 연결된 12개 PRD 문서로 바꾸는 Claude Code Agent Skill입니다.

이 저장소는 BML 기반 Lean PRD Skill 구축 과제 제출물입니다. Skill 자체는 특정 제품에 종속되지 않으며, 포함된 예시 PRD는 **ArtGuard**입니다. 실제 Cycle 1 면담 5건과 승인된 Customer Segment Pivot은 증빙과 함께 반영했고, E2 이후 결과와 사람 회고는 완료된 사실처럼 표시하지 않습니다.

## 제출물 지도

| 제출물 | 위치 | 상태 |
|---|---|---|
| Agent Skill | [`.claude/skills/lean-prd/`](.claude/skills/lean-prd/) | 구현 |
| Skill 지시문 | [`.claude/skills/lean-prd/SKILL.md`](.claude/skills/lean-prd/SKILL.md) | 구현 |
| PRD 12종 | [`docs/prd/`](docs/prd/) | Cycle 1 Pivot 반영 |
| 검증 결과 | [`docs/prd/VALIDATION.txt`](docs/prd/VALIDATION.txt) | 자동 생성 |
| Skill 호출 기록 | [`docs/skill-session.md`](docs/skill-session.md) | Codex 실행 기록 |
| 검증 규칙 증빙 | [`docs/validator-development.md`](docs/validator-development.md) | 오류 주입 사례 |
| Cycle 1 증빙 | [`experiments/cycle-1/`](experiments/cycle-1/) | 실제 5명·분석·결정 완료 |
| 회고 | [`RETROSPECTIVE.md`](RETROSPECTIVE.md) | 초안, 사람 확정 필요 |

## 사용법

Claude Code에서 이 저장소를 열고 다음처럼 요청합니다.

```text
/lean-prd
캐릭터·창작 굿즈 소비자가 상품의 진위와 출처를 확인할 근거를 정리하는 서비스의 PRD를 만들어 줘.
```

자연어로 `PRD`, `제품 기획서`, `MVP 정의`, `린 캔버스`, `아이디어 검증` 또는 “이거 만들려면 뭐부터 해야 해”를 언급해도 트리거되도록 설계했습니다.

실험 뒤에는 다음 형식으로 cycle 모드를 호출합니다.

```text
/lean-prd cycle
E1/H1 결과: 표본 5명, M1=..., 익명화한 정성 피드백=..., 증빙=experiments/cycle-1/...
```

Skill은 임계값과 비교한 결정을 **제안**하며, 제품 책임자의 승인 전에는 Pivot/Persevere/Kill을 최종 확정하지 않습니다.

## 검증

```bash
python .claude/skills/lean-prd/scripts/validate_prd.py docs/prd
```

엄격 검증은 경고도 실패로 처리합니다.

```bash
python .claude/skills/lean-prd/scripts/validate_prd.py docs/prd --strict
```

Pull Request와 `main` push 시 [Validate PRD 워크플로우](.github/workflows/validate-prd.yml)가 같은 검사를 자동 실행하고 결과를 아티팩트로 저장합니다.

## 아직 사람이 해야 하는 일

1. `docs/prd/11-bml-log.md`의 검토 메모를 읽고 본인이 실제로 고친 이유가 맞는지 확인합니다.
2. `RETROSPECTIVE.md`의 `TODO(사람 검토)` 세 곳을 본인 경험과 표현으로 확정합니다.
3. Pull Request의 CI 성공과 공개 파일의 개인정보 부재를 확인합니다.
4. 최종 확인 후 `v1.0` 태그를 만들고 저장소 URL과 태그 URL을 제출합니다.

## 민감정보 원칙

- API 키, 토큰, `.env`, 개인 식별 정보는 커밋하지 않습니다.
- 인터뷰 참여자는 `P01` 같은 익명 ID로만 기록합니다.
- 원본 연락처·동의서는 `experiments/**/private/`에 보관하며 `.gitignore`로 제외합니다.
- 공개 저장소에는 집계 결과와 비식별 인용만 올립니다.

