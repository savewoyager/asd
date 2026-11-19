
import sys

from src.config.config import parse_config
from src.dependencies.fetcher import get_direct_dependencies


def main():
    """Запускает программу и выводит прямые зависимости пакета."""
    config = parse_config()

    print("\n========== CONFIGURATION ==========")
    print(f"package: {config.package}")
    print(f"repo: {config.repo}")
    print(f"test_mode: {config.test_mode}")
    print(f"output: {config.output}")
    print(f"ascii: {config.ascii}")
    print(f"max_depth: {config.max_depth}")
    print("==================================")

    try:
        dependencies = get_direct_dependencies(config.repo)
    except ValueError as error:
        print(f"\nОшибка получения зависимостей: {error}", file=sys.stderr)
        return 1

    print(f"\nПрямые зависимости пакета {config.package}:")

    if not dependencies:
        print("Прямые зависимости не найдены.")
    else:
        for dependency in dependencies:
            print(f"- {dependency}")

    print(f"\nВсего зависимостей: {len(dependencies)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
