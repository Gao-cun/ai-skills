#!/usr/bin/env python3
"""
个人信息管理器 - 管理用户个人信息和偏好设置
"""

import json
from pathlib import Path
from datetime import datetime


# 数据目录相对于skill目录
DATA_DIR = Path(__file__).parent.parent / "data"
PROFILE_FILE = DATA_DIR / "personal_profile.json"


def ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_profile():
    """加载个人信息"""
    ensure_data_dir()
    if PROFILE_FILE.exists():
        return json.loads(PROFILE_FILE.read_text(encoding="utf-8"))
    return create_default_profile()


def create_default_profile():
    """创建默认个人信息模板"""
    return {
        "name": "",
        "role": "",
        "organization": "",
        "work_hours": {
            "start": "09:00",
            "end": "18:00",
            "lunch_start": "12:00",
            "lunch_end": "13:00"
        },
        "preferences": {
            "focus_duration_minutes": 50,
            "break_duration_minutes": 10,
            "prefer_morning_for": "complex",  # complex/simple
            "prefer_afternoon_for": "meetings"
        },
        "reminders": [],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


def save_profile(data):
    """保存个人信息"""
    ensure_data_dir()
    data["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    PROFILE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def update_profile(updates):
    """更新个人信息"""
    profile = load_profile()
    for key, value in updates.items():
        if isinstance(value, dict) and key in profile and isinstance(profile[key], dict):
            profile[key].update(value)
        else:
            profile[key] = value
    save_profile(profile)
    return profile


def set_work_hours(start, end, lunch_start=None, lunch_end=None):
    """设置工作时间"""
    profile = load_profile()
    profile["work_hours"]["start"] = start
    profile["work_hours"]["end"] = end
    if lunch_start:
        profile["work_hours"]["lunch_start"] = lunch_start
    if lunch_end:
        profile["work_hours"]["lunch_end"] = lunch_end
    save_profile(profile)
    return profile


def add_reminder(content, time=None, recurring=False):
    """添加提醒"""
    profile = load_profile()
    reminder = {
        "id": len(profile["reminders"]) + 1,
        "content": content,
        "time": time,
        "recurring": recurring,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    profile["reminders"].append(reminder)
    save_profile(profile)
    return reminder


def get_work_preferences():
    """获取工作偏好设置"""
    profile = load_profile()
    return {
        "work_hours": profile.get("work_hours", {}),
        "preferences": profile.get("preferences", {})
    }


def main():
    """命令行接口"""
    import sys
    if len(sys.argv) < 2:
        print(json.dumps(load_profile(), ensure_ascii=False, indent=2))
        return
    
    cmd = sys.argv[1]
    
    if cmd == "show":
        print(json.dumps(load_profile(), ensure_ascii=False, indent=2))
    
    elif cmd == "init":
        profile = create_default_profile()
        save_profile(profile)
        print(json.dumps(profile, ensure_ascii=False, indent=2))
    
    elif cmd == "set":
        if len(sys.argv) < 4:
            print("用法: personal_info.py set <字段> <值>")
            return
        field = sys.argv[2]
        value = sys.argv[3]
        profile = update_profile({field: value})
        print(json.dumps(profile, ensure_ascii=False, indent=2))
    
    elif cmd == "hours":
        if len(sys.argv) < 4:
            print("用法: personal_info.py hours <开始时间> <结束时间> [午休开始] [午休结束]")
            return
        start = sys.argv[2]
        end = sys.argv[3]
        lunch_start = sys.argv[4] if len(sys.argv) > 4 else None
        lunch_end = sys.argv[5] if len(sys.argv) > 5 else None
        profile = set_work_hours(start, end, lunch_start, lunch_end)
        print(json.dumps(profile, ensure_ascii=False, indent=2))
    
    elif cmd == "preferences":
        print(json.dumps(get_work_preferences(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
