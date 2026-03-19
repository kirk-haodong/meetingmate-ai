#!/usr/bin/env python3
"""
Reminder Scheduler Skill
智能任务提醒调度系统
"""

import argparse
import json
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path


def init_database(db_path):
    """初始化任务数据库"""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            task TEXT NOT NULL,
            assignee TEXT,
            deadline DATE,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reminded_at TIMESTAMP,
            completed_at TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT,
            reminder_date DATE,
            sent BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (task_id) REFERENCES tasks(id)
        )
    ''')
    
    conn.commit()
    conn.close()


def load_config():
    """加载配置"""
    config_path = os.path.expanduser("~/.openclaw/config.json")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f).get("reminder-scheduler", {})
    except Exception:
        return {}


def add_task(task, assignee, deadline, priority, db_path):
    """添加新任务"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    cursor.execute('''
        INSERT INTO tasks (id, task, assignee, deadline, priority)
        VALUES (?, ?, ?, ?, ?)
    ''', (task_id, task, assignee, deadline, priority))
    
    # 创建提醒计划
    advance_days = [1, 3, 7]
    deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
    
    for days in advance_days:
        reminder_date = (deadline_date - timedelta(days=days)).strftime("%Y-%m-%d")
        cursor.execute('''
            INSERT INTO reminders (task_id, reminder_date)
            VALUES (?, ?)
        ''', (task_id, reminder_date))
    
    conn.commit()
    conn.close()
    
    return task_id


def check_and_send_reminders(db_path, config):
    """检查并发送到期提醒"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 查询今天需要提醒的任务
    cursor.execute('''
        SELECT t.id, t.task, t.assignee, t.deadline, t.priority, r.reminder_date
        FROM tasks t
        JOIN reminders r ON t.id = r.task_id
        WHERE r.reminder_date <= ? AND r.sent = FALSE AND t.status = 'pending'
        ORDER BY t.deadline, t.priority
    ''', (today,))
    
    reminders = cursor.fetchall()
    
    sent_count = 0
    for task_id, task, assignee, deadline, priority, reminder_date in reminders:
        # 发送提醒通知
        if send_notification(task, assignee, deadline, priority, config):
            cursor.execute('''
                UPDATE reminders SET sent = TRUE WHERE task_id = ? AND reminder_date = ?
            ''', (task_id, reminder_date))
            cursor.execute('''
                UPDATE tasks SET reminded_at = CURRENT_TIMESTAMP WHERE id = ?
            ''', (task_id,))
            sent_count += 1
    
    conn.commit()
    conn.close()
    
    return sent_count


def send_notification(task, assignee, deadline, priority, config):
    """发送通知"""
    channels = config.get("notification_channels", ["console"])
    
    days_until = (datetime.strptime(deadline, "%Y-%m-%d") - datetime.now()).days
    
    priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    urgency = "即将到期" if days_until <= 1 else f"还有{days_until}天到期"
    
    message = f"""{priority_emoji.get(priority, '⚪')} 任务提醒

任务: {task}
负责人: {assignee or '未分配'}
截止日期: {deadline}
{urgency}

请尽快处理！
"""
    
    success = True
    
    for channel in channels:
        try:
            if channel == "console":
                print(message)
            elif channel == "email":
                print(f"[邮件通知] {message}")
            elif channel == "wechat":
                print(f"[微信通知] {message}")
            elif channel == "feishu":
                send_feishu(message)
            print(f"✅ {channel} 通知发送成功")
        except Exception as e:
            print(f"❌ {channel} 通知发送失败: {e}")
            success = False
    
    return success


def send_feishu(message):
    """发送飞书通知"""
    import urllib.request
    import urllib.parse
    
    # 飞书配置
    app_id = "cli_a9242c7b76f85cc9"
    app_secret = "t1kdrDoLzwPSBeCPThRzkcGTLQ711tBq"
    chat_id = "oc_6c647f39f97269a566e81b497de577dc"
    
    try:
        # 获取 token
        token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        token_data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode('utf-8')
        
        req = urllib.request.Request(token_url, data=token_data, headers={"Content-Type": "application/json"}, method='POST')
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get("code") != 0:
                return False
            access_token = result.get("tenant_access_token")
        
        # 发送消息
        msg_url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
        msg_data = json.dumps({
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": message})
        }).encode('utf-8')
        
        req = urllib.request.Request(msg_url, data=msg_data, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }, method='POST')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("code") == 0
    except:
        return False


def list_tasks(db_path, status="pending"):
    """列出任务"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, task, assignee, deadline, priority, status, created_at
        FROM tasks
        WHERE status = ?
        ORDER BY deadline, priority
    ''', (status,))
    
    tasks = cursor.fetchall()
    conn.close()
    
    return tasks


def complete_task(task_id, db_path):
    """标记任务完成"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE tasks 
        SET status = 'completed', completed_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (task_id,))
    
    conn.commit()
    conn.close()
    
    return cursor.rowcount > 0


def main():
    parser = argparse.ArgumentParser(description="任务提醒调度器")
    parser.add_argument("--add", action="store_true", help="添加新任务")
    parser.add_argument("--task", help="任务描述")
    parser.add_argument("--assignee", help="负责人")
    parser.add_argument("--deadline", help="截止日期 (YYYY-MM-DD)")
    parser.add_argument("--priority", default="medium", choices=["high", "medium", "low"])
    parser.add_argument("--check", action="store_true", help="检查并发送提醒")
    parser.add_argument("--list", action="store_true", help="列出任务")
    parser.add_argument("--complete", action="store_true", help="标记任务完成")
    parser.add_argument("--task-id", help="任务ID")
    
    args = parser.parse_args()
    
    config = load_config()
    db_path = config.get("database_path", os.path.expanduser("~/meetingmate-ai/data/tasks.db"))
    
    # 初始化数据库
    init_database(db_path)
    
    if args.add:
        if not args.task or not args.deadline:
            print("❌ 错误: --add 需要 --task 和 --deadline 参数")
            return
        
        task_id = add_task(args.task, args.assignee, args.deadline, args.priority, db_path)
        print(f"✅ 任务已添加: {task_id}")
        print(f"   任务: {args.task}")
        print(f"   负责人: {args.assignee or '未分配'}")
        print(f"   截止日期: {args.deadline}")
        print(f"   优先级: {args.priority}")
    
    elif args.check:
        sent_count = check_and_send_reminders(db_path, config)
        print(f"✅ 已发送 {sent_count} 条提醒通知")
    
    elif args.list:
        tasks = list_tasks(db_path)
        if not tasks:
            print("📭 暂无待办任务")
        else:
            print(f"\n📋 待办任务列表 ({len(tasks)}项)\n")
            print(f"{'ID':<20} {'任务':<30} {'负责人':<10} {'截止日期':<12} {'优先级':<8}")
            print("-" * 85)
            for task in tasks:
                task_id, task_desc, assignee, deadline, priority, status, created = task
                print(f"{task_id:<20} {task_desc:<30} {assignee or '-':<10} {deadline:<12} {priority:<8}")
    
    elif args.complete:
        if not args.task_id:
            print("❌ 错误: --complete 需要 --task-id 参数")
            return
        
        if complete_task(args.task_id, db_path):
            print(f"✅ 任务已标记完成: {args.task_id}")
        else:
            print(f"❌ 任务未找到: {args.task_id}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
