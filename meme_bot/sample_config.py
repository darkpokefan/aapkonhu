class Config(object):
    LOGGER = True

    API_KEY = "1641418718:AAEAo0AmK5u88LzXXG7crQSQeXvHIOrZngw"
    WEBHOOK = False
    LISTEN = "127.0.0.1"  # IP to listen for webhooks
    URL = None
    CERT_PATH = None
    PORT = 5000
    DEEPFRY_TOKEN = None  # Used for Deepfry facial recognition


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
