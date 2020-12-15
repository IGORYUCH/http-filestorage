class BaseConfig:
    UPLOAD_FOLDER = 'C:\\Users\\beasty\\Desktop\\projects\\dr_web\\store'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ADJUSTED_NAME_LENGTH = 512
    SERVER_NAME = 'localhost:80'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    SERVER_NAME = '0.0.0.0:8080'
    DEBUG = False