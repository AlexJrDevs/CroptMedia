from qt_core import *

class PyUserAccountPopup(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        
        # Background widget
        bg_widget = QWidget()
        bg_widget.setStyleSheet('background-color: #1B1E23; border-top-right-radius: 8px; border-bottom-right-radius: 8px;')
        bg_layout = QVBoxLayout(bg_widget)
        bg_layout.setContentsMargins(8, 2, 8, 8)
        bg_layout.setSpacing(4) 
        
        # Close button
        close_button = QPushButton("×", self)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #C3CCDF;
                font-size: 13px;
                border: none;
            }
            QPushButton:hover {
                color: white;
            }
        """)
        close_button.setFixedSize(16, 16)
        close_button.clicked.connect(self.close)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(4)
        
        # Account Button
        account_button = QPushButton("Account", self)
        account_button.setStyleSheet("""
            QPushButton {
                background-color: #2C313C;
                color: #C3CCDF;
                border: none;
                padding: 3px;
                border-radius: 2px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3C4454;
            }
            QPushButton:pressed {
                background-color: #1C2134;
            }
        """)
        account_button.setFixedHeight(22)
        account_button.clicked.connect(self.view_account)
        button_layout.addWidget(account_button)
        
        # Logout Button
        self.logout_button = QPushButton("Logout", self)
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #2C313C;
                color: #C3CCDF;
                border: none;
                padding: 3px;
                border-radius: 2px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #3C4454;
            }
            QPushButton:pressed {
                background-color: #1C2134;
            }
        """)
        self.logout_button.setFixedHeight(22)
        button_layout.addWidget(self.logout_button)
        
        # Membership Status
        membership_label = QLabel("Membership: Free", self)
        membership_label.setStyleSheet("color: #C3CCDF; font-size: 12px;")
        membership_label.setAlignment(Qt.AlignCenter)
        
        # Add widgets to layout
        bg_layout.addWidget(close_button, alignment=Qt.AlignRight)
        bg_layout.addLayout(button_layout)
        bg_layout.addWidget(membership_label)
        
        main_layout.addWidget(bg_widget)
        
        # Adjusted the size of the popup to fit the content better
        self.setFixedSize(200, 80)
        
        # Animation
        self.animation = QPropertyAnimation(self, b'geometry')
        self.animation.setDuration(250)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)

    def view_account(self):
        # Handle account viewing logic
        pass



    def updateGeometry(self, startRect, endRect):
        self.animation.setStartValue(startRect)
        self.animation.setEndValue(endRect)
