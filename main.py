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

    
    # PAGE 1
    # ///////////////////////////////////////////////////////////////
    
    def logindata(self):
        self.is_logged_in = MainFunctions.login_system(self)
        print(self.is_logged_in)
    
    # PAGE 2
    # ///////////////////////////////////////////////////////////////



    # Save Files Locations
    def save_file_paths(self, video, gameplay = None):
        self.video_path = video
        self.gameplay_path = gameplay
    
    # Creates Thread To Capture Images From Video
    def create_video_thumbnails(self):
        self.thumbnail_thread  = PyThumbnailCapture(self.video_path)
        self.thumbnail_thread.thumbnail_completed.connect(self.video_player_screen)
        self.thumbnail_thread.start()

    # Updates Video Player & Resets Loading Bar
    def video_player_screen(self, thumbnails = None):
        if thumbnails: # Checks wether its a Subclip or Normal video
            self.ui.video_player_subclip.setMedia(self.video_path, thumbnails)
            MainFunctions.set_page2_page(self, self.ui.load_pages.subclip_page_2)
        else:
            MainFunctions.set_video_page(self, self.ui.load_pages.video_page)
            video_filename = self.video_processing_thread.get_output_files()
            self.ui.video_player_main.setMedia(video_filename)
            SetupMainWindow.set_progressbar_value(self, 0)  # Reset progress bar




    # THIS WILL BE CHANGED TO ALLOW DIFFERENT PAGES AS VIDEO PLAYERS AND CREATE DIFFERENT VIDEOS
    # Video Creation
    def tiktok_creation(self, subclip_duration):

        MainFunctions.set_video_page(self, self.ui.load_pages.loading_video)
        MainFunctions.set_page2_page(self, self.ui.load_pages.main_page_2)
                
        # Create a thread to run video processing in the background
        self.video_processing_thread = StoryVideo(self.video_path, self.gameplay_path, subclip_duration, self.audio_transcript, self.percentage_logger)
        self.video_processing_thread.creating_video.connect(self.update_text_loading)
        self.video_processing_thread.start()



    # Creates Next Video
    def create_next_video(self):
        self.ui.video_player_main.reset_media()
        MainFunctions.set_video_page(self, self.ui.load_pages.loading_video)
        self.video_processing_thread.start()


    # Updates Loading Bar Accurate
    def update_loading_bar(self, value):
        SetupMainWindow.set_progressbar_value(self, value)
        if float(value) >= 100:
            self.video_player_screen()
            SetupMainWindow.resize_main_widget(self)

    def update_text_loading(self, text):
        SetupMainWindow.set_progressbar_text(self, text)

    def update_transcript_widget(self, transcript_location):
        self.ui.transcript_widget.load_srt_file(transcript_location)
    
    def edit_video_attributes(self, sender, text):
        try:
            if self.video_processing_thread:
                if sender == "Watermark":
                    self.video_processing_thread.edit_attributes(watermark=text)
                    print("Watermark: ", text)
                
                elif sender == "Text_color":
                    self.video_processing_thread.edit_attributes(text_color=text)
                
                elif sender == "Characters_show":
                    self.video_processing_thread.edit_attributes(length=text)
        except Exception as e:
            print("Error setting attributes: ", e)


    # VIDEO TEXT PREVIEW
    def show_text_preview(self, text):
        self.ui.video_player_main.create_preview_text(text)

    def text_preview_widgets(self, widgets, graphics_scene):
        self.ui.text_settings.update_available_text(widgets, graphics_scene)

 
    



    

    

        

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