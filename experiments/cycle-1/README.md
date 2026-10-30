# Cycle 1 — 실제 데이터 수집 안내

이 폴더는 E1/H1 실험 증빙을 위한 공개 가능한 자료만 저장합니다. 실제 응답은 아직 수집되지 않았으며, 결과를 임의로 만들지 않습니다.

## 준비된 파일

- `consent-script.md`: 참여 전 안내 문구
- `interview-template.md`: 익명 인터뷰 기록 양식
- `results-template.csv`: 정량 집계용 빈 CSV
- `analysis-template.md`: 임계값 비교와 결정 초안 양식
- `mvp/index.html`: H1 문제 검증용 정적 랜딩 페이지. 버튼은 개인정보를 전송하지 않음
- `survey_gui.py`: E1 문제 검증과 E2 리포트 평가를 통합한 로컬 GUI 입력기
- `run-survey.bat`: Windows에서 더블 클릭으로 GUI를 실행하는 런처
- `responses.csv`: GUI·CLI가 함께 사용하는 비식별 응답 원장

## 통합 GUI 실행

Windows 파일 탐색기에서 `run-survey.bat`를 더블 클릭하거나 저장소 루트에서 다음을 실행한다.

```powershell
python experiments/cycle-1/survey_gui.py
```

응답은 `responses.csv`와 `participants/P##.md`에 동시 저장된다. 이름·연락처·계정명은 입력하지 않는다. E1의 M1은 참여자 적합성, `월1회이상`, `후속 참여 있음`을 기준으로 계산하고 E2의 리포트 점수와 구분해 해석한다.

## 수집 절차

1. 실제 잠재고객 5명 이상을 모집한다.
2. 참여자에게 목적·보관·중단·삭제 방법을 안내하고 동의를 받는다.
3. `P01`~`Pnn` 익명 ID만 공개 파일에 사용한다.
4. 연락처·원본 동의서는 `private/`에 보관한다. 이 폴더는 `.gitignore` 대상이다.
5. 정량 결과와 비식별 인용을 입력한 뒤 `/lean-prd cycle`을 호출한다.

## 완료 조건

- 실제 참여자 5명 이상
- 주 지표 M1 값 계산 가능
- 참여자별 정성 피드백 최소 1개
- 사전 임계값과 비교한 결정 제안
- 제품 책임자의 최종 결정 승인

