
# 🤖 Secluded 词库开发技能包

> 让 AI 学会为 Secluded 框架编写可直接运行的 QQ 机器人词库（.txt 纯文本）。

本技能包沉淀了 Secluded 词库开发的完整规范：语法结构、变量字节规则、转义、流程控制、函数清单、菜单与权限设计、接口 JSON 取值，以及一套自动化校验工具。目标是让任何 AI 拿到本包后，都能写出**符合规范、可直接加载运行、无多余污染**的词库文件。

**English Version 见文末 / English version at the bottom.**

---

## 中文版

### 目录

- [项目简介](#项目简介)
- [特性](#特性)
- [目录结构](#目录结构)
- [安装方法](#安装方法)
- [快速开始](#快速开始)
- [语法速览](#语法速览)
- [接口对接与 JSON 取值](#接口对接与-json-取值)
- [自动校验](#自动校验)
- [菜单与权限规范](#菜单与权限规范)
- [语言说明](#语言说明)
- [License](#license)

### 项目简介

Secluded 是一个 QQ 机器人词库/自定义回复框架。词库文件为纯文本 `.txt`，由多个**词汇块**组成，每个词汇块 = 触发正则（词汇头）+ 执行内容（词汇体）。引擎按词汇块逐行解析执行。

本技能包解决的核心问题：

1. **语法规范复杂**：变量名有严格的字节限制（1 字节或 3 字节），写错会把赋值行当文本输出到群里
2. **转义陷阱多**：`%` 未转义会被当变量解析，导致词库运行异常
3. **验收成本高**：词库写完需要反复测试，本包提供自动校验脚本，一次扫描常见错误
4. **内容纯净性**：严禁在词库末尾添加 AI 生成注明等多余行，否则会被引擎解析执行

### 特性

- ✅ 完整语法规范：结构、变量、转义、注释、流程控制、函数
- ✅ 变量字节规则详解：1 字节 / 3 字节（含真实踩坑案例）
- ✅ 内置变量清单：优先使用内置变量，避免重复造轮子
- ✅ 卡片/消息构造：组合式消息、多媒体卡片模板
- ✅ 菜单设计规范：三层结构、四字菜单名、一行两项对齐、`\n` 换行
- ✅ 权限分级体系：全局主人 → 主人 → 群主 → 管理员 → 手动白名单
- ✅ 接口对接规范：实际请求验证 JSON 结构，用 `@变量[键]` 取值
- ✅ 高频踩坑清单：8 条血泪教训
- ✅ 自动校验脚本：扫描变量字节、`%` 转义、未知变量、空行、AI 注明残留
- ✅ 原创示例词库：许愿池 + 菜单 + 权限的完整范例
- ✅ 中英双语文档：便于 AI 理解，词库正文始终为中文

### 目录结构

```
secluded-skill/
├── SKILL.md                          # 技能主规范（13 章 + 接口对接小节）
├── AGENT.md                          # 技能使用说明（给调用方 Agent）
├── SOUL.md                           # 技能人格定义
├── README.md                         # 项目说明（本文件）
├── meta.json                         # 技能元信息（名称/图标/简介/作者/版本）
├── references/
│   └── Secluded变量大全.txt           # 全量变量与函数参考（8253 行，按需查阅）
├── examples/
│   └── 示例词库_菜单版_v1.txt         # 标准示例词库（许愿池+菜单+权限）
└── scripts/
    └── check_wordlib.py              # 词库语法校验器
```

### 安装方法

#### 方式一：Git 安装（推荐）

项目托管在 GitHub 后，可直接克隆：

```bash
git clone https://github.com/cy-api/secluded-skill
```

1. **获取技能包**：克隆仓库到本地（或在 GitHub 页面下载 zip 压缩包解压，效果相同），得到技能目录 `secluded-skill/`
2. **放入技能目录**：将整个技能目录放入 AI 环境的技能目录，通常为 `skills/custom/`（具体路径以你的 AI 框架文档为准）
3. **自动注册**：框架启动或扫描时会读取技能目录内的 `meta.json`，自动在技能列表中注册（显示名称、图标、简介、分类均由此文件控制）
4. **验证安装**：在对话中发起词库编写需求（如"帮我写一个签到词库"），若 AI 正确加载并调用本技能，即安装成功

#### 方式二：下载压缩包

在 GitHub 仓库页面点击 Code → Download ZIP，解压后按上述第 2~4 步操作即可。

### 快速开始

1. **阅读主规范**：先读 `SKILL.md`，掌握词库结构与核心规则
2. **按需查阅参考**：遇到不确定的函数/变量，grep `references/Secluded变量大全.txt`，禁止凭记忆猜测
3. **对照示例**：参考 `examples/示例词库_菜单版_v1.txt`，模仿其结构
4. **编写词库**：遵守标准作业流程（确认需求 → 查规范 → 设计结构 → 编写 → 自检 → 交付）
5. **运行校验**：

```bash
python3 scripts/check_wordlib.py <词库文件>
```

校验通过后交付。

### 语法速览

#### 词库结构

```
词汇头（触发正则）
词汇体（执行内容，不允许空行）

下一个词汇头
...
```

- 词汇块之间用**空行**分隔
- 词汇体**严禁出现空行**（空行即表示块结束）

#### 变量字节规则（最容易出错）

引擎按**字节**判定变量名合法性，只认 **1 字节** 或 **3 字节**：

| 变量名 | 字节数 | 是否合法 | 示例 |
|---|---|---|---|
| `A`、`B`、`I`、`s` | 1 | ✅ | `A:666` |
| `API`、`TXT`、`PKG`、`CUR` | 3 | ✅ | `API:$访问 url$` |
| `名`（1 个汉字） | 3 | ✅ | `名:@API[name]` |
| `当前值`（3 个汉字） | 9 | ❌ | 赋值行会被当文本输出 |

三种赋值形式：

```
A:666                          # 单字节变量
TXT:内容                       # 三字节变量（3 ASCII 或 1 汉字）
$变量 哈哈哈666 我是内容$       # 多字节键值
```

取值：`%变量名%`；JSON 取值：`@变量名[键]`，如 `名:@API[name]`。

#### 转义

文本中的 `%` 若不是变量引用，必须写成 `\%`：

```
错误：$写 应用 版本 v1%201.0.0$     # %20 会被当变量解析
正确：$写 应用 版本 v1\%201.0.0$
```

#### 流程控制

```
如果:条件
...
返回              # 结束本词汇（不回复）
如果尾
```

- 支持 `==`、`!=`、`>=`、`<=`、`|`（或）、`&`（与）
- `elif:` 多分支；`[...]` 为计算表达式

#### 核心函数

| 函数 | 语法 | 说明 |
|---|---|---|
| 读 | `$读 路径 键 默认值$` | 读配置 |
| 写 | `$写 路径 键 值$` | 写配置 |
| 访问 | `$访问 URL$` | HTTP 请求，结果存入变量 |
| 计算 | `$计算 表达式 取整方式$` | 数学计算 |
| 回调 | `$回调 词汇名$` | 调用另一个词汇块 |
| 休眠 | `$休眠 毫秒$` | 延时 |
| 全局变量 | `$全局变量 键 值$` | 定义全局变量 |
| 标签跳转 | `$标签跳转 标签名$` | 配合 `:标签名` 使用 |

### 接口对接与 JSON 取值

词库需要对接 HTTP 接口并解析响应 JSON 时：

1. **确认接口与参数**：`$访问 URL$` 发起请求，响应存入变量后用 `@变量[键]` 取值，如 `名:@API[name]`、`名:@API[data][name]`；多层路径用 `[键]` 逐级连接
2. **尽量实际请求验证**：写词库前先尝试真实请求一次接口，解析响应 JSON 结构，确认字段路径后再写进词库，禁止凭空猜字段名
3. **缺少参数先问用户**：接口需要但尚未提供的参数（如 token、签名、用户输入内容），先向用户提问补齐，禁止编造
4. **主动提供方案**：若不确定响应结构，可询问用户是否需要先实际请求一遍接口、解析 JSON 后把取值写成词库中需要对接的部分

### 自动校验

`scripts/check_wordlib.py` 会扫描以下问题：

| 检查项 | 类型 |
|---|---|
| 变量名超过 1/3 字节 | 错误 |
| `%` 未配对/未转义 | 错误 |
| 末尾 AI 生成注明 | 错误 |
| 词汇头过宽（如纯 `([0-9]+)`） | 警告 |
| 引用非内置且未定义的变量 | 警告 |
| 连续空行 | 警告 |
| 疑似函数嵌套 | 警告 |
| 最后一行以 `\n` 结尾 | 警告 |

```bash
python3 scripts/check_wordlib.py 词库.txt
# 输出：错误数 / 警告数 / 具体行号
```

### 菜单与权限规范

- 功能多时设计**主菜单 → 子菜单 → 具体功能**三层结构，入口统一
- 换行必须用 `\n`（文件内直接换行会被引擎拼接）
- 菜单默认简洁对称：非列表不编号，每行 2 个功能项，菜单名四字对齐
- 权限从高到低：**全局主人 → 主人 → 群主 → 管理员 → 手动白名单**
- 需要权限的功能做专属菜单，无权限者看不到内容
- 推荐把权限校验做成 `[内部]XXX校验` 词汇，用 `$回调` 复用

### 语言说明

技能文档（SKILL.md / AGENT.md / SOUL.md / README.md）支持中英双语，仅为方便 AI 理解规范。**产出词库正文一律使用中文**（触发词、回复文案、菜单、注释），除非用户明确要求其他语言。

### License

MIT License. 本技能包可自由使用、修改与分发。示例词库为原创内容，可直接用于学习与二次开发。

---

## English Version

### Overview

A skill pack for the **Secluded framework** (QQ bot word libraries / custom replies). It provides complete syntax rules, variable byte rules, escaping, control flow, function reference, menu & permission design guidelines, API JSON extraction conventions, and an automated checker to guarantee runnable `.txt` word libraries.

### Features

- ✅ Complete syntax specification: structure, variables, escaping, comments, control flow, functions
- ✅ Variable byte rules: only 1-byte or 3-byte names (with real pitfall cases)
- ✅ Built-in variable list — prefer them over reinventing the wheel
- ✅ Message & card construction templates
- ✅ Menu design standards: three-level structure, four-character names, two per line, `\n` line breaks
- ✅ Permission hierarchy: global owner → owner → group owner → admin → manual whitelist
- ✅ API integration: verify JSON structure with real requests, extract via `@变量[键]`
- ✅ Pitfall checklist: 8 hard-learned lessons
- ✅ Automated checker script
- ✅ Original example word library (wishing pool + menu + permissions)
- ✅ Bilingual docs for AI comprehension; word library content stays in Chinese

### Structure

```
secluded-skill/
├── SKILL.md                          # Main skill specification (13 chapters + API section)
├── AGENT.md                          # Usage guide for the calling agent
├── SOUL.md                           # Skill persona definition
├── README.md                         # Project README (this file)
├── meta.json                         # Skill metadata (name/icon/description/author/version)
├── references/
│   └── Secluded变量大全.txt           # Full variable & function reference (8253 lines)
├── examples/
│   └── 示例词库_菜单版_v1.txt         # Standard example word library
└── scripts/
    └── check_wordlib.py              # Word library syntax checker
```

### Installation

#### Option A: Git (recommended)

Once the project is on GitHub, clone it directly:

```bash
git clone https://github.com/cy-api/secluded-skill
```

1. **Get the pack**: clone the repo (or download the zip archive from GitHub and unzip — same result), you get the skill directory `secluded-skill/`
2. **Place it**: move the whole directory into your AI environment's skills folder, usually `skills/custom/` (check your framework's docs for the exact path)
3. **Auto-registration**: the framework scans `meta.json` inside the skill directory and registers it in the skill list (name, icon, description, category are all controlled by this file)
4. **Verify**: ask your AI to write a word library (e.g. "write a check-in word library"); if it loads this skill, installation succeeded

#### Option B: Download zip

On the GitHub repo page, click Code → Download ZIP, unzip, then follow steps 2–4 above.

### Quick Start

1. Read `SKILL.md` to learn the rules
2. Grep `references/Secluded变量大全.txt` when unsure — never guess from memory
3. Follow the example in `examples/`
4. Write following the standard workflow
5. Run the checker:

```bash
python3 scripts/check_wordlib.py <word_library.txt>
```

### Variable Byte Rules

Names are validated by byte length: only **1 byte** or **3 bytes**.

| Name | Bytes | Valid | Example |
|---|---|---|---|
| `A`, `B`, `I`, `s` | 1 | ✅ | `A:666` |
| `API`, `TXT`, `PKG`, `CUR` | 3 | ✅ | `API:$访问 url$` |
| `名` (one CJK char) | 3 | ✅ | `名:@API[name]` |
| `当前值` (3 CJK chars) | 9 | ❌ | output as text |

Assignment: `A:666`, `TXT:内容`, `$变量 键 值$`. Read: `%变量名%`. JSON: `@变量[键]`.

### Escaping

Any `%` that is not a variable reference must be written `\%`.

### API JSON Extraction

1. Confirm the API and parameters; use `@变量[键]` to read JSON fields
2. Verify with a real request before writing — never guess field names
3. Ask the user for missing parameters instead of fabricating
4. Offer to probe the API and parse the response if the structure is unclear

### Checker

`scripts/check_wordlib.py` scans: variable byte violations (error), unbalanced `%` (error), AI-generated disclaimers at the end (error), over-broad headers (warning), undefined variables (warning), consecutive blank lines (warning), suspected function nesting (warning), trailing `\n` (warning).

### Language Note

The bilingual docs exist only for AI comprehension; **word library content is always in Chinese**, unless the user explicitly requests another language.

### License

MIT License. Free to use, modify, and distribute. The example word library is original work.
