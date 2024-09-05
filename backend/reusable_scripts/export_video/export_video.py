from bs4 import BeautifulSoup
from qt_core import QThread, Signal
import subprocess
import datetime
import os, re

class ExportVideo(QThread):
    exporting_video = Signal(str)
    video_completed = Signal()

    def __init__(self, save_location, text_and_stroke, video_location, ffmpeg_logger):
        super().__init__()
        self.save_dir = save_location
        self.temp_dir = os.path.abspath(r'backend\tempfile')
        os.makedirs(self.temp_dir, exist_ok=True)

        self.text_and_stroke = text_and_stroke
        self.video_location = video_location
        self.ffmpeg_logger = ffmpeg_logger
        print("Video Name: ", self.video_location)

    def run(self):
        dialogues = self._create_dialogues()
        ass_content = self._create_ass_content(dialogues)
        ass_file_location = self._save_ass_file(ass_content)
        self._add_subtitle_to_video(ass_file_location)


    def _create_dialogues(self):
        dialogues = []
        for html_file_path, pos_x, pos_y, stroke_size, stroke_color, start, end, scale_factor in self.text_and_stroke:
            with open(html_file_path, 'r') as file:
                html_content = file.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            body_tag = soup.find('body')

            if body_tag:
                body_tag_style = body_tag.get('style')

                print("Stroke: ", stroke_size, stroke_color)
                text_styles = self.text_styles(soup, body_tag_style, stroke_size, stroke_color, scale_factor)
                text_styles = "".join(text_styles)
                
            new_dialogue = f"""Dialogue: {start},{end},Default,{{\pos({pos_x},{pos_y})}}{text_styles}"""
            dialogues.append(new_dialogue)

        return dialogues

    

    def text_styles(self, soup, body_tag_style, stroke_size, stroke_color, scale_factor):
        text_styles = []
        
        # Get all paragraphs
        paragraphs = soup.find_all('p')
        body_font_size = ""

        for style in body_tag_style.split(';'):
            if 'font-size' in style:
                body_font_size = style.split(':')[1].strip()
                body_font_size = (float(body_font_size.replace('pt', '')) * scale_factor) * 1.55
                body_font_size = f"{{\\fs{body_font_size}}}"

        stroke_style = ""
        if stroke_size > 0:
            print("Applying stroke to all text")
            hex_qcolor = stroke_color.name()  # Converts QColor to hex
            hex_color = hex_qcolor.replace('#', '')
            red = int(hex_color[0:2], 16)
            green = int(hex_color[2:4], 16)
            blue = int(hex_color[4:6], 16)
            text_stroke = f"{{\\bord{(stroke_size * scale_factor ) * 1.55}\\3c&H{blue:02X}{green:02X}{red:02X}&}}"

        for paragraph in paragraphs:
            paragraph_texts = []
            last_pos = 0
            
            # Apply body_font_size at the start of each paragraph
            paragraph_style = body_font_size + text_stroke
            
            # Iterate over all content inside the paragraph
            for content in paragraph.contents:
                if isinstance(content, str):
                    # Handle plain text
                    paragraph_texts.append((last_pos, last_pos + len(content), content, {}))
                    last_pos += len(content)
                elif content.name == 'span':
                    # Handle styled text in spans
                    style_attr = content.get('style', '')
                    style_and_name = style_attr.split(';')
                    
                    # Collect style attributes
                    style_modifiers = {
                        "italic": "",
                        "underline": "",
                        "font-weight": "",
                        "font-size": "",
                        "font-family": "",
                        "color": "",
                        "background-color": "",
                        "outline-color": "",
                        "outline": ""
                    }

                    for text in style_and_name:
                        if ':' in text:
                            style, value = map(str.strip, text.split(':'))

                            if style == 'color':
                                hex_color = value.replace('#', '')
                                red = int(hex_color[0:2], 16)
                                green = int(hex_color[2:4], 16)
                                blue = int(hex_color[4:6], 16)
                                style_modifiers['color'] = "\\c&H{0:02X}{1:02X}{2:02X}&".format(blue, green, red)

                            elif style == 'font-size':
                                font_size = (float(value.replace('pt', '')) * scale_factor) * (1920 / 1080)
                                style_modifiers['font-size'] = "\\fs{}".format(font_size)

                            elif style == 'font-family':
                                style_modifiers['font-family'] = "\\fn{}".format(value.replace('\'', ''))

                            elif style == 'font-weight':
                                style_modifiers['font-weight'] = "\\b1" if value == '700' else ""

                            elif style == 'italic':
                                style_modifiers['italic'] = "\\i1" if value == 'italic' else ""

                            elif style == 'underline':
                                style_modifiers['underline'] = "\\u1" if value == 'underline' else ""

                            elif style == 'background-color':
                                hex_color = value.replace('#', '')
                                red = int(hex_color[0:2], 16)
                                green = int(hex_color[2:4], 16)
                                blue = int(hex_color[4:6], 16)
                                style_modifiers['background-color'] = f"\\rBackground\\bord1\\3c&H{blue:02X}{green:02X}{red:02X}&"
                    

                    # Append styled text segment
                    styled_text = "{{{}}}{}{{\\r}}".format("".join([v for v in style_modifiers.values() if v]), content.text)
                    paragraph_texts.append((last_pos, last_pos + len(content.text), styled_text, style_modifiers))
                    last_pos += len(content.text)
            
            # Handle any trailing text
            if last_pos < len(paragraph.get_text()):
                trailing_text = paragraph.get_text()[last_pos:]
                paragraph_texts.append((last_pos, last_pos + len(trailing_text), trailing_text, {}))
            
            # Combine and format text segments
            formatted_text = paragraph_style  # Start with the body font size
            for start, end, text, styles in paragraph_texts:
                formatted_text += text
            
            text_styles.append(formatted_text)

        return " ".join(text_styles).strip()



        

    def _create_ass_content(self, dialogues):
        ass_content = [
            "[Script Info]",
            "Title: Video Subtitles",
            "ScriptType: v4.00+",
            "Collisions: Normal",
            "WrapStyle: 2"
            "PlayDepth: 0",
            "PlayResX: 1080",
            "PlayResY: 1920",
            "",
            "[V4+ Styles]",
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BorderStyle, Encoding, Alignment",
            f"Style: Default,Roboto,148.8,&H00FFFFFF,&HFFFF00,&H00FFFFFF,0,0,5",
            f"Style: Background,Roboto,148.8,&H00FFFFFF,&H000000FF,&H00000000,3,0,5",
            "",
            "[Events]",
            "Format: Start, End, Style, Text"
        ]
        
        for dialogue in dialogues:
            ass_content.append(dialogue)
        
        return "\n".join(ass_content)

    def _save_ass_file(self, ass_content):
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        ass_file_location = os.path.join(self.temp_dir, f"Subtitle_{timestamp}.ass")
        
        with open(ass_file_location, 'w', encoding='utf-8') as file:
            file.write(ass_content)
        
        return ass_file_location

    def _generate_output_filename(self):
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        return f"Video_{timestamp}.mp4"

    def _add_subtitle_to_video(self, ass_file):
        ffmpeg_command = [
            "ffmpeg",
            "-y",
            "-i", self.video_location,
            "-vf", f"subtitles={ass_file}",
            "-c:a", "copy",
            self.save_dir
        ]
        
        process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print("Successfully Exported Video")
            self.video_completed.emit()
        else:
            print("Error Exporting Video")
            print("FFmpeg stdout:", stdout)
            print("FFmpeg stderr:", stderr)
            self.exporting_video.emit("Error occurred during video export")

