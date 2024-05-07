import os
import random

import datetime

import subprocess

from ...reusable_scripts import *

from qt_core import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.main_window.functions_main_window import *


class StoryVideo(QThread):

    creating_video = Signal(str)

    def __init__(self, video_path, gameplay_path, subclip_duration, audio_transcribe, logger,):
        super().__init__()

        self.width, self.height = 1080, 1920

        # SETTING PROPERTIES
        self.top_video_file = video_path
        self.bottom_video_file = gameplay_path
        self.subclip_duration = subclip_duration
        self.subclip_amount = len(subclip_duration)
        self.logger = logger

        # NOT EDITABLE PUBLICALLY
        # //////////////////////////////////////////////////////
        self.temp_dir = os.path.abspath(r'backend\tempfile')
        self.files_list = []


        self.subtitle_segments = []

        self.audio_transcribe = audio_transcribe

        self.subclip_index = 0




    def create_transcribe(self, audio_file, timestamp):
        transcript_location = self.audio_transcribe.start_transcribe(audio_file, 10, timestamp)
        return transcript_location
    
        
        


    def run(self):
        try:
            if self.subclip_index < self.subclip_amount:
                start_time, end_time = (sum(int(x) * 60 ** i for i, x in enumerate(reversed(subclip_time.split(':')))) for subclip_time in self.subclip_duration[self.subclip_index])
                duration = end_time - start_time
                
                self.subclip_index += 1
 

                timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

                # Use ffmpeg to get the duration of the top and bottom videos
                top_video_start = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', self.top_video_file]).strip())
                bottom_video_start= random.uniform(0, top_video_start - duration)


                output_file = os.path.join(self.temp_dir, f"Video_{timestamp}.mp4")
                audio_file = os.path.join(self.temp_dir, f"Video_{timestamp}.mp3")

                self.files_list.append(output_file)
                
                ffmpeg_audio = [
                    'ffmpeg',
                    '-ss', str(start_time),
                    '-i', self.top_video_file,
                    '-ss', str(bottom_video_start),
                    '-i', self.bottom_video_file,
                    '-t', str(duration),
                    '-c:v', 'libmp3lame',
                    '-y',  # Overwrite output file if exists
                    audio_file
                ]

                subprocess.run(ffmpeg_audio, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)

                while True:
                    if audio_file:
                        transcript_location = self.create_transcribe(audio_file, timestamp)
                        break

                # Using ffmpeg to concatenate videos
                ffmpeg_video = [
                    'ffmpeg',
                    '-ss', str(start_time),
                    '-i', self.top_video_file,
                    '-ss', str(bottom_video_start),
                    '-i', self.bottom_video_file,
                    '-filter_complex', '[0:v]scale=-1:960[v0];[1:v]scale=-1:960[v1];[v0][v1]vstack, crop=w=1080:x=(iw-1080)/2',
                    '-t', str(duration),
                    '-c:v', 'libx264',
                    '-y',  # Overwrite output file if exists
                    output_file
                ]

                process = subprocess.Popen(ffmpeg_video, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
                self.creating_video.emit("Creating Video...")
                self.logger.video_logger(process, duration)
            
            else:
                self.subclip_amount = 0
                self.creating_video.emit("Subclips Completed")
        except Exception as e:
            print("Error occurred:", str(e))
    

    
    def get_output_files(self):
        return self.files_list[-1]

        
    


        

    
    

        

    



