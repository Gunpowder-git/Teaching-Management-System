#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 教学管理系统 Demo（与给定 C++ 功能一致，并增加可视化）

需求要点：
- 10名学生，3门课（高等数学/英语/计算机程序设计），学分 5/3/4
- 面向对象：Student 类（学号、姓名、三门课成绩、绩点），ClassRoom 类
- 计算每位学生：每门课绩点 + 加权平均绩点（按学分加权）
- 按平均绩点降序排序输出
- 输出到 CSV 文件：学号、姓名、每门课绩点、平均绩点（这里也额外保留了原始成绩，方便核对）
- matplotlib 可视化：①各学生三门课成绩分组柱状图 ②绩点分布柱状图

说明：
- 绩点换算与 C++ 附件保持一致（100分制 -> 0/2/3/4/5）：
    >=90: 5.0
    >=80: 4.0
    >=70: 3.0
    >=60: 2.0
    <60 : 0.0
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import csv
import argparse

import matplotlib.pyplot as plt

# 尝试设置中文字体（不同系统字体不同，尽量兼容；若仍有警告，不影响功能）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


COURSES = ["高等数学", "英语", "计算机程序设计"]
CREDITS = {"高等数学": 5.0, "英语": 3.0, "计算机程序设计": 4.0}
TOTAL_CREDITS = sum(CREDITS.values())


def score_to_gpa(score: float) -> float:
    """单科绩点：与给定 C++ 版本保持一致（0/2/3/4/5）"""
    if score >= 90:
        return 5.0
    if score >= 80:
        return 4.0
    if score >= 70:
        return 3.0
    if score >= 60:
        return 2.0
    return 0.0


@dataclass
class Student:
    student_id: str
    name: str
    scores: Dict[str, float]  # course -> score (0-100)

    gpas: Dict[str, float] = field(default_factory=dict)
    avg_gpa: float = 0.0

    def compute_gpa(self) -> None:
        """计算每门课绩点与加权平均绩点"""
        self.gpas = {c: score_to_gpa(self.scores[c]) for c in COURSES}
        weighted = sum(self.gpas[c] * CREDITS[c] for c in COURSES)
        self.avg_gpa = weighted / TOTAL_CREDITS

    def as_row(self) -> Dict[str, str]:
        """用于输出 CSV"""
        return {
            "学号": self.student_id,
            "姓名": self.name,
            "高等数学成绩": f"{self.scores['高等数学']:.1f}",
            "英语成绩": f"{self.scores['英语']:.1f}",
            "程序设计成绩": f"{self.scores['计算机程序设计']:.1f}",
            "高等数学绩点": f"{self.gpas['高等数学']:.2f}",
            "英语绩点": f"{self.gpas['英语']:.2f}",
            "程序设计绩点": f"{self.gpas['计算机程序设计']:.2f}",
            "平均绩点": f"{self.avg_gpa:.2f}",
        }


