#!/usr/bin/env python3
"""
时间日期工具 - 获取当前日期和时间
"""

import datetime
import json


def get_current_datetime():
    """获取当前日期时间"""
    now = datetime.datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][now.weekday()],
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": now.timestamp()
    }


def get_today_filename():
    """获取今日日程文件名"""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"schedule_{today}.json"


def main():
    result = get_current_datetime()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
