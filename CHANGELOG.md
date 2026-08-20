# Changelog

## v1.0.3 (2026-08-20)

- 菜单规范强化：新增硬规则「菜单项名 = 触发指令」，菜单显示的功能名必须与词库词汇头一字不差；重写第 9 章示例（含同名词汇块要求）、修正第 10 章群管菜单示例、第 11 章新增踩坑条目
- 第 2 章变量系统按变量大全重写：键名 1/3 字节规则、三种赋值形式、JSON 取值（@变量名[键] 须 1/3 字节、$JSON 解析 变量名任意）、内置变量分类清单（账号/操作者/群/消息/参数/正则捕获/其他）、整段转义、行变量（#->var:）、随机数
- README 中英文同步更新菜单规范与校验描述
- meta.json / SKILL.md frontmatter 版本号更新为 1.0.3
- 压缩包更名为 secluded-skill_v1.0.3.zip

## v1.0.2 (2026-08-18)

- 新增 SKILL.md 第 14 章「功能授权约束」：完整授权函数清单（群聊/频道/好友/消息/用户/其他）+ 默认不调用规则 + 三选一提问确认流程 + 交付授权状态告知
- AGENTS.md 同步新增「功能授权约束」章节与交付授权告知要求
- 标准作业流程强化：先分析规划并向用户复述确认再动笔；references 参考词库为"参考不是抄"
- 子技能 admin / fun 各加授权功能提示
- 将 scripts/check_wordlib.py 修改为 references/词库校验规范.md，校验无需 Python 环境
- meta.json / SKILL.md frontmatter 版本号更新为 1.0.2

## v1.0.1 (2026-08-18)

- SKILL.md 增加 YAML frontmatter（name/description/version/author），兼容 Codex / Claude 技能识别
- SKILL.md 新增「子技能路由」章节，按功能类型加载对应子技能
- 新增 `skills/` 子技能目录：`secluded-skill-admin`（管理功能域）、`secluded-skill-fun`（娱乐功能域）
- `references/` 新增用户参考词库：群管词库.txt、发言统计.txt、钓鱼娱乐.txt
- 删除 `examples/` 目录
- `AGENT.md` 重命名为 `AGENTS.md`（Codex 标准命名，删除原文件）
- 新增 `CHANGELOG.md`、`.gitignore`
- README.md 更新仓库地址与目录结构
- meta.json 版本号更新为 1.0.1
- AGENTS.md 新增「检查更新」章节：加载技能时请求 GitHub 远程 meta.json 对比版本号，旧版提示 git pull 或重新下载

## v1.0.0 (2026-08-17)

- 初始版本：SKILL.md 完整语法规范（13 章）、Secluded 变量大全、示例词库、校验脚本 check_wordlib.py
