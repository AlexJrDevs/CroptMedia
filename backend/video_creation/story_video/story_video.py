import os
import datetime, random
import subprocess
import cv2
import numpy as np
from qt_core import *
from VideoTalkingTracker import VideoTalkingTracker

class StoryVideo(QThread):
    creating_video = Signal(str) 
    finished_subclip = Signal(str)

    def __init__(self, text_word_amount, subclip_durations, audio_transcribe, logger, video_path, gameplay_path=None):
        super().__init__()

        # Constants for target resolution
        self.target_width = 1080
        self.target_height = 1920

        if gameplay_path != None:
            self.video_height = int(self.target_height // 2)  # Half of the target height
        else:
            self.video_height = self.target_height

        self.movement_threshold = 28  # Threshold for stabilizing face tracking

        self.temp_dir = os.path.abspath(r'backend\tempfile')
        os.makedirs(self.temp_dir, exist_ok=True)

        self.text_word_amount = int(text_word_amount)
        self.top_video_file = video_path
        self.bottom_video_file = gameplay_path
        self.subclip_duration = subclip_durations
        self.audio_transcribe = audio_transcribe
        self.logger = logger

    def trim_video(self, input_file, start_time, end_time, output_file):
        duration = end_time - start_time
        ffmpeg_trim_command = [
            'ffmpeg',
            '-ss', str(start_time),
            '-i', input_file,
            '-t', str(duration),
            '-c:v', 'copy',
            '-c:a', 'copy',
            '-y',
            output_file
        ]
        subprocess.run(ffmpeg_trim_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    def run(self):
        try:
            start_time, end_time = (sum(int(x) * 60 ** i for i, x in enumerate(reversed(subclip_time.split(':')))) for subclip_time in self.subclip_duration)
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

            trimmed_video_file = os.path.join(self.temp_dir, f"Trimmed_Video_{timestamp}.mp4") # Trims the original video to the correct start and end time
            temp_output_file = os.path.join(self.temp_dir, f'temp_Video_{timestamp}.mp4') # Cv2 Final video without audio
            audio_file = os.path.join(self.temp_dir, f"Video_audio_{timestamp}.mp3") # Extracts the audio from the video
            output_file = os.path.join(self.temp_dir, f"Video_{timestamp}.mp4") # Adds the Cv2 video and audio together

            self.trim_video(self.top_video_file, start_time, end_time, trimmed_video_file)

            ffmpeg_audio = [
                'ffmpeg',
                '-i', trimmed_video_file,
                '-q:a', '0',
                '-map', 'a',
                '-y',
                audio_file
            ]
            subprocess.run(ffmpeg_audio, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

            self.audio_transcribe.start_transcribe(audio_file, self.text_word_amount, timestamp)

            cap = cv2.VideoCapture(trimmed_video_file)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            fps = cap.get(cv2.CAP_PROP_FPS)
            output_video = cv2.VideoWriter(temp_output_file, fourcc, fps, (self.target_width, self.target_height))
            

            if self.bottom_video_file:
                # Get the duration of the top video
                video_duration = frame_count / fps

                gameplay_cap = cv2.VideoCapture(self.bottom_video_file)
                gameplay_fps = gameplay_cap.get(cv2.CAP_PROP_FPS)
                gameplay_frame_count = int(gameplay_cap.get(cv2.CAP_PROP_FRAME_COUNT))
                gameplay_duration = gameplay_frame_count / gameplay_fps

                # Randomly select a start point within the gameplay video, ensuring there's enough duration left
                max_start_time = gameplay_duration - video_duration
                random_start_time = random.uniform(0, max_start_time)
                gameplay_cap.set(cv2.CAP_PROP_POS_MSEC, random_start_time * 1000)

            last_crop_x, last_crop_y = 0, 0

            self.creating_video.emit("Tracking Video Speaker(s)...")
            talking_tracker = VideoTalkingTracker()
            data = talking_tracker.process(trimmed_video_file)
            face_data = {frame_data.get("frame_number"): frame_data.get("faces", []) for frame_data in data}

            self.creating_video.emit("Creating Video...")

            for frame_number in range(frame_count):
                ret, frame = cap.read()

                print(int((frame_number / frame_count) * 100))
                if not ret:
                    break

                frame_has_face = face_data.get(frame_number, [])

                # Calculate the scaling factor
                scale_factor = max(self.target_width / frame_width, self.video_height / frame_height)
                
                # Calculate new dimensions
                new_width = int(frame_width * scale_factor)
                new_height = int(frame_height * scale_factor)
                
                # Resize the frame
                resized_frame = cv2.resize(frame, (new_width, new_height))

                if frame_has_face:
                    best_face = max(frame_has_face, key=lambda face: face['speaking_score'])

                    if best_face['speaking_score'] >= 0:
                        x1, y1, x2, y2 = best_face['x1'], best_face['y1'], best_face['x2'], best_face['y2']
                        face_center_x = int((x1 + x2) * scale_factor / 2)
                        face_center_y = int((y1 + y2) * scale_factor / 2)

                        crop_x = max(0, min(new_width - self.target_width, face_center_x - self.target_width // 2))
                        crop_y = max(0, min(new_height - self.video_height, face_center_y - self.video_height // 2))

                        if abs(crop_x - last_crop_x) < self.movement_threshold and abs(crop_y - last_crop_y) < self.movement_threshold:
                            crop_x, crop_y = last_crop_x, last_crop_y

                        last_crop_x, last_crop_y = crop_x, crop_y
                    else:
                        crop_x = (new_width - self.target_width) // 2
                        crop_y = (new_height - self.video_height) // 2
                else:
                    crop_x = (new_width - self.target_width) // 2
                    crop_y = (new_height - self.video_height) // 2

                # Ensure we have enough area to crop from
                crop_x = min(crop_x, new_width - self.target_width)
                crop_y = min(crop_y, new_height - self.video_height)

                # Crop the frame to 1080x960 or 1080x1920
                cropped_frame = resized_frame[crop_y:crop_y+int(self.video_height), crop_x:crop_x+self.target_width]

                # Create a black canvas of the target resolution
                canvas = np.zeros((self.target_height, self.target_width, 3), dtype=np.uint8)

                # Place the cropped frame at the top of the canvas
                canvas[:int(self.video_height), :] = cropped_frame

                if self.bottom_video_file:
                    ret_gameplay, gameplay_frame = gameplay_cap.read()
                    if ret_gameplay:
                        # Scale gameplay frame to cover the 1080x960 area
                        gameplay_height, gameplay_width = gameplay_frame.shape[:2]
                        gameplay_scale_factor = max(self.target_width / gameplay_width, (self.target_height - self.video_height) / gameplay_height)

                        new_gameplay_width = int(gameplay_width * gameplay_scale_factor)
                        new_gameplay_height = int(gameplay_height * gameplay_scale_factor)

                        # Resize the gameplay frame
                        gameplay_resized = cv2.resize(gameplay_frame, (new_gameplay_width, new_gameplay_height))

                        # Calculate the crop position to center the video
                        crop_x = (new_gameplay_width - self.target_width) // 2
                        crop_y = (new_gameplay_height - (self.target_height - self.video_height)) // 2

                        # Crop the frame to exactly fit 1080x960
                        gameplay_cropped = gameplay_resized[crop_y:crop_y + (self.target_height - self.video_height), crop_x:crop_x + self.target_width]

                        # Place the cropped gameplay frame on the canvas
                        canvas[self.video_height:, :] = gameplay_cropped

                output_video.write(canvas)


            cap.release()

            if self.bottom_video_file:
                gameplay_cap.release()
            output_video.release()


            ffmpeg_command = [
                'ffmpeg',
                '-i', temp_output_file,
                '-i', audio_file,
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-map', '0:v:0',
                '-map', '1:a:0',
                '-shortest',
                '-y',
                output_file
            ]

            process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            process.wait()
            successful = process.returncode

            if successful == 0:
                self.finished_subclip.emit(output_file)
            else:
                print("Error Story_Video: ", successful)

        except Exception as e:
            print("Error occurred:", str(e))