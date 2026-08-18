#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Secluded 词库语法校验器
用法: python3 check_wordlib.py <词库文件> [更多文件...]

依据 SKILL.md 规范检查:
  1. 变量名 1/3 字节规则（1字节字母 或 3字节/1汉字）
  2. % 配对与转义
  3. 非内置变量引用提示（确认是否已在词库内定义）
  4. 词汇头过宽警告
  5. 连续空行警告
  6. 末尾 AI 生成注明（影响词库运行）
  7. 最后一行字面 \n 警告

退出码: 0=通过, 1=有错误, 2=用法错误
"""

import re
import sys
from pathlib import Path

BUILTIN_VARS = {
    "群主QQ", "QQ", "群", "群号", "时间戳毫秒", "时间戳进程",
    "上线模式", "消息来源", "括号1", "括号2", "括号3",
    "随机数", "空格", "换行", "回车", "当前时间", "日期",
    "昵称", "用户昵称", "图片", "语音", "文本", "原文本",
}

AI_MARK_PATTERNS = [
    r"AI\s*生成", r"内容由AI", r"仅供参考", r"由AI生成", r"ChatGPT 生成",
]

WIDE_HEADER_HINTS = [
    (r"^\(\[0-9\]\+\)$", "纯数字匹配会拦截所有数字消息，建议加前缀"),
    (r"^\(\[\\s\\S\]\*\)$", "全匹配含换行，触发面过大，确认是否必要"),
]


def is_valid_var(name: str) -> bool:
    return len(name.encode("utf-8")) in (1, 3)


def check_file(path: str):
    p = Path(path)
    if not p.exists():
        print(f"[错误] 文件不存在: {path}")
        return 1, 0
    try:
        lines = p.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        print(f"[错误] 无法按 UTF-8 读取: {path}")
        return 1, 0

    errors, warns = [], []
    text = "\n".join(lines)
    if not text.strip():
        errors.append("文件为空")

    # 末尾 AI 生成注明
    tail = text[-300:]
    for pat in AI_MARK_PATTERNS:
        if re.search(pat, tail, re.IGNORECASE):
            errors.append(f"末尾命中疑似 AI 生成注明: {pat!r}，会被引擎当词库内容解析导致运行异常")
            break

    # 收集词库内已定义的变量（冒号赋值形式）
    defined = set()
    for line in lines:
        m = re.match(r"^([^$:\s][^:\s]*):", line)
        if m:
            defined.add(m.group(1))

    in_block = False
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s:
            # 空行 = 块分隔；连续空行属于多余结构
            if i >= 2 and not lines[i - 2].strip():
                warns.append(f"L{i}: 连续空行（块间一个空行即可，多余空行易导致块误截断）")
            in_block = False
            continue
        if s.startswith(("//", "##", "&&")) or s.startswith("[系统消息]") or s.startswith(":"):
            in_block = True
            continue
        if not in_block:
            # 词汇头行
            in_block = True
            for pat, hint in WIDE_HEADER_HINTS:
                if re.fullmatch(pat, s):
                    warns.append(f"L{i}: 词汇头过宽 {s!r} —— {hint}")
            continue

        # 赋值行：变量名 1/3 字节检查（跳过流程控制关键词）
        m = re.match(r"^([^$:\s][^:\s]*):", s)
        if m and m.group(1) not in ("如果", "elif", "else"):
            name = m.group(1)
            b = len(name.encode("utf-8"))
            if b not in (1, 3):
                errors.append(f"L{i}: 变量名 {name!r} 为 {b} 字节，只允许 1 或 3 字节，否则赋值行会被当文本输出")
            defined.add(name)

        # % 配对检查（排除已转义的 \%）
        pct = re.findall(r"(?<!\\)%", s)
        if len(pct) % 2 == 1:
            errors.append(f"L{i}: % 出现奇数个({len(pct)})，存在未转义/未配对 %，应写 \\%")

        # 非内置变量引用提示
        for var in re.findall(r"(?<!\\)%([^%\s]+)%", s):
            if var not in BUILTIN_VARS and var not in defined:
                warns.append(f"L{i}: 引用非内置变量 %{var}%，若未在词库中定义过将取不到值")

        # 疑似函数嵌套
        if s.count("$") >= 4:
            warns.append(f"L{i}: 行内出现 {s.count('$')} 个 $，疑似函数嵌套（不支持）或参数含 $")

    # 最后一行字面 \n
    if lines and lines[-1].rstrip().endswith("\\n"):
        warns.append(f"L{len(lines)}: 最后一行以 \\n 结尾，规范要求最后一行末尾不加 \\n")

    print(f"===== {p.name} =====")
    for e in errors:
        print(f"  [错误] {e}")
    for w in warns:
        print(f"  [警告] {w}")
    if not errors and not warns:
        print("  PASS: 0 错误 0 警告")
    print(f"结果: {len(errors)} 错误, {len(warns)} 警告\n")
    return len(errors), len(warns)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 check_wordlib.py <词库文件> [更多文件...]")
        return 2
    total_e = total_w = 0
    for f in sys.argv[1:]:
        e, w = check_file(f)
        total_e += e
        total_w += w
    print(f"总计: {total_e} 错误, {total_w} 警告")
    return 1 if total_e else 0


if __name__ == "__main__":
    sys.exit(main())
