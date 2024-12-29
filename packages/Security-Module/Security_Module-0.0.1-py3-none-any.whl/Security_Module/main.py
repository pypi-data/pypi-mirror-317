import random
import time

class User:
    def __init__(self, chat_id, phone_number):
        self.chat_id = chat_id
        self.phone_number = phone_number
        self.verification_code = None
        self.last_request_time = None
        self.is_authenticated = False

    def generate_verification_code(self):
        self.verification_code = str(random.randint(100000, 999999))
        return self.verification_code

class SecurityManager:
    def __init__(self):
        self.users_db = {}

    def add_user(self, chat_id, phone_number):
        user = User(chat_id, phone_number)
        self.users_db[chat_id] = user

    def get_user(self, chat_id):
        return self.users_db.get(chat_id)

    def can_request_verification(self, chat_id):
        user = self.get_user(chat_id)
        current_time = time.time()

        if user is None:
            return True

        # Проверяем, прошло ли 60 секунд с последнего запроса
        if user.last_request_time is None or (current_time - user.last_request_time) > 60:
            user.last_request_time = current_time
            return True

        return False

    def request_verification(self, chat_id):
        user = self.get_user(chat_id)
        if user is None:
            raise ValueError("User not found.")

        verification_code = user.generate_verification_code()
        return verification_code

    def verify_code(self, chat_id, code):
        user = self.get_user(chat_id)
        if user is None or user.verification_code is None:
            raise ValueError("User not found or no verification code generated.")

        if code == user.verification_code:
            user.is_authenticated = True
            user.verification_code = None  # Сбрасываем код после успешной проверки
            return True

        return False