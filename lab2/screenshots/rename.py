"""Переименование сырых скриншотов в имена SHOTLIST.

Запуск:
    python rename.py

Просто копирует исходники под целевыми именами (без аннотаций — описания
«куда смотреть» лежат в README рядом с каждой картинкой).
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).parent

MAPPING = {
    "Screenshot from 2026-04-28 18-55-01.png": "01-gitlab-login-page.png",
    "Screenshot from 2026-04-28 18-56-49.png": "02-gitlab-main-page.png",
    "Screenshot from 2026-04-28 18-59-26.png": "03-new-project-form.png",
    "Screenshot from 2026-04-28 18-59-41.png": "04-empty-project-page.png",
    "Screenshot from 2026-04-28 19-08-19.png": "05-settings-cicd-runners.png",
    "Screenshot from 2026-04-28 19-10-40.png": "06-runner-token.png",
    "Screenshot from 2026-04-28 19-12-32.png": "07-runner-online.png",
    "Screenshot from 2026-04-28 19-26-40.png": "09-pipeline-all-green.png",
    "Screenshot from 2026-04-28 19-27-13.png": "10-test-job-log.png",
    "Screenshot from 2026-04-28 19-29-27.png": "11-artifacts-browse.png",
    "Screenshot from 2026-04-28 19-32-44.png": "12-lint-failed-pipeline.png",
    "Screenshot from 2026-04-28 19-32-53.png": "12b-lint-job-log.png",
}


def main():
    for src, dst in MAPPING.items():
        src_p = ROOT / src
        dst_p = ROOT / dst
        if not src_p.exists():
            print(f"  ! {src} — отсутствует, пропускаю")
            continue
        shutil.copy2(src_p, dst_p)
        print(f"  ✓ {dst}")
    print("Готово.")


if __name__ == "__main__":
    main()
