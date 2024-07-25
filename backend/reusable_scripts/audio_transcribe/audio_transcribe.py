import whisperx
from datetime import timedelta
import torch
import re
import os
from qt_core import *

class AudioTranscribe(QObject):

    transcript_location = Signal(str)
    transcript_started = Signal(str)

    def __init__(self):
        super(AudioTranscribe, self).__init__()
        self.segment_length = None
        self.output = []
        self.video_dir = os.path.abspath(r'backend\tempfile')

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.batch_size = 16  # reduce if low on GPU mem
        self.compute_type = "float16" if torch.cuda.is_available() else "int8"  # change to "int8" if low on GPU mem (may reduce accuracy)

    def transcribe(self, audio_path: str):

        # 1. Transcribe with original whisper (batched)
        model = whisperx.load_model("medium", self.device, compute_type=self.compute_type)
        audio = whisperx.load_audio(audio_path)
        result = model.transcribe(audio, batch_size=self.batch_size)

        # 2. Align whisper output
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=self.device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, self.device, return_char_alignments=False)

        os.remove(audio_path)
        return result


    def writeSubtitlesIntoFile(self, input_results: list[dict], output_path: str, words_per_line: int):

        output = []
        self.segment_length = len(input_results)
        cur_segment_words = []
        cur_segment_start = None
        cur_segment_end = None

        for i in range(self.segment_length):
            words = input_results[i]["words"]

            for word_info in words:
                if "start" not in word_info or "end" not in word_info:
                    print(f"Skipping word with missing 'start' or 'end': {word_info}")
                    continue

                word = word_info["word"].strip()  # Remove leading/trailing spaces

                if not cur_segment_words:
                    cur_segment_start = word_info["start"]

                cur_segment_words.append(word)

                if len(cur_segment_words) >= words_per_line:
                    cur_segment_end = word_info["end"]
                    output.append({"words": cur_segment_words[:], "start": cur_segment_start, "end": cur_segment_end})
                
                    cur_segment_words = []
                    cur_segment_start = None
                    cur_segment_end = None

        # Add any remaining words as the last segment
        if cur_segment_words:
            cur_segment_end = words[-1]["end"]
            output.append({"words": cur_segment_words[:], "start": cur_segment_start, "end": cur_segment_end})


        
        file_content = ""
        for segment in output:
            start_seconds = int(segment["start"])
            start_milliseconds = int((segment["start"] - start_seconds) * 1000)
            start_time = timedelta(seconds=start_seconds, milliseconds=start_milliseconds)

            end_seconds = int(segment["end"])
            end_milliseconds = int((segment["end"] - end_seconds) * 1000)
            end_time = timedelta(seconds=end_seconds, milliseconds=end_milliseconds)

            start_time_str = f"{start_time.seconds//3600:02}:{(start_time.seconds//60)%60:02}:{start_time.seconds%60:02},{start_milliseconds:03d}"
            end_time_str = f"{end_time.seconds//3600:02}:{(end_time.seconds//60)%60:02}:{end_time.seconds%60:02},{end_milliseconds:03d}"

            text = " ".join(segment["words"])
            text = re.sub(f'[.,?"\-!]', '', text).upper()  # Convert text to uppercase & Remove Some Characters
            segment_text = f"{start_time_str} --> {end_time_str}\n{text}\n\n"
            file_content += segment_text


        with open(output_path, "w") as f:
            f.write(file_content)
            print("File has been written")




    def start_transcribe(self, path, words_per_line, time_stamp):
        # Locations to save
        self.transcript_started.emit("Creating Transcript...")
        transcript_location = os.path.join(self.video_dir, f"transcript_{time_stamp}.srt")

        
        # Creates the subs in srt file
        self.writeSubtitlesIntoFile(self.transcribe(path)["segments"], transcript_location, words_per_line)
        print(transcript_location)
        self.transcript_location.emit(transcript_location)

        
        