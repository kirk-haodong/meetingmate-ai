#!/usr/bin/env python3
"""
使用 MiniMax image-01 模型生成产品界面截图
"""

import os
import requests
import json
import time

API_KEY = os.getenv("MINIMAX_API_KEY", "sk-cp-_smOHtq7w6qYyCQoQQIRl32Y5jiib_WhGpnUB_fsBRQDgjdSEQyD91o7lfk7loLHQ-zycd1heeXjRgzZ7psLv7Xm8_beIpwFoNrVkox0b9tqqvLfhEIdBnw")
BASE_URL = "https://api.minimaxi.com"

# 创建输出目录
os.makedirs("screenshots", exist_ok=True)

# 5张产品截图的提示词
SCREENS = [
    {
        "name": "01_meeting_notes",
        "prompt": "Modern web application interface screenshot, meeting minutes document, clean UI design, dark blue theme, markdown format showing meeting title '产品周会 2026.03.15', bullet points for key decisions, action items list with checkboxes, professional SaaS dashboard style, high quality, 1920x1080 resolution, Chinese interface",
        "description": "会议纪要界面"
    },
    {
        "name": "02_task_list", 
        "prompt": "Modern task management web interface, dark theme with blue accents, task list showing multiple todo items with assignee names, due dates, priority tags, checkbox status, clean card-based layout, professional productivity app UI, Chinese text, high quality, 1920x1080",
        "description": "任务列表界面"
    },
    {
        "name": "03_transcription",
        "prompt": "Audio transcription web interface, dark theme, audio waveform visualization at top, transcribed text below with timestamps, speaker labels, clean modern UI design, professional speech-to-text application, Chinese characters, blue accent color, high quality, 1920x1080",
        "description": "转录界面"
    },
    {
        "name": "04_search",
        "prompt": "Search interface for meeting knowledge base, dark theme web app, search bar at top with '搜索历史会议' placeholder, search results showing meeting cards with dates, titles, highlighted keywords, clean list view, professional enterprise app style, Chinese UI, high quality, 1920x1080",
        "description": "搜索界面"
    },
    {
        "name": "05_analytics",
        "prompt": "Data analytics dashboard for meeting efficiency, dark theme with charts, bar chart showing meeting hours per week, pie chart for meeting types, statistics cards with numbers, line graph for trends, professional business intelligence interface, Chinese labels, blue and green accents, high quality, 1920x1080",
        "description": "效率分析界面"
    }
]

def generate_image(prompt, output_path):
    """调用 MiniMax 生成图片"""
    url = f"{BASE_URL}/v1/image_generation"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": "16:9"
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        data = resp.json()
        
        if data.get('base_resp', {}).get('status_code') == 0:
            task_id = data.get('task_id')
            print(f"✅ 任务创建成功: {task_id}")
            return task_id
        else:
            error_msg = data.get('base_resp', {}).get('status_msg', 'Unknown error')
            print(f"❌ 创建失败: {error_msg}")
            return None
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None

def check_image_status(task_id):
    """查询图片生成状态"""
    url = f"{BASE_URL}/v1/query/image_generation?task_id={task_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.json()
    except Exception as e:
        print(f"❌ 查询异常: {e}")
        return None

def download_image(url, output_path):
    """下载生成的图片"""
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(resp.content)
            return True
    except Exception as e:
        print(f"❌ 下载失败: {e}")
    return False

def main():
    print("=" * 60)
    print("🖼️ MiniMax 产品截图生成器")
    print("=" * 60)
    print()
    
    tasks = []
    
    # 第一步：创建所有生成任务
    for i, screen in enumerate(SCREENS, 1):
        print(f"\n[{i}/{len(SCREENS)}] {screen['description']}")
        print(f"提示词: {screen['prompt'][:60]}...")
        
        task_id = generate_image(screen['prompt'], screen['name'])
        if task_id:
            tasks.append({
                "name": screen['name'],
                "task_id": task_id,
                "description": screen['description']
            })
        time.sleep(1)
    
    if not tasks:
        print("\n❌ 没有成功创建的任务")
        return
    
    print("\n" + "=" * 60)
    print("⏳ 等待图片生成完成...")
    print("=" * 60)
    
    # 第二步：轮询检查状态
    completed = []
    failed = []
    
    max_attempts = 30
    attempt = 0
    
    while len(completed) + len(failed) < len(tasks) and attempt < max_attempts:
        attempt += 1
        print(f"\n检查第 {attempt} 次...")
        
        for task in tasks:
            if task['task_id'] in [c['task_id'] for c in completed] or \
               task['task_id'] in [f['task_id'] for f in failed]:
                continue
            
            result = check_image_status(task['task_id'])
            if result:
                status = result.get('status', 'unknown')
                print(f"  {task['description']}: {status}")
                
                if status == 'Success':
                    img_url = result.get('img_url')
                    if img_url:
                        output_path = f"screenshots/{task['name']}.png"
                        if download_image(img_url, output_path):
                            completed.append({**task, "path": output_path})
                            print(f"    ✅ 已下载: {output_path}")
                        else:
                            failed.append(task)
                    else:
                        failed.append(task)
                elif status == 'Fail':
                    print(f"    ❌ 生成失败")
                    failed.append(task)
            
            time.sleep(1)
        
        if len(completed) + len(failed) < len(tasks):
            time.sleep(5)
    
    # 结果汇总
    print("\n" + "=" * 60)
    print("✅ 图片生成完成！")
    print("=" * 60)
    print(f"\n📁 保存位置: ./screenshots/")
    print(f"✅ 成功: {len(completed)} 张")
    print(f"❌ 失败: {len(failed)} 张")
    
    if completed:
        print("\n🖼️ 生成的截图:")
        for item in completed:
            print(f"   - {item['path']}")
    
    if failed:
        print("\n❌ 失败的截图:")
        for item in failed:
            print(f"   - {item['description']}")

if __name__ == "__main__":
    main()
