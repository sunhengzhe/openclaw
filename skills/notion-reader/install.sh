#!/bin/bash

# Notion Reader Skill 安装脚本
# 用于安装和设置Notion Reader Skill

echo "🦞 Notion Reader Skill 安装脚本"
echo "=================================="

# 检查是否在技能目录中
if [ ! -f "SKILL.md" ]; then
    echo "❌ 错误: 请在技能目录中运行此脚本"
    exit 1
fi

echo "✅ 检测到技能目录"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

echo "✅ Python3环境检查通过"

# 安装依赖
echo "📦 安装Python依赖..."
pip3 install requests

if [ $? -eq 0 ]; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败"
    exit 1
fi

# 设置权限
echo "🔐 设置文件权限..."
chmod +x notion_to_markdown.py
chmod +x notion_diary_downloader.py
chmod +x run_converter.sh
chmod +x example_usage.sh
chmod +x test_skill.py

echo "✅ 权限设置完成"

# 创建配置文件
if [ ! -f "notion_config.json" ]; then
    echo "📝 创建配置文件..."
    cp notion_config.json.template notion_config.json
    echo "✅ 配置文件已创建"
    echo "⚠️  请编辑 notion_config.json 文件，填入你的API密钥和页面ID"
else
    echo "✅ 配置文件已存在"
fi

# 运行测试
echo "🧪 运行功能测试..."
python3 test_skill.py

if [ $? -eq 0 ]; then
    echo "✅ 所有测试通过！"
else
    echo "⚠️  部分测试失败，请检查配置"
fi

echo ""
echo "🎉 安装完成！"
echo ""
echo "📋 使用方法："
echo "   1. 编辑 notion_config.json，填入API密钥和页面ID"
echo "   2. 运行 ./run_converter.sh 开始转换"
echo "   3. 查看生成的Markdown文件"
echo ""
echo "📖 更多信息："
echo "   - 查看技能文档: cat SKILL.md"
echo "   - 查看使用示例: ./example_usage.sh"
echo "   - 运行测试: python3 test_skill.py"
echo ""
echo "🔗 相关链接："
echo "   - Notion Integration: https://www.notion.so/my-integrations"
echo "   - 技能文档: https://docs.openclaw.ai/skills/notion-reader"