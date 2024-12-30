from colorama import Fore, Back, Style, init
import time
import math

class FormatTime:
    def __init__(self, seconds):
        self.seconds = seconds

    def get_format_time(self):
        h = self.seconds // 3600
        m = (self.seconds % 3600) // 60
        s = ((self.seconds % 3600) % 60)

        return h, m, s

class TextStyle:
    def __init__(self) -> None:
        init()

    def get_text(self, text: str, color: any = "", back: any = "") -> str:
        return color + back + str(text) + Style.RESET_ALL

class ProgressBar():
    def __init__(self, part) -> None:
        self.procent = 0
        self.all = part
        self.len = 60
        self.old = ""

        self.start_time = -1


    
    def progress(self, name):
        ts = TextStyle()
        print(f"\r {' ' * (self.len + len(self.old) + 10)}", end="")
        self.procent += 1
        procent = math.ceil((self.procent / self.all)  * 100)
        proc = math.ceil(self.len / 100 *  procent)
        bar = ts.get_text(text=" ", back=Back.WHITE) * proc + " " * (self.len - proc)
        procent = ts.get_text(text=str(procent) + "%", color=Fore.GREEN)
        print(f"\r {procent} |{bar}|: {ts.get_text(name, color=Fore.CYAN)}", end="")

        self.old = name

    def progress_with_time(self, name):

        if self.start_time != -1:
            curr_last = self.all - self.procent
            time_to_finish = int(curr_last * (time.time() - self.start_time))
            format_time = FormatTime(time_to_finish)
            h, m, s = format_time.get_format_time()
            time_str = f"{h}h {m}m {s}s"

            new_name = f"{name} || left: {time_str}"
        else:
            new_name = name

        self.progress(name=new_name)
        self.start_time = time.time()