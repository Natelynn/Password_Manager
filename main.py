from datetime import datetime
import random
import string
import json
import os

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


class PasswordController:
    """Контроллер для обработки бизнес-логики и работы с JSON."""
    def __init__(self, file_path: str = "passwords.json"):
        self.file_path = file_path
        self.records = []
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.file_path): return
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.records = [PasswordRecord(r["Service"], r["Username"], r["Password"], r["CreatedAt"]) for r in data]
        except (json.JSONDecodeError, KeyError): pass

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in self.records], f, ensure_ascii=False, indent=4)

    def add_record(self, service: str, username: str, password: str) -> bool:
        if not service.strip() or not username.strip() or not password.strip(): return False
        self.records.append(PasswordRecord(service, username, password))
        self.save_data()
        return True

    def get_all_records(self) -> list: return self.records

    def delete_record(self, index: int) -> bool:
        if 0 <= index < len(self.records):
            self.records.pop(index)
            self.save_data()
            return True
        return False
    
    
class PasswordView:
    """Представление для взаимодействия с пользователем."""
    @staticmethod
    def show_menu():
        print("\n=== PASSWORD MANAGER ===\n1. Посмотреть все пароли\n2. Добавить новый пароль\n3. Сгенерировать пароль\n4. Удалить пароль\n5. Выйти")
    @staticmethod
    def display_records(records: list):
        if not records: print("\n[!] База пуста."); return
        print(f"\n{'№':<3} | {'Сервис':<15} | {'Логин':<15} | {'Пароль':<15}")
        for idx, r in enumerate(records): print(f"{idx:<3} | {r.service:<15} | {r.username:<15} | {r.password:<15}")
    @staticmethod
    def get_input(prompt: str) -> str: return input(prompt)

def main():
    controller = PasswordController()
    generator = AdvancedPasswordGenerator()
    view = PasswordView()
    while True:
        view.show_menu()
        choice = view.get_input("Действие: ").strip()
        if choice == "1": view.display_records(controller.get_all_records())
        elif choice == "2":
            if controller.add_record(view.get_input("Сервис: "), view.get_input("Логин: "), view.get_input("Пароль: ")): print("[+] Сохранено")
            else: print("[-] Ошибка валидации")
        elif choice == "3": print(f"Пароль: {generator.generate()}")
        elif choice == "4":
            try:
                if controller.delete_record(int(view.get_input("Номер для удаления: "))): print("[+] Удалено")
                else: print("[-] Не найдено")
            except ValueError: print("[-] Некорректный ввод")
        elif choice == "5": break

if __name__ == "__main__":
    main()
