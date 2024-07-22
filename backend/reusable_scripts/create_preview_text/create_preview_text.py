from qt_core import *
from functools import partial
from gui.widgets import PyGraphicsTextItem, PyIconButton
import re, os
import uuid

class CreatePreviewText(QObject):
    text_data_updated = Signal(tuple)

    def __init__(self, video_item, graphics_scene, transcript_model):
        super().__init__()

        self.text_data_dict = {}  # Use a dictionary to map unique IDs to text data
        self.previous_text = {}

        self.video_item = video_item
        self.graphics_scene = graphics_scene
        self.transcript_model = transcript_model

        self.transcript_model.dataChanged.connect(self.handle_model_data_changed)

    # LOADS THE SRT FILE TO THE QAbstractItemModel
    # ///////////////////////////////////////////////////////////////

    def load_srt_file(self, file_path):
        transcript = []
        with open(file_path, 'r') as file:
            content = file.read()
            pattern = re.compile(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)(?=\n\n|\Z)', re.DOTALL)
            matches = pattern.findall(content)
            for match in matches:
                transcript.append({
                    'id': str(uuid.uuid4()),  # Generate a unique ID for each subtitle
                    'duration': f"{match[0]} --> {match[1]}",
                    'text': match[2].replace('\n', ' ')
                })
                
        self.transcript_model.subtitles = transcript
        self.transcript_model.layoutChanged.emit()
        self.create_preview_text()

    # CREATES THE QGRAPHICSTEXTITEM TEXT PREVIEW
    # ///////////////////////////////////////////////////////////////

    def create_preview_text(self):
        try:
            for subtitles in self.transcript_model.subtitles:
                subtitle_id = subtitles['id']
                subtitle_duration = subtitles['duration']
                subtitle_text = subtitles['text']

                start_time, end_time = subtitle_duration.split(' --> ')
                start_total_milliseconds, end_total_milliseconds = self.convert_to_ms(start_time, end_time)

                text_preview = PyGraphicsTextItem()
                text_preview.setDefaultTextColor(QColor("White"))
                text_preview.setPlainText(subtitle_text)
                
                text_preview.setFlags(QGraphicsTextItem.ItemIsSelectable | QGraphicsTextItem.ItemIsMovable | QGraphicsTextItem.ItemIsFocusable)

                # Connect contentsChange signal and store the connection object
                text_preview.document().contentsChange.connect(partial(self.handle_text_preview_change, subtitle_id=subtitle_id, text_item=text_preview))

                self.text_data_dict[subtitle_id] = (text_preview, subtitle_duration, subtitle_text, start_total_milliseconds, end_total_milliseconds)

                text_preview.hide()
                self.graphics_scene.addItem(text_preview)

            self.text_data_updated.emit(list(self.text_data_dict.values()))

        except Exception as e:
            print("Error creating: ", e)

    # HANDLES THE SYNC BETWEEN THE TEXT PREVIEW CHANGES TO THE SUBTITLES
    # ///////////////////////////////////////////////////////////////

    def handle_text_preview_change(self, position, chars_removed, chars_added, subtitle_id, text_item):
        new_text = text_item.toPlainText()
        self.update_subtitle_text(subtitle_id, new_text)

    def update_subtitle_text(self, subtitle_id, new_text):
        for subtitle in self.transcript_model.subtitles:
            if subtitle['id'] == subtitle_id:
                subtitle['text'] = new_text
                self.transcript_model.layoutChanged.emit()
                break

    # HANDLES THE SYNC BETWEEN THE SUBTITLES CHANGES TO THE TEX PREVIEW
    # ///////////////////////////////////////////////////////////////

    def handle_model_data_changed(self, topLeft, bottomRight, roles):
        if Qt.DisplayRole in roles or Qt.EditRole in roles:
            for row in range(topLeft.row(), bottomRight.row() + 1):
                subtitle_index = row // 2
                if 0 <= subtitle_index < len(self.transcript_model.subtitles):
                    self.update_preview(subtitle_index)

    def update_preview(self, subtitle_index):
        print("Update Text")
        subtitle = self.transcript_model.subtitles[subtitle_index]
        subtitle_id = subtitle['id']
        duration = subtitle['duration']
        text = subtitle['text']
        
        start_time, end_time = duration.split(' --> ')
        start_total_milliseconds, end_total_milliseconds = self.convert_to_ms(start_time, end_time)

        text_data_entry = self.text_data_dict.get(subtitle_id)
        if text_data_entry:
            text_preview, subtitle_duration, subtitle_text, start_total_milliseconds_prev, end_total_milliseconds_prev = text_data_entry
            text_preview.setPlainText(text)
            self.text_data_dict[subtitle_id] = (text_preview, subtitle_duration, subtitle_text, start_total_milliseconds, end_total_milliseconds)
            self.text_data_updated.emit(list(self.text_data_dict.values()))
        else:
            print(f"Subtitle with ID {subtitle_id} not found.")

    # MANAGEMENT
    # ///////////////////////////////////////////////////////////////

    def convert_to_ms(self, start_time, end_time):
        start_parts = start_time.split(':')
        start_hours = int(start_parts[0])
        start_minutes = int(start_parts[1])
        start_seconds, start_milliseconds = map(int, start_parts[2].split(','))
        start_total_milliseconds = (start_hours * 3600 + start_minutes * 60 + start_seconds) * 1000 + start_milliseconds
        
        end_parts = end_time.split(':')
        end_hours = int(end_parts[0])
        end_minutes = int(end_parts[1])
        end_seconds, end_milliseconds = map(int, end_parts[2].split(','))
        end_total_milliseconds = (end_hours * 3600 + end_minutes * 60 + end_seconds) * 1000 + end_milliseconds

        return start_total_milliseconds, end_total_milliseconds

    def remove_transcript_widgets(self, button_layout=None, duration_line=None, text_edit=None):
        try:
            if duration_line is None:
                if hasattr(self, 'text_data_dict') and self.text_data_dict:
                    for subtitle_id, (text_preview, subtitle_duration, subtitle_text, start_total_milliseconds, end_total_milliseconds) in self.text_data_dict.items():
                        text_preview.deleteLater()

                    self.text_data_dict.clear()
            

            self.text_data_updated.emit(list(self.text_data_dict.values()))

        except Exception as e:
            print(f"Error in delete_text: {e}")

