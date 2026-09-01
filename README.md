# Dev Rules — 通用软件开发规则 Skill

[![Rules](https://img.shields.io/badge/rules-16_chapters-green?style=for-the-badge)](references/dev-rules.md)
[![Agents](https://img.shields.io/badge/agents-15%2B-purple?style=for-the-badge)](README.md#适配的-agent-平台)
[![Zero Deps](https://img.shields.io/badge/zero-dependencies-yellow?style=for-the-badge)](#安装)

一个**把 AI 辅助开发中反复踩过的坑沉淀为可执行规则**的 Skill 包。让任何 AI 编程助手（Claude Code、Cursor、Windsurf、GitHub Copilot、Codex、Roo Code、Marvis 等 15+ 平台）在任意项目中都按同一套开发纪律工作——**少踩坑、少返工、少让用户擦屁股**。

> 本项目的规则源自真实全栈项目（全球化电商 SaaS：Python 后端 + Nuxt 前端 + 容器化部署）的开发实践。每一条规则背后都是一个真实的踩坑案例，详见 [实战案例](#实战案例真实踩坑与避免的问题)。

---

## 特色

### 1. 16 章通用开发规则，覆盖开发全流程

| 章节 | 主题 | 解决什么问题 |
|------|------|-------------|
| §1 | 版本管理（Git Flow 归集铁律） | 分支混乱、代码丢失、未验证就合并 |
| §2-3 | 缓存清理与部署策略 | 改完代码不生效、镜像缓存命中旧代码 |
| §4 | 知识检索优先级 | 凭记忆瞎猜架构、重复排查已知故障 |
| §5-6 | 执行前计划与产出声明 | AI 闷头改代码、用户不知道改了什么 |
| §7 | 规则自增长机制 | 踩过的坑下次还踩 |
| §8 | 变更行为准则 | 残留代码污染工作区、多变量同时改无法定位 |
| §9 | 会话启动上下文恢复 | 新会话不知道代码在哪、工作区脏着就开始 |
| §10 | 重建后端到端验证 | 只凭"源码存在"就宣布修复成功 |
| §11 | 开发验证流程 | 验证环境与生产不一致、误信静态结论 |
| §12 | 临时文件与产物管理 | 垃圾文件污染仓库 |
| §13 | 代码质量与安全检查 | 越权漏洞、密钥入库、质量门槛不过就提交 |
| §14 | 数据与发布安全 | 直连数据库改坏数据、无法回滚 |
| §15 | 版本发布与提交规范 | 提交信息混乱、镜像无法追溯 |
| §16 | 踩坑反思与规则固化 | 教训只留在会话记忆里，换个会话就忘 |

### 2. 规则自增长机制——AI 开发纪律的"进化"

这是本项目与其他规则文档最大的区别：**不是一份静态文档，而是一个会自我进化的系统**。

- 每次踩坑、失败、返工后，AI 被要求主动做根因分析并评估"是否值得固化为新规则"
- 固化标准：可复用、可执行、不冗余
- 每次固化后必须向用户声明"新增/修改了哪条规则"
- 规则文档持续积累，越用越懂你的项目

### 3. 强制前置动作——把"先想清楚再做"变成纪律

- **会话启动先查 git 状态**：工作区是否干净、功能代码在哪个分支、stash 里有什么——禁止依赖对话记忆代替实际 git 状态
- **环境故障先查文档**：遇到疑似已固化的基础设施故障，第一步检索 docs/ 与规则文档，确认是否已有结论，禁止从零排查
- **宣布成功前先端到端验证**：API 路径一致性、数据链路完整性、需求逐条核对——禁止仅凭"源码存在"宣布修复成功

### 4. 变更行为准则——工作区神圣不可侵犯

- **禁止残留**：失败的尝试必须立即还原，一秒都不能留
- **禁止污染**：排查异常前先 `git diff` / `git status`，任何时候都知道工作区里多了什么
- **禁止盲动**：先证明问题存在，再试图修复
- **禁止跳跃**：一次只动一个变量，修改后立即验证
- **禁止并行编辑同一文件**：后写覆盖先写会导致修改静默丢失

### 5. 数据安全红线

- migration 等数据库操作**必须在容器内执行**，禁止本地直连数据库
- 变更前先备份，失败可回滚，每季度做恢复演练
- 部署回滚：镜像按 commit sha 打 tag，可精确指回上一版本
- **完成定义（DoD）**：8 项 checklist 逐条满足才算"完成"

### 6. 零依赖 + 多平台

- 纯 Markdown（SKILL.md + references/），任何 agent 都能读
- 安装脚本仅用 Python 标准库，不装任何东西、不联网
- 一键安装到 15+ AI 编程助手平台

---

## 实战案例（真实踩坑与避免的问题）

以下案例均来自本规则的实际使用过程。**每一条规则都不是凭空想出来的，而是用时间换来的教训。**

### 案例 1：RBAC 越权漏洞——避免敏感数据泄露

- **场景**：全栈 SaaS 项目 RBAC 权限体系落地
- **踩坑**：多个 admin 路由仅做登录检查，未加资源级权限。`GET /ai/probe` 接口甚至无任何鉴权依赖，**无 token 也能 200 访问**；operator/support 低权限角色可越权访问供应商凭据、AI 探针等敏感接口
- **后果**：若未在开发期发现，线上将存在严重越权漏洞，供应商凭据等敏感数据可被低权限角色获取
- **对应规则**：§13 代码质量与安全检查、§14 数据与发布安全
- **如何避免**：对敏感路由统一加 `require_permission(resource, action)` 依赖；审计时用"无 token 直连 + 低权限角色"双维度验证越权路径

### 案例 2：前端页面存在但后端 API 缺失——避免"功能 404"

- **场景**：RBAC 前端管理页开发
- **踩坑**：前端 roles/admin-users 页面已完整实现，但后端对应写操作 API **全部缺失**（POST/PUT/DELETE 均未实现）；且运行时代码用静态矩阵校验，与数据库里已建好的多对多权限表是两套未打通的体系
- **后果**：若直接联调，功能必然 404；用户会以为"页面有了 = 功能有了"
- **对应规则**：§4 知识检索优先级、§10 重建后端到端验证
- **如何避免**：落地前端管理页前先盘点后端 API 与数据层真实状态（容器内查表、git 历史、seed 脚本），确认体系差异，统一为 DB 权威

### 案例 3：误判容器未重启——避免盲目重启浪费时间

- **场景**：鉴权改造后的容器化验证
- **踩坑**：审计发现低权限角色访问敏感接口返回 200（期望 403），第一反应是"容器没重启，没加载新代码"，准备重启容器
- **真相**：容器实际已运行新代码（grep 确认源码含 2 处 require_permission），200 是因为这些角色在迁移后**确实拥有对应权限**，权限设计如此，并非鉴权失效
- **后果**：若盲目重启，浪费时间且问题依旧；若误改代码，会引入新 Bug
- **对应规则**：§8 禁止盲动（先证明问题存在再修复）、§10 端到端验证
- **如何避免**：遇到"越权返回 200"先核对角色实际权限种子（/me 的 permissions 或 role_permissions 表），确认是真实缺陷还是权限设计如此，再决定下一步

### 案例 4：WSL localhost 转发故障重复排查——避免重复造轮子浪费数小时

- **场景**：podman + WSL2 容器化开发环境日常运维
- **踩坑**：localhost:8080 转发失效的根因与恢复 SOP **已经沉淀在文档里**，但新会话的 AI 仍从零开始排查——检查 gvproxy/win-sshproxy、entries 文件、切换 UserModeNetworking、加 Hyper-V 规则，逐层重查，浪费大量时间
- **后果**：已知问题的重复排查，每次故障都像第一次遇到
- **对应规则**：§4 知识检索优先级（"先查已有基线再动手"被固化为环境类故障的强制前置动作）
- **如何避免**：遇到疑似已固化过的基础设施故障，第一步检索 docs/ 与规则文档确认是否有结论；有就直接套用

### 案例 5：iframe 跨域元素选择——避免无效方案

- **场景**：admin 装修页给 iframe 预览框加"元素选择模式"
- **踩坑**：AI 先尝试直接访问 `iframe.contentDocument` 注入高亮样式与事件，发现无效——admin 与 iframe 不同端口即不同源，跨域无法访问
- **后果**：无效方案浪费实现时间；若强行绕过跨域限制，会引入安全风险
- **对应规则**：§16 踩坑反思与规则固化、§11 开发验证流程
- **如何避免**：改用 postMessage 跨域通信——portal 侧监听指令做 hover 高亮与 click 选中，结果回传父窗口；此方案后续被固化为规则文档中的跨域通信最佳实践

### 案例 6：验证绕路 dev server——避免验证环境与生产不一致

- **场景**：商品列表 SKU 抽屉功能验证
- **踩坑**：为定位前端报错，AI 自行启动 dev server 并临时修改代理指向，绕开正式验证入口——验证环境与生产环境行为不一致，且违背唯一入口规则
- **后果**：dev 模式验证通过不代表生产环境正常，可能导致线上问题漏检
- **对应规则**：§11 开发验证流程（唯一入口、禁止绕路、能用非浏览器手段自查的绝不派浏览器）
- **如何避免**：固化"本地验证必须走正式入口"规则；排查前端问题直接在正式环境 build 重建容器验证

### 规则 → 案例映射

| 规则 | 实战依据 |
|------|---------|
| §8 禁止盲动 / §10 端到端验证 | 案例 3（误判容器未重启） |
| §4 知识检索优先级 | 案例 2（前后端体系未盘点）、案例 4（WSL 故障重复排查） |
| §13 代码质量与安全检查 | 案例 1（RBAC 越权） |
| §11 开发验证流程 | 案例 5（iframe 跨域）、案例 6（验证绕路） |
| §16 踩坑反思与规则固化 | 全部案例（经验沉淀为规则） |

---

## 适配的 Agent 平台

本项目采用**单一事实源**结构：规则只维护一份（`SKILL.md` + `references/dev-rules.md`），通过安装脚本复制到各平台对应目录。

| 平台 | 安装目录 |
|------|---------|
| Claude Code | `.claude/skills/` 或 `~/.claude/skills/` |
| Cursor | `.cursor/skills/` |
| Windsurf | `~/.codeium/windsurf/skills/` |
| GitHub Copilot | `~/.copilot/skills/` |
| Codex CLI | `~/.codex/skills/` |
| Roo Code | `.roo/skills/` |
| Kiro | `.kiro/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| Trae | `.trae/skills/` |
| OpenCode | `.opencode/skill/` |
| Continue | `.continue/skills/` |
| Cline | `.cline/skills/` |
| Kilo Code | `.kilocode/skills/` |
| Antigravity | `.antigravity/skills/` |
| Qoder | `.qoder/skills/` |
| 通用 / Agent Standard | `.agents/skills/` 或 `~/.agents/skills/` |
| Marvis（Windows 桌面助手） | `skills/custom/`（用户目录）或自定义技能目录 |

> 各平台具体加载机制以平台文档为准；目录约定参考 [Anthropic Agent Skills 标准](https://github.com/anthropics/skills) 与主流 agent 的 skill 目录规范。

---

## 安装

### 方式一：一键安装脚本（推荐）

需要 Python 3.x（仅标准库，不装依赖、不联网）：

```bash
# 安装到当前项目（单项目）
python scripts/install.py --ai claude        # Claude Code
python scripts/install.py --ai cursor        # Cursor
python scripts/install.py --ai marvis        # Marvis
python scripts/install.py --ai universal     # Agent Standard (~/.agents/skills/)

# 全局安装（所有项目可用）
python scripts/install.py --ai claude --global

# 安装到所有支持的平台
python scripts/install.py --ai all

# 查看所有支持的平台
python scripts/install.py --list
```

### 方式二：手动安装

把 `SKILL.md` 与 `references/dev-rules.md` 复制到目标平台的 skills 目录下，保持 `dev-rules/` 目录结构：

```
<目标目录>/dev-rules/
├── SKILL.md
└── references/
    └── dev-rules.md
```

---

## 使用

安装后无需特殊命令，自然语言触发即可：

```
帮我开发这个功能（会先检查 git 状态、归集 dev、说明计划）
帮我排查这个 Bug（会先确认工作区干净、复现问题再动手）
帮我看下这个部署为什么没生效（会先查文档基线、核对缓存与重建策略）
```

规则激活的典型信号：

- 任何代码修改、分支操作、合并请求
- 容器重建、镜像构建、部署操作
- 数据库变更、数据迁移
- 功能验证、代码审查、问题排查

---

## 目录结构

```
dev-rules-skill/
├── SKILL.md                    # 技能入口（frontmatter + 铁律速查）
├── references/
│   └── dev-rules.md            # 16 章完整规则手册（单一事实源）
├── scripts/
│   └── install.py              # 跨平台一键安装脚本（Python 标准库）
├── .claude/skills/dev-rules/   # Claude Code 预置目录（可直接引用）
└── LICENSE
```

---

## License

[MIT](LICENSE)
