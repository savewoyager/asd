
import unittest

from src.config.config import (
    DEFAULT_MAX_DEPTH,
    parse_config,
)
from src.config.config import parse_config


class TestConfig(unittest.TestCase):

    def test_default_values(self):
        config = parse_config([
            "--package", "flask",
            "--repo", "https://pypi.org/pypi/flask/json"
        ])

        self.assertEqual(config.package, "flask")
        self.assertEqual(config.test_mode, False)
        self.assertEqual(config.output, "graph.png")
        self.assertEqual(config.ascii, False)
        self.assertEqual(config.max_depth, DEFAULT_MAX_DEPTH)

    def test_all_parameters(self):
        config = parse_config([
            "--package", "requests",
            "--repo", "https://pypi.org/pypi/requests/json",
            "--test-mode", "false",
            "--output", "result.png",
            "--ascii",
            "--max-depth", "3"
        ])

        self.assertEqual(config.package, "requests")
        self.assertEqual(config.output, "result.png")
        self.assertTrue(config.ascii)
        self.assertEqual(config.max_depth, 3)

    def test_invalid_package(self):
        with self.assertRaises(SystemExit):
            parse_config([
                "--package", "bad package!",
                "--repo", "https://pypi.org"
            ])

    def test_empty_repo(self):
        with self.assertRaises(SystemExit):
            parse_config([
                "--package", "flask",
                "--repo", ""
            ])

    def test_invalid_test_mode(self):
        with self.assertRaises(SystemExit):
            parse_config([
                "--package", "flask",
                "--repo", "https://pypi.org",
                "--test-mode", "yes"
            ])

    def test_invalid_output(self):
        with self.assertRaises(SystemExit):
            parse_config([
                "--package", "flask",
                "--repo", "https://pypi.org",
                "--output", "graph.txt"
            ])

    def test_invalid_depth(self):
        with self.assertRaises(SystemExit):
            parse_config([
                "--package", "flask",
                "--repo", "https://pypi.org",
                "--max-depth", "-1"
            ])

    def test_invalid_url(self):
        with self.assertRaises(SystemExit):
            parse_config([
                "--package", "flask",
                "--repo", "invalid_url"
            ])


if __name__ == "__main__":
    unittest.main()
