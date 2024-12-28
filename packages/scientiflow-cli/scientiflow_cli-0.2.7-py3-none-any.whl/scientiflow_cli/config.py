import os

class Config:
    APP_BASE_URL = os.getenv("APP_BASE_URL", "https://www.scientiflow-backend-dev.scientiflow.com/api")