from app.core.config import get_settings

class Email():
    def __init__(self):
        self.resend_key = get_settings().general.resend_key.get_secret_value()
        pass

