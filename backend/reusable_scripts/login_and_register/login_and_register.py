from qt_core import *  # Make sure you import necessary PyQt modules
import pyrebase
import re

# Firebase configuration
firebaseConfig = {
            'apiKey': "AIzaSyBoLHqzaRmlp_J0CcjVnW8gghWkSxjiU4g",
            'authDomain': "croptmedia-5adb9.firebaseapp.com",
            'projectId': "croptmedia-5adb9",
            'storageBucket': "croptmedia-5adb9.appspot.com",
            'messagingSenderId': "714450047320",
            'appId': "1:714450047320:web:015da592562a3db031152d",
            'measurementId': "G-NZLNLXTXTJ",
            "databaseURL": "https://croptmedia-5adb9-default-rtdb.firebaseio.com/"
        }

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

class LoginAndRegister(QThread):

    login_and_register_signal = Signal(str)
    sign_in_successful = Signal(bool)

    def __init__(self, email, password, confirm_pass = None):
        super().__init__()
        self.email = email
        self.password = password
        self.confirm_pass = confirm_pass


    def run(self):
        if self.confirm_pass == None:
            try:
                auth.sign_in_with_email_and_password(self.email, self.password)
                self.sign_in_successful.emit(True)

            except:
                self.login_and_register_signal.emit("Error signing in")
                return False

        else:
            if not self.validate_inputs():
                return False
            
            try:
                # Create user with email and password
                auth.create_user_with_email_and_password(self.email, self.password)
                self.sign_in_successful.emit(True)

            except Exception as e:
                self.login_and_register_signal.emit(f"Email already exists.")
                return False
        



    def validate_inputs(self):

        # Email validation
        if not self.is_valid_email(self.email):
            self.login_and_register_signal.emit("Invalid email format. Please enter a valid email.")
            return False

        # Password and Confirm Password Validation
        if self.password == "" or self.confirm_pass == "":
            print("Password fields cannot be empty.")
            self.login_and_register_signal.emit("Password fields cannot be empty.")
            return False

        if self.password != self.confirm_pass:
            self.login_and_register_signal.emit("Passwords do not match.")
            return False

        # Minimum password length check
        if len(self.password) < 6:
            self.login_and_register_signal.emit("Password must be at least 6 characters long.")
            return False

        return True
    
    def is_valid_email(self, email):
        # Regular expression for validating email (RFC 5322 official standard)
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)