from qt_core import *
from functools import partial
from gui.widgets import PyGraphicsTextItem
import re, os
import uuid

class CreatePreviewText(QObject):
    text_data_updated = Signal(dict)

    def __init__(self, video_item, graphics_scene, transcript_view, transcript_model, transcript_delegate):
        super().__init__()

        self.text_data_dict = {}  # Use a dictionary to map unique IDs to text data
        self.previous_text = {}

        self.video_item = video_item
        self.graphics_scene = graphics_scene

        self.transcript_view = transcript_view
        self.transcript_model = transcript_model
        self.transcript_delegate = transcript_delegate

        self.transcript_model.dataChanged.connect(self.handle_model_data_changed)
        self.transcript_delegate.add_transcript.connect(self.add_transcript)
        self.transcript_delegate.remove_transcript.connect(self.remove_transcript_widgets)

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
        os.remove(file_path)
        self.create_preview_text(for_all=True)

    # CREATES THE QGRAPHICSTEXTITEM TEXT PREVIEW
    # ///////////////////////////////////////////////////////////////

    def create_preview_text(self, for_all=False, subtitle_id=None):
        try:
            if for_all:
                for subtitle in self.transcript_model.subtitles:
                    self._create_single_preview(subtitle)
            else:
                self._create_single_preview(subtitle_id)

            self.text_data_updated.emit(self.text_data_dict)

        except Exception as e:
            print("Error creating: ", e)

    def _create_single_preview(self, subtitle):
        subtitle_id = subtitle['id']
        subtitle_duration = subtitle['duration']
        subtitle_text = subtitle['text']

        start_time, end_time = subtitle_duration.split(' --> ')
        start_total_milliseconds, end_total_milliseconds = self.convert_to_ms(start_time, end_time)

        text_preview = PyGraphicsTextItem()
        text_preview.setDefaultTextColor(QColor("White"))
        text_preview.setHtml(f'<div style="text-align: center;">{subtitle_text}</div>')
        text_preview.setFont(QFont("Roboto", 90))

        text_preview.adjustSize()
 

        text_preview.setPos(self.graphics_scene.sceneRect().center().x() - text_preview.boundingRect().center().x(), self.graphics_scene.sceneRect().center().y() - text_preview.boundingRect().center().y())
        
        text_preview.setFlags(QGraphicsTextItem.ItemIsSelectable | QGraphicsTextItem.ItemIsMovable | QGraphicsTextItem.ItemIsFocusable)

        # Connect contentsChange signal and store the connection object
        text_preview.document().contentsChange.connect(partial(self.handle_text_preview_change, subtitle_id=subtitle_id, text_preview=text_preview))

        self.text_data_dict[subtitle_id] = (text_preview, subtitle_duration, subtitle_text, start_total_milliseconds, end_total_milliseconds)

        text_preview.hide()
        self.graphics_scene.addItem(text_preview)

    # HANDLES THE SYNC BETWEEN THE TEXT PREVIEW CHANGES TO THE SUBTITLES
    # ///////////////////////////////////////////////////////////////

    def handle_text_preview_change(self, position, chars_removed, chars_added, subtitle_id, text_preview):
        
        text_preview.adjustSize()
        
        new_text = text_preview.toPlainText()
        self.update_subtitle_text(subtitle_id, new_text)

    def update_subtitle_text(self, subtitle_id, new_text):
        for subtitle in self.transcript_model.subtitles:
            if subtitle['id'] == subtitle_id:
                if subtitle['text'] != new_text:
                    subtitle['text'] = new_text
                    self.transcript_model.layoutChanged.emit()
                break

    # HANDLES THE SYNC BETWEEN THE SUBTITLES CHANGES TO THE TEXT PREVIEW
    # ///////////////////////////////////////////////////////////////

    def handle_model_data_changed(self, topLeft, bottomRight, roles):

        if Qt.DisplayRole in roles or Qt.EditRole in roles:
            for row in range(topLeft.row(), bottomRight.row() + 1):
                subtitle_index = row // 4
                if 0 <= subtitle_index < len(self.transcript_model.subtitles):
                    self.update_preview(subtitle_index)

    def update_preview(self, subtitle_index):
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
            self.text_data_updated.emit(self.text_data_dict)
        else:
            print(f"Subtitle with ID {subtitle_id} not found.")

    # SELECTS THE TRANSCRIPT TEXT TO SHOW USERS WHAT IS CURRENTLY SHOWING
    # ///////////////////////////////////////////////////////////////

    def transcript_select_text(self, subtitle_id):
        # Get the text for the given subtitle_id
        subtitle_entry = self.text_data_dict.get(subtitle_id)
        if subtitle_entry:
            text = subtitle_entry[2]  # text is the third item in the tuple

            # Find the row in the model that has this text
            for row in range(self.transcript_model.rowCount()):
                index = self.transcript_model.index(row, 0)  # Assuming text is in column 1
                if self.transcript_model.data(index, Qt.DisplayRole) == text:
                    self.transcript_view.scrollTo(index)
                    return
        else:
            print(f"Subtitle ID '{subtitle_id}' not found in text data dictionary.")



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
    
    def add_transcript(self, subtitle_id):

        # Add a single subtitle and create its preview
        prev_subtitles = self.transcript_model.subtitles[subtitle_id]
        duration = prev_subtitles['duration']
        new_id = str(uuid.uuid4())

        self.transcript_model.insertRow(subtitle_id, new_id, duration)
        new_subtitles = self.transcript_model.subtitles[subtitle_id]
        
        self.create_preview_text(for_all=False, subtitle_id=new_subtitles) 

    def remove_transcript_widgets(self, subtitle_id=None):
        try:
            if subtitle_id is None:
                if hasattr(self, 'text_data_dict') and self.text_data_dict:
                    for subtitle_index, (text_preview, subtitle_duration, subtitle_text, start_total_milliseconds, end_total_milliseconds) in self.text_data_dict.items():
                        text_preview.deleteLater()

                    self.text_data_dict.clear()
                    self.transcript_model.clearAllRows()
            else:
                subtitle = self.transcript_model.subtitles[subtitle_id]
                subtitle_index = subtitle['id']
                text_data_entry = self.text_data_dict.get(subtitle_index)

                if text_data_entry:
                    text_preview, subtitle_duration, subtitle_text, start_total_milliseconds_prev, end_total_milliseconds_prev = text_data_entry
                    text_preview.deleteLater()
                    self.text_data_dict.pop(subtitle_index)


                self.transcript_model.removeRow(subtitle_id)

            self.text_data_updated.emit(self.text_data_dict)

        except Exception as e:
            print(f"Error in delete_text: {e}")
