import firebase_admin._auth_client
import firebase_admin.auth
from qt_core import *
import pyrebase

import socket
from typing import Optional


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




class UserAccountManager(QThread):
    login_and_register_signal = Signal(str)
    sign_in_successful = Signal(bool)

    email_sign_signal = Signal(str, str)  # Signal for login
    email_register_signal = Signal(str, str, str)  # Signal for registration
    social_login_signal = Signal(str) # Logins user with social

    user_reset_password = Signal(str) # Resets user password
    user_logout = Signal() # Logouts user

    def __init__(self):
        super().__init__()
        self.current_server: Optional[WebServer] = None

        self.email_sign_signal.connect(self.email_login)
        self.email_register_signal.connect(self.email_register)  
        self.social_login_signal.connect(self.social_login) 

        self.user_reset_password.connect(self.reset_password)
        self.user_logout.connect(self.logout_user)
        

    # EMAIL SIGN UP / IN
    # ///////////////////////////////////////////////////////////////

    def email_login(self, user_email, user_password):
        try:
            user = auths.sign_in_with_email_and_password(user_email, user_password)
            print(user_email, user_password)
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

    def email_register(self, user_email, user_password, confirm_pass):
        if not self.validate_inputs(user_email, user_password, confirm_pass):
            return

        try:
            user = auths.create_user_with_email_and_password(user_email, user_password)
            auths.send_email_verification(user['idToken'])
            
            self.login_and_register_signal.emit("Registration successful. Please check your email for verification.")
        except Exception as e:
            self.login_and_register_signal.emit(f"Email already exists.")


    # USER INPUT VALIDATION
    # ///////////////////////////////////////////////////////////////

    def validate_inputs(self, user_email, user_password, confirm_pass):
        if not self.is_valid_email(user_email):
            self.login_and_register_signal.emit("Invalid email format. Please enter a valid email.")
            return False

        if user_password == "" or confirm_pass == "":
            self.login_and_register_signal.emit("Password fields cannot be empty.")
            return False

        if user_password != confirm_pass:
            self.login_and_register_signal.emit("Passwords do not match.")
            return False

        if len(user_password) < 6:
            self.login_and_register_signal.emit("Password must be at least 6 characters long.")
            return False

        return True

    def is_valid_email(self, user_email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, user_email)


    # LOGOUT / RESET PASSWORD
    # ///////////////////////////////////////////////////////////////

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
            self.login_and_register_signal.emit("You are now logged out. See you soon!")
            
        except Exception as e:
            print(f"Error during logout process: {e}")
            self.login_and_register_signal.emit("Error during logout")




    def reset_password(self, email):
        print("Starting reset_password function")
        print("Email: ", email)
        try:
            # Email validation regex pattern
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            # Then validate email format
            if not re.match(email_pattern, email):
                print("Email validation failed")
                self.login_and_register_signal.emit("Invalid email format. Please try again.")
                return
            
            print("About to send reset email")
            auths.send_password_reset_email(email)
            print("Reset email sent successfully")
            self.login_and_register_signal.emit("Password reset email sent. Please check your inbox / spam.")
        except Exception as e:
            print(f"Exception occurred: {str(e)}")
            self.login_and_register_signal.emit("Failed to send password reset email... Try Again.")


    

    # SOCIAL MEDIA SIGN IN SECTION
    # ///////////////////////////////////////////////////////////////

    def social_login(self, social_provider):
        try:
            # Clean up any existing server
            if self.current_server:
                self.current_server.stop()
                self.current_server = None

            # Determine the authentication URL based on the social provider
            if social_provider == 'Google':
                self.auth_url, code_verifier, expected_state = self.google_user_authentication()
            elif social_provider == 'Facebook':
                self.auth_url, code_verifier, expected_state = self.facebook_user_authentication()
            else:
                print("Unsupported social provider")
                return

            print("Open new web browser")
            webbrowser.open(self.auth_url)

            print("Create new thread")
            self.current_server = WebServer()
            self.current_server.auth_error.connect(self.handle_auth_error)
            self.current_server.set_auth_params(social_provider, code_verifier)
            self.current_server.start()
            self.current_server.finished.connect(self.process_auth_response)
            print("finished creating new thread")

        except Exception as e:
            self.login_and_register_signal.emit(f"Error starting authentication: {str(e)}")


    def handle_auth_error(self, error_message: str):
        self.login_and_register_signal.emit(error_message)
        if self.current_server:
            self.current_server.stop()
            self.current_server = None

    def process_auth_response(self):
        if not self.current_server:
            return

        print("Server finished")
        # Access social provider and code verifier from the server_thread
        social_provider = self.current_server.social_provider
        code_verifier = self.current_server.code_verifier

        if self.current_server.authorization_code and self.current_server.state:
            try:
                # Use social_provider and code_verifier in the token exchange
                token_data = self.exchange_code_for_token(
                    social_provider, 
                    code_verifier, 
                    self.current_server.authorization_code
                )

                id_token_str = token_data.get('id_token')
                access_token = token_data.get('access_token')

                user_info = self.get_user_info(social_provider, access_token)

                firebase_user = self.authenticate_user_with_firebase(
                    user_info, 
                    social_provider, 
                    id_token_str, 
                    access_token
                )
                
                if firebase_user:
                    print(f"Authenticated Firebase user: {firebase_user.uid}")
                    self.sign_in_successful.emit(True)
                else:
                    self.login_and_register_signal.emit("Failed to sign in. Please try again.")
            except Exception as e:
                print(f"Error during authentication process: {e}")
                self.login_and_register_signal.emit(f"Authentication failed: {str(e)}")
        else:
            print("Authorization failed")
            self.login_and_register_signal.emit("Authorization failed or cancelled.")

        # Clean up the server
        self.current_server.stop()
        self.current_server = None



    # SAVES SOCIAL SIGN UP TOKENS AND ADDS IT TO FIREBASE DATABASE
    # ///////////////////////////////////////////////////////////////

    def authenticate_user_with_firebase(self, user_info, social_provider, id_token_str=None, access_token=None):
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

            if social_provider == 'Google' and id_token_str:
                decoded_token = id_token.verify_oauth2_token(id_token_str, Request(), GOOGLE_CLIENT_ID)
                if decoded_token['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                    raise ValueError("Invalid token issuer")
            elif social_provider == 'Facebook' and access_token:
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
                provider=social_provider
            )

            return firebase_user

        except ValueError as e:
            print(f"Authentication error: {str(e)}")
            return None



    # SAVES SOCIAL AUTHENTICATION / TOKEN RETRIEVE
    # ///////////////////////////////////////////////////////////////

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

    def exchange_code_for_token(self, social_provider, code_verifier, authorization_code):
        if social_provider == 'Google':
            data = {
                'client_id': GOOGLE_CLIENT_ID,
                'client_secret': GOOGLE_CLIENT_SECRET,
                'code': authorization_code,
                'code_verifier': code_verifier,
                'grant_type': 'authorization_code',
                'redirect_uri': REDIRECT_URI
            }
            response = requests.post(GOOGLE_TOKEN_URL, data=data)
        elif social_provider == 'Facebook':
            params = {
                'client_id': FACEBOOK_CLIENT_ID,
                'client_secret': FACEBOOK_CLIENT_SECRET,
                'code': authorization_code,
                'redirect_uri': REDIRECT_URI
            }
            response = requests.get(FACEBOOK_TOKEN_URL, params=params)
        else:
            raise ValueError("Unsupported provider")

        response.raise_for_status()
        return response.json()

    def get_user_info(self, social_provider, access_token):
        if social_provider == 'Google':
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.get(GOOGLE_USER_INFO_URL, headers=headers)
        elif social_provider == 'Facebook':
            params = {
                'fields': 'id,name,email',
                'access_token': access_token
            }
            response = requests.get(FACEBOOK_USER_INFO_URL, params=params)
        else:
            raise ValueError("Unsupported provider")

        response.raise_for_status()
        return response.json()
    

    def generate_code_verifier(self):
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip("=")

    def generate_code_challenge(self, verifier):
        return base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode('utf-8').rstrip("=")

        



    # USER ACCOUNT TOKEN MANAGEMENT
    # ///////////////////////////////////////////////////////////////
    
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
    

    def get_token_values(self):
        tokens_data = self.load_tokens()
        if tokens_data:
            return (
                tokens_data.get('id_token'),
                tokens_data.get('refresh_token'),
                tokens_data.get('expiration_time')
            )
        return None, None, None
    

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
        
        
    
        

