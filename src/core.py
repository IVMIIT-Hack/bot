#!seperaokeq/bin/python
import logging, configparser 

"""
    Logging + Config
"""

file_path = r"C:/Users/seper/Documents/IVMIIT-Hack/bot"
config = configparser.ConfigParser() 
config.read(file_path + "/config.ini")

token_telegram_api = config["BOT_DATA"]["TOKEN_API"].strip('"');
db_user_file_path = "C:/Users/seper/Documents/IVMIIT-Hack/bot" + "/db/user.db"
logging.basicConfig(level=logging.DEBUG);