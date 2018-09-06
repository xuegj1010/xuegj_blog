class Config:
    SECRET_KEY = '我是密钥'
    RECAPTCHA_PUBLIC_KEY = '6Lc9r24UAAAAAFB7CT9jd-ZQtlcMRHpeWVwV9AuL'
    RECAPTCHA_PRIVATE_KEY = '6Lc9r24UAAAAACVjrSkm_gu0-tC4drkzKQ7gTKR1'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xgj891010@127.0.0.1:3306/xuegj_blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENCODING = "utf-8"
