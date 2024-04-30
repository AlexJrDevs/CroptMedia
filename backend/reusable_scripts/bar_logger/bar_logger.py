
from qt_core import *

class BarLogger(QObject):
    
    # Signals That Are Send To Slots
    loading_percent = Signal(str)
    def __init__(self):
        super().__init__()

    def video_logger(self, process, duration):
        for line in process.stdout:
            if "time=" in line:
                time_info = line.split("time=")[1].split()[0]
                current_time = sum(float(x) * 60 ** i for i, x in enumerate(reversed(time_info.split(':'))))
                percentage_done = (current_time / duration) * 100
                percentage_done_str = "{:.2f}".format(percentage_done)
                self.loading_percent.emit(percentage_done_str)
                print(f"Percentage done: {percentage_done_str}%")




