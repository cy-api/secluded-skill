# Changelog

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
