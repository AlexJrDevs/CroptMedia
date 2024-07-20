
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

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        
        self._button_color = QColor("#343B48")

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

        


