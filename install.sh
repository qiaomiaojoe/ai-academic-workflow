#!/usr/bin/env bash
#
# AI学术工作流（乔淼PhD · AI学术训练营）· 一键安装 skills
# 用法: curl -fsSL https://raw.githubusercontent.com/qiaomiaojoe/ai-academic-workflow/main/install.sh | bash
#
set -e

REPO="https://github.com/qiaomiaojoe/ai-academic-workflow.git"
TMP_DIR="$(mktemp -d)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  AI学术工作流 · skills 安装（Claude Code / Codex）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. 检查 git
if ! command -v git >/dev/null 2>&1; then
    echo "❌ 没找到 git。请先装 git: https://git-scm.com/downloads"
    exit 1
fi

# 2. 确定目标目录（Claude Code 和/或 Codex，装到所有存在的环境）
TARGETS=()
if [ -d "$HOME/.claude" ]; then
    TARGETS+=("$HOME/.claude/skills")
fi
CODEX_DIR="${CODEX_HOME:-$HOME/.codex}"
if [ -d "$CODEX_DIR" ]; then
    TARGETS+=("$CODEX_DIR/skills")
fi
if [ ${#TARGETS[@]} -eq 0 ]; then
    echo "⚠️  没找到 ~/.claude/ 或 ${CODEX_DIR}/ 目录"
    echo "   你可能还没装 Claude Code / Claude Desktop / Codex, 或者还没启动过。"
    echo "   装好并启动一次后, 再回来跑这个脚本。"
    exit 1
fi

# 3. clone 到临时目录
echo "📥 下载仓库..."
git clone --depth 1 --quiet "$REPO" "$TMP_DIR/repo"

# 4. 安装仓库内全部 skills 到每个目标环境
for SKILLS_DIR in "${TARGETS[@]}"; do
    mkdir -p "$SKILLS_DIR"
    echo ""
    echo "📦 安装到 $SKILLS_DIR ..."
    for skill_dir in "$TMP_DIR/repo/skills"/*/; do
        skill="$(basename "$skill_dir")"
        if [ -d "$SKILLS_DIR/$skill" ]; then
            echo "   ↻ $skill (覆盖已有版本)"
            rm -rf "$SKILLS_DIR/$skill"
        else
            echo "   + $skill"
        fi
        cp -R "$skill_dir" "$SKILLS_DIR/$skill"
    done
done

# 5. 清理
rm -rf "$TMP_DIR"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ 安装完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  下一步:"
echo "    1. 重启 Claude Code / Claude Desktop / Codex"
echo "    2. 试试说: \"帮我选题\" / \"检查这些参考文献是不是编的\" /"
echo "       \"帮我找 research gap\" / \"我要分析这份调查数据\""
echo "    3. AI 会自动调用对应 skill"
echo ""
echo "  📚 完整 skills 树: https://github.com/qiaomiaojoe/ai-academic-workflow"
echo "  📝 使用问题反馈: https://github.com/qiaomiaojoe/ai-academic-workflow/issues"
echo ""
