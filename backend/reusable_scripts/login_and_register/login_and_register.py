from qt_core import *
import pyrebase


import re

import os
import base64
import hashlib
import secrets
import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs, urlparse
from google.auth.transport.requests import Request
from google.oauth2 import id_token
import firebase_admin
from firebase_admin import credentials, auth
import threading

# OAuth credentials
GOOGLE_CLIENT_ID = '945419716964-16gsh5dlcd0lvlpdueovhchq31tcb58c.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
FACEBOOK_CLIENT_ID = '922140056392006'
FACEBOOK_CLIENT_SECRET = '6e2557a1633d3833ee829309faaf4a63'

REDIRECT_URI = 'http://localhost:8080/'  # Added trailing slash

# OAuth URLs
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'

FACEBOOK_AUTH_URL = 'https://www.facebook.com/v12.0/dialog/oauth'
FACEBOOK_TOKEN_URL = 'https://graph.facebook.com/v12.0/oauth/access_token'
FACEBOOK_USER_INFO_URL = 'https://graph.facebook.com/me'
FACEBOOK_DEBUG_TOKEN_URL = 'https://graph.facebook.com/debug_token'

firebase_config = {
    "apiKey": "AIzaSyBoLHqzaRmlp_J0CcjVnW8gghWkSxjiU4g",
    "authDomain": "croptmedia-5adb9.firebaseapp.com",
    "databaseURL": "https://croptmedia-5adb9-default-rtdb.firebaseio.com",
    "projectId": "croptmedia-5adb9",
    "storageBucket": "croptmedia-5adb9.appspot.com",
    "messagingSenderId": "714450047320",
    "appId": "1:714450047320:web:015da592562a3db031152d",
    "measurementId": "G-NZLNLXTXTJ"
}

# Initialize Firebase
cred = credentials.Certificate('fire_priv_key.json')
firebase = firebase_admin.initialize_app(cred)


# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
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

        self.authorization_code = None
        self.state = None

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
    

    # SOCIAL MEDIA SIGNIN SECTION
    # ///////////////////////////////////////////////////////////////

    def social_login(self):
        if self.social_provider == 'Google':
            self.auth_url, code_verifier, expected_state = self.google_user_authentication()
        elif self.social_provider == 'Facebook':
            self.auth_url, code_verifier, expected_state = self.facebook_user_authentication()
        else:
            self.login_and_register_signal.emit("Unsupported social provider")
            return

        self.open_auth_url()

        # Start server and wait for a request
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

        # Wait for server to handle the request
        server_thread.join()

        if self.authorization_code and self.state == expected_state:
            try:
                tokens = self.exchange_code_for_token(self.social_provider, self.authorization_code, code_verifier)
                access_token = tokens.get('access_token')
                id_token_str = tokens.get('id_token')  # This will be None for Facebook
                user_info = self.get_user_info(self.social_provider, access_token)

                firebase_user, custom_token = self.authenticate_user_with_firebase(self.social_provider, user_info, id_token_str, access_token)
                
                if firebase_user:
                    self.login_and_register_signal.emit(f"Succesfully signed in")
                    self.sign_in_successful.emit(True)
                else:
                    self.login_and_register_signal.emit("Signed failed. Try Again.")
            except Exception as e:
                self.login_and_register_signal.emit(f"An error occurred during social login: {str(e)}")
        else:
            print("Failed to obtain valid authorization code or state mismatch.")
            self.login_and_register_signal.emit(f"Signed failed. Try Again.")

    def open_auth_url(self):
        webbrowser.open(self.auth_url)


    def generate_code_verifier(self):
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip("=")

    def generate_code_challenge(self, verifier):
        return base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode('utf-8').rstrip("=")

    def start_server(self):
        print("Starting server...")
        server = HTTPServer(('localhost', 8080), OAuthHandler)
        server.timeout = 60
        # Store the instance's data into the server
        server.auth_data = {}
        server.handle_request()  # This will block until a request is received
        print("Server stopped.")
        # Access the data after the request is handled
        self.authorization_code = server.auth_data.get('code')
        self.state = server.auth_data.get('state')


    def google_user_authentication(self):
        code_verifier = self.generate_code_verifier()
        code_challenge = self.generate_code_challenge(code_verifier)
        state = secrets.token_urlsafe(16)

        params = {
            'response_type': 'code',
            'client_id': GOOGLE_CLIENT_ID,
            'redirect_uri': REDIRECT_URI,
            'scope': 'openid profile email',
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
            'state': state
        }
        auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

        return auth_url, code_verifier, state

    def facebook_user_authentication(self):
        state = secrets.token_urlsafe(16)

        params = {
            'client_id': FACEBOOK_CLIENT_ID,
            'redirect_uri': REDIRECT_URI,
            'state': state,
            'scope': 'email'
        }
        auth_url = f"{FACEBOOK_AUTH_URL}?{urlencode(params)}"
    
        return auth_url, None, state

    def exchange_code_for_token(self, provider, code, code_verifier):
        if provider == 'Google':
            data = {
                'client_id': GOOGLE_CLIENT_ID,
                'client_secret': GOOGLE_CLIENT_SECRET,
                'code': code,
                'code_verifier': code_verifier,
                'grant_type': 'authorization_code',
                'redirect_uri': REDIRECT_URI
            }
            response = requests.post(GOOGLE_TOKEN_URL, data=data)
        elif provider == 'Facebook':
            params = {
                'client_id': FACEBOOK_CLIENT_ID,
                'client_secret': FACEBOOK_CLIENT_SECRET,
                'code': code,
                'redirect_uri': REDIRECT_URI
            }
            response = requests.get(FACEBOOK_TOKEN_URL, params=params)
        else:
            raise ValueError("Unsupported provider")

        response.raise_for_status()
        return response.json()

    def get_user_info(self, provider, access_token):
        if provider == 'Google':
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(GOOGLE_USER_INFO_URL, headers=headers)
        elif provider == 'Facebook':
            params = {
                'fields': 'id,name,email',
                'access_token': access_token
            }
            response = requests.get(FACEBOOK_USER_INFO_URL, params=params)
        else:
            raise ValueError("Unsupported provider")

        response.raise_for_status()
        return response.json()

    def verify_facebook_token(self, access_token):
        params = {
            'input_token': access_token,
            'access_token': f'{FACEBOOK_CLIENT_ID}|{FACEBOOK_CLIENT_SECRET}'
        }
        response = requests.get(FACEBOOK_DEBUG_TOKEN_URL, params=params)
        response.raise_for_status()
        data = response.json()['data']
        
        if data['is_valid']:
            return data['user_id']
        else:
            raise ValueError("Invalid Facebook access token")

    def authenticate_user_with_firebase(self, provider, user_info, id_token_str=None, access_token=None):
        try:
            email = user_info.get('email')
            if not email:
                raise ValueError("Email not provided by the OAuth provider")

            try:
                firebase_user = auth.get_user_by_email(email)
            except auth.UserNotFoundError:
                firebase_user = auth.create_user(
                    email=email,
                    display_name=user_info.get('name'),
                    photo_url=user_info.get('picture')
                )

            if provider == 'Google' and id_token_str:
                decoded_token = id_token.verify_oauth2_token(id_token_str, Request(), GOOGLE_CLIENT_ID)
                if decoded_token['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                    raise ValueError("Invalid token issuer")
            elif provider == 'Facebook' and access_token:
                facebook_user_id = self.verify_facebook_token(access_token)
                if facebook_user_id != user_info['id']:
                    raise ValueError("Facebook user ID mismatch")

            custom_token = auth.create_custom_token(firebase_user.uid)
            return firebase_user, custom_token

        except ValueError as e:
            self.login_and_register_signal.emit(f"Authentication error: {str(e)}")
            return None, None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        code = query_components.get('code', [None])[0]
        state = query_components.get('state', [None])[0]

        # Assume unsuccessful by default
        success = False

        # Check if code and state are valid
        if code and state:
            # You can add further validation of the code and state here if necessary
            success = True
            self.server.auth_data = {'code': code, 'state': state}
        
        # Send response based on success
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        if success:
            self.wfile.write(b'Authorization successful! You can close this window.')
        else:
            self.wfile.write(b'Authorization failed. Please try again.')

