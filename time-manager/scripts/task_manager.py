#!/usr/bin/env python3
"""
任务管理器 - 管理任务总表（增删改查）
任务状态：pending(未开始), in_progress(进行中), completed(已完成), cancelled(取消)
"""

import json
import os
from pathlib import Path
from datetime import datetime


# 数据目录相对于skill目录
DATA_DIR = Path(__file__).parent.parent / "data"
TASKS_FILE = DATA_DIR / "tasks.json"


def ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text(json.dumps({"tasks": []}, ensure_ascii=False, indent=2))


def load_tasks():
    """加载所有任务"""
    ensure_data_dir()
    try:
        return json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    except:
        return {"tasks": []}


def save_tasks(data):
    """保存任务"""
    ensure_data_dir()
    TASKS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def add_task(name, description="", deadline="", estimated_hours=0, priority="medium"):
    """
    添加新任务
    Args:
        name: 任务名称
        description: 任务描述
        deadline: 截止日期 (YYYY-MM-DD)
        estimated_hours: 预估工时
        priority: 优先级 (high/medium/low)
    """
    data = load_tasks()
    task_id = len(data["tasks"]) + 1
    
    task = {
        "id": task_id,
        "name": name,
        "description": description,
        "deadline": deadline,
        "estimated_hours": estimated_hours,
        "actual_hours": 0,
        "priority": priority,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "completed_at": None,
        "progress_notes": []
    }
    
    data["tasks"].append(task)
    save_tasks(data)
    return task


def update_task_status(task_id, status, note=""):
    """更新任务状态"""
    data = load_tasks()
    for task in data["tasks"]:
        if task["id"] == task_id:
            task["status"] = status
            task["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if status == "completed":
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if note:
                task["progress_notes"].append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "note": note
                })
            save_tasks(data)
            return task
    return None


def update_task_progress(task_id, actual_hours, note=""):
    """更新任务进度"""
    data = load_tasks()
    for task in data["tasks"]:
        if task["id"] == task_id:
            task["actual_hours"] = actual_hours
            task["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if note:
                task["progress_notes"].append({
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "note": note
                })
            save_tasks(data)
            return task
    return None


def get_pending_tasks():
    """获取所有未完成的任务"""
    data = load_tasks()
    return [t for t in data["tasks"] if t["status"] in ["pending", "in_progress"]]


def get_tasks_by_status(status):
    """按状态获取任务"""
    data = load_tasks()
    return [t for t in data["tasks"] if t["status"] == status]


def get_tasks_summary():
    """获取任务统计摘要"""
    data = load_tasks()
    tasks = data["tasks"]
    return {
        "total": len(tasks),
        "pending": len([t for t in tasks if t["status"] == "pending"]),
        "in_progress": len([t for t in tasks if t["status"] == "in_progress"]),
        "completed": len([t for t in tasks if t["status"] == "completed"]),
        "cancelled": len([t for t in tasks if t["status"] == "cancelled"]),
        "total_estimated_hours": sum(t.get("estimated_hours", 0) for t in tasks if t["status"] in ["pending", "in_progress"]),
        "high_priority_pending": len([t for t in tasks if t["status"] in ["pending", "in_progress"] and t.get("priority") == "high"])
    }


def main():
    """命令行接口"""
    import sys
    if len(sys.argv) < 2:
        print(json.dumps(get_tasks_summary(), ensure_ascii=False, indent=2))
        return
    
    cmd = sys.argv[1]
    if cmd == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        if status:
            tasks = get_tasks_by_status(status)
        else:
            tasks = load_tasks()["tasks"]
        print(json.dumps(tasks, ensure_ascii=False, indent=2))
    
    elif cmd == "pending":
        print(json.dumps(get_pending_tasks(), ensure_ascii=False, indent=2))
    
    elif cmd == "add":
        if len(sys.argv) < 3:
            print("用法: task_manager.py add <任务名称> [描述] [截止日期] [预估工时] [优先级]")
            return
        name = sys.argv[2]
        desc = sys.argv[3] if len(sys.argv) > 3 else ""
        deadline = sys.argv[4] if len(sys.argv) > 4 else ""
        hours = float(sys.argv[5]) if len(sys.argv) > 5 else 0
        priority = sys.argv[6] if len(sys.argv) > 6 else "medium"
        task = add_task(name, desc, deadline, hours, priority)
        print(json.dumps(task, ensure_ascii=False, indent=2))
    
    elif cmd == "status":
        if len(sys.argv) < 4:
            print("用法: task_manager.py status <任务ID> <新状态> [备注]")
            return
        task_id = int(sys.argv[2])
        status = sys.argv[3]
        note = sys.argv[4] if len(sys.argv) > 4 else ""
        task = update_task_status(task_id, status, note)
        print(json.dumps(task, ensure_ascii=False, indent=2))
    
    elif cmd == "summary":
        print(json.dumps(get_tasks_summary(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
