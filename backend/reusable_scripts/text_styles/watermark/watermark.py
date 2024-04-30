from moviepy.editor import TextClip

class Watermark():
    def __init__(self):
        super().__init__()
        self.watermark_text_stroke = None
        self.watermark_text = None
        
    def create_watermark(self, watermark, font, text_color, stroke_width, stroke_color, video_width, subclip_duration):
        print("Inside Watermark")
        # WaterMark Text Creation
        self.watermark_text_stroke = TextClip(
            watermark,
            font=font,
            fontsize=45,
            color=text_color,
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            size=(video_width * 3/4 + stroke_width, None),
            method='caption',
            align="north",
        ).set_duration(subclip_duration).set_start(0).set_position(('center', 1180))

        self.watermark_text = TextClip(
            watermark,
            font=font,
            fontsize=45,
            color="white",
            size=(video_width * 3/4, None),
            method='caption',
            align="north",
        ).set_duration(subclip_duration).set_start(0).set_position(('center', 1180))

        return self.watermark_text_stroke, self.watermark_text
