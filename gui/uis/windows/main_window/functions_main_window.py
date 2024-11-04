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
import os

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *


# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from . ui_main import *


# FUNCTIONS
class MainFunctions():
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)



    # SET MAIN WINDOW PAGES
    # ///////////////////////////////////////////////////////////////
    def set_page(self, page):
        self.ui.load_pages.pages.setCurrentWidget(page)
    
    def set_video_page(self, page):
        self.ui.load_pages.video_pages.setCurrentWidget(page)
    
    def set_page2_page(self, page):
        self.ui.load_pages.page_2_layout.setCurrentWidget(page)
    

    # SET LEFT COLUMN PAGES
    # ///////////////////////////////////////////////////////////////
    def set_left_column_menu(
        self,
        menu,
        title,
        icon_path
    ):
        self.ui.left_column.menus.menus.setCurrentWidget(menu)
        self.ui.left_column.title_label.setText(title)
        self.ui.left_column.icon.set_icon(icon_path)

    # RETURN IF LEFT COLUMN IS VISIBLE
    # ///////////////////////////////////////////////////////////////
    def left_column_is_visible(self):
        width = self.ui.left_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    # RETURN IF RIGHT COLUMN IS VISIBLE
    # ///////////////////////////////////////////////////////////////
    def right_column_is_visible(self):
        width = self.ui.right_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    # SET RIGHT COLUMN PAGES
    # ///////////////////////////////////////////////////////////////
    def set_right_column_menu(self, menu):
        self.ui.right_column.menus.setCurrentWidget(menu)

    # GET TITLE BUTTON BY OBJECT NAME
    # ///////////////////////////////////////////////////////////////
    def get_title_bar_btn(self, object_name):
        return self.ui.title_bar_frame.findChild(QPushButton, object_name)

    # GET TITLE BUTTON BY OBJECT NAME
    # ///////////////////////////////////////////////////////////////
    def get_left_menu_btn(self, object_name):
        return self.ui.left_menu.findChild(QPushButton, object_name)
    
    # LEFT AND RIGHT COLUMNS / SHOW / HIDE
    # ///////////////////////////////////////////////////////////////
    def toggle_left_column(self):
        # GET ACTUAL CLUMNS SIZE
        width = self.ui.left_column_frame.width()
        right_column_width = self.ui.right_column_frame.width()

        MainFunctions.start_box_animation(self, width, right_column_width, "left")

    def toggle_right_column(self):
        # GET ACTUAL CLUMNS SIZE
        left_column_width = self.ui.left_column_frame.width()
        width = self.ui.right_column_frame.width()

        MainFunctions.start_box_animation(self, left_column_width, width, "right")

    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0
        time_animation = self.ui.settings["time_animation"]
        minimum_left = self.ui.settings["left_column_size"]["minimum"]
        maximum_left = self.ui.settings["left_column_size"]["maximum"]
        minimum_right = self.ui.settings["right_column_size"]["minimum"]
        maximum_right = self.ui.settings["right_column_size"]["maximum"]

        # Check Left Values        
        if left_box_width == minimum_left and direction == "left":
            left_width = maximum_left
        else:
            left_width = minimum_left

        # Check Right values        
        if right_box_width == minimum_right and direction == "right":
            right_width = maximum_right
        else:
            right_width = minimum_right       

        # ANIMATION LEFT BOX        
        self.left_box = QPropertyAnimation(self.ui.left_column_frame, b"minimumWidth")
        self.left_box.setDuration(time_animation)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

        # ANIMATION RIGHT BOX        
        self.right_box = QPropertyAnimation(self.ui.right_column_frame, b"minimumWidth")
        self.right_box.setDuration(time_animation)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.stop()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.finished.connect(self.resize_widget)
        self.group.start()

    def show_account_popup(self, button):
        # Set the popup's position relative to the button
        button_pos = button.mapToGlobal(button.rect().topRight())
        popup_pos = self.ui.left_menu_frame.mapFromGlobal(button_pos)
        
        # Adjust for the popup's width to align its right edge with the button
        popup_pos.setX(popup_pos.x() - self.ui.account_popup.width())
        
        # Ensure the popup doesn't go off-screen
        if popup_pos.x() < 0:
                popup_pos.setX(self.ui.left_column_frame.pos().x())
        if popup_pos.y() + self.ui.account_popup.height() > self.ui.left_menu_frame.height():
            popup_pos.setY(self.ui.left_menu_frame.height() - self.ui.account_popup.height())

        # Move the popup to the desired position and show it without animation
        self.ui.account_popup.move(popup_pos.x(), popup_pos.y() - 3)


        # Show the popup
        if self.ui.account_popup.isHidden():
            self.ui.account_popup.show()
        else:
            self.ui.account_popup.hide()



        
    # NOTIFICATION POPUP ANIMATION
    # ///////////////////////////////////////////////////////////////
    def show_popup_alert(self, alerts_list, central_widget, message=None, timeout=250):
        # Remove the previous alert if it exists
        if alerts_list:
            previous_alert = alerts_list.pop()
            previous_alert.animation.finished.disconnect()
            previous_alert.deleteLater()

        # Create and configure the new alert
        alert = PyNotificationPopup(central_widget, message or 'Some message to the user')
        alerts_list.append(alert)
        
        alert.slideIn.setDuration(timeout)
        alert.slideOut.setDuration(timeout)
        
        def deleteLater():
            alerts_list.remove(alert)
            alert.deleteLater()
        
        alert.animation.finished.connect(deleteLater)
        MainFunctions.update_alert_animation(self, alert)
        alert.show()
        alert.animation.start()


    def update_alert_animation(self, alert):
        width = alert.width()
        height = alert.height()
        x = self.ui.load_pages.pages.width()  # Start from the right edge
        startRect = QRect(x, 10, width, height)
        endRect = startRect.translated(-width, 0)
        alert.updateGeometry(startRect, endRect)

    def update_all_alert_animations(self, alerts_list, central_widget):
        x = central_widget.width()
        for alert in reversed(alerts_list):
            width = alert.width()
            height = alert.height()
            x -= width
            startRect = QRect(x + width, 10, width, height)
            endRect = QRect(x, 10, width, height)
            alert.updateGeometry(startRect, endRect)
            
            # Update current geometry if in pause state
            if isinstance(alert.animation.currentAnimation(), QPauseAnimation):
                alert.setGeometry(endRect)







