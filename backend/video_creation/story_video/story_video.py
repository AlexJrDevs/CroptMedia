import os
import random
import datetime
import subprocess
import cv2
from qt_core import *
from VideoTalkingTracker import VideoTalkingTracker

class StoryVideo(QThread):
    creating_video = Signal(str)
    finished_subclip = Signal(str)

    def __init__(self, word_amount, subclip_durations, audio_transcribe, logger, video_path, gameplay_path=None):
        super().__init__()

        self.crop_ratio = 0.9  # Adjust the ratio to control how much of the face is visible in the cropped video
        self.vertical_ratio = 9 / 16  # Aspect ratio for the vertical video
        self.movement_threshold = 28  # Threshold for face movement to stabilize cropping

        if word_amount == "0" or word_amount == "":
            word_amount = "1"

        self.text_word_amount = int(word_amount)
        self.temp_dir = os.path.abspath(r'backend\tempfile')

        # Ensure the temporary directory exists
        os.makedirs(self.temp_dir, exist_ok=True)

        # Setting properties
        self.top_video_file = video_path
        self.bottom_video_file = gameplay_path
        self.subclip_duration = subclip_durations
        self.audio_transcribe = audio_transcribe
        self.logger = logger

    def create_transcribe(self, audio_file, timestamp):
        transcript_location = self.audio_transcribe.start_transcribe(audio_file, self.text_word_amount, timestamp)
        return transcript_location

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
            # Parse the subclip duration to get start and end times
            start_time, end_time = (sum(int(x) * 60 ** i for i, x in enumerate(reversed(subclip_time.split(':')))) for subclip_time in self.subclip_duration)
            duration = end_time - start_time
            timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

            # Set up file paths for temporary output files
            trimmed_video_file = os.path.join(self.temp_dir, f"Trimmed_Video_{timestamp}.mp4")
            self.output_file = os.path.join(self.temp_dir, f"Video_{timestamp}.mp4")
            audio_file = os.path.join(self.temp_dir, f"Video_{timestamp}.mp3")

            # Trim the video first
            self.trim_video(self.top_video_file, start_time, end_time, trimmed_video_file)

            # Extract audio from the trimmed video
            ffmpeg_audio = [
                'ffmpeg',
                '-i', trimmed_video_file,
                '-q:a', '0',
                '-map', 'a',
                '-y',
                audio_file
            ]
            subprocess.run(ffmpeg_audio, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

            # Transcribe the extracted audio
            while True:
                if audio_file:
                    transcript_location = self.create_transcribe(audio_file, timestamp)
                    break

            # Load the trimmed video for face tracking and cropping
            cap = cv2.VideoCapture(trimmed_video_file)

            # Get the frame dimensions
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # TO DO: FIX THE RATIO TO BE 1080X1920, AND ADD OPTION FOR GAMEPLAY
            target_height = frame_height
            target_width = int(target_height * self.vertical_ratio)

            # Create a temporary file for the video without audio
            temp_output_file = os.path.join(self.temp_dir, f'temp_Video_{timestamp}.mp4')

            # Create a VideoWriter object to save the output video
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            fps = cap.get(cv2.CAP_PROP_FPS)
            output_video = cv2.VideoWriter(temp_output_file, fourcc, fps, (target_width, target_height))

            frame_number = 0
            last_crop_x, last_crop_y = 0, 0  # Initialize last cropping coordinates

            # Process the trimmed video using VideoTalkingTracker
            talking_tracker = VideoTalkingTracker()
            data = talking_tracker.process(trimmed_video_file)

            face_data = {frame_data.get("frame_number"): frame_data.get("faces", []) for frame_data in data}

            # Loop through each frame of the trimmed video
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Initialize crop coordinates
                crop_x, crop_y = 0, 0
                crop_x2, crop_y2 = target_width, target_height

                # Check if there are faces in the current frame
                frame_has_face = face_data.get(frame_number, [])

                if frame_has_face:
                    best_face = max(frame_has_face, key=lambda face: face['speaking_score'])

                    if best_face['speaking_score'] >= 0:
                        x1, y1, x2, y2 = best_face['x1'], best_face['y1'], best_face['x2'], best_face['y2']

                        # Calculate the crop coordinates
                        face_width = x2 - x1
                        face_height = y2 - y1
                        crop_x = max(0, x1 + (face_width - target_width) // 2)
                        crop_y = max(0, y1 + (face_height - target_height) // 2)
                        crop_x2 = min(crop_x + target_width, frame_width)
                        crop_y2 = min(crop_y + target_height, frame_height)

                        if abs(crop_x - last_crop_x) < self.movement_threshold and abs(crop_y - last_crop_y) < self.movement_threshold:
                            crop_x, crop_y = last_crop_x, last_crop_y
                            crop_x2 = min(crop_x + target_width, frame_width)
                            crop_y2 = min(crop_y + target_height, frame_height)

                        last_crop_x, last_crop_y = crop_x, crop_y
                    else:
                        # Center the crop if no face detected for too long
                        crop_x = max(0, (frame_width - target_width) // 2)
                        crop_y = max(0, (frame_height - target_height) // 2)
                        last_crop_x, last_crop_y = crop_x, crop_y
                else:
                    # Center the crop if no face detected for too long
                    crop_x = max(0, (frame_width - target_width) // 2)
                    crop_y = max(0, (frame_height - target_height) // 2)
                    last_crop_x, last_crop_y = crop_x, crop_y

                crop_x2 = min(crop_x + target_width, frame_width)
                crop_y2 = min(crop_y + target_height, frame_height)

                cropped_frame = frame[crop_y:crop_y2, crop_x:crop_x2]
                resized_frame = cv2.resize(cropped_frame, (target_width, target_height))
                output_video.write(resized_frame)

                frame_number += 1

            # Release the input and output video objects
            cap.release()
            output_video.release()

            # Use FFmpeg to add audio back to the cropped video
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
                self.output_file
            ]

            process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            stdout, stderr = process.communicate()
            self.creating_video.emit("Creating Video...")
            process.wait()
            successful = process.returncode

            if successful == 0:
                self.finished_subclip.emit(self.output_file)
            else:
                print("Error Story_Video: ", process.returncode)
                print("FFmpeg error output:", stderr)

        except Exception as e:
            print("Error occurred:", str(e))
