# Python 教学管理系统 / Python Teaching Management System

## 中文简介

这是一个由 C++ 简易教学管理系统迁移到 Python 的课程作业项目。项目使用面向对象编程方法，定义了 `Student` 学生类和 `ClassRoom` 班级类，实现了学生成绩管理、单科绩点计算、学分加权平均绩点计算、按平均绩点排序、CSV 文件导出，并额外加入了 `matplotlib` 可视化功能。

本项目模拟一个班级中 10 名学生的三门课程成绩：

- 高等数学
- 英语
- 计算机程序设计

三门课程对应学分分别为：

| 课程 | 学分 |
|---|---:|
| 高等数学 | 5 |
| 英语 | 3 |
| 计算机程序设计 | 4 |

---

## English Introduction

This is a Python course project migrated from a simple C++ teaching management system. The project uses object-oriented programming and defines a `Student` class and a `ClassRoom` class. It supports student grade management, course GPA calculation, credit-weighted average GPA calculation, GPA-based ranking, CSV export, and additional data visualization with `matplotlib`.

The project simulates a class of 10 students with scores in three courses:

- Advanced Mathematics
- English
- Computer Programming

Course credits:

| Course | Credit |
|---|---:|
| Advanced Mathematics | 5 |
| English | 3 |
| Computer Programming | 4 |

---

## 功能 Features

### 中文

- 初始化 10 名学生的课程成绩
- 使用面向对象方式管理学生和班级
- 将 100 分制成绩转换为绩点
- 按课程学分计算加权平均绩点
- 按平均绩点降序排序学生
- 在控制台输出原始数据和排序后数据
- 导出学生成绩与绩点到 `student_scores.csv`
- 生成两张可视化图表：
  - `scores_bar.png`：三门课程成绩分组柱状图
  - `gpa_dist.png`：平均绩点分布柱状图

### English

- Initialize course scores for 10 students
- Manage students and class information using object-oriented programming
- Convert 100-point scores to GPA values
- Calculate credit-weighted average GPA
- Sort students by average GPA in descending order
- Print original and sorted student data in the terminal
- Export student scores and GPA results to `student_scores.csv`
- Generate two visualization charts:
  - `scores_bar.png`: grouped bar chart of course scores
  - `gpa_dist.png`: average GPA distribution chart

---

## 绩点换算规则 / GPA Conversion Rule

| 分数区间 Score Range | 绩点 GPA |
|---|---:|
| >= 90 | 5.0 |
| >= 80 and < 90 | 4.0 |
| >= 70 and < 80 | 3.0 |
| >= 60 and < 70 | 2.0 |
| < 60 | 0.0 |

平均绩点采用学分加权计算：

```text
平均绩点 = Σ(单科绩点 × 课程学分) / 总学分
