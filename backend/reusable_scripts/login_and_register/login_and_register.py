from qt_core import *
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
auths = firebase.auth()


class LoginAndRegister(QThread):
    login_and_register_signal = Signal(str)
    sign_in_successful = Signal(bool)

    def __init__(self, email=None, password=None, confirm_pass=None, social_provider=None):
        super().__init__()
        self.email = email
        self.password = password
        self.confirm_pass = confirm_pass
        self.social_provider = social_provider

    def run(self):
        if self.social_provider:
            self.social_login()
        elif self.confirm_pass is None:
            self.email_login()
        else:
            self.email_register()

    def email_login(self):
        try:
            user = auths.sign_in_with_email_and_password(self.email, self.password)
            user_info = auths.get_account_info(user['idToken'])
            users = user_info.get('users', [])
            
            if users:
                email_verified = users[0].get('emailVerified')
            if email_verified:
                self.sign_in_successful.emit(True)
            else:
                self.login_and_register_signal.emit("Email not verified. Please verify your email before logging in.")
                
        except Exception as e:
            self.login_and_register_signal.emit(f"Incorrect email or password. Please try again.")

    def email_register(self):
        if not self.validate_inputs():
            return

        try:
            user = auths.create_user_with_email_and_password(self.email, self.password)
            auths.send_email_verification(user['idToken'])
            
            self.login_and_register_signal.emit("Registration successful. Please check your email for verification.")
        except Exception as e:
            self.login_and_register_signal.emit(f"Email already exists.")

    def social_login(self):
        print("Logging in")

    def validate_inputs(self):
        if not self.is_valid_email(self.email):
            self.login_and_register_signal.emit("Invalid email format. Please enter a valid email.")
            return False

        if self.password == "" or self.confirm_pass == "":
            self.login_and_register_signal.emit("Password fields cannot be empty.")
            return False

        if self.password != self.confirm_pass:
            self.login_and_register_signal.emit("Passwords do not match.")
            return False

        if len(self.password) < 6:
            self.login_and_register_signal.emit("Password must be at least 6 characters long.")
            return False

        return True

    def is_valid_email(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)