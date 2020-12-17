class BaseConfig:
    UPLOAD_FOLDER = '/home/username/filestorage/store'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ADJUSTED_NAME_LENGTH = 512


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False