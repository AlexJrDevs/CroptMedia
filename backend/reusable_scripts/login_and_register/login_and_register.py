import firebase_admin._auth_client
import firebase_admin.auth
from qt_core import *
import pyrebase


import re

import json
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
from datetime import datetime, timedelta
from dotenv import set_key, dotenv_values

config = {**dotenv_values(".env.secret")}

# Load sensitive data from environment variables
GOOGLE_CLIENT_ID = config.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = config.get('GOOGLE_CLIENT_SECRET')
FACEBOOK_CLIENT_ID = config.get('FACEBOOK_CLIENT_ID')
FACEBOOK_CLIENT_SECRET = config.get('FACEBOOK_CLIENT_SECRET')
FIREBASE_SECRET = config.get('FIREBASE_SECRET')
FIREBASE_CONFIG = config.get('FIREBASE_CONFIG')
FIREBASE_TOKENS = config.get('FIREBASE_TOKENS')

REDIRECT_URI = 'http://localhost:8080/'  # Added trailing slash

# OAuth URLs
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'

FACEBOOK_AUTH_URL = 'https://www.facebook.com/v12.0/dialog/oauth'
FACEBOOK_TOKEN_URL = 'https://graph.facebook.com/v12.0/oauth/access_token'
FACEBOOK_USER_INFO_URL = 'https://graph.facebook.com/me'
FACEBOOK_DEBUG_TOKEN_URL = 'https://graph.facebook.com/debug_token'

# Initialize Firebase
cred = credentials.Certificate(json.loads(FIREBASE_SECRET))
firebase_admin.initialize_app(cred)


# Initialize Firebase
firebase = pyrebase.initialize_app(json.loads(FIREBASE_CONFIG))
auths = firebase.auth()




