#Developer: Matrix Huang
#Repo: https://github.com/WilsonHuang080705/PomodoroClock
import time
import random
from tkinter import Tk, Label, Button, StringVar, Entry

class PomodoroClock(Tk):
    #创建PomodoroCock类
    def __init__(self):
        super().__init__()
        self.title("番茄钟计时器")
        self.work_minutes = 25
        self.short_break_minutes = 5
        self.long_break_minutes = 15
        self.pomodoros_completed = 0
        self.paused = False
        self.remaining_time = None
        self.create_widgets()

    def create_widgets(self):
        # 创建输入框及变量
        work_label = Label(self, text="工作时长(分钟):")
        work_label.grid(row=0, column=0)
        self.work_var = StringVar(value=str(self.work_minutes))
        work_entry = Entry(self, textvariable=self.work_var)
        work_entry.grid(row=0, column=1)

        sb_label = Label(self, text="短休息时长(分钟):")
        sb_label.grid(row=1, column=0)
        self.sb_var = StringVar(value=str(self.short_break_minutes))
        sb_entry = Entry(self, textvariable=self.sb_var)
        sb_entry.grid(row=1, column=1)

        lb_label = Label(self, text="长休息时长(分钟):")
        lb_label.grid(row=2, column=0)
        self.lb_var = StringVar(value=str(self.long_break_minutes))
        lb_entry = Entry(self, textvariable=self.lb_var)
        lb_entry.grid(row=2, column=1)

        self.timer_label = Label(self, text="")
        self.timer_label.grid(row=3, column=0, columnspan=2)

        start_button = Button(self, text="开始", command=self.start_pomodoro)
        start_button.grid(row=4, column=0)
        
        pause_resume_button = Button(self, text="暂停/继续", command=self.toggle_pause)
        pause_resume_button.grid(row=4, column=1)

    def countdown(self, remaining_time, is_break=False, long_break=False):
        #创建倒计时函数
        if self.paused:
            return
        
        if remaining_time <= 0:
            if long_break:
                self.pomodoros_completed += 1
                self.show_random_message()
                self.countdown(self.long_break_minutes * 60, is_break=True, long_break=True)
            else:
                if is_break:
                    self.pomodoros_completed += 1
                    if self.pomodoros_completed % 4 == 0:
                        self.countdown(self.long_break_minutes * 60, is_break=True, long_break=True)
                    else:
                        self.countdown(self.short_break_minutes * 60, is_break=True)
                else:
                    self.countdown(self.work_minutes * 60)
            return

        minutes, seconds = divmod(remaining_time, 60)
        self.timer_label.config(text=f"剩余时间: {minutes:02d} 分钟 {seconds:02d} 秒")
        self.after(1000, lambda: self.countdown(remaining_time - 1, is_break=is_break, long_break=long_break))

    def toggle_pause(self):
        #暂停按钮
        self.paused = not self.paused
        if self.paused:
            self.timer_label.config(text="已暂停")
        else:
            self.countdown(self.remaining_time)

    def show_random_message(self):
        #展示“一言”功能
        messages = ["面朝大海，春暖花开。",
                    "想要的都拥有，得不到的都释怀。",
                    "明月松间照，清泉石上流",
                    "日出江花红胜火，春来江水绿如蓝。"]
        random_message = random.choice(messages)
        self.timer_label.config(text=random_message)

    def start_pomodoro(self):
        #启动番茄钟
        try:
            self.work_minutes = int(self.work_var.get())
            self.short_break_minutes = int(self.sb_var.get())
            self.long_break_minutes = int(self.lb_var.get())
        except ValueError:
            self.show_error_message("请输入有效的数字!")
            return

        self.remaining_time = self.work_minutes * 60
        self.countdown(self.remaining_time)

    def show_error_message(self, message):
        #报错信息
        self.timer_label.config(text=message)

if __name__ == "__main__":
    app = PomodoroClock()
    app.mainloop()