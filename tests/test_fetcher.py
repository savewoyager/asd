
import json
import unittest
from io import BytesIO
from urllib.error import HTTPError, URLError
from unittest.mock import patch

from src.dependencies.fetcher import (
    extract_direct_dependencies,
    fetch_metadata,
)


TEST_URL = "https://pypi.org/pypi/flask/json"
NOT_FOUND_STATUS = 404


class TestFetchMetadata(unittest.TestCase):
    """Проверки получения метаданных из репозитория."""

    def test_successful_request(self):
        """Проверяет получение корректного JSON."""
        response_data = {"info": {"name": "flask"}}
        response = BytesIO(json.dumps(response_data).encode("utf-8"))

        with patch(
            "src.dependencies.fetcher.urlopen",
            return_value=response,
        ):
            result = fetch_metadata(TEST_URL)

        self.assertEqual(result, response_data)

    def test_http_error(self):
        """Проверяет обработку HTTP-ошибки."""
        error = HTTPError(
            TEST_URL,
            NOT_FOUND_STATUS,
            "Not Found",
            {},
            None,
        )

        with patch(
            "src.dependencies.fetcher.urlopen",
            side_effect=error,
        ):
            with self.assertRaisesRegex(ValueError, "HTTP"):
                fetch_metadata(TEST_URL)

    def test_connection_error(self):
        """Проверяет обработку ошибки подключения."""
        with patch(
            "src.dependencies.fetcher.urlopen",
            side_effect=URLError("Connection failed"),
        ):
            with self.assertRaisesRegex(ValueError, "подключиться"):
                fetch_metadata(TEST_URL)

    def test_invalid_json(self):
        """Проверяет обработку некорректного JSON."""
        response = BytesIO(b"invalid json")

        with patch(
            "src.dependencies.fetcher.urlopen",
            return_value=response,
        ):
            with self.assertRaisesRegex(ValueError, "JSON"):
                fetch_metadata(TEST_URL)


class TestExtractDependencies(unittest.TestCase):
    """Проверки извлечения прямых зависимостей."""

    def test_extract_dependencies(self):
        """Проверяет извлечение списка зависимостей."""
        metadata = {
            "info": {
                "requires_dist": [
                    "requests>=2.0",
                    "flask>=3.0",
                ]
            }
        }

        result = extract_direct_dependencies(metadata)

        self.assertEqual(
            result,
            ["requests>=2.0", "flask>=3.0"],
        )

    def test_empty_dependencies(self):
        """Проверяет пакет без зависимостей."""
        metadata = {"info": {"requires_dist": None}}

        result = extract_direct_dependencies(metadata)

        self.assertEqual(result, [])

    def test_exclude_optional_dependencies(self):
        """Исключает зависимости для дополнительных extras."""
        metadata = {
            "info": {
                "requires_dist": [
                    "requests>=2.0",
                    "pytest>=7.0; extra == 'test'",
                ]
            }
        }

        result = extract_direct_dependencies(metadata)

        self.assertEqual(result, ["requests>=2.0"])

    def test_preserve_environment_markers(self):
        """Сохраняет условия совместимости зависимостей."""
        dependency = "colorama>=0.4; sys_platform == 'win32'"
        metadata = {
            "info": {
                "requires_dist": [dependency]
            }
        }

        result = extract_direct_dependencies(metadata)

        self.assertEqual(result, [dependency])

    def test_missing_info(self):
        """Проверяет отсутствие раздела info."""
        with self.assertRaisesRegex(ValueError, "info"):
            extract_direct_dependencies({})

    def test_invalid_requirements_format(self):
        """Проверяет неверный формат списка зависимостей."""
        metadata = {"info": {"requires_dist": "requests"}}

        with self.assertRaisesRegex(ValueError, "формат"):
            extract_direct_dependencies(metadata)


if __name__ == "__main__":
    unittest.main()
