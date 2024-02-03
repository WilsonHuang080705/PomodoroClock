# Repo: https://github.com/WilsonHuang080705/PomodoroClock   
# Developer: Matrix Huang
import time 
import sys
import datetime
import argparse
import textwrap
import random
import signal
import asyncio

# 主要程序
async def main():
    # 设置中断信号处理函数
    signal.signal(signal.SIGINT, signal_handler)

    # 休息时长，工作时长
    parser = argparse.ArgumentParser(
        description=textwrap.dedent("""\
            The Pomodoro Technique is a time management method developed by Francesco Cirillo in the late 1980s. To use the Pomodoro method, choose a task to be completed, set the Pomodoro time to 25 minutes, focus on the work, not allowed to do anything unrelated to the task until the Pomodoro clock rings, and then tick on the paper to take a short break (5 minutes will do), and every four Pomodoro are completed to take a break for a little longer。
            """),
        epilog=textwrap.dedent("""\
            CORE COMMANDS
            --w, --work       Set the work duration in minutes (default: 25)
            --sb, --short-break  Set the short break duration in minutes (default: 5)
            --lb, --long-break  Set the long break duration in minutes after four Pomodoros (default: 15)
            --help             Show this help message and exit.
            --version          Show program's version number and exit.
            """),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # 添加命令行参数
    parser.add_argument("--w", "--work", type=int, default=25, help="工作时长(分钟, 默认25分钟)")
    parser.add_argument("--sb", "--short-break", type=int, default=5, help="短休息时长(分钟, 默认5分钟)")
    parser.add_argument("--lb", "--long-break", type=int, default=15, help="长休息时长(分钟, 默认15分钟)")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0 Beta', help='显示程序版本信息')

    # 解析参数
    args = parser.parse_args()

    pomodoros_completed = 0

    while True:
        # 开始工作
        print(f"INFO 欢迎使用番茄钟! \nINFO 你可以在https://github.com/WilsonHuang080705/PomodoroClock来查看更多.\n\nINFO 开始工作，时长 {args.w} 分钟。\nINFO 按下Ctrl+C(Command+C)以退出番茄钟")
        start_time = datetime.datetime.now()
        remaining_time = args.w * 60

        countdown_task = asyncio.create_task(countdown("剩余时间:", remaining_time))

        await countdown_task

        print("\nINFO 工作完成了, 休息一下吧！\nINFO 按下Ctrl+C或Command+C以退出番茄钟")

        if pomodoros_completed % 4 == 0:
            print(f"INFO 4轮番茄钟已经过去, 进行长休息吧！时长 {args.lb} 分钟。INFO 按下Ctrl+C或Command+C以退出番茄钟")
            long_break_messages = ["面朝大海，春暖花开。", "想要的都拥有，得不到的都释怀。", "明月松间照，清泉石上流", "日出江花红胜火，春来江水绿如蓝。"]
            random_message = random.choice(long_break_messages)
            print(random_message)
            long_break_task = asyncio.create_task(countdown("INFO 长休息剩余时间:", args.lb * 60))
            await long_break_task
        else:
            short_break_task = asyncio.create_task(countdown("INFO 剩余时间:", args.sb * 60))
            await short_break_task

        pomodoros_completed += 1

async def countdown(prefix, seconds):
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    while datetime.datetime.now() < end_time:
        remaining_time = (end_time - datetime.datetime.now()).total_seconds()
        minutes, seconds = divmod(int(remaining_time), 60)  # 将分钟和秒数转换为整数
        print(f"{prefix} {minutes:02d} 分钟 {seconds:02d} 秒", end='\r')
        await asyncio.sleep(1)

def signal_handler(signal, frame):
    print("\nINFO 收到中断信号, 程序将退出。")
    sys.exit(0)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nINFO 收到中断信号, 程序将退出。")