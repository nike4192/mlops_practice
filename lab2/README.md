# Лабораторная работа №2 — CI/CD пайплайн для ML на Docker + GitLab

Замена Jenkins-варианта на **локальный GitLab + Docker**. Студент разворачивает у себя GitLab, регистрирует runner, собирает свой ML-пайплайн в `.gitlab-ci.yml` и прогоняет его в CI.

> **Что в этой папке — шаблон, а не готовое решение.**
> ML-скрипты (`data_collection.py`, `data_preprocessing.py`, `model_training.py`, `model_testing.py`) пишете вы сами по требованиям модуля 2 (см. корневой `README.md`). Они опираются на скрипты из lab1, которые уже у вас есть.
>
> Из коробки даны: инфраструктура локального GitLab (`gitlab-compose.yml`), линтер `.gitlab-ci.yml` (`ci_lint.py`), и пример каркаса пайплайна (`.gitlab-ci.yml`, `Dockerfile`, `requirements.txt`) — адаптируйте под свой набор скриптов.

---

## Требования к пайплайну (что сдаётся)

В вашем `.gitlab-ci.yml` должны быть **минимум 3 обязательных стейджа** — это проверяет линтер `ci_lint.py`:

| Stage | Что должно происходить | Артефакт (рекомендуется) |
|-------|------------------------|--------------------------|
| `prepare-dataset` | Сбор и/или предобработка данных | `data/` |
| `train` | Обучение модели, сериализация в файл | `models/` |
| `test` | Прогон модели на тестовых данных, метрики | `logs/` или stdout |

Дополнительно полезно вынести `lint` в отдельный первый stage и подключить `ci_lint.py`, чтобы CI падал при сломанной структуре yaml.

---

## Структура папки

```
lab2/
├── README.md                   ← этот файл
├── Dockerfile                  ← пример образа python:3.12-slim + зависимости
├── .dockerignore
├── .gitignore                  ← исключает data/, logs/, models/
├── .gitlab-ci.yml              ← пример пайплайна: lint → prepare-dataset → train → test
├── gitlab-compose.yml          ← локальный GitLab + Runner (НЕ часть проекта-лабы!)
├── requirements.txt            ← минимальный набор зависимостей (расширьте)
└── ci_lint.py                  ← линтер .gitlab-ci.yml (обязательная часть сдачи)
```

---

## Локальный прогон без GitLab (опционально)

Когда напишете свои скрипты — можно проверить пайплайн локально через Docker, без поднятия GitLab:

```bash
cd lab2
docker build -t lab2 .
docker run --rm -v "$(pwd)/_run:/app/_run" -w /app/_run lab2 bash -c "
  python /app/data_collection.py &&
  python /app/data_preprocessing.py &&
  python /app/model_training.py &&
  python /app/model_testing.py
"
```

Если всё отрабатывает — переходите к запуску в локальном GitLab.

---

# Запуск в локальном GitLab — основной путь сдачи

> **Нужен Docker.** Если ещё не установлен:
> [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS) или
> `sudo apt install docker.io docker-compose-v2` (Ubuntu/Debian).
> Проверить: `docker --version && docker compose version`.
>
> **Потребуется ~4 ГБ RAM** для GitLab. Закройте тяжёлые приложения.

## Шаг 1. Поднять локальный GitLab

Скопируйте `gitlab-compose.yml` в **отдельную папку** (НЕ внутрь проекта-лабы), например `~/gitlab-local/`:

```bash
mkdir -p ~/gitlab-local && cp gitlab-compose.yml ~/gitlab-local/
cd ~/gitlab-local
```

Добавьте локальный домен `gitlab.local` в hosts (один раз):

```bash
# Linux / macOS:
sudo sh -c 'echo "127.0.0.1 gitlab.local" >> /etc/hosts'
# Windows: открыть от админа C:\Windows\System32\drivers\etc\hosts и добавить ту же строку
```

Запустите:

```bash
docker compose -f gitlab-compose.yml up -d
docker compose -f gitlab-compose.yml logs -f gitlab
```

Ждите ~5 минут до строки `gitlab Reconfigured!`. Потом Ctrl+C — это просто выйдет из логов, GitLab продолжит работу.

Откройте http://gitlab.local:8929. Должен открыться экран входа.

![SCREENSHOT-01-login-page](screenshots/01-gitlab-login-page.png)

## Шаг 2. Войти как root

- **Логин:** `root`
- **Пароль:** `ChangeMe-2026!` (задан в `gitlab-compose.yml`)

После входа вы окажетесь на главной странице GitLab.

![SCREENSHOT-02-after-login](screenshots/02-gitlab-main-page.png)

## Шаг 3. Создать новый проект

Меню слева → **Projects** → **New project** → **Create blank project**.

- Project name: `lab2-mlops`
- Visibility: **Private** (или Internal — не Public)
- **Снимите галку** «Initialize repository with a README» — мы зальём свои файлы.

Нажмите **Create project**.

![SCREENSHOT-03-new-project-form](screenshots/03-new-project-form.png)

После создания GitLab покажет страницу проекта с инструкциями по push кода. Запомните URL вида `http://gitlab.local:8929/root/lab2-mlops.git`.

![SCREENSHOT-04-empty-project](screenshots/04-empty-project-page.png)

## Шаг 4. Зарегистрировать GitLab Runner

