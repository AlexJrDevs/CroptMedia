from qt_core import *

from gui.widgets import PyIconButton

class PyFolderPicker(QWidget):

    def __init__(self):
        super().__init__()

        self.save_location = QStandardPaths.writableLocation(QStandardPaths.MoviesLocation)

        # Create widgets
        save_text = QLabel("Save Location")
        save_text.setStyleSheet("font-family: 'Roboto';")

        self.text_browser = QTextBrowser(self)
        self.text_browser.setText(self.save_location)
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setStyleSheet("border: 2px solid #2C313C; background: #343B48; border-radius: 10px;")

        self.text_browser.setTextInteractionFlags(Qt.TextBrowserInteraction)  # Make text selectable
        
        # Disable text wrapping and enable horizontal scrolling
        self.text_browser.setWordWrapMode(QTextOption.NoWrap)  # Disable text wrapping
        self.text_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Show horizontal scrollbar if needed
        self.text_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Hide vertical scrollbar

        # Adjust the size policy to handle horizontal scrolling better
        self.text_browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.text_browser.setFixedHeight(30)  # Set a fixed height for consistency

        button = PyIconButton(icon_path= r"gui\images\svg_icons\icon_save.svg", 
                                  width=30,
                                  height=30,
                                  parent=None,
                                  app_parent=None,
                                  tooltip_text=None,
                                  icon_margin=10,
                                  bg_color_hover="#2C313C",
                                  bg_color="#2C313C",
                                  bg_color_pressed="#2C313C",
                                  radius=0
                                  )

        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # Connect button click to method
        button.clicked.connect(self.open_folder_dialog)

        # Create a background widget and set its background color to black
        background_widget = QWidget(self)
        background_widget.setStyleSheet("background-color: #2C313C;")

        # Set up layout for background widget
        background_layout = QHBoxLayout(background_widget)
        background_layout.setContentsMargins(0, 0, 0, 0)
        background_layout.setSpacing(0)

        background_layout.addWidget(button)
        background_layout.addWidget(self.text_browser)

        # Set up layout
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 5)
        text_layout.addWidget(save_text)

        contents_layout = QVBoxLayout()
        contents_layout.setContentsMargins(0, 0, 0, 0)
        contents_layout.setSpacing(0)

        contents_layout.addLayout(text_layout)
        contents_layout.addWidget(background_widget)

        self.setLayout(contents_layout)


    def open_folder_dialog(self):
        # Open folder dialog
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        
        if folder:
            # Update text browser with selected folder path
            self.text_browser.setText(folder)
            self.save_location = folder
