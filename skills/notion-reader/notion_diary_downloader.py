#!/usr/bin/env python3
"""
Notion Diary Downloader
从Notion API获取日记数据并转换为Markdown格式
"""

import json
import requests
import os
from notion_to_markdown import notion_json_to_markdown


def get_notion_api_key():
    """获取Notion API密钥"""
    # 尝试从环境变量获取
    api_key = os.getenv('NOTION_API_KEY')
    if not api_key:
        # 如果没有环境变量，尝试从配置文件读取
        try:
            with open('notion_config.json', 'r') as f:
                config = json.load(f)
                api_key = config.get('NOTION_API_KEY')
        except FileNotFoundError:
            pass
    
    return api_key


def fetch_notion_page(page_id, api_key):
    """获取Notion页面内容"""
    if not api_key:
        raise ValueError("未找到Notion API密钥。请设置NOTION_API_KEY环境变量或创建notion_config.json文件。")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Notion-Version': '2025-09-03',
        'Content-Type': 'application/json'
    }
    
    # 获取页面基本信息
    page_url = f'https://api.notion.com/v1/pages/{page_id}'
    response = requests.get(page_url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"获取页面失败: {response.status_code} - {response.text}")
    
    page_data = response.json()
    
    # 获取页面内容（块）
    blocks_url = f'https://api.notion.com/v1/blocks/{page_id}/children'
    all_blocks = []
    start_cursor = None
    
    while True:
        params = {}
        if start_cursor:
            params['start_cursor'] = start_cursor
        
        response = requests.get(blocks_url, headers=headers, params=params)
        
        if response.status_code != 200:
            raise Exception(f"获取块失败: {response.status_code} - {response.text}")
        
        data = response.json()
        blocks = data.get('results', [])
        all_blocks.extend(blocks)
        
        # 检查是否还有更多内容
        if not data.get('has_more', False):
            break
        
        start_cursor = data.get('next_cursor')
        if not start_cursor:
            break
    
    # 构建完整的JSON数据
    result = {
        'object': 'list',
        'results': all_blocks,
        'next_cursor': data.get('next_cursor'),
        'has_more': data.get('has_more', False)
    }
    
    return result


def main():
    """主函数"""
    print("🔍 Notion日记下载器")
    print("=" * 50)
    
    # 获取API密钥
    api_key = get_notion_api_key()
    
    # 页面ID（从环境变量或配置文件获取）
    page_id = os.getenv('NOTION_PAGE_ID')
    if not page_id:
        try:
            with open('notion_config.json', 'r') as f:
                config = json.load(f)
                page_id = config.get('NOTION_PAGE_ID')
        except FileNotFoundError:
            pass
    
    if not page_id:
        print("❌ 错误: 未找到页面ID。")
        print("请设置NOTION_PAGE_ID环境变量或在notion_config.json中配置。")
        return
    
    print(f"📄 页面ID: {page_id}")
    
    try:
        # 获取数据
        print("📡 正在从Notion获取数据...")
        json_data = fetch_notion_page(page_id, api_key)
        
        # 保存JSON文件
        json_file = f'notion_diary_{page_id}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 JSON数据已保存到: {json_file}")
        
        # 转换为Markdown
        print("📝 正在转换为Markdown格式...")
        markdown_content = notion_json_to_markdown(json_data)
        
        # 保存Markdown文件
        markdown_file = f'notion_diary_{page_id}_markdown.md'
        with open(markdown_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Markdown格式已保存到: {markdown_file}")
        
        # 显示预览
        print("\n" + "=" * 50)
        print("📋 日记预览（前500字符）:")
        print("=" * 50)
        preview = markdown_content[:500] + "..." if len(markdown_content) > 500 else markdown_content
        print(preview)
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return


if __name__ == "__main__":
    main()