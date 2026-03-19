# Reminder Scheduler

## 描述
智能任务提醒调度系统，根据任务截止日期自动发送提醒通知，支持邮件、企业微信、钉钉等多通道。

## 使用场景
- 会议待办任务到期提醒
- 项目里程碑节点提醒
- 周期性任务自动提醒
- 团队任务进度跟踪

## 安装
```bash
openclaw skill install reminder-scheduler
```

## 使用
```bash
# 添加任务提醒
openclaw run reminder-scheduler --add --task "完成Q1报告" --assignee "张三" --deadline "2026-03-20" --priority high

# 检查并发送到期提醒
openclaw run reminder-scheduler --check

# 查看所有待办任务
openclaw run reminder-scheduler --list

# 标记任务完成
openclaw run reminder-scheduler --complete --task-id "task_001"
```

## 配置
```json
{
  "reminder-scheduler": {
    "check_interval": "0 8,16 * * *",
    "notification_channels": ["email", "wechat"],
    "advance_notice_days": [1, 3, 7],
    "database_path": "~/meetingmate-ai/data/tasks.db"
  }
}
```

## 提醒规则
- 截止前7天: 发送首次提醒（低优先级任务）
- 截止前3天: 发送二次提醒（中优先级任务）
- 截止前1天: 发送紧急提醒（高优先级任务）
- 截止当天: 发送最终提醒（所有未完成任务）
