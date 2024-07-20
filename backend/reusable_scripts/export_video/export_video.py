from bs4 import BeautifulSoup
from qt_core import *

import subprocess, cv2, datetime, os

class ExportVideo(QThread):

    exporting_video = Signal(str)
    video_completed = Signal()

    def __init__(self, save_location, text_and_stroke, video_location, ffmpeg_logger):
        super().__init__()
        self.text_and_stroke = text_and_stroke
        self.video_location = video_location
        self.ffmpeg_logger = ffmpeg_logger
        self.save_dir = save_location
    
    # CREATES THE VIDEO TEXT AND ADDS IT TO THE VIDEO
    # ///////////////////////////////////////////////////////////////

    def run(self):
        dialogues = []

        for html_file_path, pos_x, pos_y, stroke_size, stroke_color, start, end in self.text_and_stroke:
            with open(html_file_path, 'r') as file:
                html_content = file.read()
                
            soup = BeautifulSoup(html_content, 'html.parser')
            body_tag = soup.find('body')


            if body_tag:
                self.styles_attributes = self.retrieve_text_style(body_tag.get('style'))
                text_style = self.text_styles(soup, stroke_size, stroke_color)

                self.styles_attributes = ",".join(self.styles_attributes)
                text_style = "".join(text_style)

                new_dialogue = f"""Dialogue: {start},{end},Default,{{\pos({pos_x},{pos_y})}}{text_style}"""
                dialogues.append(new_dialogue)

            file.close()
            os.remove(html_file_path)



        create_ass_file = f"""[Script Info]
Title: Video Subtitles
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BorderStyle, Encoding, Alignment
Style: Default,{self.styles_attributes},&H00FFFFFF,&HFFFF00,&H00FFFFFF,0,0,7
Style: Background,{self.styles_attributes},&H00FFFFFF,&H000000FF,&H00000000,3,0,7

[Events]
Format: Start, End, Style, Text
"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        folder_path = "backend/tempfile/"
        ass_file_location = f"{folder_path}Subtitle_{timestamp}.ass"
        output_file = os.path.join(self.save_dir, f"Video_{timestamp}.mp4")

        for dialogue in dialogues:
            create_ass_file += f"{dialogue}\n"

        with open(ass_file_location, 'w') as file:
            file.write(create_ass_file)

        file.close()
        
        self.add_subtitle_to_video(self.video_location, ass_file_location, self.ffmpeg_logger, output_file)

    # FFMPEG CONVERTS SUBTITLES TO TEXT AND OVERLAPS IT ON VIDEO
    # ///////////////////////////////////////////////////////////////
        
    def add_subtitle_to_video(self, video_file, ass_file, ffmpeg_logger, output_file):
        
        self.exporting_video.emit("Exporting Video...")

        video_text = [
            "ffmpeg",
            "-y",
            "-i", video_file,
            "-vf", f"subtitles={ass_file}",
            "-c:a", "copy",
            output_file
        ]
        process = subprocess.Popen(video_text, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)

        try:
            video = cv2.VideoCapture(video_file)
            total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
            video.release()

            ffmpeg_logger.video_logger(process, total_frames)

            process.wait()
            
            # Ensure the process has completed and all handles are released
            if process.returncode == 0:
                print("Successfully Exported Video")
            else:
                print("Error Exporting Video, File: Export_video")
            
        finally:
            # Attempt to delete files
            try:
                os.remove(ass_file)
                os.remove(video_file)
            except FileNotFoundError:
                print(f"File not found: {ass_file} or {video_file}")
            except PermissionError as e:
                print(f"Permission error: {e}")
            except Exception as e:
                print(f"Error deleting file: {e}")

        if process.returncode == 0:
            self.video_completed.emit()



    # ADDS ANY TEXT STYLE TO THE TEXT
    # ///////////////////////////////////////////////////////////////

    def text_styles(self, soup, stroke_size, stroke_color):
        text_styles = []
        paragraph = soup.find_all('p')
        span_elements = soup.find_all('span')
        last_part = ""

        if paragraph:
            for paragraph_element in paragraph:
                for index, content in enumerate(paragraph_element.contents):
                    if isinstance(content, str):
                        written_text = content.strip()
                        if index == 0:
                            text_styles.append(written_text)
                        elif index == len(paragraph_element.contents) - 1:
                            last_part = written_text
                        else:
                            text_styles.append(written_text)


        if span_elements:

            for span in span_elements:

                style_attr = span.get('style')
                style_and_name = style_attr.split(';')

                # Initialize variables to hold style modifications
                italic_str = underline_str = ""
                color_str = background_color_str = text_stroke = ""
                font_weight_str = font_size_str = ""
                font_family_str = ""

                for text in style_and_name:
                    if ':' in text:
                        style = text.split(':')[0].strip()
                        style_name = text.split(':')[1].strip()

                        if stroke_size > 0:
                            hex_qcolor = stroke_color.name() # Converts QColor to hex
                            hex_color = hex_qcolor.replace('#', '')
                            red = int(hex_color[0:2], 16)
                            green = int(hex_color[2:4], 16)
                            blue = int(hex_color[4:6], 16)
                            text_stroke = f"\\bord{stroke_size}\\3c&H{blue:02X}{green:02X}{red:02X}&"

                        # Modify text based on style
                        if style_name == 'italic':
                            italic_str = "\\i1"

                        elif style_name == 'underline':
                            underline_str = "\\u1"

                        elif style == 'color':
                            hex_color = style_name.replace('#', '')
                            red = int(hex_color[0:2], 16)
                            green = int(hex_color[2:4], 16)
                            blue = int(hex_color[4:6], 16)
                            color_str = f"\\c&H{blue:02X}{green:02X}{red:02X}&"

                        elif style == 'background-color' and stroke_size <= 0:
                            hex_color = style_name.replace('#', '')
                            red = int(hex_color[0:2], 16)
                            green = int(hex_color[2:4], 16)
                            blue = int(hex_color[4:6], 16)
                            background_color_str = f"\\rBackground\\bord1\\3c&H{blue:02X}{green:02X}{red:02X}&"

                        elif style == 'font-weight':
                            font_weight_str = "\\b1"

                        elif style == 'font-size':
                            font_size = style_name.replace('pt', '')
                            font_size = float(font_size) * (1920 / 1080)
                            font_size_str = f"\\fs{font_size}"
                        
                        elif style == 'font-family':
                            style_name = style_name.replace("'", '')
                            font_family_str = f"\\fn{style_name}"

                        
                        # Combine all style modifications
                        text_style = "{" + text_stroke + background_color_str + color_str + italic_str + underline_str + font_size_str + font_family_str + font_weight_str + "}"  
                        text_with_styles = f"{text_style}{span.text}{{\\r}}" # \\r resets the style
            
                # Append modified text to the list
                text_styles.append(text_with_styles + last_part)

        return text_styles
    
    

    # Retrive the basic text style attributes
    # ///////////////////////////////////////////////////////////////

    def retrieve_text_style(self, style_attr):
        style_and_name = style_attr.split(';')
        style_attributes = []
        
        for text in style_and_name:
            if ':' in text:
                style_name = text.split(':')[1].strip().replace("'", '')
                if 'pt' in style_name:
                    style_name = style_name.replace('pt', '')
                    style_attributes.append(style_name)
                    break
                
                style_attributes.append(style_name)
        
        return style_attributes
    
