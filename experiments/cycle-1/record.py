#!/usr/bin/env python3
"""cycle-1 인터뷰 기록 도구 (표준 라이브러리만 사용).
  python experiments/cycle-1/record.py add      # 새 참여자 입력 → responses.csv + participants/P##.md
  python experiments/cycle-1/record.py summary  # 평균/분포 집계 → summary.md
기록 동의(consent_record)가 '아니요'면 아무것도 저장하지 않는다.
"""
import csv, os, sys, datetime, statistics, collections

# Windows PowerShell에서 한글 프롬프트가 깨지지 않도록 출력을 UTF-8로 고정한다.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BASE = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(BASE, "responses.csv")
PDIR = os.path.join(BASE, "participants")
SUMMARY = os.path.join(BASE, "summary.md")
FIELDS = [
    "participant_id", "date", "participant_type", "creator_exp", "creator_form",
    "seen_case_route", "curious_items", "top_curiosity", "check_freq",
    "current_method", "current_minutes", "score_source_url", "score_checked_at",
    "score_visual_table", "score_license", "score_next_action", "score_disclaimer",
    "least_useful", "missing_info", "action_after_report", "followup_intent",
    "followup_reason", "trust_concern", "quote", "consent_record", "consent_quote",
    "note",
]
SCORES = ["score_source_url","score_checked_at","score_visual_table","score_license","score_next_action","score_disclaimer"]
SCORE_LABELS = {
    "score_source_url": "출처 URL",
    "score_checked_at": "확인 시각",
    "score_visual_table": "시각적 비교표",
    "score_license": "라이선스 확인 정보",
    "score_next_action": "다음 행동 안내",
    "score_disclaimer": "비법률 판단 고지",
}

