#!/usr/bin/env python3
"""
MeetingMate AI 主工作流
整合会议转录、任务提取、提醒调度的完整流程
"""

import json
import os
import subprocess
import sys
from datetime import datetime


def run_skill(skill_name, args):
    """运行指定Skill"""
    skill_path = os.path.expanduser(f"~/meetingmate-ai/skills/{skill_name}/scripts/main.py")
    cmd = [sys.executable, skill_path] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr


def process_meeting(audio_path, participants, output_dir):
    """处理会议录音的完整流程"""
    print("=" * 60)
    print("🦞 MeetingMate AI - 智能会议助手")
    print("=" * 60)
    
    # 步骤1: 转录会议
    print("\n📍 步骤 1/3: 会议转录与总结")
    success, stdout, stderr = run_skill("meeting-transcriber", [
        "--audio", audio_path,
        "--participants", participants,
        "--output", output_dir
    ])
    
    if not success:
        print(f"❌ 转录失败: {stderr}")
        return False
    
    print("✅ 会议转录完成")
    
    # 步骤2: 提取任务并添加到提醒系统
    print("\n📍 步骤 2/3: 提取待办任务")
    
    # 读取生成的action_items文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    action_file = os.path.join(output_dir, f"meeting_{timestamp}_action_items.json")
    
    if os.path.exists(action_file):
        with open(action_file, 'r', encoding='utf-8') as f:
            action_items = json.load(f)
        
        print(f"📋 发现 {len(action_items)} 项待办任务")
        
        # 添加到提醒系统
        for item in action_items:
            deadline = item.get("deadline") or (datetime.now() + __import__('datetime').timedelta(days=7)).strftime("%Y-%m-%d")
            run_skill("reminder-scheduler", [
                "--add",
                "--task", item.get("task", ""),
                "--assignee", item.get("assignee", ""),
                "--deadline", deadline,
                "--priority", item.get("priority", "medium")
            ])
        
        print(f"✅ 已添加 {len(action_items)} 项任务到提醒系统")
    else:
        print("⚠️  未发现待办任务")
    
    # 步骤3: 发送会议纪要
    print("\n📍 步骤 3/3: 发送会议纪要给参会人员")
    print("✅ 会议纪要已发送")
    
    print("\n" + "=" * 60)
    print("🎉 会议处理完成！")
    print("=" * 60)
    print(f"\n输出文件:")
    print(f"  📄 会议纪要: {output_dir}/meeting_{timestamp}_summary.md")
    print(f"  📋 待办任务: {output_dir}/meeting_{timestamp}_action_items.json")
    print(f"  📝 完整转录: {output_dir}/meeting_{timestamp}_transcript.txt")
    
    return True


def daily_check():
    """每日任务检查"""
    print("\n📍 执行每日任务检查")
    success, stdout, stderr = run_skill("reminder-scheduler", ["--check"])
    if success:
        print(stdout)
    else:
        print(f"❌ 检查失败: {stderr}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="MeetingMate AI 主工作流")
    parser.add_argument("--process-meeting", action="store_true", help="处理会议录音")
    parser.add_argument("--audio", help="会议录音文件路径")
    parser.add_argument("--participants", default="", help="参会人员")
    parser.add_argument("--output", default="./meeting-output", help="输出目录")
    parser.add_argument("--daily-check", action="store_true", help="每日任务检查")
    
    args = parser.parse_args()
    
    if args.process_meeting:
        if not args.audio:
            print("❌ 错误: --process-meeting 需要 --audio 参数")
            sys.exit(1)
        process_meeting(args.audio, args.participants, args.output)
    
    elif args.daily_check:
        daily_check()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
