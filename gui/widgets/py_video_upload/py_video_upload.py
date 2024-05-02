from qt_core import *
from gui.widgets import PyIconButton
import os.path

class PyVideoUpload(QWidget):

    def __init__(self, parent=None):
        super(PyVideoUpload, self).__init__(parent)
        self.parent = parent

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
                


    


        
