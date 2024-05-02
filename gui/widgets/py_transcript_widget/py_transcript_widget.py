
from qt_core import *

from functools import partial


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

        # Done Button ( WILL BE SWITCHED TO SAVE PRESET )
        self.done_button = QPushButton("Done")
        layout.addWidget(self.done_button)

        self.setLayout(layout)






    def load_srt_file(self, file_path):

        try:
            self.transcript_line_edit.hide()
            with open(file_path, 'r') as file:
                srt_lines = file.readlines()

                self.text_and_duration.clear()

                for line in srt_lines:
                    if '-->' in line:
                        start, end = line.strip().split(' --> ')

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

                        duration_str = f"{start} --> {end}"
                        duration_line = QLineEdit(duration_str)
                        duration_line.setStyleSheet("border: none;")
                        duration_line.setReadOnly(False)
                        duration_line.setInputMask("99:99:99,999 \-\-\> 99:99:99,999")
                        self.scroll_layout.addWidget(duration_line)


                        text_edit = QTextEdit()
                        text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                        text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                        text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                        self.scroll_layout.addWidget(text_edit)
                        
                    else:
                        line = line.strip()  # Remove leading and trailing spaces
                        if line:  # Check if line is not empty after stripping
                            text_edit.append(line)
                            self.text_and_duration.append([duration_line, text_edit, start_total_milliseconds, end_total_milliseconds])

            self.transcript_text.emit(self.text_and_duration)
   


        except Exception as e:
            print("Error Writing Transcribe To Widget:", e)


