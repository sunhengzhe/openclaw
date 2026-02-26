#!/usr/bin/env python3

"""
Notion Reader Skill 测试脚本
用于验证技能功能的正确性
"""

import json
import os
import sys
import subprocess
from pathlib import Path

def test_conversion():
    """测试转换功能"""
    print("🧪 测试转换功能...")
    
    # 测试数据路径
    test_data_path = Path(__file__).parent / "test_notion_data.json"
    
    if not test_data_path.exists():
        print("❌ 测试数据文件不存在")
        return False
    
    # 运行转换脚本
    try:
        result = subprocess.run([
            sys.executable, "notion_to_markdown.py", str(test_data_path)
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ 转换功能测试通过")
            
            # 检查输出文件
            output_file = test_data_path.with_suffix('_markdown.md')
            if output_file.exists():
                print("✅ 输出文件生成成功")
                
                # 检查输出内容
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if "📔 Notion日记" in content and "260101" in content:
                    print("✅ 输出内容格式正确")
                    return True
                else:
                    print("❌ 输出内容格式不正确")
                    return False
            else:
                print("❌ 输出文件未生成")
                return False
        else:
            print(f"❌ 转换失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 测试运行出错: {str(e)}")
        return False

def test_dependencies():
    """测试依赖"""
    print("📦 测试依赖...")
    
    try:
        import requests
        print("✅ requests库可用")
        return True
    except ImportError:
        print("❌ requests库不可用")
        return False

def test_config():
    """测试配置文件"""
    print("⚙️  测试配置文件...")
    
    config_path = Path(__file__).parent / "notion_config.json"
    
    if not config_path.exists():
        print("❌ 配置文件不存在")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if "NOTION_API_KEY" in config and "NOTION_PAGE_ID" in config:
            if not config["NOTION_API_KEY"].startswith("your_") and not config["NOTION_PAGE_ID"].startswith("your_"):
                print("✅ 配置文件已正确设置")
                return True
        
        print("⚠️  配置文件需要设置")
        return False
        
    except Exception as e:
        print(f"❌ 配置文件格式错误: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🦞 Notion Reader Skill 测试")
    print("=" * 40)
    
    tests = [
        ("依赖检查", test_dependencies),
        ("配置文件检查", test_config),
        ("转换功能测试", test_conversion),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 40)
    print("📊 测试结果汇总:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📈 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！技能可以正常使用。")
        return 0
    else:
        print("⚠️  部分测试失败，请检查相关配置。")
        return 1

if __name__ == "__main__":
    sys.exit(main())