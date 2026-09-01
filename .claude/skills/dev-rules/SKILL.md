---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 14f48488fead00d28e11c31f9845685c_62bedaafa62b11f1b3f6525400826444
    ReservedCode1: XMPuO005NWyxfyulv0PusfSht1nySSRzMOjEQvF7hv2f5uQEeMU8KxnS0p+AvSuIMhAom64k2TsaIiTrzdv4gPcd+m7SzmI3JUnlLxGEEFV7w0EsYW3yLsoLPm6MZ3MSSFl61edGAnQjQOiMVY8qiJw9qdmdXhHCaeitZlzehzjjm9OHsX57SaDLrM4=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 14f48488fead00d28e11c31f9845685c_62bedaafa62b11f1b3f6525400826444
    ReservedCode2: XMPuO005NWyxfyulv0PusfSht1nySSRzMOjEQvF7hv2f5uQEeMU8KxnS0p+AvSuIMhAom64k2TsaIiTrzdv4gPcd+m7SzmI3JUnlLxGEEFV7w0EsYW3yLsoLPm6MZ3MSSFl61edGAnQjQOiMVY8qiJw9qdmdXhHCaeitZlzehzjjm9OHsX57SaDLrM4=
---

---
name: dev-rules
description: Generic software development rules applicable to any project. Enforces Git Flow with dev-branch consolidation, cache clearing and deployment strategy (rebuild vs restart matrix), pre-execution planning, knowledge retrieval priority, end-to-end verification after rebuild, code quality gates (lint/type/mypy), data & release safety (containerized migrations, backup/rollback, DoD), change behavior rules (no residue / no blind edits / single-variable changes), session-start git context recovery, temporary file management, and rule self-growth. Use when working on code in any repo - modifying source files, container/deployment operations, code changes requiring cache clear or rebuild, creating documentation, or any development task in a software project.
---

# 通用软件开发规则（Dev Rules）

> 适用于任意软件项目的通用开发规则。使用本 Skill 时，请将各章节中的占位符（项目根目录、容器名、compose 文件路径等）替换为当前项目的实际值，项目专属细节以当前项目 docs/ 与 git 状态为准。

## 适用范围

本 Skill 覆盖软件开发全流程的通用约束：

| 章节 | 主题 | 何时使用 |
|------|------|----------|
| 1 | 版本管理（Git Flow） | 开始任何 fix/feature、分支归集、合并 dev 前 |
| 2 | 缓存清理与重启 | 修改源码后判断是否需要清缓存/重启 |
| 3 | 部署策略 | Dockerfile/配置/依赖变更、镜像重建、容器管理 |
| 4 | 知识检索优先级 | 不确定架构、配置或业务逻辑时 |
| 5 | 执行前计划 | 每次执行任务前 |
| 6 | 新增文件与变更记录 | 完成任务后声明产出物 |
| 7 | 规则自增长机制 | 踩坑后评估是否沉淀新规则 |
| 8 | 变更行为准则 | 任何代码修改过程中（禁止残留/污染/盲动/跳跃） |
| 9 | 会话启动上下文恢复 | 每次开始处理项目任务前 |
| 10 | 重建后端到端验证 | 容器重建/重启后宣布修复前 |
| 11 | 开发验证流程 | 完成修改后选择验证手段 |
| 12 | 临时文件与产物管理 | 产生测试产物、日志、临时数据时 |
| 13 | 代码质量与安全检查 | 提交前质量门槛、CI、安全红线 |
| 14 | 数据与发布安全 | 数据库变更、备份、回滚、完成定义 |
| 15 | 版本发布与提交规范 | 提交信息、语义化版本、镜像 tag |
| 16 | 踩坑反思与规则固化 | 任何踩坑/失败/返工后 |

## 铁律速查（Top 10）

1. 新 fix/feature 必须先从 dev 归集并切新分支完成，禁止直接在 dev 上改代码
2. 用户明确"验证通过"之前禁止合并 dev / push origin dev，通过 PR 合并
3. 执行前先向用户说明计划（改哪些文件、做什么操作），完成后用 `yyb-product` 声明产出物
4. migration 等数据库操作必须在容器内执行，禁止本地直连数据库；变更前先备份
5. 无 HMR 的静态构建端任何源码变更必须 `build --no-cache` 重建镜像 + `up -d --force-recreate` 重建容器
6. 提交前必须过质量门槛（lint / type / mypy 等），提交信息遵循 Conventional Commits
7. 重建/重启后必须完成端到端验证（API 链路、数据链路、需求逐条核对），禁止仅凭"源码存在"宣布修复成功
8. 工作区是神圣的：排查异常前先 `git diff` / `git status`，失败的尝试必须立即还原（禁止残留）
9. 一次只动一个变量：每次修改一个文件中的一处逻辑，修改后立即验证（禁止跳跃）
10. 踩坑后必须主动反思并将经验固化进规则文档，不把教训只留在会话记忆里

## Reference

For full details, read [references/dev-rules.md](references/dev-rules.md).
*（内容由AI生成，仅供参考）*
