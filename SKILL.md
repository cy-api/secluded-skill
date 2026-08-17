# Secluded 词库开发规范

面向 Secluded 框架（QQ 机器人词库/自定义回复）。词库文件为纯文本 `.txt`，引擎按词汇块逐行解析执行。

完整函数与变量参考见 [references/Secluded变量大全.txt](references/Secluded变量大全.txt)（8253 行，按需查阅，不要整篇塞进上下文）。

## 1. 词库结构

- 一个词库 = 多个**词汇块**，块与块之间用**空行**分隔
- 词汇块第一行是**词汇头**（触发正则），其余行是**词汇体**（执行内容）
- 词汇体内**严禁出现空行**（空行即表示块结束）
- 示例：

```
测试
你好
```

- 词汇头常用正则：`(.*)` 全匹配、`([\s\S]*)` 全匹配含换行、`([0-9]+)` 数字、`(.*)xxx` 前缀、`xxx(.*)` 后缀
- 词汇头尽量精确，避免过宽（如纯 `([0-9]+)` 会拦截所有数字消息，慎用）

## 2. 变量系统（最容易出错，必读）

引擎按**字节**判定变量名合法性，只认 **1 字节** 或 **3 字节**：

| 变量名 | 字节数 | 是否合法 | 示例 |
|---|---|---|---|
| `A`、`B`、`I`、`s` | 1 | ✅ | `A:666` |
| `API`、`TXT`、`PKG`、`CUR` | 3 | ✅ | `API:$访问 url$` |
| `名`、`歌`、`分`、`答`（1 个汉字） | 3 | ✅ | `名:@API[name]` |
| `当前值`（3 个汉字） | 9 | ❌ | 赋值行会被当文本输出 |
| `AA`（2 字节）、`ABCD`（4 字节） | 2/4 | ❌ | 非法 |

**三种赋值形式**：
1. 形式1：`单字节变量:值`，如 `A:666`
2. 形式2：`三字节变量:值`，三字节为 3 个 ASCII 字符或 1 个汉字，如 `TXT:内容`、`名:标题`
3. 形式3：`$变量 键 值$`，键值均可多字节，如 `$变量 哈哈哈666 我是内容$`

**取值**：`%变量名%`。**JSON 取值**：`@变量名[键]`，如 `名:@API[name]`。

**注意**：
- **优先使用内置变量**，不要重复造轮子。常用内置变量：`%群主QQ%`（群主 QQ，无需自己定义）、`%QQ%`（发送者 QQ）、`%群%`（群号）、`%时间戳毫秒%`、`%时间戳进程%`、`%上线模式%`、`%括号1%`（正则第一组捕获）、`%消息来源%`。完整清单见变量大全，动手前先 grep 确认是否存在
- 存储路径/键（`$读`/`$写` 的路径与键）**不受字节限制**，可写中文，如 `$读 签到/%QQ% 分 0$`
- `$全局变量 键 值$`、`$变量 键 值$` 的键不受限制
- 非法变量名的后果：赋值行不会被识别为赋值，而是**原样输出给用户**（真实踩坑案例："当前值:5" 被发到群里）

## 3. 转义

- 文本中的 `%` 若**不是变量引用**，必须写成 `\%`，否则引擎会尝试解析变量
  - 错误：`$写 应用 版本 v1%201.0.0$`（`%20` 会被当变量解析）
  - 正确：`$写 应用 版本 v1\%201.0.0$`

## 4. 注释

行首以 `//`、`##`、`&&` 开头的行是注释，不输出、不执行。注意是**行首**，URL 中段出现的 `&` 不受影响。

## 5. 流程控制

```
如果:条件
...
返回          ← 结束本词汇（不回复）
如果尾
```

- `如果:` 后接条件表达式，支持 `==`、`!=`、`>=`、`<=`、`|`（或）、`&`（与）等
- 判断分支用 `如果:` / `如果尾` 包裹，分支内可嵌套
- `elif:` 多分支
- 循环用标签跳转：

```
I:1
L:10
:loop
如果:%I%<%L%
I:[%I%+1]
$标签跳转 loop$
如果尾
```

- 方括号 `[...]` 是计算表达式，可用于赋值：`s:[(%时间戳毫秒%-%时间戳进程%)/1000]`

## 6. 核心函数

