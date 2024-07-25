
from qt_core import *

from gui.widgets import PyTranscriptModel, PyTranscriptDelegate

from functools import partial

import os


stylesheet = """
    /* QTableView */
    QTableView {
        gridline-color: #343B48;
        background-color: #343B48;
        color: #F0F0F0;
        selection-background-color: #343B48;
        selection-color: #F0F0F0;
        border: 2px solid #343B48; /* Border color and width */
        border-radius: 15px; /* Rounded corners */
        padding: 10px;
    }

    /* QHeaderView::section */
    QHeaderView::section {
        background-color: #343B48;
        color: #F0F0F0;
        padding: 4px;
        border: 0px;
    }

    QTableCornerButton::section {
    background-color: #343B48;
    }

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
"""

class PyTranscriptWidget(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        

        main_layout = QVBoxLayout()

        
        # Transcript Table
        self.model = PyTranscriptModel()
        self.delegate = PyTranscriptDelegate()

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setItemDelegateForColumn(0, self.delegate)

        self.view.setStyleSheet(stylesheet)
        self.view.setEditTriggers(QTableView.AllEditTriggers)
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # Disable resizing

        # Resize columns to fit the width of the table
        self.view.horizontalHeader().setStretchLastSection(True)
        self.view.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.view.horizontalHeader().setSectionsClickable(False)
        self.view.horizontalHeader().setHighlightSections(False)


        # Add the background widget to the main layout
        main_layout.addWidget(self.view)

        self.setLayout(main_layout)

        


