# config.py
import os

APP_NAME = os.getenv("APP_NAME", "chatagent_api")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
APP_API_PORT = os.getenv("APP_API_PORT", 8005)
APP_API_KEY = os.getenv("APP_API_KEY", "s!df$Asd")

APP_ENV = os.getenv("APP_ENV", "dev")
APP_LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