def ensure_storage():
    os.makedirs(PDIR, exist_ok=True)
    if not os.path.exists(CSV):
        with open(CSV, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()

ensure_storage()

def ask(label, kind="text", choices=None):
    while True:
        v = input(f"{label}{' ['+'/'.join(choices)+']' if choices else ''}{' (1~5)' if kind=='score' else ''}: ").strip()
        if kind == "score":
            if v.isdigit() and 1 <= int(v) <= 5: return v
            print("  1~5 정수로 입력"); continue
        if choices and v not in choices:
            print("  선택지 중에서 입력"); continue
        return v

def next_id():
    n = 0
    if os.path.exists(CSV):
        for r in csv.DictReader(open(CSV, encoding="utf-8")):
            n = max(n, int(r["participant_id"][1:]))
    return f"P{n+1:02d}"

def add():
    if ask("0-1 익명 기록 동의", choices=["예","아니요"]) != "예":
        print("동의 없음 → 저장하지 않고 종료"); return
    cq = ask("0-2 의견 인용 동의", choices=["예","아니요"])
    r = {"participant_id": next_id(), "date": datetime.date.today().isoformat(),
         "consent_record": "예", "consent_quote": cq}
    r["participant_type"] = ask("1 참여자 유형(작가/판매자/팬/기타)")
    r["creator_exp"] = ask("2 작품 공개/판매 경험", choices=["있음","없음"])
    r["creator_form"] = ask("2-1 형태(없으면 엔터)")
    r["seen_case_route"] = ask("3 논란 사례 처음 본 경로(없으면 '본 적 없음')")
    r["curious_items"] = ask("4 궁금했던 것(여러 개는 ; 로 구분)")
    r["top_curiosity"] = ask("4 가장 궁금한 것 1개")
    r["check_freq"] = ask("5 확인 빈도", choices=["월1회이상","분기1회","거의없음"])
    r["current_method"] = ask("6 현재 확인 방법")
    r["current_minutes"] = ask("6 소요 시간(분, 숫자)")
    for k in SCORES: r[k] = ask(f"7 {k}", "score")
    r["least_useful"] = ask("7-1 가장 쓸모없/헷갈린 항목")
    r["missing_info"] = ask("7-2 아쉬운 정보")
    r["action_after_report"] = ask("8 가장 먼저 할 행동", choices=["저장","원문방문","추가검토요청","지인공유","행동없음","기타"])
    r["followup_intent"] = ask("9 후속 참여 의향", choices=["있음","없음"])
    r["followup_reason"] = ask("9 이유")
    r["trust_concern"] = ask("10 우려되는 신뢰 문제")
    r["quote"] = ask("12 한 문장 의견") if cq == "예" else ""
    r["note"] = ask("메모(면담자 관찰, 지인 편향 등)")
    with open(CSV, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerow({k: r.get(k, "") for k in FIELDS})
    with open(os.path.join(PDIR, r["participant_id"] + ".md"), "w", encoding="utf-8") as f:
        f.write(f"# {r['participant_id']} ({r['date']})\n\n" + "\n".join(f"- **{k}**: {r.get(k,'')}" for k in FIELDS if k not in ("participant_id","date")) + "\n")
    print(f"저장 완료: {r['participant_id']}")

def summary():
    rows = list(csv.DictReader(open(CSV, encoding="utf-8")))
    if not rows: print("데이터 없음"); return
    creator_words = ("창작", "작가", "판매자", "제작")
    eligible = [
        r for r in rows
        if r.get("creator_exp") == "있음" or any(word in r.get("participant_type", "") for word in creator_words)
    ]
    m1_pass = [r for r in eligible if r.get("check_freq") == "월1회이상" and r.get("followup_intent") == "있음"]
    out = [f"# Cycle-1 집계 (n={len(rows)}, 생성 {datetime.date.today()})\n", "## E1 문제 검증 (M1)"]
    if eligible:
        rate = len(m1_pass) / len(eligible) * 100
        out += [
            f"- 적합 참여자: {len(eligible)}명 (" + ", ".join(r["participant_id"] for r in eligible) + ")",
            f"- 월 1회 이상 문제 경험 + 후속 참여 있음: {len(m1_pass)}명",
            f"- **M1 = {len(m1_pass)}/{len(eligible)} = {rate:.1f}%**",
            "- 사전 기준: 60% 이상 통과, 40% 미만 실패, 40~60% 표본 확대",
        ]
    else:
        out.append("- 창작·굿즈 제작/판매 경험으로 적합성을 확인할 참여자가 없음")
    out += ["", "## E2 리포트 항목 유용성 (1~5)\n", "| 항목 | 평균 | 4점 이상 비율 |", "|---|---|---|"]
    for k in SCORES:
        v = [int(r[k]) for r in rows if r[k]]
        if v:
            out.append(f"| {SCORE_LABELS[k]} | {statistics.mean(v):.2f} | {sum(x>=4 for x in v)}/{len(v)} |")
        else:
            out.append(f"| {SCORE_LABELS[k]} | 측정 없음 | 0/0 |")
    def dist(k):
        c = collections.Counter(r[k] for r in rows if r[k]); return ", ".join(f"{a} {b}명" for a, b in c.most_common())
    mins = [float(r["current_minutes"]) for r in rows if r["current_minutes"].replace(".","",1).isdigit()]
    out += ["", "## 분포", f"- 확인 빈도: {dist('check_freq')}", f"- 리포트 후 첫 행동: {dist('action_after_report')}",
            f"- 후속 참여 의향: {dist('followup_intent')}", f"- 가장 궁금한 것: {dist('top_curiosity')}",
            f"- 현재 확인 소요 시간(분): 평균 {statistics.mean(mins):.1f}, 중앙값 {statistics.median(mins):.1f}" if mins else "- 소요 시간 데이터 없음",
            "", "## 인용 가능한 의견(동의자만)"] + [f"- {r['participant_id']}: {r['quote']}" for r in rows if r["consent_quote"] == "예" and r["quote"]]
    out += ["", "> 임계값 비교는 `06-experiment-plan.md`의 기준과 대조해 `11-bml-log.md`에 기록할 것."]
    with open(SUMMARY, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("\n".join(out))

if __name__ == "__main__":
    {"add": add, "summary": summary}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: print(__doc__))()
