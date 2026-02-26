#!/bin/bash

# Notion Reader Skill 使用示例
# 这个脚本演示如何使用Notion Reader Skill来转换日记内容

echo "🦞 Notion Reader Skill 使用示例"
echo "=================================="

# 检查技能目录是否存在
SKILL_DIR="/workspaces/openclaw/skills/notion-reader"
if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ 错误: Notion Reader Skill 未找到"
    echo "请确保技能已正确安装"
    exit 1
fi

echo "✅ 找到Notion Reader Skill目录: $SKILL_DIR"

# 进入技能目录
cd "$SKILL_DIR"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

echo "✅ Python3环境检查通过"

# 检查依赖库
echo "📦 检查Python依赖..."
python3 -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  正在安装requests库..."
    pip3 install requests
fi

echo "✅ 依赖检查通过"

# 检查配置文件
if [ ! -f "notion_config.json" ]; then
    echo "📝 创建配置文件模板..."
    cp notion_config.json.template notion_config.json
    echo "⚠️  请编辑 notion_config.json 文件，填入你的API密钥和页面ID"
    echo "   然后重新运行此脚本"
    exit 1
fi

echo "✅ 配置文件检查通过"

# 检查API密钥和页面ID
if grep -q "your_notion_api_key_here" notion_config.json || \
   grep -q "your_page_id_here" notion_config.json; then
    echo "⚠️  请先编辑 notion_config.json 文件，填入你的API密钥和页面ID"
    echo "配置文件路径: $SKILL_DIR/notion_config.json"
    exit 1
fi

echo "✅ 配置文件已正确设置"

# 运行转换工具
echo "🚀 开始转换Notion日记..."
python3 notion_diary_downloader.py

echo "=================================="
echo "🎉 转换完成！"
echo "📁 生成的文件："
echo "   - notion_diary_*.json (原始JSON数据)"
echo "   - notion_diary_*_markdown.md (Markdown格式日记)"
echo "=================================="

# 显示生成的文件
echo "📋 生成的文件列表："
ls -la notion_diary_* 2>/dev/null || echo "   未找到生成的文件"

echo ""
echo "💡 提示："
echo "   - 查看转换结果: cat notion_diary_*_markdown.md"
echo "   - 编辑配置: nano notion_config.json"
echo "   - 查看技能文档: cat SKILL.md"