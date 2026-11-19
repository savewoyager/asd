
import unittest

from src.dependencies.graph import (
    build_dependency_graph,
    invert_dependency_graph,
)
from src.dependencies.test_repository import load_test_repository
FULL_GRAPH_DEPTH = 10

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
            max_depth=FULL_GRAPH_DEPTH,
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


    def test_invert_graph(self):
        """Проверяет изменение направления рёбер."""
        reverse_graph = invert_dependency_graph(self.repository)

        expected_graph = {
            "A": [],
            "B": ["A", "F"],
            "C": ["A"],
            "D": ["B", "C"],
            "E": ["C"],
            "F": ["D"],
            "G": [],
        }

        self.assertEqual(reverse_graph, expected_graph)

    def test_reverse_dependencies(self):
        """Проверяет поиск обратных зависимостей."""
        reverse_graph = invert_dependency_graph(self.repository)

        graph, cycles = build_dependency_graph(
            "D",
            reverse_graph.get,
            max_depth=FULL_GRAPH_DEPTH,
        )

        expected_graph = {
            "D": ["B", "C"],
            "B": ["A", "F"],
            "A": [],
            "F": ["D"],
            "C": ["A"],
        }

        self.assertEqual(graph, expected_graph)
        self.assertEqual(cycles, [["D", "B", "F", "D"]])

    def test_reverse_dependencies_from_b(self):
        """Проверяет обратный обход от пакета B."""
        reverse_graph = invert_dependency_graph(self.repository)

        graph, cycles = build_dependency_graph(
            "B",
            reverse_graph.get,
            max_depth=FULL_GRAPH_DEPTH,
        )

        self.assertEqual(
            set(graph),
            {"A", "B", "C", "D", "F"},
        )
        self.assertEqual(cycles, [["B", "F", "D", "B"]])

    def test_reverse_maximum_depth(self):
        """Проверяет ограничение глубины обратного обхода."""
        reverse_graph = invert_dependency_graph(self.repository)

        graph, cycles = build_dependency_graph(
            "D",
            reverse_graph.get,
            max_depth=LIMITED_DEPTH,
        )

        self.assertEqual(set(graph), {"D", "B", "C"})
        self.assertEqual(cycles, [])

    def test_reverse_package_without_dependents(self):
        """Проверяет пакет без обратных зависимостей."""
        reverse_graph = invert_dependency_graph(self.repository)

        graph, cycles = build_dependency_graph(
            "G",
            reverse_graph.get,
            max_depth=LIMITED_DEPTH,
        )

        self.assertEqual(graph, {"G": []})
        self.assertEqual(cycles, [])

if __name__ == "__main__":
    unittest.main()
