#!/usr/bin/env python3
"""skill 库体检：检查每个 skill 的 frontmatter、版本清单、README 计数和链接。

用法：
    python3 scripts/validate_skills.py           # 有「错误」时退出码 1
    python3 scripts/validate_skills.py --strict  # 「提醒」也算失败

错误 = 会让 skill 装不上、触发不了或互相找不到；提醒 = 建议改，不影响使用。
只用 Python 标准库；装了 PyYAML 时用它严格解析 frontmatter。
"""
import argparse
import difflib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESC = 1024          # Claude Code / Codex 的 description 上限
MIN_DESC = 100           # 太短的 description 很难被正确触发
MAX_LINES = 500          # 官方建议 SKILL.md 正文控制在 500 行内
# 本库调用、但不在本库里的 skill（README「依赖与降级」那张表里列着）
EXTERNAL_SKILL_PREFIXES = ("cnki-", "wos-", "sd-", "gs-")
EXTERNAL_SKILLS = {"scansci-pdf", "skill-creator"}
# 投稿与审稿 skill 以前用的工作台编号；只允许出现在「旧工作台编号 sNN」这一处
OLD_ID_RE = re.compile(r"\bs0[1-7]\b")
OLD_ID_NOTE_RE = re.compile(r"旧工作台编号 s0[1-7]")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
TICK_RE = re.compile(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`")

errors, warnings = [], []


def err(where, msg):
    errors.append(f"{where}: {msg}")


def warn(where, msg):
    warnings.append(f"{where}: {msg}")


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 4:]


def parse_frontmatter(raw, where):
    try:
        import yaml
    except ImportError:
        yaml = None
    if yaml is not None:
        try:
            data = yaml.safe_load(raw)
        except yaml.YAMLError as e:
            err(where, f"frontmatter 不是合法 YAML：{e}")
            return {}
        if not isinstance(data, dict):
            err(where, "frontmatter 不是键值对")
            return {}
        return data
    # 没装 PyYAML：只认顶层 `key: value`，并挡住最常见的写法错误
    data = {}
    for line in raw.splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            if value and value[0] not in "\"'|>" and (": " in value or " #" in value):
                err(where, f"frontmatter 的 {key} 里有英文冒号加空格「: 」或「 #」，"
                           "严格的 YAML 解析（比如 Codex）会读错；改成中文冒号「：」，或给整段加引号")
            data[key] = value
    return data


def check_links(text, base, where):
    # 代码块和行内代码里的链接是要写给用户的模板文字，不检查
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    for target in LINK_RE.findall(text):
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        path = target.split("#", 1)[0]
        if path and not (base / path).exists():
            err(where, f"链接指向的文件不存在：{target}")


def check_skill(d, names):
    where = f"skills/{d.name}"
    f = d / "SKILL.md"
    if not f.is_file():
        err(where, "缺 SKILL.md")
        return
    text = f.read_text(encoding="utf-8")
    raw, body = split_frontmatter(text)
    if raw is None:
        err(where, "SKILL.md 开头没有 --- 包起来的 frontmatter")
        return
    fm = parse_frontmatter(raw, where)
    name = fm.get("name")
    desc = fm.get("description")
    if not name:
        err(where, "frontmatter 缺 name")
    elif name != d.name:
        err(where, f"name「{name}」和文件夹名不一致")
    elif not NAME_RE.match(name) or len(name) > MAX_NAME:
        err(where, f"name「{name}」只能用小写字母、数字和连字符，最长 {MAX_NAME}")
    if not desc or not str(desc).strip():
        err(where, "frontmatter 缺 description")
    else:
        desc = str(desc)
        if len(desc) > MAX_DESC:
            err(where, f"description {len(desc)} 字符，超过上限 {MAX_DESC}")
        if len(desc) < MIN_DESC:
            warn(where, f"description 只有 {len(desc)} 字符，说清做什么、什么时候用，容易被正确触发")
        if "Trigger on" not in desc:
            warn(where, "description 没有「Trigger on：」触发例句（本库其他 skill 都有）")

    lines = text.count("\n") + 1
    if lines > MAX_LINES:
        warn(where, f"SKILL.md 有 {lines} 行，超过建议的 {MAX_LINES} 行，细节可以拆进 references/")

    for p in [f, *sorted(d.glob("references/*.md"))]:
        t = p.read_text(encoding="utf-8")
        rel = p.relative_to(ROOT)
        check_links(t, p.parent, str(rel))
        hits = OLD_ID_RE.findall(OLD_ID_NOTE_RE.sub("", t))
        if hits:
            err(str(rel), f"还在用旧工作台编号 {sorted(set(hits))}，请改写成 skill 名")

    external = set()
    for token in set(TICK_RE.findall(body)):
        if token in names:
            continue
        if token.startswith(EXTERNAL_SKILL_PREFIXES) or token in EXTERNAL_SKILLS:
            external.add(token)
            continue
        close = difflib.get_close_matches(token, names, n=1, cutoff=0.88)
        if close:
            err(where, f"引用了不存在的 skill「{token}」，是不是「{close[0]}」？")
    return external


def check_version(names):
    p = ROOT / "version.json"
    try:
        v = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        err("version.json", f"读不出来：{e}")
        return None
    ver = v.get("version", "")
    if not re.match(r"^\d+\.\d+\.\d+$", ver):
        err("version.json", f"version「{ver}」不是 x.y.z")
    listed = v.get("skills", [])
    if len(listed) != len(set(listed)):
        err("version.json", "skills 名单里有重复")
    for n in sorted(set(listed) - names):
        err("version.json", f"名单里有「{n}」，但 skills/ 下没有这个文件夹")
    for n in sorted(names - set(listed)):
        err("version.json", f"skills/{n} 没写进名单")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if not re.search(rf"^## {re.escape(ver)}\b", changelog, re.M):
        err("CHANGELOG.md", f"没有 version.json 当前版本 {ver} 的记录（## {ver}）")
    return ver


def check_readme(names):
    p = ROOT / "README.md"
    text = p.read_text(encoding="utf-8")
    n = len(names)
    for label, pat in (("开头简介", r"共 \*\*(\d+) 个 skills\*\*"),
                       ("Skills 树标题", r"Skills 树（按工作流分类 · (\d+) 个）")):
        m = re.search(pat, text)
        if m and int(m.group(1)) != n:
            err("README.md", f"{label}写的是 {m.group(1)} 个 skill，实际 {n} 个")
    check_links(text, ROOT, "README.md")
    for n_ in sorted(names):
        if f"skills/{n_}/SKILL.md" not in text:
            warn("README.md", f"skill 导航里没有 {n_}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--strict", action="store_true", help="提醒也算失败")
    args = ap.parse_args()

    dirs = sorted(d for d in SKILLS.iterdir() if d.is_dir() and not d.name.startswith("."))
    names = {d.name for d in dirs}
    external = {}
    for d in dirs:
        for token in check_skill(d, names) or ():
            external.setdefault(token, []).append(d.name)
    ver = check_version(names)
    check_readme(names)

    print(f"体检了 {len(dirs)} 个 skill（版本 {ver}）")
    if external:
        print(f"\n用到的外部 skill（不在本库，见 README「依赖与降级」）：{len(external)} 个")
        for token in sorted(external):
            print(f"  {token} ← {', '.join(sorted(external[token]))}")
    for title, items in (("错误", errors), ("提醒", warnings)):
        if items:
            print(f"\n{title} {len(items)} 条：")
            for i in items:
                print(f"  - {i}")
    if not errors and not warnings:
        print("\n全部通过。")
    failed = bool(errors) or (args.strict and bool(warnings))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