class LoginAndRegister(QThread):
    login_and_register_signal = Signal(str)
    sign_in_successful = Signal(bool)

    def __init__(self, operation=None, email=None, password=None, confirm_pass=None, social_provider=None):
        super().__init__()
        self.email = email
        self.password = password
        self.confirm_pass = confirm_pass
        self.social_provider = social_provider
        self.operation = operation

        self.authorization_code = None
        self.state = None

    def run(self):

        if self.operation == "social_login":
            self.social_login()

        if self.operation == "email_login":
            self.email_login()
        
        if self.operation == "email_register":
            self.email_register()


    def logout_user(self):
        try:
            # Load saved tokens
            tokens_data = self.load_tokens()
            if tokens_data is None:
                print("No tokens found to revoke")
                return

            # Revoke tokens based on provider
            provider = tokens_data.get('provider')
            access_token = tokens_data.get('access_token')
            
            if provider and access_token:
                if provider == 'Google':
                    self.revoke_google_token(access_token)
                elif provider == 'Facebook':
                    self.revoke_facebook_token(access_token)

            # Clear stored tokens
            set_key(dotenv_path=".env.secret", key_to_set="FIREBASE_TOKENS", value_to_set="")
            print("FIREBASE_TOKENS cleared.")
            
            # Clear current user
            auths.current_user = None
            
            print("Logout completed successfully")
            self.login_and_register_signal.emit("Logged out successfully")
            
        except Exception as e:
            print(f"Error during logout process: {e}")
            self.login_and_register_signal.emit("Error during logout")






    def reset_password(self):
        print("Starting reset_password function")
        print("Email: ", self.email)
        try:
            # Email validation regex pattern
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            # Then validate email format
            if not re.match(email_pattern, self.email):
                print("Email validation failed")
                self.login_and_register_signal.emit("Invalid email format. Please try again.")
                return
            
            print("About to send reset email")
            auths.send_password_reset_email(self.email)
            print("Reset email sent successfully")
            self.login_and_register_signal.emit("Password reset email sent. Please check your inbox / spam.")
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            self.login_and_register_signal.emit("Failed to send password reset email... Try Again.")


    def email_login(self):
        try:
            user = auths.sign_in_with_email_and_password(self.email, self.password)
            user_info = auths.get_account_info(user['idToken'])
            users = user_info.get('users', [])
            
            if users:
                email_verified = users[0].get('emailVerified')
            if email_verified:
                expires_in = int(user.get('expiresIn', 3600))
                expiration_time = datetime.now() + timedelta(seconds=expires_in)
                self.save_tokens(user['idToken'], user['refreshToken'], expiration_time.isoformat())
                self.login_and_register_signal.emit("Successfully signed in!")
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
        id_token = self.get_valid_id_token()

        if id_token:
            try:
                decoded_token = auth.verify_id_token(id_token)
                uid = decoded_token.get('uid')
                email = decoded_token.get('email')

                print(f"User already authenticated:\nUID: {uid}\nEmail: {email}")
                self.sign_in_successful.emit(True)
                return
            except Exception as e:
                print(f"Error verifying existing token: {e}")

    
        if self.social_provider == 'Google':
            self.auth_url, code_verifier, expected_state = self.google_user_authentication()
        elif self.social_provider == 'Facebook':
            self.auth_url, code_verifier, expected_state = self.facebook_user_authentication()
        else:
            print("Unsupported social provider")
            return

        self.open_auth_url()

        # Start server and wait for a request
        server_thread = threading.Thread(target=self.start_server)
        server_thread.start()

        # Wait for server to handle the request
        server_thread.join()

        if self.authorization_code and self.state:
            try:
                token_data = self.exchange_code_for_token(code_verifier)

                id_token_str = token_data.get('id_token')
                access_token = token_data.get('access_token')

                user_info = self.get_user_info(access_token)

                firebase_user = self.authenticate_user_with_firebase(user_info, id_token_str, access_token)
                if firebase_user:
                    print(f"Authenticated Firebase user: {firebase_user.uid}")
                    self.sign_in_successful.emit(True)
                else:
                    self.login_and_register_signal("Failed to sign in. Please try again.")
            except Exception as e:
                print(f"Error during authentication process: {e}")
        else:
            print("Authorization failed")

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


        #if server.success:
            #self.login_and_register_signal.emit("Successfully signed in!")
       # else:
            #self.login_and_register_signal.emit("Sign in failed. Please try again.")



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

    def exchange_code_for_token(self, code_verifier):
        if self.social_provider == 'Google':
            data = {
                'client_id': GOOGLE_CLIENT_ID,
                'client_secret': GOOGLE_CLIENT_SECRET,
                'code': self.authorization_code,
                'code_verifier': code_verifier,
                'grant_type': 'authorization_code',
                'redirect_uri': REDIRECT_URI
            }
            response = requests.post(GOOGLE_TOKEN_URL, data=data)
        elif self.social_provider == 'Facebook':
            params = {
                'client_id': FACEBOOK_CLIENT_ID,
                'client_secret': FACEBOOK_CLIENT_SECRET,
                'code': self.authorization_code,
                'redirect_uri': REDIRECT_URI
            }
            response = requests.get(FACEBOOK_TOKEN_URL, params=params)
        else:
            raise ValueError("Unsupported provider")

        response.raise_for_status()
        return response.json()

    def get_user_info(self, access_token):
        if self.social_provider == 'Google':
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(GOOGLE_USER_INFO_URL, headers=headers)
        elif self.social_provider == 'Facebook':
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
    
    def refresh_firebase_token(self, refresh_token):
        try:
            user = auths.refresh(refresh_token)
            return user['idToken'], user['refreshToken'], user['expiresIn']
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return None, None, None
        
    def get_valid_id_token(self):
        id_token, refresh_token, expiration_time = self.get_token_values()
        
        if id_token and refresh_token and expiration_time:
            if datetime.now() < expiration_time:
                return id_token
            else:
                new_id_token, new_refresh_token, expiration_time = self.refresh_firebase_token(refresh_token)
                if new_id_token and new_refresh_token:
                    expiration_time = datetime.now() + timedelta(seconds=int(expiration_time))
                    self.save_tokens(new_id_token, new_refresh_token, expiration_time.isoformat())
                    return new_id_token
        
        return None
    

    def load_tokens(self):
        if FIREBASE_TOKENS:
            try:
                data = json.loads(FIREBASE_TOKENS)
                tokens_data = {
                    'id_token': data.get('id_token'),
                    'refresh_token': data.get('refresh_token'),
                    'expiration_time': datetime.fromisoformat(data.get('expiration_time')) if data.get('expiration_time') else None,
                    'access_token': data.get('access_token'),
                    'provider': data.get('provider')
                }
                return tokens_data
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Error decoding FIREBASE_TOKENS: {e}")
                return None
        return None

    def get_token_values(self):
        tokens_data = self.load_tokens()
        if tokens_data:
            return (
                tokens_data.get('id_token'),
                tokens_data.get('refresh_token'),
                tokens_data.get('expiration_time')
            )
        return None, None, None

    def save_tokens(self, id_token, refresh_token, expiration_time, access_token=None, provider=None):
        tokens_data = {
            'id_token': id_token,
            'refresh_token': refresh_token,
            'expiration_time': expiration_time,
            'access_token': access_token,  # Save access token
            'provider': provider  # Save provider information
        }
        set_key(dotenv_path=".env.secret", key_to_set="FIREBASE_TOKENS", value_to_set=json.dumps(tokens_data))
        print("Tokens saved in environment variable.")

    def revoke_google_token(self, access_token):
        try:
            response = requests.post(
                'https://oauth2.googleapis.com/revoke',
                params={'token': access_token},
                headers={'content-type': 'application/x-www-form-urlencoded'}
            )
            if response.status_code == 200:
                print("Google token revoked successfully")
                return True
            else:
                print(f"Failed to revoke Google token: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error revoking Google token: {e}")
            return False

    def revoke_facebook_token(self, access_token):
        try:
            response = requests.delete(
                'https://graph.facebook.com/v12.0/me/permissions',
                params={'access_token': access_token}
            )
            if response.status_code == 200:
                print("Facebook token revoked successfully")
                return True
            else:
                print(f"Failed to revoke Facebook token: {response.status_code}")
                return False
        except Exception as e:
            print(f"Error revoking Facebook token: {e}")
            return False


    def authenticate_user_with_firebase(self, user_info, id_token_str=None, access_token=None):
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

            if self.social_provider == 'Google' and id_token_str:
                decoded_token = id_token.verify_oauth2_token(id_token_str, Request(), GOOGLE_CLIENT_ID)
                if decoded_token['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                    raise ValueError("Invalid token issuer")
            elif self.social_provider == 'Facebook' and access_token:
                facebook_user_id = self.verify_facebook_token(access_token)
                if facebook_user_id != user_info['id']:
                    raise ValueError("Facebook user ID mismatch")

            custom_token = auth.create_custom_token(firebase_user.uid)
            custom_token_str = custom_token.decode('utf-8')

            user = auths.sign_in_with_custom_token(custom_token_str)
            expires_in = int(user.get('expiresIn', 3600))
            expiration_time = datetime.now() + timedelta(seconds=expires_in)
            
            # Save tokens with provider information and access token
            self.save_tokens(
                user['idToken'], 
                user['refreshToken'], 
                expiration_time.isoformat(),
                access_token=access_token,
                provider=self.social_provider
            )

            print(f"All tokens saved.")
            return firebase_user

        except ValueError as e:
            print(f"Authentication error: {str(e)}")
            return None

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

 