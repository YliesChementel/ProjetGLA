class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    SECRET_KEY = 'test_secret'
    WTF_CSRF_ENABLED = False
