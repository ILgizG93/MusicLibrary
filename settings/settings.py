import os
import json

DATABASE_FILE_NAME = 'db/database.json'
SETTINGS_FILE_NAME = 'settings/settings.json'
ROOT_DIR = os.path.abspath(os.curdir)

class Settings:
    def __init__(self):
        ...

    def load_from_json(self, file_name: str) -> None:
        with open(file_name, 'r', encoding='utf-8') as json_file:
            json_data: dict = json.load(json_file)
            for setting in json_data:
                setattr(self, setting, json_data[setting])

class DataBase(Settings):
    def __init__(self):
        self.host: str
        self.port: int
        self.name: str
        self.username: str
        self.password: str
        self.schema: str

        self.load_from_json(DATABASE_FILE_NAME)
