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
import json
import os

# APP SETTINGS
# ///////////////////////////////////////////////////////////////
class Settings(object):
    # APP PATH
    # ///////////////////////////////////////////////////////////////
    json_file = "settings.json"
    text_json_file = "text_settings.json"
    app_path = os.path.abspath(os.getcwd())

    settings_path = os.path.normpath(os.path.join(app_path, json_file))
    text_settings_path = os.path.normpath(os.path.join(app_path, text_json_file))

    if not os.path.isfile(settings_path):
        print(f"WARNING: \"{json_file}\" not found! Check in the folder {settings_path}")
    if not os.path.isfile(text_settings_path):
        print(f"WARNING: \"{text_json_file}\" not found! Check in the folder {text_settings_path}")
    
    # INIT SETTINGS
    # ///////////////////////////////////////////////////////////////
    def __init__(self):
        super(Settings, self).__init__()

        # DICTIONARIES WITH SETTINGS
        self.items = {}        # For settings.json
        self.text_items = {}   # For text_settings.json

        # DESERIALIZE
        self.deserialize()

    # SERIALIZE JSON
    # ///////////////////////////////////////////////////////////////
    def serialize(self):
        # WRITE settings.json
        with open(self.settings_path, "w", encoding='utf-8') as write_file:
            json.dump(self.items, write_file, indent=4)
        
        # WRITE text_settings.json
        with open(self.text_settings_path, "w", encoding='utf-8') as write_file:
            json.dump(self.text_items, write_file, indent=4)

    # DESERIALIZE JSON
    # ///////////////////////////////////////////////////////////////
    def deserialize(self):
        # READ settings.json
        if os.path.isfile(self.settings_path):
            with open(self.settings_path, "r", encoding='utf-8') as read_file:
                self.items = json.load(read_file)

        # READ text_settings.json
        if os.path.isfile(self.text_settings_path):
            with open(self.text_settings_path, "r", encoding='utf-8') as read_file:
                self.text_items = json.load(read_file)

