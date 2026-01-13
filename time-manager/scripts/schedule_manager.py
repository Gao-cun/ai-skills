#!/usr/bin/env python3
"""
日程管理器 - 管理每日时刻表
每日日程以日期命名存储，格式：schedule_YYYY-MM-DD.json
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta


# 数据目录相对于skill目录
DATA_DIR = Path(__file__).parent.parent / "data"
SCHEDULES_DIR = DATA_DIR / "schedules"


def ensure_data_dir():
    """确保数据目录存在"""
    SCHEDULES_DIR.mkdir(parents=True, exist_ok=True)


def get_schedule_path(date=None):
    """获取指定日期的日程文件路径"""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    return SCHEDULES_DIR / f"schedule_{date}.json"


def load_schedule(date=None):
    """加载指定日期的日程"""
    ensure_data_dir()
    path = get_schedule_path(date)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "date": date or datetime.now().strftime("%Y-%m-%d"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "time_slots": [],
        "notes": "",
        "daily_summary": None
    }


def save_schedule(data, date=None):
    """保存日程"""
    ensure_data_dir()
    path = get_schedule_path(date or data.get("date"))
    data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def create_daily_schedule(date, time_slots, notes=""):
    """
    创建/更新每日日程
    Args:
        date: 日期 (YYYY-MM-DD)
        time_slots: 时间段列表，每个元素格式:
            {"start": "09:00", "end": "10:00", "task_id": 1, "task_name": "xxx", "type": "work/break/meeting"}
        notes: 备注
    """
    schedule = {
        "date": date,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "time_slots": time_slots,
        "notes": notes,
        "daily_summary": None
    }
    save_schedule(schedule, date)
    return schedule


def add_time_slot(date, start, end, task_name, task_id=None, slot_type="work"):
    """添加时间段到日程"""
    schedule = load_schedule(date)
    slot = {
        "start": start,
        "end": end,
        "task_id": task_id,
        "task_name": task_name,
        "type": slot_type,
        "status": "planned",  # planned/completed/skipped/partial
        "actual_notes": ""
    }
    schedule["time_slots"].append(slot)
    # 按开始时间排序
    schedule["time_slots"].sort(key=lambda x: x["start"])
    save_schedule(schedule, date)
    return schedule


def update_slot_status(date, start_time, status, notes=""):
    """更新时间段完成状态"""
    schedule = load_schedule(date)
    for slot in schedule["time_slots"]:
        if slot["start"] == start_time:
            slot["status"] = status
            slot["actual_notes"] = notes
            break
    save_schedule(schedule, date)
    return schedule


def add_daily_summary(date, summary):
    """添加每日总结"""
    schedule = load_schedule(date)
    schedule["daily_summary"] = {
        "content": summary,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    save_schedule(schedule, date)
    return schedule


def get_recent_schedules(days=7):
    """获取最近N天的日程"""
    ensure_data_dir()
    schedules = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        path = get_schedule_path(date)
        if path.exists():
            schedules.append(load_schedule(date))
    return schedules


def list_all_schedules():
    """列出所有日程文件"""
    ensure_data_dir()
    files = sorted(SCHEDULES_DIR.glob("schedule_*.json"), reverse=True)
    return [f.stem.replace("schedule_", "") for f in files]


def main():
    """命令行接口"""
    import sys
    if len(sys.argv) < 2:
        # 显示今日日程
        print(json.dumps(load_schedule(), ensure_ascii=False, indent=2))
        return
    
    cmd = sys.argv[1]
    
    if cmd == "today":
        print(json.dumps(load_schedule(), ensure_ascii=False, indent=2))
    
    elif cmd == "date":
        if len(sys.argv) < 3:
            print("用法: schedule_manager.py date <YYYY-MM-DD>")
            return
        date = sys.argv[2]
        print(json.dumps(load_schedule(date), ensure_ascii=False, indent=2))
    
    elif cmd == "recent":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        print(json.dumps(get_recent_schedules(days), ensure_ascii=False, indent=2))
    
    elif cmd == "list":
        print(json.dumps(list_all_schedules(), ensure_ascii=False, indent=2))
    
    elif cmd == "add":
        if len(sys.argv) < 6:
            print("用法: schedule_manager.py add <日期> <开始时间> <结束时间> <任务名称> [任务ID] [类型]")
            return
        date = sys.argv[2]
        start = sys.argv[3]
        end = sys.argv[4]
        task_name = sys.argv[5]
        task_id = int(sys.argv[6]) if len(sys.argv) > 6 else None
        slot_type = sys.argv[7] if len(sys.argv) > 7 else "work"
        result = add_time_slot(date, start, end, task_name, task_id, slot_type)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
