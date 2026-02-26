#!/usr/bin/env python3
"""
Notion JSON to Markdown Converter
将Notion API返回的JSON数据转换为易读的Markdown格式
"""

import json
import re
from datetime import datetime
import sys


def parse_notion_date(date_str):
    """解析Notion日期格式"""
    if not date_str:
        return ""
    
    try:
        # 处理不同的日期格式
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime("%Y年%m月%d日")
        return date_str
    except:
        return date_str


def convert_block_to_markdown(block):
    """将单个Notion块转换为Markdown"""
    block_type = block.get('type', '')
    rich_text = block.get(block_type, {}).get('rich_text', [])
    
    if not rich_text:
        return ""
    
    # 提取文本内容
    text = ""
    for text_item in rich_text:
        content = text_item.get('text', {}).get('content', '')
        if content:
            text += content
    
    # 根据块类型处理
    if block_type == 'heading_1':
        return f"# {text}\n"
    elif block_type == 'heading_2':
        return f"## {text}\n"
    elif block_type == 'heading_3':
        return f"### {text}\n"
    elif block_type == 'paragraph':
        return f"{text}\n\n"
    elif block_type == 'toggle':
        return f"> {text}\n"
    elif block_type == 'bulleted_list_item':
        return f"- {text}\n"
    elif block_type == 'numbered_list_item':
        return f"1. {text}\n"
    elif block_type == 'callout':
        return f"> [!NOTE] {text}\n"
    else:
        return f"{text}\n"


def format_date_entry(date_key, blocks):
    """格式化日期条目"""
    result = f"\n## {date_key}\n\n"
    
    for block in blocks:
        # 跳过日期标题本身，避免重复
        if extract_date_from_block(block) == date_key:
            continue
        result += convert_block_to_markdown(block)
    
    return result


def extract_date_from_block(block):
    """从块中提取日期"""
    heading_types = ['heading_1', 'heading_2', 'heading_3']
    for block_type in heading_types:
        if block.get('type') == block_type:
            rich_text = block.get(block_type, {}).get('rich_text', [])
            if rich_text:
                date_text = rich_text[0].get('text', {}).get('content', '')
                # 检查是否是日期格式（如260101, 260102等）
                if re.match(r'^\d{6}$', date_text):
                    return date_text
    return None


def notion_json_to_markdown(json_data):
    """将Notion JSON转换为Markdown"""
    if not json_data:
        return "# Notion日记转换失败\n\n数据为空。\n"
    
    results = json_data.get('results', [])
    
    if not results:
        return "# Notion日记转换失败\n\n没有找到任何内容。\n"
    
    # 按日期分组
    date_entries = {}
    other_blocks = []
    
    for block in results:
        date_key = extract_date_from_block(block)
        if date_key:
            if date_key not in date_entries:
                date_entries[date_key] = []
            date_entries[date_key].append(block)
        else:
            other_blocks.append(block)
    
    # 生成Markdown
    markdown_content = "# 📔 Notion日记\n\n"
    markdown_content += f"生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n\n"
    
    # 按日期排序
    sorted_dates = sorted(date_entries.keys())
    
    for date_key in sorted_dates:
        markdown_content += format_date_entry(date_key, date_entries[date_key])
    
    # 添加其他块
    if other_blocks:
        markdown_content += "\n## 其他内容\n\n"
        for block in other_blocks:
            markdown_content += convert_block_to_markdown(block)
    
    return markdown_content


def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python notion_to_markdown.py <notion_json_file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        markdown_content = notion_json_to_markdown(json_data)
        
        # 输出到控制台
        print(markdown_content)
        
        # 保存到文件
        output_file = input_file.replace('.json', '_markdown.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"\n✅ 转换完成！Markdown内容已保存到: {output_file}")
        
    except FileNotFoundError:
        print(f"❌ 错误: 文件 {input_file} 不存在")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ 错误: 文件 {input_file} 不是有效的JSON格式")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 转换失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()