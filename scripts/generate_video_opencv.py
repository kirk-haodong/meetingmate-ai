#!/usr/bin/env python3
"""
使用 OpenCV 生成简单的演示视频
安装: pip install opencv-python-headless pillow numpy
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# 创建输出目录
os.makedirs("demo_videos_cv", exist_ok=True)

# 视频配置
WIDTH, HEIGHT = 1920, 1080
FPS = 30

# 定义场景
scenes = [
    {
        "name": "01_opening",
        "lines": ["会议记录，从30分钟到2分钟", "MeetingMate AI - 智能会议助手"],
        "duration": 3,
        "bg": (30, 58, 138)  # 深蓝
    },
    {
        "name": "02_problem",
        "lines": ["这些场景，你是否熟悉？", "会后整理要花30分钟 | 任务总被遗漏 | 决策难找"],
        "duration": 4,
        "bg": (30, 58, 100)
    },
    {
        "name": "03_solution",
        "lines": ["AI自动转录、提取任务、跟踪进度", "让你的会议真正产生价值"],
        "duration": 3,
        "bg": (37, 99, 235)  # 亮蓝
    },
    {
        "name": "04_feature1",
        "lines": ["🎙️ 智能转录", "录音 → 文字纪要 + 待办清单，一键完成"],
        "duration": 3,
        "bg": (30, 58, 138)
    },
    {
        "name": "05_feature2",
        "lines": ["📋 任务提取", "自动识别待办，分配负责人"],
        "duration": 3,
        "bg": (30, 58, 138)
    },
    {
        "name": "06_feature3",
        "lines": ["⏰ 自动提醒", "到期前自动提醒，支持多平台"],
        "duration": 3,
        "bg": (30, 58, 138)
    },
    {
        "name": "07_stats",
        "lines": ["93% ↓ 记录时间  |  88% ↓ 任务遗漏  |  42% ↑ 完成率", "基于20个团队内部测试数据"],
        "duration": 4,
        "bg": (16, 185, 129)  # 绿色
    },
    {
        "name": "08_ending",
        "lines": ["MeetingMate AI", "夺回你的会议时间 | 13128614087@163.com"],
        "duration": 3,
        "bg": (30, 58, 138)
    }
]

def create_text_image(lines, bg_color, width=1920, height=1080):
    """创建带文字的图像"""
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 尝试加载字体，如果失败则用默认字体
    try:
        # 尝试中文字体
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", 80)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", 50)
    except:
        try:
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # 绘制主标题
    line1 = lines[0]
    bbox1 = draw.textbbox((0, 0), line1, font=font_large)
    w1 = bbox1[2] - bbox1[0]
    h1 = bbox1[3] - bbox1[1]
    x1 = (width - w1) // 2
    y1 = height // 2 - h1 - 50
    draw.text((x1, y1), line1, fill=(255, 255, 255), font=font_large)
    
    # 绘制副标题
    if len(lines) > 1:
        line2 = lines[1]
        bbox2 = draw.textbbox((0, 0), line2, font=font_small)
        w2 = bbox2[2] - bbox2[0]
        h2 = bbox2[3] - bbox2[1]
        x2 = (width - w2) // 2
        y2 = height // 2 + 50
        draw.text((x2, y2), line2, fill=(180, 180, 180), font=font_small)
    
    return np.array(img)

def create_scene_video(scene_info):
    """创建单个场景视频"""
    output_path = f"demo_videos_cv/{scene_info['name']}.mp4"
    
    # 创建视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, FPS, (WIDTH, HEIGHT))
    
    # 生成帧
    total_frames = scene_info["duration"] * FPS
    
    for frame_idx in range(total_frames):
        # 创建图像
        img = create_text_image(scene_info["lines"], scene_info["bg"], WIDTH, HEIGHT)
        
        # BGR 转 RGB (OpenCV 使用 BGR)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        # 添加淡入淡出效果
        if frame_idx < 15:  # 淡入 0.5秒
            alpha = frame_idx / 15.0
            img = cv2.addWeighted(img, alpha, np.zeros_like(img), 1-alpha, 0)
        elif frame_idx > total_frames - 15:  # 淡出 0.5秒
            alpha = (total_frames - frame_idx) / 15.0
            img = cv2.addWeighted(img, alpha, np.zeros_like(img), 1-alpha, 0)
        
        out.write(img)
    
    out.release()
    print(f"✅ 已生成: {output_path} ({scene_info['duration']}秒)")
    return output_path

def merge_videos(video_files, output_path):
    """合并所有视频片段"""
    # 读取第一个视频获取参数
    cap = cv2.VideoCapture(video_files[0])
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, FPS, (WIDTH, HEIGHT))
    
    for video_file in video_files:
        cap = cv2.VideoCapture(video_file)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        cap.release()
    
    out.release()
    print(f"✅ 合并完成: {output_path}")

def main():
    print("=" * 60)
    print("🎬 MeetingMate AI 演示视频生成器 (OpenCV)")
    print("=" * 60)
    print()
    
    # 检查依赖
    try:
        import cv2
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install opencv-python-headless pillow numpy")
        return
    
    print(f"📋 共生成 {len(scenes)} 个视频片段\n")
    
    generated = []
    for i, scene in enumerate(scenes):
        print(f"[{i+1}/{len(scenes)}] {scene['name']}: {scene['lines'][0][:30]}...")
        try:
            path = create_scene_video(scene)
            generated.append(path)
        except Exception as e:
            print(f"❌ 生成失败: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ 视频片段生成完成！")
    print("=" * 60)
    print(f"\n📁 保存位置: ./demo_videos_cv/")
    print(f"✅ 成功生成: {len(generated)} 个片段")
    
    # 合并所有片段
    if generated:
        print("\n🔄 正在合并所有片段...")
        final_path = "demo_videos_cv/00_final_video.mp4"
        try:
            merge_videos(generated, final_path)
            
            # 计算总时长
            cap = cv2.VideoCapture(final_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / FPS
            cap.release()
            
            print(f"📹 总时长: {duration:.1f} 秒")
            print(f"\n🎉 演示视频已生成: {final_path}")
        except Exception as e:
            print(f"❌ 合并失败: {e}")
    
    print("\n💡 提示:")
    print("   1. 使用剪映打开 00_final_video.mp4")
    print("   2. 添加旁白和背景音乐")
    print("   3. 导出最终版本")

if __name__ == "__main__":
    main()
