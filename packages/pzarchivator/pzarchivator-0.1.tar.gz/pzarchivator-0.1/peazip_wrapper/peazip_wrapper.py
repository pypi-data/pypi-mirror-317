import subprocess
from typing import List, Optional

class PeaZipWrapper:
    def __init__(self, executable: str = r"C:\Program Files\PeaZip\res\bin\7z\7z.exe"):
        """
        Клас-обгортка для роботи з 7z (використовується в PeaZip).

        :param executable: Шлях до виконуваного файлу 7z.exe
        """
        self.executable = executable

    def _run_command(self, command: List[str]) -> str:
        """
        Виконує команду 7z з аргументами.

        :param command: Список аргументів командного рядка
        :return: Результат виконання команди
        """
        try:
            result = subprocess.run(
                [self.executable] + command,
                check=True,
                text=True,
                capture_output=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"

    def create_archive(self, archive_name: str, files: List[str], password: Optional[str] = None) -> str:
        """
        Створює ZIP-архів з можливістю захисту паролем.

        :param archive_name: Назва архіву (з повним шляхом)
        :param files: Список файлів для архівації
        :param password: Пароль для архіву (опціонально)
        :return: Результат виконання команди
        """
        command = ['a', '-tzip', archive_name]
        command.extend(files)
        if password:
            command.extend(['-p' + password, '-mem=AES256'])  # Додає пароль із шифруванням AES256
        return self._run_command(command)

    def extract_archive(self, archive_name: str, output_dir: str, password: Optional[str] = None) -> str:
        """
        Витягує файли з архіву.

        :param archive_name: Назва архіву (з повним шляхом)
        :param output_dir: Каталог для витягу файлів
        :param password: Пароль для архіву (опціонально)
        :return: Результат виконання команди
        """
        command = ['x', archive_name, '-o' + output_dir, '-y']  # -y для автоматичного підтвердження
        if password:
            command.append('-p' + password)  # Додає пароль для розархівації
        return self._run_command(command)