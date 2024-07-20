from qt_core import *
from gui.widgets import PyIconButton, PyToggle
import os.path

class PyVideoUpload(QWidget):

    def __init__(self, parent=None):
        super(PyVideoUpload, self).__init__(parent)
        self.parent = parent

        # Create the background widget for upload
        upload_bg_widget = QWidget()
        upload_bg_widget.setStyleSheet("border-radius: 15px; background: #343B48; border-radius: 15px;")
        
        # Layouts
        upload_layout = QVBoxLayout()
        upload_bg_widget.setLayout(upload_layout)

        # Create the first icon button
        self.video_upload_button = PyIconButton(
            icon_path=r"gui\images\svg_icons\icon_folder_upload.svg",
            width=180,
            height=180,
            parent=self,
            app_parent=self,
            tooltip_text="Top Video",
            icon_margin=-30
        )
        self.video_upload_button.clicked.connect(self.open_file)
        upload_layout.addWidget(self.video_upload_button, alignment=Qt.AlignCenter)

        # Add a horizontal line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("border: 2px solid #1B1E23;")  # Line color
        upload_layout.addWidget(line)

        # Create the second icon button
        self.gameplay_upload_button = PyIconButton(
            icon_path=r"gui\images\svg_icons\icon_folder_upload.svg",
            width=180,
            height=180,
            parent=self,
            app_parent=self,
            tooltip_text="Bottom Video",
            icon_margin=-30
        )
        self.gameplay_upload_button.clicked.connect(self.open_file)
        upload_layout.addWidget(self.gameplay_upload_button, alignment=Qt.AlignCenter)
        
        # Set the size policy for the buttons
        self.video_upload_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.gameplay_upload_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Video Settings
        #//////////////////////////////////////////////////////

        # Create the background widget for settings
        settings_bg_widget = QWidget()
        settings_bg_widget.setStyleSheet("border-radius: 15px; background: #343B48;")
        
        # Layouts
        settings_layout = QHBoxLayout() 
        settings_layout.setContentsMargins(0, 8, 0, 8)
        settings_bg_widget.setLayout(settings_layout)

        # Create the Word Limit section
        word_limit_layout = QVBoxLayout()
        word_limit_layout.setSpacing(5)
        word_limit_layout.setContentsMargins(0, 0, 0, 0)
        
        word_limit_label = QLabel("Max Words")
        word_limit_label.setAlignment(Qt.AlignCenter)
        word_limit_label.setStyleSheet("font-family: 'Roboto', sans-serif; font-weight: bold; font-size: 12px;")

        # Create the QLineEdit with a validator
        self.word_limit_input = QLineEdit()
        self.word_limit_input.setText('5')
        self.word_limit_input.setAlignment(Qt.AlignCenter)
        self.word_limit_input.setStyleSheet("border: 2px solid #1B1E23; border-radius: 12px; background-color: #1B1E23;")
        self.word_limit_input.setFixedWidth(150)
        self.word_limit_input.setFixedHeight(27)

        # Set the input validator to accept only positive integers
        regex = QRegularExpression(r"^[1-9][0-9]*$")
        validator = QRegularExpressionValidator(regex, self)
        self.word_limit_input.setValidator(validator)

        word_limit_layout.addWidget(word_limit_label)
        word_limit_layout.addWidget(self.word_limit_input)
        
        settings_layout.addLayout(word_limit_layout)

        # Create the Gameplay section
        gameplay_layout = QVBoxLayout()
        gameplay_layout.setSpacing(5)
        gameplay_layout.setContentsMargins(0, 0, 0, 0)

        gameplay_label = QLabel("Gameplay")
        gameplay_label.setAlignment(Qt.AlignCenter)
        gameplay_label.setStyleSheet("font-family: 'Roboto', sans-serif; font-weight: bold; font-size: 12px;")
        gameplay_toggle = PyToggle(width=150, bg_color='#1B1E23', active_color='#3f6fd1')
        gameplay_layout.addWidget(gameplay_label)
        gameplay_layout.addWidget(gameplay_toggle)
        
        settings_layout.addLayout(gameplay_layout)

        # Set the main layout of the widget to be the bg_widget layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(upload_bg_widget, 1)
        main_layout.addWidget(settings_bg_widget)
        self.setLayout(main_layout)

    # Open File System
    def open_file(self):
        button = self.sender()  # Get the sender (the button that was clicked)

        # Video Button
        if button == self.video_upload_button:
            file_name, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi);;All Files (*)")
            if os.path.exists(file_name):
                self.parent.save_file_paths(video=file_name)  # Store the video file location

                # Sets new icon / text
                self.video_upload_button.set_icon(r"gui\images\svg_icons\icon_folder_uploaded.svg")
                

        # Gameplay Button
        elif button == self.gameplay_upload_button:
            file_name, _ = QFileDialog.getOpenFileName(self, "Open Gameplay File", "", "Video Files (*.mp4 *.avi);;All Files (*)")
            if os.path.exists(file_name):
                self.parent.save_file_paths(gameplay=file_name)
  
                # Sets new icon / text
                self.gameplay_upload_button.set_icon(r"gui\images\svg_icons\icon_folder_uploaded.svg")

    def reset_folder_icon(self):
        self.video_upload_button.set_icon(r"gui\images\svg_icons\icon_folder_upload.svg")
        self.gameplay_upload_button.set_icon(r"gui\images\svg_icons\icon_folder_upload.svg")
