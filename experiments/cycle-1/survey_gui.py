#!/usr/bin/env python3
"""ArtGuard Cycle 1 통합 설문 GUI (E1 문제 검증 + E2 리포트 평가)."""

from __future__ import annotations

import csv
import datetime
import os
import tkinter as tk
from tkinter import messagebox, ttk

from record import CSV, FIELDS, PDIR, ensure_storage, next_id


SCORE_LABELS = {
    "score_source_url": "원본과 후보의 출처 URL",
    "score_checked_at": "확인 시각",
    "score_visual_table": "형태·색상·구성 비교표",
    "score_license": "공식 라이선스 확인 정보",
    "score_next_action": "신고·추가 검토 등 다음 행동 안내",
    "score_disclaimer": "‘법률적 침해 판정이 아님’ 고지",
}

FIELD_LABELS = {
    "participant_type": "참여자 유형",
    "creator_exp": "작품 공개·굿즈 제작/판매 경험",
    "creator_form": "작품 공개·판매 형태",
    "seen_case_route": "유사성 논란 사례를 처음 본 경로",
    "curious_items": "사례에서 궁금했던 정보",
    "top_curiosity": "가장 필요한 정보",
    "check_freq": "유사 굿즈 확인 빈도",
    "current_method": "현재 확인 방법",
    "current_minutes": "현재 확인 소요 시간(분)",
    **SCORE_LABELS,
    "least_useful": "가장 쓸모없거나 헷갈린 항목",
    "missing_info": "리포트에 없어서 아쉬운 정보",
    "action_after_report": "리포트 후 가장 먼저 할 행동",
    "followup_intent": "후속 테스트 참여 의향",
    "followup_reason": "후속 참여 의향의 이유",
    "trust_concern": "가장 우려되는 신뢰 문제",
    "quote": "공개 가능한 익명 의견",
    "consent_record": "익명 기록·저장소 제출 동의",
    "consent_quote": "익명 의견 공개 인용 동의",
    "note": "면담자 메모",
}

PARTICIPANT_TYPES = [
    "1인 시각 창작자",
    "굿즈 제작·판매자",
    "창작 경험이 있는 굿즈 소비자",
    "일반 굿즈 소비자",
    "기타",
]
CURIOUS_OPTIONS = [
    "공식 라이선스 여부",
    "원본과의 시각적 차이",
    "판매자·판매처",
    "최초 게시·판매 시점",
    "권리자 대응 여부",
    "기타",
]


class SurveyApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("ArtGuard 통합 인터뷰 기록")
        self.root.geometry("900x880")
        self.root.minsize(760, 650)
        self.root.configure(bg="#f6f7fb")

        self.vars: dict[str, tk.StringVar] = {}
        self.texts: dict[str, tk.Text] = {}
        self.curious_vars = {item: tk.BooleanVar(value=False) for item in CURIOUS_OPTIONS}

        self._configure_style()
        self._build_scroll_area()
        self._build_form()
        self._bind_scroll()

    def _configure_style(self) -> None:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        style.configure("TFrame", background="#ffffff")
        style.configure("Header.TLabel", background="#ffffff", foreground="#172033", font=("Malgun Gothic", 18, "bold"))
        style.configure("Sub.TLabel", background="#ffffff", foreground="#657085", font=("Malgun Gothic", 10))
        style.configure("Section.TLabel", background="#ffffff", foreground="#d84b32", font=("Malgun Gothic", 13, "bold"))
        style.configure("Question.TLabel", background="#ffffff", foreground="#172033", font=("Malgun Gothic", 10, "bold"))
        style.configure("TLabel", background="#ffffff", font=("Malgun Gothic", 10))
        style.configure("TRadiobutton", background="#ffffff", font=("Malgun Gothic", 10))
        style.configure("TCheckbutton", background="#ffffff", font=("Malgun Gothic", 10))
        style.configure("Accent.TButton", font=("Malgun Gothic", 11, "bold"), padding=(16, 10))

    def _build_scroll_area(self) -> None:
        outer = tk.Frame(self.root, bg="#f6f7fb")
        outer.pack(fill="both", expand=True, padx=18, pady=18)
        self.canvas = tk.Canvas(outer, bg="#f6f7fb", highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.form = ttk.Frame(self.canvas, padding=28)
        self.window = self.canvas.create_window((0, 0), window=self.form, anchor="nw")
        self.form.bind("<Configure>", lambda _e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.window, width=e.width))

    def _bind_scroll(self) -> None:
        self.root.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-e.delta / 120), "units"))

    def _section(self, title: str, description: str = "") -> None:
        ttk.Separator(self.form).pack(fill="x", pady=(24, 16))
        ttk.Label(self.form, text=title, style="Section.TLabel").pack(anchor="w")
        if description:
            ttk.Label(self.form, text=description, style="Sub.TLabel", wraplength=790).pack(anchor="w", pady=(4, 10))

    def _radio(self, key: str, label: str, choices: list[str]) -> None:
        ttk.Label(self.form, text=label, style="Question.TLabel", wraplength=790).pack(anchor="w", pady=(12, 5))
        var = self.vars[key] = tk.StringVar(value="")
        row = ttk.Frame(self.form)
        row.pack(fill="x", anchor="w")
        for choice in choices:
            ttk.Radiobutton(row, text=choice, value=choice, variable=var).pack(side="left", padx=(0, 16), pady=3)

    def _entry(self, key: str, label: str) -> None:
        ttk.Label(self.form, text=label, style="Question.TLabel", wraplength=790).pack(anchor="w", pady=(12, 5))
        var = self.vars[key] = tk.StringVar(value="")
        ttk.Entry(self.form, textvariable=var).pack(fill="x")

    def _combo(self, key: str, label: str, values: list[str]) -> None:
        ttk.Label(self.form, text=label, style="Question.TLabel", wraplength=790).pack(anchor="w", pady=(12, 5))
        var = self.vars[key] = tk.StringVar(value="")
        ttk.Combobox(self.form, textvariable=var, values=values, state="readonly").pack(fill="x")

    def _text(self, key: str, label: str, height: int = 3) -> None:
        ttk.Label(self.form, text=label, style="Question.TLabel", wraplength=790).pack(anchor="w", pady=(12, 5))
        widget = tk.Text(self.form, height=height, wrap="word", font=("Malgun Gothic", 10), relief="solid", borderwidth=1)
        widget.pack(fill="x")
        self.texts[key] = widget

    def _build_form(self) -> None:
        self.id_label = ttk.Label(self.form, text="", style="Header.TLabel")
        self.id_label.pack(anchor="w")
        ttk.Label(
            self.form,
            text="E1 문제 검증과 E2 리포트 평가를 한 번에 기록합니다. 이름·연락처·계정명은 입력하지 마세요.",
            style="Sub.TLabel",
            wraplength=790,
        ).pack(anchor="w", pady=(5, 0))
        self._refresh_id()

        self._section("0. 동의", "익명 기록 동의가 ‘아니요’면 어떤 응답도 저장하지 않습니다.")
        self._radio("consent_record", "0-1. 익명 ID로 과제 저장소에 답변을 기록해도 되나요?", ["예", "아니요"])
        self._radio("consent_quote", "0-2. 한 문장 의견을 익명으로 공개 인용해도 되나요?", ["예", "아니요"])

        self._section("E1. 문제 검증", "M1 계산에 필요한 참여자 적합성·문제 빈도·후속 참여 의향을 확인합니다.")
        self._combo("participant_type", "1. 참여자 유형", PARTICIPANT_TYPES)
        self._radio("creator_exp", "2. 온라인에 작품을 공개하거나 굿즈로 판매한 경험", ["있음", "없음"])
        self._entry("creator_form", "2-1. 경험이 있다면 간단한 형태 (없으면 비워 두기)")
        self._entry(
            "seen_case_route",
            "3. 최근 접한 유사 굿즈·이미지 논란 사례와 처음 본 경로 (없으면 ‘본 적 없음’)",
        )

        ttk.Label(self.form, text="4. 그 사례에서 궁금했던 정보 (복수 선택)", style="Question.TLabel").pack(anchor="w", pady=(12, 5))
        checks = ttk.Frame(self.form)
        checks.pack(fill="x", anchor="w")
        for index, item in enumerate(CURIOUS_OPTIONS):
            ttk.Checkbutton(checks, text=item, variable=self.curious_vars[item]).grid(row=index // 3, column=index % 3, sticky="w", padx=(0, 20), pady=3)
        self._combo("top_curiosity", "4-1. 그중 가장 필요한 정보", CURIOUS_OPTIONS)
        self._radio("check_freq", "5. 비슷한 상품의 진위·출처·유사성을 확인하는 빈도", ["월1회이상", "분기1회", "거의없음"])
        self._text("current_method", "6. 현재 확인 방법과 가장 불편한 점")
        self._entry("current_minutes", "6-1. 한 번 확인할 때 걸리는 시간(분, 숫자)")
        self._radio("followup_intent", "9. ArtGuard 후속 테스트 참여 의향", ["있음", "없음"])
        self._text("followup_reason", "9-1. 참여하거나 참여하지 않으려는 이유", height=2)

        self._section("E2. 리포트 평가", "샘플 리포트를 보여 준 뒤, 현재 방식과 비교해 각 항목을 1~5점으로 평가합니다.")
        for key, label in SCORE_LABELS.items():
            self._combo(key, f"7. {label}", ["1", "2", "3", "4", "5"])
        self._text("least_useful", "7-1. 가장 쓸모없거나 헷갈린 항목", height=2)
        self._text("missing_info", "7-2. 리포트에 없어서 아쉬운 정보", height=2)
        self._radio(
            "action_after_report",
            "8. 리포트를 본 뒤 가장 먼저 할 행동",
            ["저장", "원문방문", "추가검토요청", "지인공유", "행동없음", "기타"],
        )
        self._text("trust_concern", "10. 가장 우려되는 신뢰 문제", height=2)

        self._section("마무리")
        self._text("quote", "12. 공개 가능한 한 문장 의견 (인용 동의가 ‘예’일 때만)", height=2)
        self._text("note", "면담자 메모 (지인 편향, 통화 상황 등 — 개인정보 제외)", height=2)

        buttons = ttk.Frame(self.form)
        buttons.pack(fill="x", pady=(26, 10))
        ttk.Button(buttons, text="응답 저장", style="Accent.TButton", command=self.save).pack(side="left")
        ttk.Button(buttons, text="새 응답", command=self.clear).pack(side="left", padx=10)
        ttk.Button(buttons, text="저장 폴더 열기", command=self.open_folder).pack(side="left")

    def _refresh_id(self) -> None:
        self.id_label.configure(text=f"ArtGuard 통합 설문 · {next_id()}")

    def _value(self, key: str) -> str:
        if key in self.vars:
            return self.vars[key].get().strip()
        return self.texts[key].get("1.0", "end").strip()

    def _collect(self) -> dict[str, str]:
        result = {key: self._value(key) for key in set(self.vars) | set(self.texts)}
        result["participant_id"] = next_id()
        result["date"] = datetime.date.today().isoformat()
        result["curious_items"] = "; ".join(item for item, var in self.curious_vars.items() if var.get())
        return result

    def _validate(self, row: dict[str, str]) -> bool:
        if row["consent_record"] != "예":
            messagebox.showwarning("저장하지 않음", "익명 기록 동의가 없으므로 응답을 저장하지 않습니다.")
            return False
        required = {
            "consent_quote": "익명 의견 공개 인용 동의",
            "participant_type": "참여자 유형",
            "creator_exp": "작품 공개·판매 경험",
            "check_freq": "확인 빈도",
            "current_method": "현재 확인 방법",
            "current_minutes": "확인 소요 시간",
            "top_curiosity": "가장 필요한 정보",
            "followup_intent": "후속 참여 의향",
            "followup_reason": "후속 참여 이유",
            "action_after_report": "리포트 후 행동",
            "trust_concern": "신뢰 문제",
        }
        missing = [label for key, label in required.items() if not row.get(key)]
        missing += [label for key, label in SCORE_LABELS.items() if not row.get(key)]
        if not row["curious_items"]:
            missing.append("궁금했던 정보")
        if missing:
            messagebox.showerror("필수 항목 확인", "다음 항목을 입력해 주세요:\n\n- " + "\n- ".join(missing))
            return False
        try:
            minutes = float(row["current_minutes"])
            if minutes < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("입력 확인", "확인 소요 시간은 0 이상의 숫자로 입력해 주세요.")
            return False
        if row["consent_quote"] == "예" and not row["quote"]:
            messagebox.showerror("입력 확인", "인용에 동의했다면 공개 가능한 한 문장 의견을 입력해 주세요.")
            return False
        if row["consent_quote"] == "아니요":
            row["quote"] = ""
        return True

    def save(self) -> None:
        row = self._collect()
        if not self._validate(row):
            return
        ensure_storage()
        with open(CSV, "a", newline="", encoding="utf-8") as file:
            csv.DictWriter(file, fieldnames=FIELDS).writerow({key: row.get(key, "") for key in FIELDS})
        markdown = [f"# {row['participant_id']} ({row['date']})", ""]
        for key in FIELDS:
            if key in {"participant_id", "date"}:
                continue
            markdown.append(f"- **{FIELD_LABELS.get(key, key)}**: {row.get(key, '')}")
        participant_path = os.path.join(PDIR, f"{row['participant_id']}.md")
        with open(participant_path, "w", encoding="utf-8") as file:
            file.write("\n".join(markdown) + "\n")
        messagebox.showinfo("저장 완료", f"{row['participant_id']} 응답을 저장했습니다.\n\n{participant_path}")
        self.clear()

    def clear(self) -> None:
        for var in self.vars.values():
            var.set("")
        for widget in self.texts.values():
            widget.delete("1.0", "end")
        for var in self.curious_vars.values():
            var.set(False)
        self.canvas.yview_moveto(0)
        self._refresh_id()

    def open_folder(self) -> None:
        ensure_storage()
        os.startfile(os.path.dirname(CSV))


def main() -> None:
    ensure_storage()
    root = tk.Tk()
    SurveyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
