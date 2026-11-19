
import json
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REQUEST_TIMEOUT = 10
USER_AGENT = "DependencyVisualizer/1.0"

REQUIREMENT_PATTERN = re.compile(
    r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)"
)

OPTIONAL_EXTRA_PATTERN = re.compile(
    r"\bextra\s*==\s*(['\"])[^'\"]+\1",
    re.IGNORECASE,
)


def fetch_metadata(repo_url):
    """Получает JSON-метаданные пакета из репозитория."""
    request = Request(
        repo_url,
        headers={"User-Agent": USER_AGENT},
    )

    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            content = response.read().decode("utf-8")
    except HTTPError as error:
        raise ValueError(
            f"Ошибка HTTP: {error.code}"
        ) from error
    except URLError as error:
        raise ValueError(
            f"Не удалось подключиться к репозиторию: {error.reason}"
        ) from error
    except TimeoutError as error:
        raise ValueError(
            "Время ожидания ответа от репозитория истекло."
        ) from error

    try:
        return json.loads(content)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Репозиторий вернул некорректный JSON."
        ) from error


def extract_direct_dependencies(metadata):
    """Извлекает прямые обязательные зависимости из метаданных."""
    try:
        info = metadata["info"]
    except (KeyError, TypeError) as error:
        raise ValueError(
            "В ответе отсутствует раздел info."
        ) from error

    requirements = info.get("requires_dist") or []

    if not isinstance(requirements, list):
        raise ValueError(
            "Поле requires_dist имеет неверный формат."
        )

    dependencies = []

    for requirement in requirements:
        if not isinstance(requirement, str):
            continue

        marker = requirement.partition(";")[2]

        if OPTIONAL_EXTRA_PATTERN.search(marker):
            continue

        if not REQUIREMENT_PATTERN.match(requirement):
            raise ValueError(
                f"Некорректная запись зависимости: {requirement}"
            )

        dependencies.append(requirement.strip())

    return dependencies


def get_direct_dependencies(repo_url):
    """Получает список прямых зависимостей пакета."""
    metadata = fetch_metadata(repo_url)
    return extract_direct_dependencies(metadata)
