import os
from dotenv import load_dotenv

# 1. Загружаем переменные из файла .env в окружение os.environ
load_dotenv()
mode = os.environ.get("MODE")

# 2. Теперь os.environ['MODE'] автоматически станет равен 'DEV' (или тому, что написано в .env)
print("\n\033[1;36m")
print("┌" + "─" * 48 + "┐")
print(f"│  PYTEST environment mode: {mode:<20} │")
print("└" + "─" * 48 + "┘")
print("\033[0m")
