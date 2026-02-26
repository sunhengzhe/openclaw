# Notion Reader

## 技能简介

这个技能提供了从Notion API读取和转换日记内容的功能。它可以将Notion API返回的JSON数据转换为易读的Markdown格式，特别适合处理按日期组织的日记内容。

## 功能特点

- 🔄 **智能转换**：自动识别日期格式，按日期分组整理
- 📝 **结构化输出**：转换为易读的Markdown格式
- 🔧 **灵活配置**：支持配置文件和环境变量
- 📦 **开箱即用**：包含完整的工具链和示例
- 🧪 **测试验证**：内置测试脚本验证功能

## 快速开始

### 安装技能

```bash
# 进入技能目录
cd /workspaces/openclaw/skills/notion-reader

# 运行安装脚本
./install.sh
```

### 配置API密钥

```bash
# 编辑配置文件
nano notion_config.json

# 填入你的API密钥和页面ID
{
  "NOTION_API_KEY": "your_notion_api_key_here",
  "NOTION_PAGE_ID": "your_page_id_here"
}
```

### 运行转换

```bash
# 一键运行
./run_converter.sh

# 或直接运行
python3 notion_diary_downloader.py
```

## 使用示例

### 输入格式（Notion）

```json
{
  "type": "heading_3",
  "heading_3": {
    "rich_text": [{"text": {"content": "260101"}}]
  }
}
{
  "type": "paragraph",
  "paragraph": {
    "rich_text": [{"text": {"content": "codex weekly limit 晚上9:45 刷新"}}]
  }
}
```

### 输出格式（Markdown）

```markdown
# 📔 Notion日记

生成时间：2026年02月26日 10:05:26

## 260101

codex weekly limit 晚上9:45 刷新，紧赶慢赶写了一天游戏，最后才用到 72%。
```

## 文件说明

- `SKILL.md` - 技能详细文档
- `notion_to_markdown.py` - 核心转换脚本
- `notion_diary_downloader.py` - 完整下载和转换工具
- `run_converter.sh` - 一键运行脚本
- `example_usage.sh` - 使用示例脚本
- `test_skill.py` - 测试脚本
- `install.sh` - 安装脚本
- `notion_config.json.template` - 配置文件模板

## 获取API密钥

1. 访问 [Notion Integration](https://www.notion.so/my-integrations)
2. 点击 "New integration"
3. 填写名称并复制生成的Token
4. 将Token设置为 `NOTION_API_KEY`

## 获取页面ID

1. 打开Notion页面
2. 从浏览器地址栏复制页面ID
3. 将ID设置为 `NOTION_PAGE_ID`

## 支持的块类型

- 标题 (heading_1, heading_2, heading_3)
- 段落 (paragraph)
- 列表 (bulleted_list_item, numbered_list_item)
- 切换块 (toggle)
- 提示块 (callout)

## 故障排除

常见问题及解决方案：

- **401错误**：检查API密钥是否正确
- **404错误**：检查页面ID是否正确
- **403错误**：确保integration有页面访问权限
- **网络超时**：检查网络连接或使用代理

## 高级功能

### 批量处理

```bash
for page in "page1" "page2" "page3"; do
    sed -i "s/\"your_page_id_here\"/\"$page\"/" notion_config.json
    python3 notion_diary_downloader.py
done
```

### 定时转换

```bash
# 添加到crontab
echo "0 9 * * * $(pwd)/run_converter.sh" | crontab -
```

## 许可证

MIT License

---

**使用这个技能，轻松将Notion日记转换为易读的Markdown格式！** 🦞✨
