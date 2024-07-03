# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from PySide6.QtGui import QShowEvent
from gui.uis.windows.main_window.functions_main_window import *

import sys
import os
import threading





# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from gui.uis.windows.main_window import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'


# Backend Modules
# ///////////////////////////////////////////////////////////////
from backend.video_creation import *

from backend.reusable_scripts import *


# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(parent=self)
        


        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items


        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)


        # VIDEO CREATION SCRIPTS
        # ///////////////////////////////////////////////////////////////
        self.percentage_logger = BarLogger()
        self.audio_transcript = AudioTranscribe()

        self.percentage_logger.loading_percent.connect(self.update_loading_bar)

        self.audio_transcript.transcript_started.connect(self.update_text_loading)
        self.audio_transcript.transcript_location.connect(self.update_transcript_widget)


        # Main functions before page open
        # ///////////////////////////////////////////////////////////////
        MainFunctions.set_page(self, self.ui.load_pages.page_1)
        MainFunctions.set_video_page(self, self.ui.load_pages.upload_page)
        MainFunctions.clear_folder(self)

        # Sets login
        # ///////////////////////////////////////////////////////////////
        self.is_logged_in = True
        

        
        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()



    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////

        if btn.objectName() == "btn_home":
            # Activates The Menu
            self.ui.left_menu.select_only_one(btn.objectName())

            # Loads Page
            MainFunctions.set_page(self, self.ui.load_pages.page_1)

        # OPEN VIDEO CREATION
        if btn.objectName() == "btn_video":
            if self.is_logged_in:
                # Activates The Menu
                self.ui.left_menu.select_only_one(btn.objectName())

                # Loads Page
                MainFunctions.set_page(self, self.ui.load_pages.page_2)
                SetupMainWindow.resize_main_widget(self)
                #MainFunctions.set_video_page(self, self.ui.load_pages.video_page)
    
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Login First")
                msg.setWindowTitle("Info")
                msg.exec()
                print("Displayed")
                print("Login to start")
        
        


   
        
        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////
              

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")
        

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")


    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)
        SetupMainWindow.resize_main_widget(self)

    def showEvent(self, event):
        SetupMainWindow.resize_grips(self)
        SetupMainWindow.resize_main_widget(self)
 


        

     


    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition()

    # MAIN FUNCTIONS
    # ///////////////////////////////////////////////////////////////

    
    # PAGE 1 - Login / Signup Page
    # ///////////////////////////////////////////////////////////////
    
    def logindata(self):
        self.is_logged_in = MainFunctions.login_system(self)
        print(self.is_logged_in)


    
    # PAGE 2 - Video Creation
    # ///////////////////////////////////////////////////////////////



    # Save Files Locations
    def save_file_paths(self, video=None, gameplay=None):
        if video:
            print("Video Uploaded")
            self.video_path = video

        if gameplay:
            print("Gameplay Uploaded")
            self.gameplay_path = gameplay


    def save_subclips(self, subclip_durations):
        self.subclip_durations = subclip_durations
        self.create_video()
    
    # Creates Thread To Capture Images From Video
    def create_video_thumbnails(self):
        if self.video_path and self.gameplay_path:
            self.thumbnail_thread  = PyThumbnailCapture(self.video_path)
            self.thumbnail_thread.thumbnail_completed.connect(self.video_player_screen)
            self.thumbnail_thread.start()


    # Updates Video Player & Resets Loading Bar | *args are the thumbnails or video path
    def video_player_screen(self, *args):
        sender = self.sender()

        if sender == self.thumbnail_thread: # Checks wether its a Subclip or Normal video

            self.ui.video_player_subclip.setMedia(self.video_path, *args)
            MainFunctions.set_page2_page(self, self.ui.load_pages.subclip_page_2)
            self.ui.upload_video.reset_folder_icon()


        else:
            self.video_filename = args[0]
            MainFunctions.set_video_page(self, self.ui.load_pages.video_page)
            self.ui.video_player_main.setMedia(*args)



    # THIS WILL BE CHANGED TO ALLOW DIFFERENT PAGES AS VIDEO PLAYERS AND CREATE DIFFERENT VIDEOS
    # Video Creation
    def create_video(self):

        MainFunctions.set_video_page(self, self.ui.load_pages.loading_video)
        MainFunctions.set_page2_page(self, self.ui.load_pages.main_page_2)
                
        # Create a thread to run video processing in the background
        self.video_processing_thread = StoryVideo(self.video_path, self.gameplay_path, self.subclip_durations[0], self.audio_transcript, self.percentage_logger)
        self.video_processing_thread.creating_video.connect(self.update_text_loading)
        self.video_processing_thread.finished_subclip.connect(self.video_player_screen)
        self.video_processing_thread.start()


    # creates preview text and manages the sync between the TextEdit, TextLine and GraphicsText
    def create_preview_text(self, text_data):

        if hasattr(self, 'preview_text') and self.preview_text:
            self.preview_text.delete_text()
            self.preview_text.create_preview_text(text_data)

        else:
            self.preview_text = CreatePreviewText(self.ui.video_player_main.video_item, self.ui.video_player_main.graphic_scene)
            self.preview_text.text_data_updated.connect(self.update_preview_text)
            self.preview_text.create_preview_text(text_data)

    # Updates text start and end time, and gives references of GraphicsText to the text settings
    def update_preview_text(self, text_data):
        self.ui.text_settings.text_widgets = [item[0] for item in text_data]
        self.ui.video_player_main.text_data = text_data

    # Sets the actual value for the loading bar
    def update_loading_bar(self, value):
        self.circular_progress_1.set_value(value)

        
    # Sets a text below the value to show what it is creating
    def update_text_loading(self, text):
        self.circular_progress_1.set_text(text)

    def update_transcript_widget(self, transcript_location):
        self.ui.transcript_widget.load_srt_file(transcript_location)

    def export_video_file(self):
        self.ui.video_player_main.mediaPlayer.stop()
        self.subclip_durations.pop(0)
        MainFunctions.set_video_page(self, self.ui.load_pages.loading_video)
        text_data = self.ui.video_player_main.extract_text_data()
        self.export_video = ExportVideo(text_data, self.video_filename, self.percentage_logger)
        self.export_video.exporting_video.connect(self.update_text_loading)
        self.export_video.video_completed.connect(self.video_exported)
        self.export_video.start()


    def video_exported(self):
        if len(self.subclip_durations) > 0:
            print("Create Another Clip")
            self.create_video()
        else:
            print("No more clips to create insert new video")
            self.video_path = ""
            self.gameplay_path = ""
            MainFunctions.set_video_page(self, self.ui.load_pages.upload_page)


        
    

# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()

    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    sys.exit(app.exec())