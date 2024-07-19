
from qt_core import *

from gui.widgets import PyIconButton

from functools import partial

import os


# Define the stylesheet
stylesheet = """
    /* QScrollBar */
    QScrollBar:vertical {
        background-color: transparent;
        width: 15px;
        margin: 15px 3px 15px 3px;
        border: 1px transparent #2A2929;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background-color: #1B1E23;
        min-height: 5px;
        border-radius: 4px;
    }
    QScrollBar::sub-line:vertical {
        margin: 3px 0px 3px 0px;
        border-image: url(:/qss_icons/rc/up_arrow_disabled.png);
        height: 10px;
        width: 10px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }

    QScrollBar::add-line:vertical
    {
        margin: 3px 0px 3px 0px;
        border-image: url(:/qss_icons/rc/down_arrow_disabled.png);
        height: 10px;
        width: 10px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }

    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical
    {
        background: none;
    }

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
    {
        background: none;
    }
    /* Add more QScrollBar styles as needed */
"""

# Define a style template for buttons
style_template = """ 
QPushButton::menu-indicator {{ 
    width:0px;
}}

QPushButton {{
    background-color: {};
}}
"""

class PyTranscriptWidget(QWidget):
    transcript_text = Signal(tuple)
    transcript_text_remove = Signal(QWidget, QWidget)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self._button_color = QColor("#343B48")
        self.text_and_duration = []

        layout = QVBoxLayout()

        # MAIN TRANSCRIPT
        # ///////////////////////////////////////////////////////////////

        # Transcript Line Edit
        self.transcript_line_edit = QLineEdit("Transcript will appear here...")
        self.transcript_line_edit.setReadOnly(True)
        self.transcript_line_edit.setStyleSheet("border: none;")

        # Scroll Container
        scroll_container = QWidget()
        scroll_container.setStyleSheet(
            "background-color: #343B48; border-radius: 15px;"
        )
        scroll_container_layout = QVBoxLayout(scroll_container)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.NoFrame)
        scroll_area.setStyleSheet(stylesheet)
        scroll_container_layout.addWidget(self.transcript_line_edit)
        scroll_container_layout.addWidget(scroll_area)

        # Scroll Content Widget
        scroll_content = QWidget(scroll_area)
        scroll_content.setStyleSheet("background-color: #343B48;")
        scroll_area.setWidget(scroll_content)

        self.scroll_layout = QVBoxLayout(scroll_content)


        # SETTING UP MAIN LAYOUT
        # ///////////////////////////////////////////////////////////////

        # Add layouts to main layout
        layout.addWidget(scroll_container)

        self.setLayout(layout)






    def load_srt_file(self, file_path):
        try:
            self.clear_transcript()
            self.transcript_line_edit.hide()

            with open(file_path, 'r') as file:
                srt_lines = file.readlines()

            for line in srt_lines:
                if '-->' in line:
                    start, end = line.strip().split(' --> ')

                    text_edit = self.create_transcript_widgets(None, start, end)
                else:
                    line = line.strip()
                    if line:
                        text_edit.setText(line)
                        
            file.close()
            os.remove(file_path)

        except Exception as e:
            print("Error Writing Transcribe To Widget:", e)

        
    def convert_to_time(self, start, end):
        start_parts = start.split(':')
        start_hours = int(start_parts[0])
        start_minutes = int(start_parts[1])
        start_seconds, start_milliseconds = map(int, start_parts[2].split(','))
        start_total_milliseconds = (start_hours * 3600 + start_minutes * 60 + start_seconds) * 1000 + start_milliseconds

        end_parts = end.split(':')
        end_hours = int(end_parts[0])
        end_minutes = int(end_parts[1])
        end_seconds, end_milliseconds = map(int, end_parts[2].split(','))
        end_total_milliseconds = (end_hours * 3600 + end_minutes * 60 + end_seconds) * 1000 + end_milliseconds

        return start_total_milliseconds, end_total_milliseconds

    def create_transcript_widgets(self, button_layout=None, start=None, end=None):

        add_button = PyIconButton(icon_path= r"gui\images\svg_icons\icon_add.svg", 
                                        width=20,
                                        height=20,
                                        parent = self,
                                        app_parent = self,
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
                                        parent = self,
                                        app_parent = self,
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

        if start is not None:
            duration_str = f"{start} --> {end}"
            new_duration_line.setText(duration_str)

            start_total_milliseconds, end_total_milliseconds = self.convert_to_time(start, end)

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
                    start_total_milliseconds, end_total_milliseconds = self.convert_to_time(new_start, new_end)

            # Find the index of the clicked button's layout
            if index != -1:
                # Insert new widgets above the clicked button
                self.scroll_layout.insertLayout(index, new_button_layout)
                self.scroll_layout.insertWidget(index + 1, new_duration_line)
                self.scroll_layout.insertWidget(index + 2, new_text_edit)

        add_button.clicked.connect(partial(self.create_transcript_widgets, new_button_layout))
        remove_button.clicked.connect(partial(self.remove_transcript_widgets, new_button_layout, new_duration_line, new_text_edit))

        self.text_and_duration.append([new_duration_line, new_text_edit, start_total_milliseconds, end_total_milliseconds, new_button_layout])
        self.transcript_text.emit([new_duration_line, new_text_edit, start_total_milliseconds, end_total_milliseconds])

        return new_text_edit



    def remove_transcript_widgets(self, button_layout, duration_line, text_edit):
        self.transcript_text_remove.emit(duration_line, text_edit)

        # Remove from layout
        self.scroll_layout.removeWidget(duration_line)
        self.scroll_layout.removeWidget(text_edit)
        self.scroll_layout.removeItem(button_layout)

        # Delete the widgets
        duration_line.deleteLater()
        text_edit.deleteLater()

        # Remove button layout
        for i in reversed(range(button_layout.count())):
            widget = button_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        button_layout.deleteLater()

        # Remove entry from internal lists
        self.text_and_duration = [entry for entry in self.text_and_duration if entry[0] != duration_line and entry[1] != text_edit]

        self.scroll_layout.update()

        
            
    def clear_transcript(self):
            
            # Clear existing widgets from text_and_duration and the scroll_layout
            if hasattr(self, 'text_and_duration') and self.text_and_duration:
                for duration_line, text_edit, start_ms, end_ms, btn_layout in self.text_and_duration:
                    self.scroll_layout.removeWidget(duration_line)
                    self.scroll_layout.removeWidget(text_edit)
                    self.scroll_layout.removeItem(btn_layout)
                    duration_line.deleteLater()
                    text_edit.deleteLater()

                    # Remove button layout
                    for i in reversed(range(btn_layout.count())):
                        widget = btn_layout.itemAt(i).widget()
                        if widget is not None:
                            widget.setParent(None)
                            widget.deleteLater()

                    btn_layout.deleteLater()
            
            self.text_and_duration.clear()

            self.transcript_line_edit.show()


