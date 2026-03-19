# Meeting Transcriber

## 描述
自动将会议录音转换为结构化会议纪要，包括要点总结、决策事项、待办任务。

## 使用场景
- 团队周会/日会记录
- 项目评审会议纪要
- 客户会议内容归档
- 培训/讲座内容整理

## 安装
```bash
openclaw skill install meeting-transcriber
```

## 使用
```bash
# 处理本地录音文件
openclaw run meeting-transcriber --audio /path/to/meeting.mp3 --output ./meeting-notes/

# 处理在线会议录音链接
openclaw run meeting-transcriber --url "https://example.com/meeting.mp3" --participants "张三,李四,王五"
```

## 配置
在 `~/.openclaw/config.json` 中添加：
```json
{
  "meeting-transcriber": {
    "whisper_api_key": "your-whisper-api-key",
    "language": "zh",
    "output_format": "markdown",
    "auto_summarize": true
  }
}
```

## 输出示例
输入：会议录音文件  
输出：
- `meeting_20260315_summary.md` - 会议纪要
- `meeting_20260315_action_items.json` - 待办任务列表
- `meeting_20260315_transcript.txt` - 完整转录文本
