import re
import os
from configparser import ConfigParser
from typing import List
from pathlib import Path


def read_config(file_path: str = "config.ini") -> ConfigParser:
    """
    Читает конфигурационный файл и возвращает объект ConfigParser.

    :param file_path: Путь к конфигурационному файлу. По умолчанию "config.ini".
    :return: Объект ConfigParser с загруженной конфигурацией.
    """
    config = ConfigParser()
    config.read(file_path)
    return config


def extract_numbers_from_string(content: str) -> List[int]:
    """
    Извлекает числа из строки и возвращает список целых чисел.

    :param content: Строка, из которой нужно извлечь числа.
    :return: Список целых чисел.
    """
    numbers = []
    for re_match in re.finditer(r"\d+\-\d+|\d+", content):
        number_range = re_match.group(0)
        if "-" in number_range:
            start, end = map(int, number_range.split("-"))
            numbers.extend(range(start, end + 1))
        else:
            numbers.append(int(number_range))
    return numbers


def process_file(input_file: Path, output_directory: Path) -> None:
    """
    Обрабатывает входной файл, извлекает числа и записывает их в выходной файл.

    :param input_file: Путь к входному файлу.
    :param output_directory: Путь к выходной директории.
    :return: None
    """
    with input_file.open("r") as file:
        content = file.read()

    numbers = extract_numbers_from_string(content)

    output_file_name = input_file.name.lower().replace("test_", "test_auchan_success_")
    output_file = output_directory / output_file_name

    with output_file.open("w") as file:
        file.writelines(f"{number}\n" for number in numbers)


def process_files_in_directory(input_directory: Path, output_directory: Path) -> None:
    """
    Обрабатывает все файлы в указанной директории.

    :param input_directory: Путь к директории с входными файлами.
    :param output_directory: Путь к директории, в которую будут записаны выходные файлы.
    :return: None
    """
    output_directory.mkdir(parents=True, exist_ok=True)

    for input_file in input_directory.glob("TEST_*.txt"):
        process_file(input_file, output_directory)


if __name__ == "__main__":
    config = read_config()

    input_directory = Path(
        os.environ.get("INPUT_DIRECTORY", config.get("Directories", "INPUT_DIRECTORY"))
    )
    output_directory = Path(
        os.environ.get(
            "OUTPUT_DIRECTORY", config.get("Directories", "OUTPUT_DIRECTORY")
        )
    )

    for subdirectory in input_directory.iterdir():
        if subdirectory.is_dir():
            process_files_in_directory(subdirectory, output_directory)