| 函数 | 语法 | 说明 |
|---|---|---|
| 读 | `$读 路径 键 默认值$` | 读配置，如 `$读 群聊/%群%/开关 状态 0$` |
| 写 | `$写 路径 键 值$` | 写配置，如 `$写 群聊/%群%/开关 状态 开$` |
| 访问 | `$访问 URL$` | HTTP 请求，结果存入变量，如 `API:$访问 https://...$` |
| 计算 | `$计算 表达式 取整方式$` | 数学计算 |
| 回调 | `$回调 词汇名$` | 调用另一个词汇块执行（内部逻辑词汇） |
| 休眠 | `$休眠 毫秒$` | 延时 |
| 全局变量 | `$全局变量 键 值$` | 定义全局变量 |
| 变量 | `$变量 键 值$` | 多字节键赋值 |
| 取变量 | `$取变量 变量名$` | 取值 |
| 主人 | `$添加主人 QQ$` / `$删除主人 QQ$` / `$清空主人$` / `$主人列表 变量$` | 主人管理 |
| 标签跳转 | `$标签跳转 标签名$` | 配合 `:标签名` 使用 |
| 字符长度 | `$字符长度 内容$` | 返回长度 |

### JSON 取值（接口对接规范）

当词库需要对接 HTTP 接口并解析响应 JSON 时：

1. **确认接口与参数**：`$访问 URL$` 发起请求，响应存入变量后用 `@变量[键]` 取值，如 `名:@API[name]`、`名:@API[data][name]`；多层路径用 `[键]` 逐级连接，具体以变量大全为准
2. **尽量实际请求验证**：写词库前先尝试真实请求一次接口，解析响应 JSON 结构，确认字段路径后再写进词库，禁止凭空猜字段名
3. **缺少参数先问用户**：接口需要但尚未提供的参数（如 token、签名、用户输入内容），先向用户提问补齐，禁止编造
4. **主动提供方案**：若不确定响应结构，可询问用户是否需要先实际请求一遍接口、解析 JSON 后把取值写成词库中需要对接的部分

## 7. 消息发送

组合式构造消息：

```
$新建消息 A$
$添加消息 A Reply$
$添加消息 A Cmd OidbSvc.0xb77_9$
$添加消息 A Dat %R%$
$发送消息 A R$
```

## 8. 系统消息

词库顶部可定义系统事件块：

```
[系统消息]词库初始化
$全局变量 全局主人 10001$
$写 群聊/%群%/开关 状态 开$
```

常用事件：`词库初始化`、`上线`、`即时消息`、`邮件`、`转账`、`收到点赞`、`处理进度`。`[系统消息]` 词汇块同样由空行与其他块分隔。

## 9. 菜单设计规范（必须养成）

- 词库功能多时，先设计**主菜单 → 子菜单 → 具体功能**三层结构，入口统一
- **换行必须用 `\n`**：词库文件里的直接换行只方便人读，引擎解析后不会产生换行（会被拼接）。要输出换行就写 `\n`，且最后一行末尾不加 `\n`
- 菜单默认**简洁美观、对称**：不是列表类的内容不要列序号，每行放 2 个左右的功能项；用户要求详细时才列序号和逐条说明
- **菜单名默认四字、一行两个、严格对齐**：菜单项名称不必要时一律用四字（如"许愿功能/娱乐功能/群管功能/视频功能"），每行两个、上下对齐美观；除非用户明确要求详细才放宽
- 需要权限的功能单独做**专属菜单**（如群管菜单），无权限者看不到内容

正确示例（词库文件中的写法，实际输出即换行效果）：

```
菜单
许愿功能 娱乐功能\n
群管功能 视频功能
```

```
许愿池菜单
许愿 内容 捞愿望\n
倒掉池子（仅群主）
```

错误示例：靠文件换行分隔（实际输出会连成一行）：

```
菜单
1.许愿池（发送：许愿池菜单）
2.娱乐（发送：娱乐菜单）
```

## 10. 权限分级规范

权限从高到低：**全局主人 → 主人 → 群主 → 管理员 → 手动白名单**。