# CREATES THE SERVER TO RETRIEVE AUTHORIZATION
# ///////////////////////////////////////////////////////////////


class WebServer(QThread):
    auth_error = Signal(str)  # New signal for error handling

    def __init__(self):
        super().__init__()
        self.social_provider = None
        self.code_verifier = None
        self.authorization_code = None
        self.state = None
        self.server: Optional[HTTPServer] = None
        self._port_in_use = False

    def set_auth_params(self, social_provider, code_verifier):
        self.social_provider = social_provider
        self.code_verifier = code_verifier

    def is_port_in_use(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return False
            except socket.error:
                return True

    def run(self):
        try:
            if self.is_port_in_use(8080):
                self.auth_error.emit("Authentication server is already running. Please close any open authentication windows and try again.")
                return

            self._port_in_use = True
            self.server = HTTPServer(('localhost', 8080), OAuthHandler)
            self.server.auth_data = {}
            self.server.timeout = 60
            self.server.handle_request()

            self.authorization_code = self.server.auth_data.get('code')
            self.state = self.server.auth_data.get('state')

        except Exception as e:
            self.auth_error.emit(f"Authentication error: {str(e)}")
            print(f"Authentication error inside of WebServer: {str(e)}")
        finally:
            self.cleanup()

    def cleanup(self):
        if self.server:
            try:
                self.server.server_close()
            except Exception:
                pass
            self.server = None
        self._port_in_use = False

    def stop(self):
        self.cleanup()
        self.quit()
        self.wait()


# Custom HTTP request handler for OAuth
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

 