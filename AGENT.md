# AGENT.md — 技能使用说明（给调用方 Agent）/ Usage Guide (for the Calling Agent)

本文件支持中英双语，便于 AI 理解；**产出词库正文一律使用中文**。
This file is bilingual for AI comprehension; **word library output must be in Chinese**.

---

## 中文版

### 技能用途
本技能用于编写、修改、审查 Secluded 框架的 QQ 机器人词库（.txt 纯文本），保证产出符合语法规范、可直接加载运行。

### 加载时机
当用户请求涉及以下内容时，加载本技能：
- 编写新的 Secluded 词库 / 词库功能
- 修改或审查现有词库（触发词、菜单、权限、卡片等）
- 询问 Secluded 语法、变量规则、函数用法

### 使用流程
按 `SKILL.md` 第 12 章标准作业流程执行：确认需求 → 查变量大全 → 设计结构 → 编写 → 运行校验脚本自检 → 交付。

### 职责边界
- 只产出 .txt 词库文件，不创建其它类型产物
- 不触碰用户业务词库；示例词库必须原创，禁止直接使用用户业务词库作示例
- 不擅自修改用户系统配置、不执行与词库开发无关的操作
- 拿不准的函数/变量必须查 `references/Secluded变量大全.txt`，禁止编造

### 交付规范
交付时给出：词库文件路径 + 新增/改动说明 + 触发词列表。词库末尾严禁任何 AI 生成注明。

### 语言约束（硬性）
技能文档双语仅为方便 AI 理解；**交付的词库正文必须使用中文**，除非用户明确要求其他语言。

---

## English Version

### Purpose
This skill writes, modifies, and reviews Secluded-framework QQ bot word libraries (.txt plain text), ensuring output is syntax-compliant and ready to load.

### When to Load
Load this skill when the user asks to:
- Write a new Secluded word library or feature
- Modify or review an existing word library (triggers, menus, permissions, cards, etc.)
- Ask about Secluded syntax, variable rules, or function usage

### Workflow
Follow the standard workflow in `SKILL.md` §12: confirm requirements → consult the variable encyclopedia → design structure → write → run the check script → deliver.

### Boundaries
- Produce .txt word library files only
- Never touch the user's business word libraries; examples must be original, never derived from user business libraries
- Never modify user system settings or do anything unrelated to word library development
- When unsure about a function/variable, consult `references/Secluded变量大全.txt` — never fabricate

### Delivery Norms
Deliver with: word library file path + change summary + trigger word list. Never append AI-generated disclaimers at the end.

### Language Constraint (Hard Rule)
The bilingual documentation is only for AI comprehension; **delivered word library content must be in Chinese**, unless the user explicitly requests another language.