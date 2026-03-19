#!/usr/bin/env python3
"""
使用 MoviePy 生成简单的演示视频
安装: pip install moviepy
"""

import os
from moviepy.editor import *
from moviepy.video.fx.all import fadein, fadeout

# 创建输出目录
os.makedirs("demo_videos_simple", exist_ok=True)

# 定义视频片段
scenes = [
    {
        "name": "01_opening",
        "text": "会议记录，从30分钟到2分钟",
        "subtext": "MeetingMate AI - 智能会议助手",
        "duration": 3
    },
    {
        "name": "02_problem", 
        "text": "这些场景，你是否熟悉？",
        "subtext": "会后整理记录要花30分钟 | 任务总被遗漏 | 历史决策难找",
        "duration": 4
    },
    {
        "name": "03_solution",
        "text": "AI自动转录、提取任务、跟踪进度",
        "subtext": "让你的会议真正产生价值",
        "duration": 3
    },
    {
        "name": "04_feature1",
        "text": "🎙️ 智能转录",
        "subtext": "录音 → 文字纪要 + 待办清单，一键完成",
        "duration": 3
    },
    {
        "name": "05_feature2",
        "text": "📋 任务提取",
        "subtext": "自动识别待办，分配负责人",
        "duration": 3
    },
    {
        "name": "06_feature3",
        "text": "⏰ 自动提醒",
        "subtext": "到期前自动提醒，支持多平台",
        "duration": 3
    },
    {
        "name": "07_stats",
        "text": "93% ↓ 记录时间  |  88% ↓ 任务遗漏  |  42% ↑ 完成率",
        "subtext": "基于20个团队内部测试数据",
        "duration": 4
    },
    {
        "name": "08_ending",
        "text": "MeetingMate AI",
        "subtext": "夺回你的会议时间 | 13128614087@163.com",
        "duration": 3
    }
]

def create_scene(scene_info, index):
    """创建单个视频片段"""
    
    # 背景颜色（根据索引循环）
    colors = ['#1e3a8a', '#1e40af', '#2563eb', '#3b82f6']
    bg_color = colors[index % len(colors)]
    
    # 创建背景
    bg = ColorClip(size=(1920, 1080), color=(30, 58, 138))  # 深蓝背景
    bg = bg.set_duration(scene_info["duration"])
    
    # 主标题
    txt_clip = TextClip(
        scene_info["text"],
        fontsize=80 if len(scene_info["text"]) < 20 else 60,
        color='white',
        font='Arial-Bold',
        method='caption',
        size=(1800, 400),
        align='center'
    ).set_duration(scene_info["duration"])
    txt_clip = txt_clip.set_position(('center', 400))
    
    # 副标题
    sub_clip = TextClip(
        scene_info["subtext"],
        fontsize=40,
        color='#94a3b8',
        font='Arial',
        method='caption',
        size=(1800, 200),
        align='center'
    ).set_duration(scene_info["duration"])
    sub_clip = sub_clip.set_position(('center', 600))
    
    # 合并
    video = CompositeVideoClip([bg, txt_clip, sub_clip])
    video = fadein(video, 0.5)
    video = fadeout(video, 0.5)
    
    # 保存
    output_path = f"demo_videos_simple/{scene_info['name']}.mp4"
    video.write_videofile(
        output_path,
        fps=30,
        codec='libx264',
        audio=False,
        verbose=False
    )
    
    print(f"✅ 已生成: {output_path}")
    return output_path

def main():
    print("=" * 60)
    print("🎬 MeetingMate AI 演示视频生成器 (MoviePy)")
    print("=" * 60)
    print()
    
    # 检查 moviepy
    try:
        import moviepy
    except ImportError:
        print("❌ 请先安装 moviepy:")
        print("   pip install moviepy")
        return
    
    print(f"📋 共生成 {len(scenes)} 个视频片段\n")
    
    generated = []
    for i, scene in enumerate(scenes):
        print(f"[{i+1}/{len(scenes)}] {scene['name']}: {scene['text'][:30]}...")
        try:
            path = create_scene(scene, i)
            generated.append(path)
        except Exception as e:
            print(f"❌ 生成失败: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 视频片段生成完成！")
    print("=" * 60)
    print(f"\n📁 保存位置: ./demo_videos_simple/")
    print(f"✅ 成功生成: {len(generated)} 个片段")
    
    # 合并所有片段
    if generated:
        print("\n🔄 正在合并所有片段...")
        clips = [VideoFileClip(f) for f in generated]
        final = concatenate_videoclips(clips, method="compose")
        final_path = "demo_videos_simple/00_final_video.mp4"
        final.write_videofile(
            final_path,
            fps=30,
            codec='libx264',
            audio=False,
            verbose=False
        )
        print(f"✅ 完整视频: {final_path}")
        print(f"📹 总时长: {final.duration:.1f} 秒")
        
        # 关闭 clips
        for c in clips:
            c.close()
        final.close()
    
    print("\n💡 提示:")
    print("   1. 使用剪映打开 00_final_video.mp4")
    print("   2. 添加旁白和背景音乐")
    print("   3. 导出最终版本")

if __name__ == "__main__":
    main()
