
from qt_core import *

class BarLogger(QObject):
    
    loading_percent = Signal(str)

    def __init__(self):
        super().__init__()

    # This checks for current frame and total frames to calculate the percentage done
    def video_logger(self, process, total_frames):
        for line in process.stdout:
            if "frame=" in line:
                current_frame = line.split("frame=")[1].split()[0]     
                percentage_done = (int(current_frame) / total_frames) * 100
                percentage_done_str = "{:.2f}".format(percentage_done)
                self.loading_percent.emit(percentage_done_str)




