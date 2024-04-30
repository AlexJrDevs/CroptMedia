# ///////////////////////////////////////////////////////////////
# NORMAL TEXT CREATION
# ///////////////////////////////////////////////////////////////

from moviepy.editor import TextClip

class TextStyle1():
    def __init__(self):
        super().__init__()
        self.text_clips_stroke = []
        self.text_clips = []

    
    def text_creation(self, transcript, font, font_size, text_color, stroke_width,
                        stroke_color, video_width, stroke_widths):
        
        for segment in transcript:
            text = " ".join(segment["words"])
            start_time = segment["start"]
            end_time = segment["end"]
            duration = end_time - start_time
            text_clip_stroke = TextClip(text, font=font, fontsize=font_size, color=text_color, stroke_width=stroke_widths,
                                        stroke_color=stroke_color, size=(video_width * 3 / 4 + stroke_width, None),
                                        method='caption', align="center")
            text_clip_stroke = text_clip_stroke.set_start(start_time).set_duration(duration).set_position('center')
            self.text_clips_stroke.append(text_clip_stroke)

        for segment in transcript:
            text = " ".join(segment["words"])
            start_time = segment["start"]
            end_time = segment["end"]
            duration = end_time - start_time
            text_clip = TextClip(text, fontsize=font_size, color=text_color, font=font,
                                size=(video_width * 3 / 4, None), method='caption', align="center")
            text_clip = text_clip.set_start(start_time).set_duration(duration).set_position('center')
            self.text_clips.append(text_clip)
        
        return self.text_clips_stroke, self.text_clips