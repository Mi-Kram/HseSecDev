# ВШЭ Разработка Безопасного ПО
| Студент | Крамаренко Михаил |
|:--|:--|
| Группа  | 234 |

[**Отчёт за модуль 1**](https://github.com/hse-secdev-2025-fall/course-project-Mi-Kram/blob/main/docs/reports/report_module1.pdf)

# Содержание

1. [**Стабильный CI (зелёные прогоны)**](#HEADER-01)
2. [**Сборка/тесты/артефакты**](#HEADER-02)
3. [**Секреты вынесены из кода**](#HEADER-03)
4. [**PR-политика и ревью по чек-листу**](#HEADER-04)
5. [**Воспроизводимый локальный запуск (Docker/compose)**](#HEADER-05)
6. [**Кэш/матрица, отчёты покрытия, релизные артефакты**](#6)
7. [**Итоговая оценка по чек-листу**](#HEADER-FINAL)

<h1 id="HEADER-01">Стабильный CI (зелёные прогоны)</h1>

В ветку `main` мержатся только ветки, чей последний коммит успешно прошёл CI (зелёный прогон). 

- [Коммиты старого репозитория](https://github.com/hse-secdev-2025-fall/course-project-Mi-Kram/commits/main/)
- [Коммиты нового репозитория](https://github.com/Mi-Kram/HseSecDev/commits/main/)


<h1 id="HEADER-02">Сборка/тесты/артефакты</h1>

[CI файл](https://github.com/Mi-Kram/HseSecDev/blob/main/.github/workflows/ci.yml)

Процесс CI включает в себя:
1. Сборка: устанавливаются необходимые зависимости, настраивается окружение.
2. Тесты: успешный запуск:
   - `ruff check .`
   - `black .`
   - `isort .`
   - `pytest -q`
   - `pre-commit run --all-files`
3. Артефакты: [Ссылка на CI с артефактами](https://github.com/Mi-Kram/HseSecDev/actions/runs/19821247651).


<h1 id="HEADER-03">Секреты вынесены из кода</h1>

- [Pull Reuest](https://github.com/Mi-Kram/HseSecDev/pull/2#user-content-secrets-and-configs)
c картинкой, в котором добавлены и продемонстрированы эти изменения


<h1 id="HEADER-04">PR-политика и ревью по чек-листу</h1>

1. Запрещены прямые `push` в ветку `main`. Изменения вносятся через `Pull Request`.
2. Разработка ведётся в рабочих ветках, после чего создаётся `Pull Request` в `main`.
3. `Pull Request` проходит CI, что включает сборку и тесты.
4. Для `Pull Request` добавлены `CODEOWNERS` и `pull_request_template.md`.
5. Внизу всегда присутствует `Check List Review`.


<h1 id="HEADER-05">Воспроизводимый локальный запуск (Docker/compose)</h1>

- [Pull Reuest](https://github.com/Mi-Kram/HseSecDev/pull/1),
в котором добавлены и продемонстрированы эти изменения


<h1 id="HEADER-06">Кэш/матрица, отчёты покрытия, релизные артефакты</h1>

- [CI файл](https://github.com/Mi-Kram/HseSecDev/blob/main/.github/workflows/ci.yml)
- [Pull Reuest](https://github.com/Mi-Kram/HseSecDev/pull/2),
в котором добавлены и продемонстрированы эти изменения
- Также, в этом [`Pull Reuest`](https://github.com/Mi-Kram/HseSecDev/pull/2#user-content-cd-promotion) продемонмтрирован CD: push docker образа на Docker Hub.


<h1 id="HEADER-FINAL">Итоговая оценка по чек-листу</h1>

| Критерий | Балл | Обоснование
|:--|:--:|:--|
| Стабильный CI (зелёные прогоны) | ✅ 2/2 | Полностью успешное прохождение CI в ветке `main` |
| Сборка/тесты/артефакты | ✅ 2/2 | Сборка (docker) + автотесты + артефакты |
| Секреты вынесены из кода | ✅ 2/2 | `GitHub Secrets/Vars` |
| PR-политика и ревью по чек-листу | ✅ 2/2 | нет пушей в `main` + `PR` проходит `CI` + `Check List Review` |
| Воспроизводимый локальный запуск (Docker/compose) | ✅ 2/2 | `Docker Compose` успешно поднимает контейнер приложения и базы данных |
| Кэш/матрица, отчёты покрытия, релизные артефакты | ✅ 2/2 | Кеш + матрица + автотесты + фртефакты |

