from qt_core import *

from functools import partial

from gui.widgets import PyGraphicsTextItem, PyIconButton

import re, os

class CreatePreviewText(QObject):
    text_data_updated = Signal(tuple)

    def __init__(self, video_item, graphics_scene, scroll_layout):
        super().__init__()

        self.text_data = []
        self.previous_text = {}

        self.video_item = video_item
        self.graphics_scene = graphics_scene
        self.scroll_layout = scroll_layout


    # LOADS THE SRT FILE AND WRITES IT TO A TEXT EDIT WITH ITS TIME
    # ///////////////////////////////////////////////////////////////

    def load_srt_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                srt_lines = file.readlines()

            transcripts = []  # Store parsed data

            for line in srt_lines:
                if '-->' in line:
                    start, end = line.strip().split(' --> ')
                    transcripts.append({'start': start, 'end': end, 'text': ''})
                else:
                    line = line.strip()
                    if line and transcripts:
                        transcripts[-1]['text'] += line + '\n'

            self.create_transcript_widgets(None, transcripts)

            file.close() 
            os.remove(file_path)

        except Exception as e:
            print("Error Writing Transcribe To Widget:", e)



    # CREATES THE TRANSCRIPT TEXT WIDGETS WITH ITS TIME
    # ///////////////////////////////////////////////////////////////

    def create_transcript_widgets(self, button_layout=None, transcripts={1}):

        text_and_duration = []

        for transcript in transcripts:
            print("Creating trans")
            if button_layout is None:
                start = transcript['start']
                end = transcript['end']
                text = transcript['text'].strip()
            else:
                start = None
                end = None
                text = ''

            add_button = PyIconButton(icon_path= r"gui\images\svg_icons\icon_add.svg", 
                                            width=20,
                                            height=20,
                                            parent = None,
                                            app_parent = None,
                                            tooltip_text=None,
                                            icon_margin=10,
                                            bg_color_hover = "#3c4454",
                                            bg_color="#3c4454",
                                            hover_effect=True
                                        )
            add_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            remove_button = PyIconButton(icon_path= r"gui\images\svg_icons\icon_minus.svg", 
                                            width=20,
                                            height=20,
                                            parent = None,
                                            app_parent = None,
                                            tooltip_text=None,
                                            icon_margin=10,
                                            bg_color_hover = "#3c4454",
                                            bg_color="#3c4454",
                                            hover_effect=True
                                        )
            remove_button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

            
            new_button_layout = QHBoxLayout()
            new_button_layout.addWidget(add_button)
            new_button_layout.addWidget(remove_button)
            new_button_layout.addStretch(1)

            # Duration / Transcript Text
            new_duration_line = QLineEdit()
            new_duration_line.setStyleSheet("border: none;")
            new_duration_line.setReadOnly(False)
            new_duration_line.setInputMask("99:99:99,999 \-\-\> 99:99:99,999")

            new_text_edit = QTextEdit()
            new_text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            new_text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            new_text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            new_text_edit.setText(text)



            add_button.clicked.connect(partial(self.create_transcript_widgets, new_button_layout))
            remove_button.clicked.connect(partial(self.remove_transcript_widgets, new_button_layout, new_duration_line, new_text_edit))
            
            new_duration_line.textChanged.connect(partial(self.change_text_duration, new_duration_line))
            new_text_edit.textChanged.connect(partial(self.change_text_preview, new_text_edit))

            if start is not None:
                duration_str = f"{start} --> {end}"
                new_duration_line.setText(duration_str)

                start_total_milliseconds, end_total_milliseconds = self.convert_to_ms(start, end)

                self.scroll_layout.addLayout(new_button_layout)
                self.scroll_layout.addWidget(new_duration_line)
                self.scroll_layout.addWidget(new_text_edit)

            else:
                # Get the duration text from the widget below the clicked button
                index = self.scroll_layout.indexOf(button_layout)
                if index != -1 and index + 1 < self.scroll_layout.count():
                    widget_below = self.scroll_layout.itemAt(index + 1).widget()
                    if isinstance(widget_below, QLineEdit):
                        new_duration_line.setText(widget_below.text())

                        new_start, new_end = widget_below.text().split('-->')
                        start_total_milliseconds, end_total_milliseconds = self.convert_to_ms(new_start, new_end)

                # Find the index of the clicked button's layout
                if index != -1:
                    # Insert new widgets above the clicked button
                    self.scroll_layout.insertLayout(index, new_button_layout)
                    self.scroll_layout.insertWidget(index + 1, new_duration_line)
                    self.scroll_layout.insertWidget(index + 2, new_text_edit)

            text_and_duration.append([new_duration_line, new_text_edit, start_total_milliseconds, end_total_milliseconds, new_button_layout])

        self.create_preview_text(text_and_duration)
            

        
    # CREATES THE QGRAPHICSTEXTITEM FOR THE VIDEO
    # ///////////////////////////////////////////////////////////////

    def create_preview_text(self, text_and_duration):

        try:
            for duration_line, text_edit, start_total_milliseconds, end_total_milliseconds, button_layout in text_and_duration:
                text_preview = PyGraphicsTextItem()
                text_preview.setDefaultTextColor(QColor("White"))
                text_edit.font().setPointSize(int(90))
                text_preview.setFont(text_edit.font())
                text_preview.setPlainText(text_edit.toPlainText())
                
                text_preview.setFlags(QGraphicsTextItem.ItemIsSelectable | QGraphicsTextItem.ItemIsMovable | QGraphicsTextItem.ItemIsFocusable)

                self.text_data.append([text_preview, duration_line, text_edit, start_total_milliseconds, end_total_milliseconds, button_layout])

                # Connect contentsChange signal and store the connection object
                text_preview.document().contentsChange.connect(partial(self.change_text_edit, text_item=text_preview))

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
            for text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds, btn_layout in self.text_data:
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

        for text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds, btn_layout in self.text_data:
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
        for index, (text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds, btn_layout) in enumerate(self.text_data):
            if duration_line_edit == time:
                text = duration_line_edit.text()
                match = re.match(r'(\d{2}:\d{2}:\d{2},\d{2,3}) \-\-\> (\d{2}:\d{2}:\d{2},\d{2,3})', text)
                if match:
                    start_time, end_time = match.group(1, 2)
                    
                    start_total_milliseconds, end_total_milliseconds = self.convert_to_ms(start_time, end_time)
                    
                    # Update the tuple in self.text_data with new start and end times
                    self.text_data[index] = (text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds, btn_layout)
                    self.text_data_updated.emit(self.text_data)
                else:
                    print("Invalid time format")

    # CONVERTS TIME TO MILLISECONDS
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
    



    # DELETES EVERYTHING / SPECIFIC TRANSCRIPTS
    # ///////////////////////////////////////////////////////////////

    def remove_transcript_widgets(self, button_layout=None, duration_line=None, text_edit=None):
        try:
            if duration_line is None:
                if hasattr(self, 'text_data') and self.text_data:
                    for text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds, btn_layout in self.text_data:
                        self.remove_widget_from_layout(duration_line_edit)
                        self.remove_widget_from_layout(text_edit_widget)
                        self.remove_layout_widgets(btn_layout)
                        text_preview.deleteLater()

                    self.text_data.clear()
            
            else:
                for text_preview, duration_line_edit, text_edit_widget, start_total_milliseconds, end_total_milliseconds, btn_layout in self.text_data:
                    if duration_line == duration_line_edit and text_edit == text_edit_widget:
                        self.graphics_scene.removeItem(text_preview)
                        self.remove_widget_from_layout(duration_line)
                        self.remove_widget_from_layout(text_edit)
                        self.remove_layout_widgets(btn_layout)
                        text_preview.deleteLater()
                        duration_line_edit.deleteLater()
                        text_edit_widget.deleteLater()

                self.text_data = [section for section in self.text_data if section[1] != duration_line]
            
            self.text_data_updated.emit(self.text_data)

        except Exception as e:
            print(f"Error in delete_text: {e}")

    def remove_widget_from_layout(self, widget):
        if widget:
            widget.setParent(None)
            widget.deleteLater()

    def remove_layout_widgets(self, layout):
        if layout:
            for i in reversed(range(layout.count())):
                widget = layout.itemAt(i).widget()
                self.remove_widget_from_layout(widget)
            layout.deleteLater()