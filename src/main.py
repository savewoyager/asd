
from src.config.config import parse_config


def main():
    config = parse_config()

    print("\n========== CONFIGURATION ==========")

    print(f"package: {config.package}")
    print(f"repo: {config.repo}")
    print(f"test_mode: {config.test_mode}")
    print(f"output: {config.output}")
    print(f"ascii: {config.ascii}")
    print(f"max_depth: {config.max_depth}")

    print("==================================")

    print("\nConfiguration loaded successfully!")


if __name__ == "__main__":
    main()
