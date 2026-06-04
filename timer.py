#!/usr/bin/env python3
"""番茄工作法专注计时器"""

import time
import os
import json
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "记录.json")

WORK_MINUTES = 25
SHORT_BREAK = 5
LONG_BREAK = 15

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def format_time(seconds):
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"

def draw_timer(remaining, total, label, session_num):
    clear()
    pct = remaining / total
    bar_width = 30
    filled = int(bar_width * pct)
    bar = "█" * filled + "░" * (bar_width - filled)

    print()
    print("  ╔══════════════════════════════════════╗")
    print(f"  ║        🍅  番茄专注计时器              ║")
    print("  ╠══════════════════════════════════════╣")
    print(f"  ║  阶段：{label:<30}║")
    print(f"  ║  第 {session_num} 个番茄                         ║")
    print("  ║                                      ║")
    print(f"  ║      [{bar}]     ║")
    print(f"  ║              {format_time(remaining)}                 ║")
    print("  ║                                      ║")
    print("  ║       按 Ctrl+C 跳过当前阶段           ║")
    print("  ╚══════════════════════════════════════╝")

def countdown(minutes, label, session_num):
    total = minutes * 60
    remaining = total
    try:
        while remaining >= 0:
            draw_timer(remaining, total, label, session_num)
            time.sleep(1)
            remaining -= 1
        return True
    except KeyboardInterrupt:
        print("\n  ⏭️  跳过当前阶段...")
        time.sleep(1)
        return False

def load_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_session(label, duration_min):
    log = load_log()
    log.append({
        "时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "类型": label,
        "时长(分钟)": duration_min,
    })
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

def show_stats():
    log = load_log()
    if not log:
        print("  暂无记录。")
        return
    today = datetime.now().strftime("%Y-%m-%d")
    today_sessions = [e for e in log if e["时间"].startswith(today) and e["类型"] == "专注"]
    total_focus = sum(e["时长(分钟)"] for e in log if e["类型"] == "专注")
    print(f"\n  📊 今日完成番茄：{len(today_sessions)} 个")
    print(f"  ⏱️  历史总专注时长：{total_focus} 分钟")
    print()

def main():
    clear()
    print()
    print("  🍅  欢迎使用番茄专注计时器")
    print()
    print("  [1] 开始专注")
    print("  [2] 查看记录")
    print("  [3] 退出")
    print()
    choice = input("  请选择：").strip()

    if choice == "2":
        clear()
        print()
        show_stats()
        input("  按回车返回...")
        main()
        return
    elif choice == "3":
        print("  再见！保持专注 💪")
        return
    elif choice != "1":
        main()
        return

    session = 1
    while True:
        # 专注阶段
        done = countdown(WORK_MINUTES, "🍅 专注中", session)
        if done:
            save_session("专注", WORK_MINUTES)

        clear()
        print()
        print(f"  ✅ 第 {session} 个番茄完成！")
        show_stats()

        # 每4个番茄休息一次长休息
        if session % 4 == 0:
            print("  🎉 完成4个番茄，享受长休息！")
            input("  按回车开始长休息（15分钟）...")
            done = countdown(LONG_BREAK, "☕ 长休息", session)
            if done:
                save_session("长休息", LONG_BREAK)
        else:
            input("  按回车开始短休息（5分钟）...")
            done = countdown(SHORT_BREAK, "🌿 短休息", session)
            if done:
                save_session("短休息", SHORT_BREAK)

        clear()
        print()
        print(f"  休息结束！继续加油？")
        print("  [1] 继续下一个番茄")
        print("  [2] 查看记录并退出")
        c = input("  请选择：").strip()
        if c != "1":
            show_stats()
            break
        session += 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  再见！💪")
