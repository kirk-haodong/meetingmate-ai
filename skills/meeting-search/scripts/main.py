#!/usr/bin/env python3
"""
Meeting Search Skill
智能会议知识库检索系统
"""

import argparse
import os
import json
from pathlib import Path
from datetime import datetime


def search_meetings(query, assignee=None, date_from=None, date_to=None, output_dir="./meeting-output"):
    """搜索会议记录"""
    print(f"🔍 搜索会议: {query}")
    
    output_path = Path(output_dir)
    if not output_path.exists():
        print("📭 暂无会议记录")
        return []
    
    # 查找所有会议纪要文件
    summary_files = list(output_path.glob("meeting_*_summary.md"))
    
    results = []
    for file_path in summary_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 简单匹配查询词
        if query.lower() in content.lower():
            # 提取基本信息
            date_match = None
            for line in content.split('\n'):
                if '会议时间:' in line:
                    date_match = line.split(':')[1].strip()
                    break
            
            results.append({
                "file": str(file_path),
                "date": date_match or "未知",
                "snippet": content[:200] + "..."
            })
    
    return results


def main():
    parser = argparse.ArgumentParser(description="会议知识库检索")
    parser.add_argument("--query", required=True, help="搜索关键词")
    parser.add_argument("--assignee", help="按负责人筛选")
    parser.add_argument("--from", dest="date_from", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--to", dest="date_to", help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--output", default="./meeting-output", help="会议文件目录")
    
    args = parser.parse_args()
    
    results = search_meetings(args.query, args.assignee, args.date_from, args.date_to, args.output)
    
    if not results:
        print("📭 未找到匹配的会议记录")
    else:
        print(f"\n📋 找到 {len(results)} 条相关会议记录\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. 📄 {result['file']}")
            print(f"   📅 日期: {result['date']}")
            print(f"   📝 摘要: {result['snippet']}")
            print()


if __name__ == "__main__":
    main()