Runner — это процесс, который выполняет ваши job'ы. Он уже запущен в Docker (см. `gitlab-compose.yml`), но его нужно «привязать» к проекту.

### 4.1. Получить registration token

В вашем проекте: **Settings** (внизу слева) → **CI/CD** → секция **Runners** → **New project runner**.

![SCREENSHOT-05-runners-section](screenshots/05-settings-cicd-runners.png)

Заполните форму:
- **Tags:** `docker` (одна метка, важно для соответствия с `.gitlab-ci.yml`)
- **Run untagged jobs:** ✓ включить
- остальное — по умолчанию

Нажмите **Create runner**. GitLab покажет токен вида `glrt-xxxxxxxxxx` — **скопируйте его**.

![SCREENSHOT-06-runner-token](screenshots/06-runner-token.png)

### 4.2. Зарегистрировать runner-контейнер

В терминале (там же, где `gitlab-compose.yml`):

```bash
docker exec -it gitlab-runner gitlab-runner register \
  --non-interactive \
  --url http://gitlab.local:8929/ \
  --token <ВАША_ТОКЕН_ИЗ_GITLAB> \
  --executor docker \
  --docker-image python:3.12-slim \
  --description "local-docker-runner" \
  --docker-network-mode gitlab-net
```

> `--docker-network-mode gitlab-net` важен — без него спавненные runner'ом контейнеры не смогут достучаться до `gitlab.local`.

Перезагрузите страницу Runners в GitLab — runner должен появиться со статусом «online» (зелёный кружок).

![SCREENSHOT-07-runner-online](screenshots/07-runner-online.png)

## Шаг 5. Залить код в проект

Подготовьте папку с вашим вариантом lab2: ваши ML-скрипты + адаптированный `.gitlab-ci.yml` + `ci_lint.py` + `Dockerfile` + `requirements.txt`. **Не кладите** туда `gitlab-compose.yml` — это инфраструктура, не часть проекта.

Инициализируйте git и push:

```bash
cd /путь/к/вашему/lab2
git init -b main
git add .
git commit -m "lab2: initial pipeline"
git remote add origin http://root@gitlab.local:8929/root/lab2-mlops.git
git push -u origin main
# Пароль при push — тот же ChangeMe-2026!
```

GitLab сразу запустит pipeline. Перейдите в проект → **Build** → **Pipelines**.

![SCREENSHOT-08-pipeline-running](screenshots/08-pipeline-running.png)

## Шаг 6. Проверить результаты

Дождитесь завершения всех стейджей (~2-3 минуты на первом прогоне из-за `pip install`). Все должны быть зелёными:

![SCREENSHOT-09-pipeline-success](screenshots/09-pipeline-all-green.png)

Кликните на job `test` → справа **Job artifacts** → **Browse** — увидите файлы артефактов (например, `logs/`, `models/`):

![SCREENSHOT-10-test-job-log](screenshots/10-test-job-log.png)
![SCREENSHOT-11-artifacts-browse](screenshots/11-artifacts-browse.png)

---

## Линтер `.gitlab-ci.yml`

`ci_lint.py` проверяет, что в `.gitlab-ci.yml`:
1. объявлены обязательные стейджи: `prepare-dataset`, `train`, `test`;
2. в каждом из них есть хотя бы один job.

Запуск отдельно от CI:

```bash
pip install pyyaml
python ci_lint.py .gitlab-ci.yml
```

Exit code: `0` — порядок, `1` — нарушения. В CI линтер запускается первым stage (`lint`) и валит сборку, если структура неправильная.

**Демо-сломайте** — удалите строку `- test` из секции `stages:` в `.gitlab-ci.yml`, закоммитьте и запушьте — увидите красный stage `lint`:

![SCREENSHOT-12-lint-failed](screenshots/12-lint-failed-pipeline.png)

---

## Каркас `.gitlab-ci.yml` — что в каком stage

| Stage | Что | Артефакты (пример) |
|-------|-----|--------------------|
| `lint` | Валидация структуры YAML — `python ci_lint.py` | — |
| `prepare-dataset` | Сбор + предобработка данных | `data/` |
| `train` | Обучение модели | `models/` |
| `test` | Метрики и отчёт | `logs/` |

`needs:` между job'ами выстраивает DAG, поэтому `train` дожидается `prepare-dataset`, `test` — обоих.

---

## Если что-то пошло не так

| Проблема | Решение |
|----------|---------|
| GitLab не открывается на 8929 | Подождите ещё минуту, GitLab инициализируется до 5 мин на первом старте |
| `Could not resolve host: gitlab.local` | Не добавлена строка в `/etc/hosts`, см. Шаг 1 |
| Runner offline в UI | Проверьте `docker logs gitlab-runner`. Часто — забыли `--docker-network-mode gitlab-net` |
| Job упал на `pip install` | Может тормозить сеть к pypi; перезапустите job (Retry) |
| Push спрашивает пароль и не принимает | Используйте логин `root` и пароль `ChangeMe-2026!` (можно поменять в Settings → Profile) |
| Линтер падает локально, а в CI ок (или наоборот) | Скрипт читает yaml как текст; убедитесь, что коммитите тот же файл, который проверяете локально |

---

## Сворачивание окружения

```bash
cd ~/gitlab-local
docker compose -f gitlab-compose.yml down          # выключить
docker compose -f gitlab-compose.yml down -v       # выключить и удалить ВСЕ данные GitLab
```
