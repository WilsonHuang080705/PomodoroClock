#Repo: https://github.com/WilsonHuang080705/PomodoroClock
#Developer: Matrix Huang
import time 
import datetime
import argparse
import textwrap
import random

#主要程序
def main():
    #休息时长，工作时长
    parser = argparse.ArgumentParser(
        description=textwrap.dedent("""\
            The Pomodoro Technique is a time management method developed by Francesco Cirillo in the late 1980s. This method involves breaking work into short, focused intervals, typically 25 minutes in duration, known as 'Pomodoros'. After each Pomodoro, a 5-minute break is taken, and after completing four Pomodoros, a longer break of 15-30 minutes is recommended. The technique aims to enhance focus and productivity by setting short work cycles and regular breaks to prevent overexertion. It encourages individuals to avoid distractions and concentrate on a single task until the time is up, which is highly effective for improving work efficiency and reducing procrastination."""),
        epilog=textwrap.dedent("""\
            CORE COMMANDS
            -w, --work       Set the work duration in minutes (default: 25)
            -s, --short-break  Set the short break duration in minutes (default: 5)
            -l, --long-break  Set the long break duration in minutes after four Pomodoros (default: 15)
            --help             Show this help message and exit.
            --version          Show program's version number and exit.
            """),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    #添加命令行参数
    parser.add_argument("--w", "--work", type=int, default=25, help="工作时长(分钟, 默认25分钟)")
    parser.add_argument("--break", "--short-break", type=int, default=5, help="短休息时长(分钟, 默认5分钟)")
    parser.add_argument("--lb", "--long-break", type=int, default=15, help="长休息时长(分钟, 默认15分钟)")
    parser.add_argument('-v', '--version',action='version',version='%(prog)s 1.0.0 Beta',help='显示程序版本信息')

    #解析参数
    args = parser.parse_args()
    
    # 初始化番茄钟轮数
    pomodoros_completed = 0

    while True:
        # 开始工作
        print(f"开始工作，时长 {args.work} 分钟。")
        start_time = datetime.datetime.now()
        while (datetime.datetime.now() - start_time).seconds < args.work * 60:
            print(f"剩余时间: {args.work - (datetime.datetime.now() - start_time).seconds // 60} 分钟")
            time.sleep(1)

        # 工作完成，休息
        print("工作完成了，休息一下吧！")
        time.sleep(args.short_break * 60)

        # 更新番茄钟轮数
        pomodoros_completed += 1

        # 检查是否需要长休息
        if pomodoros_completed % 4 == 0:
            print(f"4轮番茄钟已经过去, 进行长休息吧！时长 {args.long_break} 分钟。")
            long_break_messages = ["面朝大海，春暖花开。", "想要的都拥有，得不到的都释怀。", "明月松间照，清泉石上流", "日出江花红胜火，春来江水绿如蓝。"]
            random_message = random.choice(long_break_messages)
            print(random_message)
            time.sleep(args.long_break * 60)
        else:
            print("继续下一个番茄钟。")

if __name__ == "__main__":
    main()