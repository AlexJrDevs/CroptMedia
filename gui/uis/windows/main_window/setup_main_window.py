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
from gui.widgets.py_table_widget.py_table_widget import PyTableWidget
from . functions_main_window import *
import sys
import os


# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from . ui_main import *

# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from . functions_main_window import *




# PY WINDOW
# ///////////////////////////////////////////////////////////////
class SetupMainWindow:
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        try:
            self.ui = UI_MainWindow()
            self.ui.setup_ui(self)
        except:
            print("Error inside setupmainwindow")
        
        
        



    # ADD LEFT MENUS
    # ///////////////////////////////////////////////////////////////
    add_left_menus = [
        {
            "btn_icon" : "account_icon.svg",
            "btn_id" : "btn_home",
            "btn_text" : "Login OR Signup",
            "btn_tooltip" : "Login page",
            "show_top" : True,
            "is_active" : True
        },
        {
            "btn_icon" : "story_icon.svg",
            "btn_id" : "btn_video",
            "btn_text" : "Story Videos",
            "btn_tooltip" : "Create Clips",
            "show_top" : True,
            "is_active" : False
        },
        {
            "btn_icon" : "account_icon.svg",
            "btn_id" : "btn_account",
            "btn_text" : "Account",
            "btn_tooltip" : "Account",
            "show_top" : False,
            "is_active" : False
        },
        {
            "btn_icon" : "icon_settings.svg",
            "btn_id" : "btn_settings",
            "btn_text" : "Settings",
            "btn_tooltip" : "Open settings",
            "show_top" : False,
            "is_active" : False
        }

    ]

     # ADD TITLE BAR MENUS
    # ///////////////////////////////////////////////////////////////
    add_title_bar_menus = [
        # Example To Menu

        # {
        #    "btn_icon" : "icon_search.svg",
        #    "btn_id" : "btn_search",
        #    "btn_tooltip" : "Search",
        #    "is_active" : False
        # },
    ]

    # SETUP CUSTOM BTNs OF CUSTOM WIDGETS
    # Get sender() function when btn is clicked
    # ///////////////////////////////////////////////////////////////
    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()
    
    

    # SETUP MAIN WINDOW WITH CUSTOM PARAMETERS
    # ///////////////////////////////////////////////////////////////
    def setup_gui(self):
        # APP TITLE
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(self.settings["app_name"])
        
        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)

        # TITLE BAR / ADD EXTRA BUTTONS
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.title_bar.add_menus(SetupMainWindow.add_title_bar_menus)

        # SET SIGNALS
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        self.ui.title_bar.released.connect(self.btn_released)

        # ADD Title
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("Welcome to PyOneDark")

        # LEFT COLUMN SET SIGNALS
        # ///////////////////////////////////////////////////////////////
        self.ui.left_column.clicked.connect(self.btn_clicked)
        self.ui.left_column.released.connect(self.btn_released)

        # EXAMPLE CUSTOM WIDGETS
        # Here are added the custom widgets to pages and columns that
        # were created using Qt Designer.
        # This is just an example and should be deleted when creating
        # your application.
        #
        # OBJECTS FOR LOAD PAGES, LEFT AND RIGHT COLUMNS
        # You can access objects inside Qt Designer projects using
        # the objects below:
        #
        # <OBJECTS>
        # LEFT COLUMN: self.ui.left_column.menus
        # RIGHT COLUMN: self.ui.right_column
        # LOAD PAGES: self.ui.load_pages

        # </OBJECTS>
        # ///////////////////////////////////////////////////////////////


        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items

        # PAGES
        # ///////////////////////////////////////////////////////////////
        
        # All calls go to main.py so functions have to be called there
        # Page 1

        self.ui.load_pages.create_subclips_btn.clicked.connect(self.check_file_paths)
        self.ui.load_pages.create_next_button.clicked.connect(self.export_video_file)

        



        # CIRCULAR PROGRESS 1
        self.circular_progress_1 = PyCircularProgress(
            value = 0,
            progress_color = self.themes["app_color"]["context_color"],
            text_color = self.themes["app_color"]["text_title"],
            font_size = 14,
            bg_color = self.themes["app_color"]["dark_four"],
            subtext_color= self.themes["app_color"]["text_title"],
        )
        self.circular_progress_1.setFixedSize(200,200)

       

        # ADD WIDGETS
        self.ui.load_pages.load_layout.addWidget(self.circular_progress_1)




        # </Other Functions>
        # ///////////////////////////////////////////////////////////////
       
        # Page 2 - 9:16 Resize Function
        self.transcript_label = self.ui.load_pages.transcript_label
        self.video_label = self.ui.load_pages.video_label


        
        # ///////////////////////////////////////////////////////////////
        # END - EXAMPLE CUSTOM WIDGETS
        # ///////////////////////////////////////////////////////////////

    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized
    # ///////////////////////////////////////////////////////////////
    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)


    

    def resize_main_widget(self):
        # RESIZES THE WIDGETS TO 9 BY 16 WITH A MARGIN OF 10
        # THIS WORKS BY GRABBING THE WIDGET FIELD SIZE SO IT KNOWS HOW MUCH SPACE IT HAS AND SETS THE WIDGET CHILDREN ACCORDINGLY

        size = self.ui.load_pages.transcript_field.size()

        # Calculate the maximum width and height based on aspect ratio (9:16)
        max_width = size.height() * 9 / 16
        max_height = size.width() * 16 / 9

        # Use the smaller of the two values as the maximum size
        new_width = min(max_width, size.width())
        new_height = min(max_height, size.height())

        # Check current sizes
        current_text_settings_height = self.ui.load_pages.text_settings_label.minimumHeight()
        current_transcript_max_size = self.ui.load_pages.transcript_label.maximumSize()
        current_video_label_max_size = self.ui.load_pages.video_label.maximumSize()

        # Determine if resizing is needed
        resize_needed = (new_height != current_text_settings_height or
                        new_width != current_transcript_max_size.width() or
                        new_width + self.ui.load_pages.text_settings_label.width() != current_video_label_max_size.width() or
                        new_height != current_video_label_max_size.height())

        if resize_needed:
            # Apply the new sizes
            self.ui.load_pages.text_settings_label.setMinimumHeight(new_height)
            self.ui.load_pages.transcript_label.setMaximumSize(new_width, new_height)

            if self.ui.load_pages.video_pages.currentWidget() == self.ui.load_pages.video_page:
                self.ui.load_pages.video_label.setMaximumSize(new_width + self.ui.load_pages.text_settings_label.width(), new_height)
            else:
                self.ui.load_pages.video_label.setMaximumSize(new_width, new_height)

            # Update the geometry of the widget
            self.updateGeometry()
            self.update()





    

    
    

        
    