| 身份 | 判断方式 |
|---|---|
| 全局主人 | `如果:%QQ%==%全局主人%`（自己 `$全局变量` 定义） |
| 主人 | 机器人主人列表（`$主人列表` / `$添加主人`） |
| 群主 | `如果:%QQ%==%群主QQ%`（内置变量） |
| 管理员 | `如果:$管理员 %群号% %QQ%$`（返回真即管理员） |
| 手动白名单 | 初始化 `$写 白名单 成员 QQ$`，判断用 `如果:%QQ%==10001|%QQ%==10002` 多条件或 |

**推荐写法**：把权限校验做成 `[内部]XXX校验` 词汇，用 `$回调` 复用，校验结果存入合法变量（如 `Q`），各功能词汇开头统一调用：

```
[内部]群管校验
Q:0
如果:%QQ%==%群主QQ%
Q:1
返回
如果尾
如果:$管理员 %群号% %QQ%$
Q:1
返回
如果尾

群管菜单
$回调 群管校验$
如果:%Q%==0
你没有群管权限
返回
如果尾
群管功能：
1.禁言：发送 禁言 QQ 秒数
```

常用群管函数：`$禁言 群号 对象 时长 结果键$`、`$全体禁言 开/关 群号 结果键$`、`$撤回 群聊 群号 消息id$`、`$群聊管理员列表 群号 结果键$`。

## 11. 高频踩坑清单（血泪教训）

1. **变量名超字节**：3 个汉字（9 字节）作变量名 → 赋值行被当文本输出。必须用 1 字节（单字母）或 3 字节（3 字母/1 汉字）
2. **`%` 未转义**：URL、版本号里的 `%` 会被当变量解析，写 `\%`
3. **块内空行**：词汇体中出现空行 → 块被截断，后续行失效
4. **词汇头过宽**：如 `([0-9]+)` 会拦截所有数字消息，能加前缀尽量加前缀
5. **回调变量共享**：`$回调` 词汇中赋值的变量，调用方可直接 `%变量%` 读取；回调词汇同样遵守字节规则
6. **函数不套娃**：`$函数1 参数 $函数2 ...$ 参数$` 这类嵌套写法不支持
7. **路径分隔符**：自定义路径用 `/` 或 `\\` 通用
8. **输出即回复**：词汇体里的普通文本行就是回复内容；不想回复用 `返回` 结束

## 12. 标准作业流程（写词库必走）

1. **确认需求**：触发词、功能点、权限要求、是否需要菜单/卡片/系统事件
2. **查规范**：动手前先按需查 `references/Secluded变量大全.txt`，确认函数与内置变量真实存在及用法，禁止凭记忆猜测
3. **设计结构**：先画菜单分层与词汇块划分（含权限分级、内部校验词汇），再落笔
4. **编写**：遵守变量字节规则、`%` 转义、`\n` 换行、块间空行分隔；末尾不加任何 AI 注明
5. **自检**：写完必须运行 `python3 scripts/check_wordlib.py <词库文件>`，清零全部错误后交付
6. **交付**：给出文件路径 + 新增/改动说明 + 触发词列表

## 13. 交付要求

- 词库文件为纯文本，**严禁在文件末尾添加"AI生成""内容由AI生成""仅供参考"等任何说明、署名、水印或多余行**：这些行会被引擎当作词库内容解析执行，导致词库运行异常。写完词库后必须自查文件末尾，保持内容纯净
- **词库正文语言为中文**：技能文档（SKILL.md/AGENT.md/SOUL.md/README.md）支持中英双语仅为方便 AI 理解规范，不代表词库用英文。产出词库的触发词、回复文案、菜单、注释一律使用中文，除非用户明确要求其他语言
- 交付时给出：词库文件路径 + 新增/改动说明 + 触发词列表
- 涉及删除/覆盖用户文件前必须确认

---

## English Version

