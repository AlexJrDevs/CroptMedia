from bs4 import BeautifulSoup
from qt_core import *

import subprocess, os, datetime

class ExportVideo:

    def __init__(self):
        super().__init__()
    
    def create_video(self, text_and_stroke, video_location):
        dialogues = []

        for html_file_path, stroke_size, stroke_color, start, end in text_and_stroke:
            with open(html_file_path, 'r') as file:
                html_content = file.read()
                
            soup = BeautifulSoup(html_content, 'html.parser')
            body_tag = soup.find('body')


            if body_tag:
                self.styles_attributes = self.retrieve_text_style(body_tag.get('style'))
                text_style = self.text_styles(soup, stroke_size, stroke_color)

                self.styles_attributes = ",".join(self.styles_attributes)
                text_style = "".join(text_style)

                new_dialogue = f"""Dialogue: {start},{end},Default,{text_style}"""
                dialogues.append(new_dialogue)


        create_ass_file = f"""[Script Info]
Title: Video Subtitles
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{self.styles_attributes},&H00FFFFFF,&H000000FF,&H00000000,&H000000FF,0,0,0,0,100,100,0,0,3,0,0,2,10,10,10,1

[Events]
Format: Start, End, Style, Text
"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        ass_file_location = f"backend/tempfile/Subtitle_{timestamp}.ass"

        for dialogue in dialogues:
            create_ass_file += f"{dialogue}\n"

        with open(ass_file_location, 'w') as file:
            file.write(create_ass_file)

        file.close()
        
        self.add_subtitle_to_video(video_location, ass_file_location)

    
    def add_subtitle_to_video(self, video_file, ass_file):
        command = [
            "ffmpeg",
            "-y",
            "-i", video_file,
            "-vf", f"subtitles={ass_file}",
            "-c:a", "copy",
            "output.mp4"
        ]
        subprocess.run(command, check=True)


    # ADDS ANY TEXT STYLE TO THE TEXT
    # ///////////////////////////////////////////////////////////////

    def text_styles(self, soup, stroke_size, stroke_color):
        text_styles = []
        paragraph = soup.find_all('p')
        span_elements = soup.find_all('span')

        if paragraph:
            for paragraph_element in paragraph:
                for content in paragraph_element.contents:
                    if isinstance(content, str):
                        written_text = content.strip()
                        text_styles.append(written_text)


        if span_elements:

            for span in span_elements:

                style_attr = span.get('style')
                style_and_name = style_attr.split(';')

                # Initialize variables to hold style modifications
                italic_str = italic_end = underline_str = underline_end = ""
                color_str = color_end = background_color_str = background_color_end = ""
                font_weight_str = font_weight_end = font_size_str = font_size_end = ""
                font_family_str = font_family_end = ""

                for text in style_and_name:
                    if ':' in text:
                        style = text.split(':')[0].strip()
                        style_name = text.split(':')[1].strip().replace("'", '')

                        # Modify text based on style
                        if style_name == 'italic':
                            italic_str = "{\\i1}"
                            italic_end = "{\\i0}"

                        elif style_name == 'underline':
                            underline_str = "{\\u1}"
                            underline_end = "{\\u0}"

                        elif style == 'color':
                            hex_color = style_name.replace('#', '')
                            red = int(hex_color[0:2], 16)
                            green = int(hex_color[2:4], 16)
                            blue = int(hex_color[4:6], 16)
                            color_str = f"{{\\c&H{blue:02X}{green:02X}{red:02X}&}}"
                            color_end = "{\\c&HFFFFFF&}" # Default next text color (if text is not set to a color), white text

                        elif style == 'background-color':
                            hex_color = style_name.replace('#', '')
                            red = int(hex_color[0:2], 16)
                            green = int(hex_color[2:4], 16)
                            blue = int(hex_color[4:6], 16)
                            background_color_str = f"{{\\bord1\\3c&H{blue:02X}{green:02X}{red:02X}&}}"
                            background_color_end = "{{\\bord0\\3c&H000000&}}" # Removes background color for the next text

                        elif style == 'font-weight':
                            font_weight_str = "{\\b1}"
                            font_weight_end = "{\\b0}"

                        elif style == 'font-size':
                            font_size = style_name.replace('pt', '')
                            font_size_str = f"{{\\fs{font_size}}}"
                            old_font_size = self.styles_attributes[1] # Default font size from text
                            font_size_end = f"{{\\fs{old_font_size}}}"
                        
                        elif style == 'font-family':
                            font_family_str = f"{{\\fn{style_name}}}"
                            old_font_family = self.styles_attributes[0]
                            font_family_end = f"{{\\fn{old_font_family}}}" # Default font family from text

                        
                        # Combine all style modifications
                        text_with_styles = (f"{italic_str}{underline_str}{color_str}{background_color_str}"
                                            f"{font_weight_str}{font_size_str}{font_family_str}"
                                            f"{span.text.strip()}"
                                            f"{italic_end}{underline_end}{color_end}{background_color_end}"
                                            f"{font_weight_end}{font_size_end}{font_family_end}")
            
                # Append modified text to the list
                text_styles.append(text_with_styles)

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
    


