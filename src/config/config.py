
import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

MIN_DEPTH = 1
DEFAULT_MAX_DEPTH = 5

ALLOWED_URL_SCHEMES = ("http", "https")
PNG_EXTENSION = ".png"


def validate_package(value):
    """Проверка имени анализируемого пакета."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value):
        raise argparse.ArgumentTypeError(
            "Имя пакета содержит недопустимые символы."
        )
    return value


def validate_repo(value):
    """Проверка URL или пути к тестовому репозиторию."""
    if not value.strip():
        raise argparse.ArgumentTypeError(
            "Путь или URL репозитория не может быть пустым."
        )
    return value


def validate_output(value):
    """Проверка имени выходного PNG-файла."""
    path = Path(value)

    if not value.strip():
        raise argparse.ArgumentTypeError(
            "Имя выходного файла не может быть пустым."
        )

    if path.suffix.lower() != PNG_EXTENSION:
        raise argparse.ArgumentTypeError(
            "Выходной файл должен иметь расширение .png."
        )

    if path.name in ("", ".", ".."):
        raise argparse.ArgumentTypeError(
            "Некорректное имя выходного файла."
        )

    return value


def validate_depth(value):
    """Проверка максимальной глубины анализа."""
    try:
        depth = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Глубина анализа должна быть целым числом."
        )

    if depth < MIN_DEPTH:
        raise argparse.ArgumentTypeError(
            "Глубина анализа должна быть не меньше 1."
        )

    return depth


def validate_repository_mode(repo, test_mode):
    """Проверка репозитория с учетом выбранного режима."""
    if test_mode:
        path = Path(repo)

        if not path.exists():
            raise argparse.ArgumentTypeError(
                f"Файл тестового репозитория не найден: {repo}"
            )

        if not path.is_file():
            raise argparse.ArgumentTypeError(
                "Путь к тестовому репозиторию должен указывать на файл."
            )
    else:
        parsed = urlparse(repo)

        if parsed.scheme not in ALLOWED_URL_SCHEMES or not parsed.netloc:
            raise argparse.ArgumentTypeError(
                "Укажите корректный URL репозитория (http или https)."
            )


def create_parser():
    """Создание парсера аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Dependency Visualizer - Stage 1"
    )

    parser.add_argument(
        "--package",
        type=validate_package,
        required=True,
        help="Имя анализируемого пакета"
    )

    parser.add_argument(
        "--repo",
        type=validate_repo,
        required=True,
        help="URL репозитория или путь к тестовому файлу"
    )

    parser.add_argument(
        "--test-mode",
        choices=["true", "false"],
        default="false",
        help="Режим тестового репозитория (true/false)"
    )

    parser.add_argument(
        "--output",
        type=validate_output,
        default="graph.png",
        help="Имя выходного PNG-файла"
    )

    parser.add_argument(
        "--ascii",
        action="store_true",
        help="Вывод зависимостей в формате ASCII-дерева"
    )

    parser.add_argument(
        "--max-depth",
        type=validate_depth,
        default=DEFAULT_MAX_DEPTH,
        help="Максимальная глубина анализа"
    )

    return parser


def parse_config(args=None):
    """Получение и проверка конфигурации."""
    parser = create_parser()
    config = parser.parse_args(args)

    config.test_mode = config.test_mode == "true"

    try:
        validate_repository_mode(config.repo, config.test_mode)
    except argparse.ArgumentTypeError as error:
        parser.error(str(error))

    return config
