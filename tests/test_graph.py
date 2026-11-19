
import unittest

from src.dependencies.graph import build_dependency_graph
from src.dependencies.test_repository import load_test_repository


TEST_REPOSITORY = "tests/fixtures/repository.json"
ROOT_PACKAGE = "A"
LIMITED_DEPTH = 1


class TestDependencyGraph(unittest.TestCase):
    """Проверки построения графа зависимостей."""

    @classmethod
    def setUpClass(cls):
        """Загружает тестовый репозиторий перед тестами."""
        cls.repository = load_test_repository(TEST_REPOSITORY)

    def test_complete_graph(self):
        """Проверяет полный обход графа."""
        graph, cycles = build_dependency_graph(
            ROOT_PACKAGE,
            self.repository.get,
            max_depth=10,
        )

        self.assertEqual(set(graph), {"A", "B", "C", "D", "E", "F"})
        self.assertEqual(cycles, [["B", "D", "F", "B"]])

    def test_maximum_depth(self):
        """Проверяет ограничение глубины обхода."""
        graph, cycles = build_dependency_graph(
            ROOT_PACKAGE,
            self.repository.get,
            max_depth=LIMITED_DEPTH,
        )

        self.assertEqual(set(graph), {"A", "B", "C"})
        self.assertEqual(graph["B"], [])
        self.assertEqual(graph["C"], [])
        self.assertEqual(cycles, [])

    def test_package_without_dependencies(self):
        """Проверяет пакет без зависимостей."""
        graph, cycles = build_dependency_graph(
            "G",
            self.repository.get,
            max_depth=LIMITED_DEPTH,
        )

        self.assertEqual(graph, {"G": []})
        self.assertEqual(cycles, [])

    def test_shared_dependency(self):
        """Проверяет повторное обнаружение общей зависимости."""
        graph, cycles = build_dependency_graph(
            ROOT_PACKAGE,
            self.repository.get,
            max_depth=10,
        )

        self.assertEqual(graph["B"], ["D"])
        self.assertEqual(graph["C"], ["D", "E"])
        self.assertEqual(cycles, [["B", "D", "F", "B"]])


if __name__ == "__main__":
    unittest.main()
