from qt_core import *

from functools import partial

from gui.widgets import PyGraphicsTextItem

import re

class CreatePreviewText(QObject):
    text_data_updated = Signal(tuple)

    def __init__(self, video_item, graphics_scene):
        super().__init__()

        self.text_preview_widgets = []
        self.text_data = []
        self.previous_text = {}

        self.video_item = video_item
        self.graphics_scene = graphics_scene

        
    # CREATES THE QGRAPHICSTEXTITEM FOR THE VIDEO
    # ///////////////////////////////////////////////////////////////

    def create_preview_text(self, transcript_and_duration):

        try:
            duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds = transcript_and_duration
            text_preview = PyGraphicsTextItem()
            text_preview.setDefaultTextColor(QColor("White"))
            text_edit_widget.font().setPointSize(int(90))
            text_preview.setFont(text_edit_widget.font())
            text_preview.setPlainText(text_edit_widget.toPlainText())
            
            text_preview.setFlags(QGraphicsTextItem.ItemIsSelectable | QGraphicsTextItem.ItemIsMovable | QGraphicsTextItem.ItemIsFocusable)

            self.text_data.append([text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds])

            # Connect contentsChange signal and store the connection object
            text_preview.document().contentsChange.connect(partial(self.change_text_edit, text_item=text_preview))

            text_edit_widget.textChanged.connect(partial(self.change_text_preview, text_edit_widget))
            duration_line_edit.textChanged.connect(partial(self.change_text_duration, duration_line_edit))

            text_preview.hide()
            self.graphics_scene.addItem(text_preview)

            self.text_data_updated.emit(self.text_data)

        except Exception as e:
            print("Error creating: ", e)

    # UPDATES THE TEXT EDIT TO SYNC TO TEXT_PREVIEW
    # ///////////////////////////////////////////////////////////////

    def change_text_edit(self, position, charsRemoved, charsAdded, text_item):
        current_text = text_item.toPlainText()
        previous_text = self.previous_text.get(text_item, None)
        
        # Check if there's a change in text
        if current_text != previous_text:
            for text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds in self.text_data:
                if text_preview == text_item and text_edit_widget:
                    text_edit_widget.blockSignals(True)  # Disconnect signal temporarily
                    text_edit_widget.setPlainText(current_text)
                    self.previous_text[text_item] = current_text
                    text_edit_widget.blockSignals(False)  # Reconnect signal
                    break

    # UPDATES THE TEXT_PREVIEW TO SYNC TO TEXT EDIT
    # ///////////////////////////////////////////////////////////////

    def change_text_preview(self, text_edit):
        new_text = text_edit.toPlainText()
        cursor_position = text_edit.textCursor().position()

        for text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds in self.text_data:
            if text_edit_widget == text_edit:
                text_preview.blockSignals(True)  # Disconnect signal temporarily
                text_preview.setPlainText(new_text)
                # Restore cursor position in text_edit
                cursor = text_edit_widget.textCursor()
                cursor.setPosition(cursor_position)
                text_edit_widget.setTextCursor(cursor)
                text_edit_widget.blockSignals(False)  # Reconnect signal
                break

    # UPDATES THE TEXT_PREVIEW DURATION VISIBILITY
    # ///////////////////////////////////////////////////////////////

    def change_text_duration(self, time, *args):
        for index, (text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds) in enumerate(self.text_data):
            if duration_line_edit == time:
                text = duration_line_edit.text()
                match = re.match(r'(\d{2}:\d{2}:\d{2},\d{2,3}) \-\-\> (\d{2}:\d{2}:\d{2},\d{2,3})', text)
                if match:
                    start_time, end_time = match.group(1, 2)
                    
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
                    
                    # Update the tuple in self.text_data with new start and end times
                    self.text_data[index] = (text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds)
                    self.text_data_updated.emit(self.text_data)
                else:
                    print("Invalid time format")


    # DELETES EVERYTHING
    # ///////////////////////////////////////////////////////////////
    def delete_text(self, duration_line=None, text_edit=None):
        try:
            # If duration_line is None, delete everything
            if duration_line is None:
                for text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds in self.text_data:

                    # Remove all items in the graphics scene
                    for item in self.graphics_scene.items():
                        if isinstance(item, QGraphicsTextItem):
                            self.graphics_scene.removeItem(item)
                            item.deleteLater()
                
                self.text_data.clear()
            
            else:

                for text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds in self.text_data:
                    # Check if the current section matches the duration_line
                    if duration_line == duration_line_edit and text_edit == text_edit_widget:  # Adjust this comparison as needed
                        # Remove related items from the graphics scene
                        self.graphics_scene.removeItem(text_preview)

                        text_preview.deleteLater()
                        text_edit_widget.deleteLater()
                        duration_line_edit.deleteLater()

                        print("Remove")
                        
                        
                
                # Remove matching sections from self.text_data
                self.text_data = [section for section in self.text_data if section[1] != duration_line]  # Adjust as needed
                self.text_data_updated.emit(self.text_data)

        except Exception as e:
            print(f"Error in delete_text: {e}")
