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
1. 按 `SKILL.md` 子技能路由判断功能类型，管理类加载 `skills/secluded-skill-admin/skill.md`，娱乐类加载 `skills/secluded-skill-fun/skill.md`
2. 按 `SKILL.md` 第 12 章标准作业流程执行：确认需求 → **先分析规划并向用户复述确认** → 查变量大全/参考词库（参考不抄）→ 设计结构 → 编写 → 运行校验脚本自检 → 交付
3. 涉及授权函数按 `SKILL.md` 第 14 章三选一询问确认

### 检查更新（每次使用前建议执行）
核对当前安装版本与 GitHub 最新版本，旧版提示更新：
1. 读取本地 `meta.json` 的 `version` 字段
2. 请求远程最新版本：`https://raw.githubusercontent.com/cy-api/secluded-skill/main/meta.json`，解析其 `version` 字段
3. 对比：
   - 相同 → 已是最新，正常使用
   - 远程版本更新 → 告知用户存在新版本，并给出更新方式：
     - git 方式安装：在技能目录内执行 `git pull`
     - 手动安装（解压 zip）：请用户重新下载最新 zip 覆盖原目录
4. 更新动作必须先经用户确认，禁止未经确认擅自覆盖或删除文件

### 功能授权约束（硬性）
- 默认**不调用任何需要 Secluded 授权的函数**（授权函数清单见 `SKILL.md` 第 14 章）
- 用户需求指向授权函数时，必须三选一提问确认（A 原生函数效果 / B 文本同类效果 / C 其他自由输入），禁止猜测、禁止擅自写
- 用户选 A 后，只有用户明确声明本账号已获 Secluded 授权才可写；未声明/未知则不写并说明
- 即使有授权，也只按需求**适量补充**授权功能，不按清单全量堆砌

### 职责边界
- 只产出 .txt 词库文件，不创建其它类型产物
- 不触碰用户业务词库；示例词库必须原创，禁止直接使用用户业务词库作示例
- 不擅自修改用户系统配置、不执行与词库开发无关的操作
- 拿不准的函数/变量必须查 `references/Secluded变量大全.txt`，禁止编造

### 交付规范
交付时给出：词库文件路径 + 新增/改动说明 + 触发词列表。词库末尾严禁任何 AI 生成注明。**必须告知授权状态**：本词库默认未使用 Secluded 授权函数（授权状态未知）；如需原生授权效果，请用户声明账号已获 Secluded 授权后按需补充。

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
1. Classify the request via `SKILL.md` sub-skill routing; load `skills/secluded-skill-admin/skill.md` for admin-type or `skills/secluded-skill-fun/skill.md` for fun-type
2. Follow the standard workflow in `SKILL.md` §12: confirm requirements → **analyze, plan, and confirm with the user before writing** → consult the variable encyclopedia/reference libraries (reference, not copy) → design structure → write → run the check script → deliver
3. For authorized functions, follow the three-way question in `SKILL.md` §14

### Check for Updates (recommended before each use)
Verify the installed version against the latest one on GitHub; prompt an update if outdated:
1. Read the `version` field from the local `meta.json`
2. Request the remote version: `https://raw.githubusercontent.com/cy-api/secluded-skill/main/meta.json` and parse its `version` field
3. Compare:
   - Same → already up to date, proceed
   - Remote is newer → tell the user a new version exists and how to update:
     - Installed via git: run `git pull` inside the skill directory
     - Manually installed (extracted zip): ask the user to re-download the latest zip and overwrite the directory
4. Never overwrite or delete files without explicit user confirmation

### Feature Authorization Restrictions (Hard Rule)
- Never call any Secluded-authorized function by default (see `SKILL.md` §14 for the list)
- When a request targets an authorized function, you MUST ask a three-way question (A native function effect / B text-implementable effect / C other free input) — never guess, never write on your own
- After the user picks A, write only if the user explicitly declares this account has Secluded authorization; otherwise do not write and explain why
- Even with authorization, add only as needed — never dump the whole list

### Boundaries
- Produce .txt word library files only
- Never touch the user's business word libraries; examples must be original, never derived from user business libraries
- Never modify user system settings or do anything unrelated to word library development
- When unsure about a function/variable, consult `references/Secluded变量大全.txt` — never fabricate

### Delivery Norms
Deliver with: word library file path + change summary + trigger word list. Never append AI-generated disclaimers at the end. **Always state the authorization status**: this word library uses no Secluded-authorized functions by default (authorization status unknown); for native authorized effects, ask the user to declare Secluded authorization and add on demand.

### Language Constraint (Hard Rule)
The bilingual documentation is only for AI comprehension; **delivered word library content must be in Chinese**, unless the user explicitly requests another language.