class ClassRoom:
    def __init__(self, class_name: str):
        self.class_name = class_name
        self.students: List[Student] = []

    def add_student(self, student: Student) -> None:
        """添加学生（检查学号重复）"""
        if any(s.student_id == student.student_id for s in self.students):
            raise ValueError(f"学号已存在：{student.student_id}")
        student.compute_gpa()
        self.students.append(student)

    def sort_by_avg_gpa(self, reverse: bool = True) -> None:
        self.students.sort(key=lambda s: s.avg_gpa, reverse=reverse)

    def print_table(self) -> None:
        """控制台输出（简洁表格）"""
        print(f"\n========== {self.class_name} 学生成绩表 ==========")
        header = ["学号", "姓名", "数学", "英语", "程序设计", "平均绩点"]
        print("{:<12}{:<10}{:<8}{:<8}{:<10}{:<8}".format(*header))
        print("-" * 58)
        for s in self.students:
            print("{:<12}{:<10}{:<8.1f}{:<8.1f}{:<10.1f}{:<8.2f}".format(
                s.student_id, s.name,
                s.scores["高等数学"], s.scores["英语"], s.scores["计算机程序设计"],
                s.avg_gpa
            ))
        print("-" * 58)

    def save_to_csv(self, filename: str) -> None:
        """输出到 CSV 文件"""
        fieldnames = [
            "学号", "姓名",
            "高等数学成绩", "英语成绩", "程序设计成绩",
            "高等数学绩点", "英语绩点", "程序设计绩点",
            "平均绩点",
        ]
        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for s in self.students:
                w.writerow(s.as_row())

    # ---------------- 可视化 ----------------
    def plot_scores_bar(self, out_png: str, show: bool = False) -> None:
        """分组柱状图：每位学生三门课成绩"""
        names = [s.name for s in self.students]
        math_scores = [s.scores["高等数学"] for s in self.students]
        eng_scores = [s.scores["英语"] for s in self.students]
        prog_scores = [s.scores["计算机程序设计"] for s in self.students]

        x = list(range(len(names)))
        width = 0.25

        plt.figure(figsize=(12, 5))
        plt.bar([i - width for i in x], math_scores, width=width, label="高等数学")
        plt.bar(x, eng_scores, width=width, label="英语")
        plt.bar([i + width for i in x], prog_scores, width=width, label="程序设计")
        plt.xticks(x, names, rotation=30, ha="right")
        plt.ylabel("成绩（0-100）")
        plt.title(f"{self.class_name} 三门课成绩对比（分组柱状图）")
        plt.legend()
        plt.tight_layout()
        plt.savefig(out_png, dpi=200)
        if show:
            plt.show()
        plt.close()

    def plot_gpa_distribution(self, out_png: str, show: bool = False) -> None:
        """平均绩点分布柱状图（区间同 C++ 文本统计）"""
        bins = [
            ("4.00-5.00", 0),
            ("3.00-3.99", 0),
            ("2.00-2.99", 0),
            ("1.00-1.99", 0),
            ("0.00-0.99", 0),
        ]
        counts = {k: 0 for k, _ in bins}
        for s in self.students:
            g = s.avg_gpa
            if g >= 4.0:
                counts["4.00-5.00"] += 1
            elif g >= 3.0:
                counts["3.00-3.99"] += 1
            elif g >= 2.0:
                counts["2.00-2.99"] += 1
            elif g >= 1.0:
                counts["1.00-1.99"] += 1
            else:
                counts["0.00-0.99"] += 1

        labels = list(counts.keys())
        values = [counts[k] for k in labels]

        plt.figure(figsize=(8, 4))
        plt.bar(labels, values)
        plt.ylabel("人数")
        plt.title(f"{self.class_name} 平均绩点分布")
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout()
        plt.savefig(out_png, dpi=200)
        if show:
            plt.show()
        plt.close()


def build_demo_classroom() -> ClassRoom:
    """初始化 10 名学生（与附件 C++ 示例数据一致）"""
    cr = ClassRoom("计算机科学与技术1班")
    demo_data = [
        ("2024001", "张三", 85.5, 92.0, 78.5),
        ("2024002", "李四", 76.0, 88.5, 91.0),
        ("2024003", "王五", 93.0, 93.0, 94.5),
        ("2024004", "赵六", 68.5, 72.0, 65.0),
        ("2024005", "钱七", 88.0, 91.5, 86.0),
        ("2024006", "孙八", 72.5, 68.0, 79.5),
        ("2024007", "周九", 95.0, 87.0, 94.0),
        ("2024008", "吴十", 81.0, 76.5, 82.0),
        ("2024009", "郑十一", 64.0, 70.0, 73.5),
        ("2024010", "王十二", 89.5, 94.0, 88.5),
    ]
    for sid, name, m, e, p in demo_data:
        s = Student(
            student_id=sid,
            name=name,
            scores={"高等数学": m, "英语": e, "计算机程序设计": p},
        )
        cr.add_student(s)
    return cr


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-csv", default="student_scores.csv", help="输出 CSV 文件名")
    parser.add_argument("--score-fig", default="scores_bar.png", help="成绩柱状图输出文件名")
    parser.add_argument("--gpa-fig", default="gpa_dist.png", help="绩点分布图输出文件名")
    parser.add_argument("--show", action="store_true", help="显示图形窗口（可选）")
    args = parser.parse_args()

    classroom = build_demo_classroom()

    print("【原始数据】")
    classroom.print_table()

    classroom.sort_by_avg_gpa(reverse=True)
    print("\n【排序后数据（按平均绩点降序）】")
    classroom.print_table()

    classroom.save_to_csv(args.out_csv)
    print(f"\n已输出到文件：{args.out_csv}")

    classroom.plot_scores_bar(args.score_fig, show=args.show)
    classroom.plot_gpa_distribution(args.gpa_fig, show=args.show)
    print(f"已生成图表：{args.score_fig}、{args.gpa_fig}")


if __name__ == "__main__":
    main()
