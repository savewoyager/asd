
import json
import tempfile
import unittest
from pathlib import Path

from src.dependencies.test_repository import (
    load_test_repository,
    validate_test_graph,
)


class TestRepository(unittest.TestCase):
    """Проверки загрузки тестового репозитория."""

    def test_valid_graph(self):
        """Проверяет корректный граф."""
        graph = {"A": ["B"], "B": []}

        self.assertEqual(validate_test_graph(graph), graph)

    def test_empty_graph(self):
        """Проверяет отклонение пустого графа."""
        with self.assertRaises(ValueError):
            validate_test_graph({})

    def test_invalid_package_name(self):
        """Проверяет отклонение строчных букв."""
        with self.assertRaises(ValueError):
            validate_test_graph({"a": []})

    def test_missing_dependency(self):
        """Проверяет отсутствие зависимости в графе."""
        with self.assertRaises(ValueError):
            validate_test_graph({"A": ["B"]})

    def test_invalid_dependency_list(self):
        """Проверяет неверный формат зависимостей."""
        with self.assertRaises(ValueError):
            validate_test_graph({"A": "B"})

    def test_invalid_json_file(self):
        """Проверяет обработку некорректного JSON-файла."""
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "invalid.json"
            file_path.write_text("{invalid}", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_test_repository(file_path)

    def test_missing_file(self):
        """Проверяет обработку отсутствующего файла."""
        with self.assertRaises(ValueError):
            load_test_repository("missing_repository.json")


if __name__ == "__main__":
    unittest.main()
