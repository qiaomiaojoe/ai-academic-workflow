#!/usr/bin/env bash
#
# AI 学术工作流 · 一键安装 Claude Skill
# 用法: curl -fsSL https://raw.githubusercontent.com/qiaomiaojoe/ai-academic-workflow/main/install.sh | bash
#
set -e

REPO="https://github.com/qiaomiaojoe/ai-academic-workflow.git"
SKILLS_DIR="$HOME/.claude/skills"
TMP_DIR="$(mktemp -d)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  AI 学术工作流 · Claude Skill 安装"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. 检查 git 是否安装
if ! command -v git >/dev/null 2>&1; then
    echo "❌ 没找到 git。请先装 git: https://git-scm.com/downloads"
    exit 1
fi

# 2. 检查 Claude 配置目录
if [ ! -d "$HOME/.claude" ]; then
    echo "⚠️  没找到 ~/.claude/ 目录"
    echo "   你可能还没装 Claude Desktop 或 Claude Code, 或者还没启动过。"
    echo "   先去 https://claude.ai/download 装一个, 启动一次, 再回来跑这个脚本。"
    exit 1
fi

mkdir -p "$SKILLS_DIR"

# 3. clone 到临时目录
echo "📥 下载仓库..."
git clone --depth 1 --quiet "$REPO" "$TMP_DIR/repo"

# 4. 复制 skills
echo "📦 安装 skill..."
for skill in analyze-quantitative-data analyze-qualitative-data; do
    if [ -d "$SKILLS_DIR/$skill" ]; then
        echo "   ↻ $skill (覆盖已有版本)"
        rm -rf "$SKILLS_DIR/$skill"
    else
        echo "   + $skill"
    fi
    cp -R "$TMP_DIR/repo/skills/$skill" "$SKILLS_DIR/"
done

# 5. 清理
rm -rf "$TMP_DIR"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ 安装完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  已安装到: $SKILLS_DIR"
echo ""
echo "  下一步:"
echo "    1. 重启 Claude Desktop / Claude Code"
echo "    2. 跟 Claude 说 \"帮我分析这份调查数据\" 或 \"帮我编码这些访谈\""
echo "    3. Claude 会主动建议调用对应 skill"
echo ""
echo "  📚 完整 prompt 菜单: https://github.com/qiaomiaojoe/ai-academic-workflow"
echo "  📝 使用问题反馈: https://github.com/qiaomiaojoe/ai-academic-workflow/issues"
echo ""