Secluded framework (QQ bot word library / custom replies). A word library is plain-text `.txt`; the engine parses and executes it block by block. Full function & variable reference: [references/Secluded变量大全.txt](references/Secluded变量大全.txt) (8253 lines — consult on demand, don't dump into context).

### 1. Word Library Structure

- A library = multiple word blocks separated by blank lines
- First line of a block = trigger header (regex); remaining lines = body
- No blank lines inside a block body (a blank line ends the block)
- Common headers: `(.*)` all match, `([\s\S]*)` all match incl. newline, `([0-9]+)` digits, `(.*)xxx` prefix, `xxx(.*)` suffix
- Keep headers precise; a bare `([0-9]+)` intercepts every numeric message

### 2. Variable System (read carefully)

Variable names are validated by byte length: only **1 byte** or **3 bytes**.

| Name | Bytes | Valid | Example |
|---|---|---|---|
| `A`, `B`, `I`, `s` | 1 | ✅ | `A:666` |
| `API`, `TXT`, `PKG`, `CUR` | 3 | ✅ | `API:$访问 url$` |
| `名` (one CJK char) | 3 | ✅ | `名:@API[name]` |
| `当前值` (3 CJK chars) | 9 | ❌ | treated as text output |
| `AA` (2), `ABCD` (4) | 2/4 | ❌ | invalid |

Three assignment forms:
1. `单字节变量:值` e.g. `A:666`
2. `三字节变量:值` (3 ASCII chars or 1 CJK char) e.g. `TXT:内容`, `名:标题`
3. `$变量 键 值$` key/value may be multi-byte e.g. `$变量 哈哈哈666 我是内容$`

Read: `%变量名%`. JSON access: `@变量名[键]` e.g. `名:@API[name]`.

Notes:
- Prefer built-in variables: `%群主QQ%` (group owner), `%QQ%` (sender), `%群%` (group number), `%时间戳毫秒%`, `%时间戳进程%`, `%上线模式%`, `%括号1%` (first regex capture), `%消息来源%`. Grep the variable encyclopedia before coding.
- Storage paths/keys (`$读`/`$写`) are not byte-limited, Chinese is fine: `$读 签到/%QQ% 分 0$`
- `$全局变量 键 值$` / `$变量 键 值$` keys are not limited
- Consequence of invalid names: the line is NOT treated as assignment and is output verbatim (real case: "当前值:5" was sent to the group)

### 3. Escaping

Any `%` in text that is NOT a variable reference must be written `\%`.
- Wrong: `$写 应用 版本 v1%201.0.0$` (`%20` parsed as a variable)
- Right: `$写 应用 版本 v1\%201.0.0$`

### 4. Comments

Lines starting with `//`, `##`, `&&` are comments — not output, not executed. Only at line start; `&` mid-URL is unaffected.

### 5. Control Flow

```
如果:条件
...
返回          ← end this word (no reply)
如果尾
```

- `如果:` supports `==`, `!=`, `>=`, `<=`, `|` (or), `&` (and)
- Branches wrapped by `如果:` / `如果尾`, nestable
- `elif:` multi-branch
- Loops use label jumps:

```
I:1
L:10
:loop
如果:%I%<%L%
I:[%I%+1]
$标签跳转 loop$
如果尾
```

- Square brackets `[...]` are computed expressions: `s:[(%时间戳毫秒%-%时间戳进程%)/1000]`

### 6. Core Functions

| Function | Syntax | Description |
|---|---|---|
| 读 | `$读 路径 键 默认值$` | read config, e.g. `$读 群聊/%群%/开关 状态 0$` |
| 写 | `$写 路径 键 值$` | write config, e.g. `$写 群聊/%群%/开关 状态 开$` |
| 访问 | `$访问 URL$` | HTTP request, result into variable e.g. `API:$访问 https://...$` |
| 计算 | `$计算 表达式 取整方式$` | math |
| 回调 | `$回调 词汇名$` | invoke another word block (internal logic) |
| 休眠 | `$休眠 毫秒$` | delay |
| 全局变量 | `$全局变量 键 值$` | define global variable |
| 变量 | `$变量 键 值$` | multi-byte key assignment |
| 取变量 | `$取变量 变量名$` | get value |
| 主人 | `$添加主人 QQ$` / `$删除主人 QQ$` / `$清空主人$` / `$主人列表 变量$` | owner management |
| 标签跳转 | `$标签跳转 标签名$` | jump to `:标签名` |
| 字符长度 | `$字符长度 内容$` | string length |

### JSON Extraction (API Integration)

When a word library needs to call an HTTP API and parse a JSON response:

1. **Confirm the API and parameters**: `$访问 URL$` sends the request; read the response via `@变量[键]`, e.g. `名:@API[name]`, `名:@API[data][name]`; chain nested keys with `][` (consult the variable encyclopedia for exact syntax)
2. **Verify with a real request when possible**: before writing the word library, try calling the API once, parse the JSON response, and confirm field paths — never guess field names
3. **Ask the user for missing parameters**: if the API needs params not yet available (token, signature, user input), ask the user instead of fabricating
4. **Offer to probe**: if the response structure is unclear, ask whether to fire a test request, parse the JSON, and encode the extraction into the word library

### 7. Sending Messages

```
$新建消息 A$
$添加消息 A Reply$
$添加消息 A Cmd OidbSvc.0xb77_9$
$添加消息 A Dat %R%$
$发送消息 A R$
```

### 8. System Messages

Define system event blocks at the top of the library:

```
[系统消息]词库初始化
$全局变量 全局主人 10001$
$写 群聊/%群%/开关 状态 开$
```

Common events: `词库初始化`, `上线`, `即时消息`, `邮件`, `转账`, `收到点赞`, `处理进度`. `[系统消息]` blocks are also separated by blank lines.

### 9. Menu Design (build the habit)

- Three-level structure: main menu → sub menu → features; one unified entry
- Use `\n` for real line breaks. Literal newlines in the file are only for readability — the engine concatenates them. Last line: no trailing `\n`
- Menus default to clean and symmetric: non-list content has no numbering; ~2 items per line; enumerate only when requested
- Menu names default to four CJK characters, two per line, aligned; relax only when the user asks for detail
- Permission-restricted features get dedicated menus (e.g. admin menu) invisible to unauthorized users

Good:

```
菜单
许愿功能 娱乐功能\n
群管功能 视频功能
```

Bad: relying on file line breaks (everything concatenates into one line).

### 10. Permission Hierarchy

Global owner → owner → group owner → admin → manual whitelist.

| Identity | Check |
|---|---|
| Global owner | `如果:%QQ%==%全局主人%` (defined via `$全局变量`) |
| Owner | bot owner list (`$主人列表` / `$添加主人`) |
| Group owner | `如果:%QQ%==%群主QQ%` (built-in) |
| Admin | `如果:$管理员 %群号% %QQ%$` |
| Whitelist | init `$写 白名单 成员 QQ$`, check with `如果:%QQ%==10001|%QQ%==10002` |

Recommended: build an `[内部]XXX校验` block, reuse via `$回调`, store the result in a valid variable (e.g. `Q`), and call it at the top of each feature block.

Common admin functions: `$禁言 群号 对象 时长 结果键$`, `$全体禁言 开/关 群号 结果键$`, `$撤回 群聊 群号 消息id$`, `$群聊管理员列表 群号 结果键$`.

### 11. Pitfall Checklist

1. Variable name too many bytes: 3 CJK chars = 9 bytes → assignment output as text. Use 1 byte or 3 bytes.
2. Unescaped `%`: URLs/versions get parsed as variables; write `\%`
3. Blank line inside block → block truncated
4. Over-broad header: `([0-9]+)` intercepts all numbers; add a prefix
5. `$回调` shares variables: assignments inside the callback are readable by the caller via `%变量%`; byte rules still apply
6. No function nesting: `$函数1 参数 $函数2 ...$ 参数$` unsupported
7. Paths: `/` or `\\` both work
8. Output = reply: plain text lines in the body are the reply; use `返回` to reply nothing

### 12. Standard Workflow (always)

1. Confirm requirements: triggers, features, permissions, menu/card/system events
2. Consult `references/Secluded变量大全.txt` before coding; verify functions & built-ins; never guess from memory
3. Design structure first: menu layers & word block layout (incl. permission checks, internal validation words)
4. Write: obey byte rules, `%` escaping, `\n` line breaks, blank-line separation; no AI disclaimers at the end
5. Self-check: run `python3 scripts/check_wordlib.py <词库文件>`; clear all errors before delivery
6. Deliver: file path + change summary + trigger word list

### 13. Delivery Requirements

- Plain text only; **never append AI-generated disclaimers, signatures, watermarks, or any extra lines** — they get parsed as word library content and break runtime. Self-check the end of the file.
- **Word library content is in Chinese**: bilingual skill docs exist only for AI comprehension. Triggers, replies, menus, comments are all in Chinese unless the user explicitly requests another language.
- Deliver with: file path + change summary + trigger word list
- Confirm before deleting/overwriting user files
