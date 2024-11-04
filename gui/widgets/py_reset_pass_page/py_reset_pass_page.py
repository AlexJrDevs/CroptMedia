from qt_core import *

class PyResetPassPage(QWidget):
    def __init__(self):
        super().__init__()

        # Create the outer dark background
        self.outer_frame = QFrame(self)
        self.outer_frame.setStyleSheet("background-color: #1B1E23; border-radius: 12px;")
        outer_layout = QVBoxLayout(self.outer_frame)
        self.outer_frame.setMaximumSize(600, 600)
        outer_layout.setContentsMargins(9, 9, 9, 9)

        # Create the inner lighter background widget
        inner_widget = QFrame()
        inner_widget.setStyleSheet("background-color: #343B48; border-radius: 12px;")
        inner_layout = QVBoxLayout(inner_widget)
        inner_layout.setContentsMargins(30, 5, 30, 0)

        # Reset Password Label
        inner_layout.addStretch(1)
        self.reset_label = QLabel("Reset Your Password")
        self.reset_label.setAlignment(Qt.AlignCenter)
        self.reset_label.setStyleSheet("color: #DCE1EC;")
        self.reset_label.setMinimumHeight(30)
        inner_layout.addWidget(self.reset_label)

        inner_layout.addStretch(1)

        # Email Input
        self.email_label = QLabel('EMAIL OR PHONE NUMBER <font color="red">*</font>')
        self.email_label.setStyleSheet("color: #DCE1EC;")
        inner_layout.addWidget(self.email_label)
        
        self.email_input = QLineEdit()
        self.email_input.setStyleSheet("background-color: #1B1E23; color: white; padding: 10px;")
        self.email_input.setMinimumHeight(36)
        self.email_input.setMaximumHeight(46)
        inner_layout.addWidget(self.email_input)

        inner_layout.addSpacing(10)

        # Reset Button
        self.reset_button = QPushButton("Send Reset Link")
        self.reset_button.setStyleSheet("background-color: #3995F1; color: #DCE1EC; padding: 10px;")
        self.reset_button.setMinimumHeight(36)
        self.reset_button.setMaximumHeight(46)
        self.reset_button.setCursor(QCursor(Qt.PointingHandCursor))
        inner_layout.addWidget(self.reset_button)

        # Back to Login Label
        self.back_to_login_label = QLabel("<a style='color:#3995F1;' href='login'>Remembered Password?</a>")
        self.back_to_login_label.setAlignment(Qt.AlignCenter)
        self.back_to_login_label.setTextFormat(Qt.RichText)
        self.back_to_login_label.setOpenExternalLinks(False)
        self.back_to_login_label.setCursor(QCursor(Qt.PointingHandCursor))

        # Create a container widget for alignment
        back_container = QWidget()
        back_layout = QHBoxLayout(back_container)
        back_layout.addWidget(self.back_to_login_label)
        back_layout.addStretch()  # This pushes the label to the left
        back_layout.setContentsMargins(0, 10, 0, 0)  # Add some top margin
        inner_layout.addWidget(back_container)

        inner_layout.addStretch(2)

        # Add the inner widget (lighter background) to the outer layout
        outer_layout.addWidget(inner_widget)

        # Set the main layout for the reset password window
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.outer_frame)
        main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)

        # Set up dynamic font scaling
        self.setup_dynamic_font_scaling()

    def setup_dynamic_font_scaling(self):
        self.base_width = 600
        self.base_height = 600
        self.base_font_sizes = {
            self.reset_label: 30,
            self.email_label: 14,
            self.email_input: 16,
            self.reset_button: 14,
            self.back_to_login_label: 10,
        }
        
        self.base_button_sizes = {
            self.reset_button: (36, 46),
        }
        
        self.outer_frame.resizeEvent = self.on_resize

    def on_resize(self, event):
        width = self.outer_frame.width()
        height = self.outer_frame.height()
        scale_factor = min(width / self.base_width, height / self.base_height)
        
        # Update font sizes
        for widget, base_size in self.base_font_sizes.items():
            font = widget.font()
            font.setPointSize(int(base_size * scale_factor))
            widget.setFont(font)
        
        # Adjust button size
        for button, (base_min_height, base_max_height) in self.base_button_sizes.items():
            min_height = int(base_min_height * scale_factor)
            max_height = int(base_max_height * scale_factor)
            button.setMinimumHeight(min_height)
            button.setMaximumHeight(max_height)
            button.setStyleSheet(f"background-color: #3995F1; color: #C3CCDF; padding: {int(10 * scale_factor)}px;")
        
        # Adjust input field size
        email_input_min_height = int(36 * scale_factor)
        email_input_max_height = int(46 * scale_factor)
        self.email_input.setMinimumHeight(email_input_min_height)
        self.email_input.setMaximumHeight(email_input_max_height)
        self.email_input.setStyleSheet(f"background-color: #1B1E23; color: white; padding: {int(10 * scale_factor)}px;")
        
        QFrame.resizeEvent(self.outer_frame, event)
