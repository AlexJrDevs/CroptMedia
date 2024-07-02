import whisper
from datetime import timedelta
import re
import os
from qt_core import *

class AudioTranscribe(QObject):

    transcript_location = Signal(str)
    transcript_started = Signal(str)

    def __init__(self):
        super(AudioTranscribe, self).__init__()
        self.segmentLength = None
        self.output = []
        self.video_dir = os.path.abspath(r'backend\tempfile')

    def transcribe(self, audioPath: str):
        model = whisper.load_model('base')
        result = model.transcribe(audioPath, word_timestamps=True)
        return result


    def writeSubtitlesIntoFile(self, inputResult: list[dict], outputPath: str, preferredSegmentLength: int):


        self.output.clear()
        self.segmentLength = len(inputResult)

        for i in range(self.segmentLength):
            words = inputResult[i]["words"]
            curSegmentLength = 0
            curSegmentStart = 0
            curSegmentEnd = 0
            curSegmentWords = []
            for j in range(len(words)):
                word = words[j]["word"].replace(" ", "")

                if j == 0: 
                    curSegmentStart = words[j]["start"]
                    curSegmentEnd = words[j]["end"]
                    curSegmentLength = len(word)
                    curSegmentWords.append(word)
                    continue
                

                if curSegmentLength + len(word) < preferredSegmentLength:
                    curSegmentWords.append(word)
                    curSegmentLength += len(word)
                    curSegmentEnd = words[j]["end"]
                else:
                    curSegmentLength = 0
                    self.output.append({"words": curSegmentWords[:], "start": curSegmentStart, "end": curSegmentEnd})
                    curSegmentWords.clear()
                    curSegmentStart = words[j]["start"]
                    curSegmentEnd = words[j]["end"]
                    curSegmentLength = len(word)
                    curSegmentWords.append(word)

            self.output.append({"words": curSegmentWords[:], "start": curSegmentStart, "end": curSegmentEnd})


        
        fileContent = ""
        segmentId = 0
        for segment in self.output:


            startTime = str(0)+str(timedelta(seconds=int(str(segment["start"]).split(".")[0])))+f",{str(segment['start']).split('.')[1]}0"
            if(segmentId < len(self.output) - 1 and self.output[segmentId+1]["start"] - segment["end"] <= 0.7):
                endTime = str(0)+str(timedelta(seconds=int(str(self.output[segmentId+1]["start"]).split(".")[0])))+f",{str(self.output[segmentId+1]['start']).split('.')[1]}0"
            else:
                segment["end"] += 0.5
                endTime = str(0)+str(timedelta(seconds=int(str(segment["end"]).split(".")[0])))+f",{str(segment['end']).split('.')[1]}0"
            text = " ".join(segment["words"])
            text = re.sub(f'[.,?"\-!]', '', text).upper() # Convert text to uppercase & Remove Some Characters
            segment = f"{startTime} --> {endTime}\n{text}\n\n"
            fileContent += segment
            segmentId += 1
        with open(outputPath, "w") as f:
            f.write(fileContent)




    def start_transcribe(self, path, characters, timestamp):
        # Locations to save
        self.transcript_started.emit("Creating Transcript...")
        transcript_location = os.path.join(self.video_dir, f"transcript_{timestamp}.srt")

        
        # Creates the subs in srt file
        self.writeSubtitlesIntoFile(self.transcribe(path)["segments"], transcript_location, characters)
        self.transcript_location.emit(transcript_location)
        return

        
        