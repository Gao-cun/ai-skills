---
name: time-manager
description: |
  时间管理助手 - 帮助用户进行每日时间规划和任务管理。触发条件：
  (1) 用户说"开启新的一天"、"进行时间规划"、"开始今天的工作"等开始日程规划
  (2) 用户说"今天已经结束"、"进行时间总结"、"结束今天的工作"等进行每日复盘
  (3) 用户需要查看、添加或更新任务
  (4) 用户需要查看或修改日程表
---

# Time Manager 时间管理助手

每日时间规划与任务管理工作流。

## 文件结构

```
time-manager/
├── scripts/
│   ├── datetime_util.py    # 日期时间工具
│   ├── task_manager.py     # 任务管理器
│   ├── schedule_manager.py # 日程管理器
│   └── personal_info.py    # 个人信息管理器
└── data/
    ├── personal_profile.json   # 个人信息
    ├── tasks.json              # 任务总表
    └── schedules/              # 每日日程目录
        └── schedule_YYYY-MM-DD.json
```

## 工作流程

### 流程A：开启新的一天（早间规划）

**触发词**：「开启新的一天」「进行时间规划」「开始今天的工作」

执行步骤：

#### Step 1: 获取当前时间

```bash
python3 scripts/datetime_util.py
```

输出示例：
```json
{"date": "2025-01-14", "time": "09:00:00", "weekday": "周二", "datetime": "2025-01-14 09:00:00"}
```

#### Step 2: 读取个人信息

```bash
python3 scripts/personal_info.py show
```

若用户名为空，询问并更新：
```bash
python3 scripts/personal_info.py set name "用户姓名"
python3 scripts/personal_info.py set role "职位"
python3 scripts/personal_info.py hours 09:00 18:00 12:00 13:00
```

#### Step 3: 查看待办任务和工作量

```bash
python3 scripts/task_manager.py pending
python3 scripts/task_manager.py summary
```

向用户展示：
- 未完成任务列表（名称、截止日期、预估工时、优先级）
- 剩余总工作量（预估小时数）
- 高优先级任务数量

#### Step 4: 询问是否添加新任务

提示用户：「是否需要添加新任务？请提供任务名称、描述、截止日期、预估工时和优先级」

添加任务：
```bash
python3 scripts/task_manager.py add "任务名称" "描述" "2025-01-20" 4 high
```

#### Step 5: 询问今日安排偏好

询问用户：
1. 今天有没有会议或突发事件占用时间？
2. 今天想处理复杂任务还是简单任务？
3. 是否有需要优先处理的事项？

#### Step 6: 生成时刻表

根据用户偏好和工作时间生成时刻表。格式示例：

| 时间 | 任务 | 类型 |
|------|------|------|
| 09:00-09:50 | 高优先级任务A | work |
| 09:50-10:00 | 休息 | break |
| 10:00-10:50 | 任务B | work |
| ... | ... | ... |

添加时间段：
```bash
python3 scripts/schedule_manager.py add 2025-01-14 09:00 09:50 "任务名称" 1 work
```

#### Step 7: 确认并保存

展示完整时刻表，询问是否需要微调。确认后保存。

输出：「今日规划已完成，祝工作顺利！」

---

### 流程B：结束一天（晚间复盘）

**触发词**：「今天已经结束」「进行时间总结」「结束今天的工作」

#### Step 1: 获取当前时间

```bash
python3 scripts/datetime_util.py
```

#### Step 2: 读取今日日程

```bash
python3 scripts/schedule_manager.py today
```

#### Step 3: 逐项询问完成情况

对每个时间段的任务，询问完成状态：
- completed（已完成）
- partial（部分完成）
- skipped（跳过）

更新状态：
```bash
python3 scripts/schedule_manager.py update 2025-01-14 09:00 completed "完成备注"
```

#### Step 4: 更新任务总表

根据完成情况更新任务状态和实际工时：
```bash
python3 scripts/task_manager.py status 1 completed "已完成"
python3 scripts/task_manager.py progress 1 4.5 "实际用时"
```

#### Step 5: 添加每日总结

```bash
python3 scripts/schedule_manager.py summary 2025-01-14 "今日完成X项任务，效率良好"
```

#### Step 6: 展示统计

向用户展示：
- 今日完成任务数
- 实际工作时长
- 明日待办事项
- 工作效率建议

---

## 数据格式参考

### 任务 (tasks.json)

```json
{
  "tasks": [{
    "id": 1,
    "name": "任务名称",
    "description": "描述",
    "deadline": "2025-01-20",
    "estimated_hours": 4,
    "actual_hours": 0,
    "priority": "high",
    "status": "pending",
    "created_at": "2025-01-14 09:00:00",
    "updated_at": "2025-01-14 09:00:00",
    "completed_at": null,
    "progress_notes": []
  }]
}
```

状态说明：
- `pending`: 未开始
- `in_progress`: 进行中
- `completed`: 已完成
- `cancelled`: 已取消

优先级：`high` / `medium` / `low`

### 日程 (schedule_YYYY-MM-DD.json)

```json
{
  "date": "2025-01-14",
  "created_at": "2025-01-14 09:00:00",
  "time_slots": [{
    "start": "09:00",
    "end": "09:50",
    "task_id": 1,
    "task_name": "任务名称",
    "type": "work",
    "status": "planned",
    "actual_notes": ""
  }],
  "notes": "今日备注",
  "daily_summary": null
}
```

时间段类型：`work` / `break` / `meeting` / `other`
时间段状态：`planned` / `completed` / `partial` / `skipped`

### 个人信息 (personal_profile.json)

```json
{
  "name": "用户名",
  "role": "职位",
  "organization": "组织",
  "work_hours": {
    "start": "09:00",
    "end": "18:00",
    "lunch_start": "12:00",
    "lunch_end": "13:00"
  },
  "preferences": {
    "focus_duration_minutes": 50,
    "break_duration_minutes": 10,
    "prefer_morning_for": "complex",
    "prefer_afternoon_for": "meetings"
  }
}
```

---

## 交互风格

- 使用中文与用户交流
- 保持友好、鼓励的语气
- 提供清晰的时间表格式
- 适时给出效率建议
