#!/usr/bin/env python3
"""
MeetingMate AI 演示数据生成器
生成用于截图的产品界面数据
"""

import os
import json
from datetime import datetime, timedelta

# 创建演示输出目录
os.makedirs("demo_output", exist_ok=True)

# 1. 会议纪要示例
current_date = datetime.now().strftime("%Y年%m月%d日")
meeting_summary = f"""# 产品周会纪要

**会议时间**: {current_date} 14:00-15:00  
**参会人员**: 张三、李四、王五、赵六  
**会议时长**: 60分钟  
**记录人**: MeetingMate AI 🤖

---

## 🎯 会议要点

1. **Q2产品路线图确定**
   - 优先级1：AI会议纪要功能优化
   - 优先级2：多平台集成（钉钉/飞书/企业微信）
   - 优先级3：会议效率分析模块

2. **新功能需求讨论**
   - 用户反馈：希望支持实时转录
   - 技术评估：需要升级Whisper模型
   - 计划：Q2完成原型开发

3. **市场推广策略**
   - 参加中关村北纬龙虾大赛
   - 准备产品演示视频和网站
   - 目标：获取种子用户100+

---

## ✅ 待办任务

| 任务 | 负责人 | 截止日期 | 优先级 |
|------|--------|----------|--------|
| 完成用户调研报告 | 张三 | 3月20日 | 高 |
| 设计新版首页原型 | 李四 | 3月22日 | 高 |
| 准备比赛演示材料 | 王五 | 3月25日 | 中 |
| 联系钉钉开放平台 | 赵六 | 3月28日 | 中 |

---

## 💡 决策记录

- **决议1**: 采用MiniMax作为备用AI模型
- **决议2**: 网站采用无视频版方案
- **决议3**: 下周一开始内测

---

*本纪要由 MeetingMate AI 自动生成*  
*生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

# 2. 待办任务JSON
action_items = [
    {
        "task": "完成用户调研报告",
        "assignee": "张三",
        "deadline": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "priority": "high",
        "status": "pending",
        "source_meeting": "产品周会"
    },
    {
        "task": "设计新版首页原型",
        "assignee": "李四",
        "deadline": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
        "priority": "high",
        "status": "in_progress",
        "source_meeting": "产品周会"
    },
    {
        "task": "准备比赛演示材料",
        "assignee": "王五",
        "deadline": (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d"),
        "priority": "medium",
        "status": "pending",
        "source_meeting": "产品周会"
    },
    {
        "task": "联系钉钉开放平台",
        "assignee": "赵六",
        "deadline": (datetime.now() + timedelta(days=9)).strftime("%Y-%m-%d"),
        "priority": "medium",
        "status": "pending",
        "source_meeting": "产品周会"
    },
    {
        "task": "更新API文档",
        "assignee": "张三",
        "deadline": (datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d"),
        "priority": "high",
        "status": "overdue",
        "source_meeting": "技术评审会"
    }
]

# 3. 转录文本示例
transcript = """[00:00:00] 张三: 大家好，今天的周会开始。我们先回顾下上周的进度。
[00:02:15] 李四: 用户调研已经完成了80%，还有最后的报告需要整理。
[00:03:30] 张三: 好的，李四你明天能完成报告吗？
[00:03:45] 李四: 没问题，明天下班前提交。
[00:04:20] 王五: 网站设计我这边有新进展，准备了两套方案。
[00:05:10] 张三: 太好了，我们Q2的产品路线图需要尽快确定。
[00:06:30] 赵六: 钉钉集成的技术方案我已经评估过了，可行。
[00:08:15] 张三: 那赵六你负责联系钉钉开放平台，下周给个具体排期。
[00:09:00] 王五: 比赛演示材料我准备这周搞定。
[00:10:20] 张三: 行，那我们会议就到这里。大家辛苦了！"""

# 4. 会议列表
meetings = [
    {
        "id": "MTG001",
        "title": "产品周会",
        "date": (datetime.now() - timedelta(days=0)).strftime("%Y-%m-%d"),
        "duration": "60分钟",
        "participants": "张三、李四、王五、赵六",
        "key_decisions": 3,
        "action_items": 4
    },
    {
        "id": "MTG002",
        "title": "技术评审会",
        "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        "duration": "90分钟",
        "participants": "张三、李四、赵六",
        "key_decisions": 2,
        "action_items": 5
    },
    {
        "id": "MTG003",
        "title": "客户沟通会",
        "date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        "duration": "45分钟",
        "participants": "张三、王五",
        "key_decisions": 1,
        "action_items": 2
    }
]

# 5. 效率统计数据
analytics = {
    "total_meetings": 12,
    "total_hours": 18.5,
    "avg_duration": 52,
    "task_completion_rate": 85,
    "overdue_tasks": 1,
    "weekly_data": [
        {"week": "第1周", "meetings": 3, "hours": 4.5},
        {"week": "第2周", "meetings": 4, "hours": 6.0},
        {"week": "第3周", "meetings": 2, "hours": 3.5},
        {"week": "第4周", "meetings": 3, "hours": 4.5}
    ],
    "meeting_types": [
        {"type": "产品会议", "count": 5, "percentage": 42},
        {"type": "技术评审", "count": 4, "percentage": 33},
        {"type": "客户沟通", "count": 3, "percentage": 25}
    ]
}

# 保存文件
with open("demo_output/meeting_summary.md", "w", encoding="utf-8") as f:
    f.write(meeting_summary)

with open("demo_output/action_items.json", "w", encoding="utf-8") as f:
    json.dump(action_items, f, ensure_ascii=False, indent=2)

with open("demo_output/transcript.txt", "w", encoding="utf-8") as f:
    f.write(transcript)

with open("demo_output/meetings.json", "w", encoding="utf-8") as f:
    json.dump(meetings, f, ensure_ascii=False, indent=2)

with open("demo_output/analytics.json", "w", encoding="utf-8") as f:
    json.dump(analytics, f, ensure_ascii=False, indent=2)

print("✅ 演示数据生成完成!")
print("\n生成的文件:")
print("  📄 demo_output/meeting_summary.md - 会议纪要")
print("  📋 demo_output/action_items.json - 待办任务")
print("  📝 demo_output/transcript.txt - 转录文本")
print("  📁 demo_output/meetings.json - 会议列表")
print("  📊 demo_output/analytics.json - 效率数据")
