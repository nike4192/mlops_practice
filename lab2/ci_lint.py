"""Линтер .gitlab-ci.yml — проверяет наличие обязательных стейджей и job'ов.

Использование:
    python ci_lint.py [path_to_gitlab_ci_yml]

По умолчанию проверяет .gitlab-ci.yml в текущей директории.

Exit codes:
    0 — всё в порядке
    1 — нарушения структуры
    2 — отсутствует PyYAML или файл не читается
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ОШИБКА: PyYAML не установлен. Установите: pip install pyyaml")
    sys.exit(2)


REQUIRED_STAGES = ["prepare-dataset", "train", "test"]
RESERVED_KEYS = {"stages", "default", "variables", "cache", "include", "workflow", "image", "services"}


def lint(yaml_path: Path) -> int:
    if not yaml_path.exists():
        print(f"✗ Файл не найден: {yaml_path}")
        return 1

    with yaml_path.open("r", encoding="utf-8") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"✗ Невалидный YAML: {e}")
            return 1

    if not isinstance(config, dict):
        print("✗ Корень .gitlab-ci.yml должен быть mapping")
        return 1

    print(f"=== Линтер {yaml_path} ===\n")

    stages = config.get("stages", [])
    print(f"Объявленные стейджи: {stages}")
    print(f"Обязательные:        {REQUIRED_STAGES}\n")

    errors = 0

    missing = [s for s in REQUIRED_STAGES if s not in stages]
    if missing:
        print(f"✗ Отсутствуют обязательные стейджи: {missing}")
        errors += 1
    else:
        print("✓ Все обязательные стейджи объявлены в `stages:`")

    jobs_by_stage: dict[str, list[str]] = {}
    for key, value in config.items():
        if key in RESERVED_KEYS or key.startswith("."):
            continue
        if not isinstance(value, dict):
            continue
        stage = value.get("stage")
        if stage:
            jobs_by_stage.setdefault(stage, []).append(key)

    print("\nJob'ы по стейджам:")
    for stage in REQUIRED_STAGES:
        jobs = jobs_by_stage.get(stage, [])
        if jobs:
            print(f"  ✓ {stage}: {jobs}")
        else:
            print(f"  ✗ {stage}: нет ни одного job")
            errors += 1

    print()
    if errors:
        print(f"✗ Линтер нашёл проблем: {errors}")
        return 1

    print("✓ Структура .gitlab-ci.yml в порядке")
    return 0


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".gitlab-ci.yml")
    sys.exit(lint(target))
