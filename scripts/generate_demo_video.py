#!/usr/bin/env python3
"""
MeetingMate AI 演示视频生成脚本
使用 MiniMax Hailuo 2.3 文生视频 API

安装依赖:
pip install requests

使用方法:
1. 设置 MINIMAX_API_KEY 环境变量
2. 运行脚本: python3 generate_demo_video.py
3. 生成的视频将保存在 ./demo_videos/ 目录
"""

import os
import json
import time
import requests
from datetime import datetime

# MiniMax API 配置
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
BASE_URL = "https://api.minimaxi.com"

# 演示视频场景提示词（根据视频策划文案）
VIDEO_SCENES = [
    {
        "scene": "开场钩子",
        "prompt": "A professional business meeting room in China, 5 PM, tired office worker looking at messy handwritten notes on desk, frustrated expression, warm sunset lighting through window, cinematic shot, 4K quality",
        "duration": 5
    },
    {
        "scene": "问题场景1",
        "prompt": "Split screen showing chaos: left side person frantically searching through piles of papers and notebooks, right side showing smartphone with unanswered messages, stress and anxiety mood, modern office setting",
        "duration": 5
    },
    {
        "scene": "解决方案亮相",
        "prompt": "Clean modern interface design, MeetingMate AI logo with orange lobster icon, glowing tech blue background, futuristic UI elements floating, professional and trustworthy atmosphere",
        "duration": 5
    },
    {
        "scene": "功能1-智能转录",
        "prompt": "Futuristic AI interface showing audio waveform transforming into text, digital particles flowing, Chinese text appearing magically, blue and white color scheme, high-tech visualization",
        "duration": 5
    },
    {
        "scene": "功能2-任务提取",
        "prompt": "Digital task list automatically extracting from meeting transcript, AI highlighting action items, checkboxes appearing, organized modern dashboard interface, green accents",
        "duration": 5
    },
    {
        "scene": "功能3-自动提醒",
        "prompt": "Multiple notification popups on screen: email, WeChat, DingTalk icons, calendar event being created, modern Chinese office worker receiving notifications, organized workflow",
        "duration": 5
    },
    {
        "scene": "效果数据",
        "prompt": "Big bold numbers floating in digital space: '93%' in green, '88%' in blue, '42%' in orange, data visualization charts, success metrics glowing, celebratory atmosphere",
        "duration": 5
    },
    {
        "scene": "结尾品牌",
        "prompt": "MeetingMate AI brand logo centered, clawmate.cloud website URL below, gradient background from blue to purple, professional closing shot, memorable branding",
        "duration": 5
    }
]

def generate_video(prompt, duration=5):
    """调用 MiniMax Hailuo API 生成视频"""
    
    if not MINIMAX_API_KEY:
        print("❌ 错误: 请设置 MINIMAX_API_KEY 环境变量")
        return None
    
    url = f"{BASE_URL}/v1/video_generation"
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "hailuo-2.3",
        "prompt": prompt,
        "duration": duration,
        "aspect_ratio": "16:9"
    }
    
    try:
        print(f"🎬 正在生成视频: {prompt[:50]}...")
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 视频任务创建成功: {result.get('task_id', 'N/A')}")
            return result.get("task_id")
        else:
            print(f"❌ 生成失败: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None

def check_video_status(task_id):
    """查询视频生成状态"""
    # 正确的查询接口: /v1/query/video_generation?task_id=xxx
    url = f"{BASE_URL}/v1/query/video_generation?task_id={task_id}"
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ 查询失败: {response.status_code} - {response.text[:200]}")
            return None
    except Exception as e:
        print(f"❌ 查询异常: {e}")
        return None

def download_video(url, filename):
    """下载生成的视频"""
    
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            os.makedirs("demo_videos", exist_ok=True)
            filepath = f"demo_videos/{filename}"
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ 视频已下载: {filepath}")
            return filepath
        else:
            print(f"❌ 下载失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 下载异常: {e}")
        return None

def main():
    """主函数：批量生成演示视频片段"""
    
    print("=" * 60)
    print("🎬 MeetingMate AI 演示视频生成器")
    print("=" * 60)
    print()
    
    if not MINIMAX_API_KEY:
        print("❌ 请先设置 MINIMAX_API_KEY 环境变量")
        print("   export MINIMAX_API_KEY='sk-...'")
        return
    
    print(f"📋 共需生成 {len(VIDEO_SCENES)} 个视频片段")
    print()
    
    # 存储任务ID
    tasks = []
    
    # 第一步：提交所有视频生成任务
    for i, scene in enumerate(VIDEO_SCENES, 1):
        print(f"\n[{i}/{len(VIDEO_SCENES)}] {scene['scene']}")
        task_id = generate_video(scene['prompt'], scene['duration'])
        if task_id:
            tasks.append({
                "scene": scene['scene'],
                "task_id": task_id,
                "index": i
            })
        time.sleep(1)  # 避免请求过快
    
    print("\n" + "=" * 60)
    print("⏳ 所有任务已提交，等待生成完成...")
    print("=" * 60)
    
    # 第二步：轮询检查状态
    completed = []
    failed = []
    
    while len(completed) + len(failed) < len(tasks):
        for task in tasks:
            if task['task_id'] in [c['task_id'] for c in completed] or \
               task['task_id'] in [f['task_id'] for f in failed]:
                continue
            
            result = check_video_status(task['task_id'])
            if result:
                status = result.get('status', 'unknown')
                
                if status == 'completed':
                    video_url = result.get('video_url')
                    if video_url:
                        filename = f"{task['index']:02d}_{task['scene']}.mp4"
                        filepath = download_video(video_url, filename)
                        if filepath:
                            completed.append({**task, "filepath": filepath})
                    
                elif status == 'failed':
                    print(f"❌ 任务失败: {task['scene']}")
                    failed.append(task)
            
            time.sleep(2)
        
        print(f"\r📊 进度: {len(completed)} 完成 / {len(failed)} 失败 / {len(tasks)} 总计", end="")
        time.sleep(5)
    
    print("\n\n" + "=" * 60)
    print("✅ 视频生成完成！")
    print("=" * 60)
    print(f"\n📁 视频文件保存在: ./demo_videos/")
    print(f"✅ 成功: {len(completed)} 个")
    print(f"❌ 失败: {len(failed)} 个")
    
    if completed:
        print("\n📹 生成的视频片段:")
        for item in completed:
            print(f"   - {item['filepath']}")
    
    print("\n💡 提示:")
    print("   1. 使用剪映/CapCut 将这些片段剪辑成完整视频")
    print("   2. 添加旁白和背景音乐")
    print("   3. 按脚本顺序拼接即可")

if __name__ == "__main__":
    main()
