
import json
import re
from pathlib import Path


PACKAGE_PATTERN = re.compile(r"[A-Z]+")


def validate_test_graph(graph):
    """Проверяет структуру и содержимое тестового графа."""
    if not isinstance(graph, dict) or not graph:
        raise ValueError("Граф должен быть непустым JSON-объектом.")

    for package, dependencies in graph.items():
        if not isinstance(package, str):
            raise ValueError("Название пакета должно быть строкой.")

        if not PACKAGE_PATTERN.fullmatch(package):
            raise ValueError(
                f"Недопустимое название пакета: {package}"
            )

        if not isinstance(dependencies, list):
            raise ValueError(
                f"Зависимости пакета {package} должны быть списком."
            )

        for dependency in dependencies:
            if (
                not isinstance(dependency, str)
                or not PACKAGE_PATTERN.fullmatch(dependency)
            ):
                raise ValueError(
                    f"Недопустимая зависимость: {dependency}"
                )

            if dependency not in graph:
                raise ValueError(
                    f"Пакет {dependency} отсутствует в описании графа."
                )

    return graph


def load_test_repository(file_path):
    """Загружает и проверяет тестовый граф из JSON-файла."""
    try:
        with Path(file_path).open(
            "r",
            encoding="utf-8",
        ) as file:
            graph = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Файл тестового репозитория содержит некорректный JSON."
        ) from error
    except OSError as error:
        raise ValueError(
            f"Не удалось прочитать файл: {file_path}"
        ) from error

    return validate_test_graph(graph)
