#!/usr/bin/env python3
"""Dev Rules Skill - 跨平台一键安装脚本

零依赖（仅 Python 3.x 标准库），不联网、不安装任何包。
将 SKILL.md + references/dev-rules.md 复制到目标 agent 平台的 skills 目录。

用法:
    python scripts/install.py --list                       # 列出所有支持的平台
    python scripts/install.py --ai claude                  # 安装到 Claude Code（当前项目）
    python scripts/install.py --ai claude --global         # 安装到 Claude Code（全局）
    python scripts/install.py --ai marvis --dir <DIR>      # 安装到自定义目录（如 Marvis 技能目录）
    python scripts/install.py --ai all                     # 安装到所有平台
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

SKILL_NAME = "dev-rules"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_FILES = ("SKILL.md", "references/dev-rules.md")

# 平台 -> 安装目标模板列表（{cwd}=当前项目目录，{home}=用户主目录）
PLATFORMS: dict[str, list[str]] = {
    "claude": ["{cwd}/.claude/skills", "{home}/.claude/skills"],
    "cursor": ["{cwd}/.cursor/skills"],
    "windsurf": ["{home}/.codeium/windsurf/skills"],
    "copilot": ["{home}/.copilot/skills"],
    "codex": ["{home}/.codex/skills"],
    "roocode": ["{cwd}/.roo/skills"],
    "kiro": ["{cwd}/.kiro/skills"],
    "gemini": ["{home}/.gemini/skills"],
    "trae": ["{cwd}/.trae/skills"],
    "opencode": ["{cwd}/.opencode/skill"],
    "continue": ["{cwd}/.continue/skills"],
    "cline": ["{cwd}/.cline/skills"],
    "kilocode": ["{cwd}/.kilocode/skills"],
    "antigravity": ["{cwd}/.antigravity/skills"],
    "qoder": ["{cwd}/.qoder/skills"],
    "universal": ["{cwd}/.agents/skills", "{home}/.agents/skills"],
    # marvis 无固定目录约定，需通过 --dir 显式指定
    "marvis": [],
}

ALIASES = {
    "roo": "roocode",
    "ant": "antigravity",
    "windsurf": "windsurf",
    "copilot": "copilot",
}


def resolve_platform(name: str) -> str:
    name = name.lower()
    if name in ALIASES:
        name = ALIASES[name]
    if name not in PLATFORMS:
        sys.exit(
            f"未知平台: {name}\n可用平台: {', '.join(PLATFORMS)}"
            "\n（另支持别名: roo -> roocode, ant -> antigravity）"
        )
    return name


def install_to(target_dir: Path) -> bool:
    """把 SKILL.md + references/ 复制到 target_dir/dev-rules/，返回是否执行了安装。"""
    if not target_dir:
        return False
    dest = target_dir / SKILL_NAME
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "references").mkdir(parents=True, exist_ok=True)

    copied = []
    for rel in SOURCE_FILES:
        src = PROJECT_ROOT / rel
        if not src.exists():
            sys.exit(f"缺少源文件: {src}（请从项目根目录运行脚本）")
        shutil.copy2(src, dest / rel)
        copied.append(str(dest / rel))

    print(f"已安装到 {dest}")
    for f in copied:
        print(f"  - {f}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Dev Rules Skill 跨平台安装脚本")
    parser.add_argument("--ai", help="目标平台（--list 查看全部）")
    parser.add_argument("--global", dest="global_install", action="store_true",
                        help="安装到全局（用户主目录）而非当前项目")
    parser.add_argument("--dir", help="自定义安装目录（覆盖平台默认路径，如 Marvis 技能目录）")
    parser.add_argument("--list", action="store_true", help="列出所有支持的平台")
    args = parser.parse_args()

    if args.list:
        print("支持的平台及默认安装路径:")
        for name, templates in PLATFORMS.items():
            if templates:
                print(f"  {name:<12} {', '.join(templates)}")
            else:
                print(f"  {name:<12} （需 --dir 显式指定目录）")
        return

    if not args.ai:
        parser.print_help()
        sys.exit(0)

    cwd = Path.cwd().resolve()
    home = Path.home().resolve()

    if args.ai.lower() == "all":
        installed = 0
        for name in PLATFORMS:
            for tmpl in PLATFORMS[name]:
                if install_to(Path(tmpl.format(cwd=cwd, home=home))):
                    installed += 1
        print(f"完成，共安装 {installed} 个位置。")
        return

    name = resolve_platform(args.ai)

    if args.dir:
        install_to(Path(args.dir).expanduser().resolve())
        return

    # 自定义 --dir 未提供时，按平台模板安装
    templates = PLATFORMS[name]
    if not templates:
        sys.exit(f"平台 {name} 无默认安装路径，请用 --dir 指定目录（如: --ai marvis --dir D:/skills）")

    # --global 时只装用户主目录项；否则按优先级装第一个（项目级优先）
    if args.global_install:
        matched = [t for t in templates if t.startswith("{home}")]
        if not matched:
            sys.exit(f"平台 {name} 不支持 --global（无全局安装约定）")
        install_to(Path(matched[0].format(cwd=cwd, home=home)))
    else:
        install_to(Path(templates[0].format(cwd=cwd, home=home)))


if __name__ == "__main__":
    main()
