#!/usr/bin/env python3
"""
初始化数据库
"""

import sqlite3
import os
from pathlib import Path


def init_db():
    """初始化任务数据库"""
    db_path = os.path.expanduser("~/meetingmate-ai/data/tasks.db")
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建任务表
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
    
    # 创建提醒表
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
    
    print(f"✅ 数据库初始化完成: {db_path}")


if __name__ == "__main__":
    init_db()
