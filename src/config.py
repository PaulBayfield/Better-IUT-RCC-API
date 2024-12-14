from sanic.config import Config


class AppConfig(Config):
    API_VERSION = "1.0.0"
    API_CONTACT_EMAIL = "betteriutrcc@bayfield.dev"

    OAS = False

    CORS_ORIGINS = "*"
    CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]

    FALLBACK_ERROR_FORMAT = "json"
