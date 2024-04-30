from qt_core import *
from gui.widgets import PyIconButton
import os.path

class PyVideoUpload(QWidget):

    def __init__(self, parent=None):
        super(PyVideoUpload, self).__init__(parent)


        # Layouts
        file_layout = QVBoxLayout()

        # Create the first icon button
        self.video_upload_button = PyIconButton(icon_path= r"gui\images\svg_icons\icon_folder_upload.svg", 
                                                    width=180,
                                                    height=180,
                                                    parent = self,
                                                    app_parent = self,
                                                    tooltip_text="Top Video",
                                                    icon_margin=-30
                                                )
        self.video_upload_button.clicked.connect(self.open_file)
        file_layout.addWidget(self.video_upload_button, alignment=Qt.AlignCenter)

        # Add a horizontal line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("border: 2px solid #1B1E23;")
        file_layout.addWidget(line)

        # Create the second icon button
        self.gameplay_upload_button = PyIconButton(icon_path= r"gui\images\svg_icons\icon_folder_upload.svg",
                                                    width=180,
                                                    height=180,
                                                    parent = self,
                                                    app_parent = self,
                                                    tooltip_text="Bottom Video",
                                                    icon_margin=-30
                                                )
        self.gameplay_upload_button.clicked.connect(self.open_file)
        file_layout.addWidget(self.gameplay_upload_button, alignment=Qt.AlignCenter)
        
        self.video_upload_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.gameplay_upload_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setLayout(file_layout)

    
    # Open File System
    def open_file(self):
        button = self.sender()  # Get the sender (the button that was clicked)

        # Video Button
        if button == self.video_upload_button:
            file_name, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi);;All Files (*)")
            if file_name:
                self.selected_video_file = file_name  # Store the video file location
                print("Video Upload")

                # Sets new icon / text
                self.video_upload_button.set_icon(r"gui\images\svg_icons\icon_folder_uploaded.svg")
                

        # Gameplay Button
        elif button == self.gameplay_upload_button:
            file_name, _ = QFileDialog.getOpenFileName(self, "Open Gameplay File", "", "Video Files (*.mp4 *.avi);;All Files (*)")
            if file_name:
                self.selected_gameplay_file = file_name  # Store the gameplay file location
                print("Gameplay Upload")

                # Sets new icon / text
                self.gameplay_upload_button.set_icon(r"gui\images\svg_icons\icon_folder_uploaded.svg")

class PyCreateSubclip(QWidget):
    def __init__(self, video_location, parent=None):
        super().__init__(parent)

        self.parent = parent
        self.video_location = video_location

        button_layout = QVBoxLayout()
        self.done_button = QPushButton("Create Video")
        self.done_button.setMinimumSize(300, 23)  # Set minimum width and height for the button
    

        # Video Creation Button
        self.done_button.clicked.connect(self.start_subclip)

        # Set size policy for the button
        self.done_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        button_layout.addWidget(self.done_button)
        
        self.setLayout(button_layout)

    def start_subclip(self):
        try:
            if os.path.exists(self.video_location.selected_video_file) and os.path.exists(self.video_location.selected_gameplay_file):
                self.parent.save_file_paths(self.video_location.selected_video_file, self.video_location.selected_gameplay_file)
                self.parent.create_video_thumbnails()
        except:
            print("Error: Not All Files Uploaded")
    


        
