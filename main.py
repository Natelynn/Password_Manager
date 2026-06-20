from datetime import datetime
import random
import string

class PasswordRecord:
    """Модель данных для хранения отдельной записи пароля."""
    def __init__(self, service: str, username: str, password: str, created_at: str = None):
        self._service = service.strip()
        self._username = username.strip()
        self._password = password
        self._created_at = created_at if created_at else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def service(self) -> str: return self._service
    @property
    def username(self) -> str: return self._username
    @property
    def password(self) -> str: return self._password
    @property
    def created_at(self) -> str: return self._created_at

    def to_dict(self) -> dict:
        return {"Service": self.service, "Username": self.username, "Password": self.password, "CreatedAt": self.created_at}
    

class BaseGenerator:
    """Базовый класс для генераторов."""
    def generate(self) -> str:
        raise NotImplementedError("Метод должен быть переопределен.")

class AdvancedPasswordGenerator(BaseGenerator):
    """Продвинутый генератор паролей (Полиморфизм)."""
    def generate(self, length: int = 12, use_upper: bool = True, use_digits: bool = True, use_special: bool = True) -> str:
        char_set = string.ascii_lowercase
        if use_upper: char_set += string.ascii_uppercase
        if use_digits: char_set += string.digits
        if use_special: char_set += "!@#$%^&*()-_=+"
        if not char_set: return ""
        
        password = []
        if use_upper: password.append(random.choice(string.ascii_uppercase))
        if use_digits: password.append(random.choice(string.digits))
        if use_special: password.append(random.choice("!@#$%^&*()-_=+"))
        
        remaining_length = length - len(password)
        password += [random.choice(char_set) for _ in range(remaining_length)]
        random.shuffle(password)
        return "".join(password)
