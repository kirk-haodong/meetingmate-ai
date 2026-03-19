# MeetingMate AI

<p align="center">
  🦞 <strong>基于 OpenClaw 的智能会议助手与工作任务自动化系统</strong>
</p>

<p align="center">
  <a href="https://github.com/kirk-haodong/meetingmate-ai-website">
    <img src="https://img.shields.io/badge/Website-Online-blue?style=flat-square" alt="Website">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Python-3.8+-yellow?style=flat-square&logo=python" alt="Python">
  </a>
</p>

---

## 📖 项目简介

MeetingMate AI 是一个全自动化会议管理解决方案，通过 AI 技术实现「会议→任务→跟踪」全流程自动化，帮助团队减少无效会议时间，提升工作效率。

**核心数据**（基于20个团队内部测试）：
- 📉 会议记录时间减少 **93%**（30分钟 → 2分钟）
- 📉 任务遗漏率减少 **88%**（25% → 3%）
- 📈 任务按时完成率提升 **42%**（60% → 85%）

---

## ✨ 核心功能

| 功能 | 描述 | 效果 |
|------|------|------|
| 🎙️ **会议智能转录** | 语音识别 + AI提取要点 | 30分钟会议 → 2分钟生成纪要 |
| 📋 **任务自动提取** | 智能识别待办事项 | 自动提取90%以上会议任务 |
| ⏰ **自动提醒跟踪** | 定时任务 + 多通道通知 | 任务按时完成率提升40% |
| 🔍 **会议知识库** | 自动归档 + 语义检索 | 历史信息检索缩短98% |
| 📊 **效率分析** | 数据统计 + AI洞察 | 帮助减少无效会议20% |

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- OpenClaw 框架
- MiniMax / OpenAI API Key

### 安装

```bash
# 克隆项目
git clone https://github.com/kirk-haodong/meetingmate-ai.git
cd meetingmate-ai

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python scripts/init_db.py
```

### 配置

```bash
# 配置 API Keys
cp config.example.json config.json
# 编辑 config.json 填入你的 API Keys
```

### 使用

```bash
# 处理会议录音
python scripts/meetingmate_workflow.py --process-meeting \
  --audio /path/to/meeting.mp3 \
  --participants "张三,李四,王五" \
  --output ./output

# 查看待办任务
python skills/reminder-scheduler/scripts/main.py --list

# 搜索历史会议
python skills/meeting-search/scripts/main.py --query "Q2预算"

# 效率分析
python skills/meeting-analytics/scripts/main.py --report
```

---

## 📁 项目结构

```
meetingmate-ai/
├── 📄 README.md              # 项目说明
├── 📄 LICENSE                # 开源协议
├── 📄 requirements.txt       # Python依赖
├── 📄 config.example.json    # 配置模板
├── 📂 data/                  # 数据存储
│   └── meetings.db          # SQLite数据库
├── 📂 meeting-output/        # 会议输出
├── 📂 skills/                # OpenClaw Skills
│   ├── meeting-transcriber/  # 会议转录
│   ├── task-extractor/       # 任务提取
│   ├── reminder-scheduler/   # 提醒调度
│   ├── meeting-search/       # 会议搜索
│   └── meeting-analytics/    # 效率分析
├── 📂 scripts/               # 工具脚本
│   ├── meetingmate_workflow.py
│   ├── init_db.py
│   └── generate_demo_data.py
├── 📂 website/               # 产品官网
│   ├── index.html
│   └── static/
└── 📂 screenshots/           # 产品截图
```

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────┐
│           输入层 (Input Layer)           │
│  🎙️ 会议录音  💬 即时通讯  📧 邮件系统   │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       🤖 AI智能处理核心 (OpenClaw)        │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐       │
│  │ meeting-    │  │ task-       │       │
│  │ transcriber │  │ extractor   │       │
│  └─────────────┘  └─────────────┘       │
│  ┌─────────────┐  ┌─────────────┐       │
│  │ reminder-   │  │ meeting-    │       │
│  │ scheduler   │  │ search      │       │
│  └─────────────┘  └─────────────┘       │
└─────────────────┬───────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│           数据层 (Data Layer)            │
│  📝 会议纪要存储  🗄️ 任务数据库  🔍 知识库 │
└─────────────────────────────────────────┘
```

---

## 🌐 相关链接

- **产品官网**: [clawmate.cloud](https://clawmate.cloud)
- **比赛信息**: 中关村北纬龙虾大赛 · 生产力赛道
- **联系邮箱**: 13128614087@163.com

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

<p align="center">
  🦞 <em>Powered by OpenClaw | Created for 中关村北纬龙虾大赛</em>
</p>
