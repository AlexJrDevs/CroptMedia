from qt_core import *
from gui.widgets import PyIconButton



class PyLoginPage(QWidget):
    def __init__(self, parent):
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

        # Welcome Label
        inner_layout.addStretch(1)
        self.welcome_label = QLabel("Welcome Back!")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("color: #DCE1EC;")
        self.welcome_label.setMinimumHeight(30)
        inner_layout.addWidget(self.welcome_label)

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

        inner_layout.addStretch(1)

        # Password Input
        self.password_label = QLabel('PASSWORD <font color="red">*</font>')
        self.password_label.setStyleSheet("color: #DCE1EC;")
        inner_layout.addWidget(self.password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("background-color: #1B1E23; color: white; padding: 10px;")
        self.password_input.setMinimumHeight(36)
        self.password_input.setMaximumHeight(46)
        inner_layout.addWidget(self.password_input)

        # Forgot Password Label
        self.forgot_password = QLabel("<a style='color:#3995F1;' href='#'>Forgot password?</a>")
        self.forgot_password.setAlignment(Qt.AlignLeft)
        self.forgot_password.setTextFormat(Qt.RichText)
        self.forgot_password.setOpenExternalLinks(True)
        inner_layout.addWidget(self.forgot_password)

        inner_layout.addStretch(1)
        
        # Login Button
        self.login_button = QPushButton("Log In")
        self.login_button.setStyleSheet("background-color: #3995F1; color: #C3CCDF; padding: 10px;")
        self.login_button.setMinimumHeight(36)
        self.login_button.setMaximumHeight(46)
        self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
        inner_layout.addWidget(self.login_button)
        
        # Register label
        self.register_label = QLabel("<a style='color:#C3CCDF;'>Need an account?</a> <a style='color:#3995F1;' href='register'>Register</a>")
        self.register_label.setAlignment(Qt.AlignLeft)
        self.register_label.setTextFormat(Qt.RichText)
        self.register_label.setOpenExternalLinks(False)
        inner_layout.addWidget(self.register_label)

        inner_layout.addStretch(1)
        
        # OR Label with lines on each side
        or_layout = QHBoxLayout()
        or_layout.setContentsMargins(0, 0, 0, 0)

        # Line on the left
        left_line = QFrame()
        left_line.setFrameShape(QFrame.HLine)
        left_line.setFrameShadow(QFrame.Sunken)
        left_line.setStyleSheet("border: 2px solid #1B1E23;")
        or_layout.addWidget(left_line)

        # OR Label
        self.or_label = QLabel("OR")
        self.or_label.setAlignment(Qt.AlignCenter)
        self.or_label.setStyleSheet("color: grey;")
        or_layout.addWidget(self.or_label)

        # Line on the right
        right_line = QFrame()
        right_line.setFrameShape(QFrame.HLine)
        right_line.setFrameShadow(QFrame.Sunken)
        right_line.setStyleSheet("border: 2px solid #1B1E23;")
        or_layout.addWidget(right_line)

        # Add the OR section layout to the inner layout
        inner_layout.addLayout(or_layout)

        inner_layout.addStretch(1)
        
        # Social Media Buttons
        social_layout = QHBoxLayout()
        social_layout.setContentsMargins(0, 0, 0, 5)
        social_layout.setSpacing(40)
        

        self.google_button = QPushButton(parent=self)
        self.google_button.setIcon(QIcon("gui/images/svg_icons/icon_google.svg"))
        self.google_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.google_button.setStyleSheet("background-color: #1B1E23; color: #C3CCDF; padding: 10px;")

        social_layout.addWidget(self.google_button)


        self.facebook_button = QPushButton(parent=self)
        self.facebook_button.setIcon(QIcon("gui/images/svg_icons/icon_facebook.svg"))
        self.facebook_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.facebook_button.setStyleSheet("background-color: #1B1E23; color: #C3CCDF; padding: 10px;")

        
        social_layout.addWidget(self.facebook_button)

        inner_layout.addLayout(social_layout)

        inner_layout.addStretch(1)
        
        # Add the inner widget (lighter background) to the outer layout
        outer_layout.addWidget(inner_widget)

        # Set the main layout for the login window
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
            self.welcome_label: 30,
            self.email_label: 14,
            self.password_label: 14,
            self.email_input: 16,
            self.password_input: 16,
            self.login_button: 14,
            self.forgot_password: 10,
            self.register_label: 10,
            self.or_label: 10,
        }
        
        self.base_button_sizes = {
            self.login_button: (36, 46),
            self.google_button: (36, 23),  # Base sizes for Google button
            self.facebook_button: (36, 23)  # Base sizes for Facebook button
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
        
        # Adjust button sizes
        for button, (base_min_height, base_max_height) in self.base_button_sizes.items():
            if button == self.login_button:
                min_height = int(base_min_height * scale_factor)
                max_height = int(base_max_height * scale_factor)
                button.setMinimumHeight(min_height)
                button.setMaximumHeight(max_height)
                button.setStyleSheet(f"background-color: #3995F1; color: #C3CCDF; padding: {int(10 * scale_factor)}px;")
            else:
                button.setStyleSheet(f"background-color: #1B1E23; color: #C3CCDF; padding: {int(10 * scale_factor)}px;")
        
        # Adjust input field sizes
        email_input_min_height = int(36 * scale_factor)
        email_input_max_height = int(46 * scale_factor)
        for input_field in [self.email_input, self.password_input]:
            input_field.setMinimumHeight(email_input_min_height)
            input_field.setMaximumHeight(email_input_max_height)
            input_field.setStyleSheet(f"background-color: #1B1E23; color: white; padding: {int(10 * scale_factor)}px;")
        
        QFrame.resizeEvent(self.outer_frame, event)

