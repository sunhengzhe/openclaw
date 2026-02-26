#!/bin/bash

# Notion日记转换工具使用示例

echo "🦞 小龙虾的Notion日记转换工具"
echo "=================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

echo "✅ Python3环境检查通过"

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
if ! grep -q "your_notion_api_key_here" notion_config.json || \
   ! grep -q "your_page_id_here" notion_config.json; then
    echo "✅ 配置文件已正确设置"
else
    echo "⚠️  请先编辑 notion_config.json 文件，填入你的API密钥和页面ID"
    exit 1
fi

# 运行转换工具
echo "🚀 开始转换Notion日记..."
python3 notion_diary_downloader.py

echo "=================================="
echo "🎉 转换完成！"
echo "📁 生成的文件："
echo "   - notion_diary_*.json (原始JSON数据)"
echo "   - notion_diary_*_markdown.md (Markdown格式日记)"
echo "=================================="