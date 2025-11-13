# Wishlist

Создание и редактирование списков желаний

## Быстрый старт
```bash
# Production
docker compose --env-file .env --profile prod up -d --build
# Development
docker compose --env-file .env.dev --profile dev up -d --build
```

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
pre-commit install --hook-type pre-push
uvicorn src.app.main:app --reload
```

## Ритуал перед PR
```bash
ruff check --fix .
black .
isort .
pytest -q
pre-commit run --all-files
```

## CI
В репозитории настроен workflow **CI** (GitHub Actions) — required check для `main`.
Badge добавится автоматически после загрузки шаблона в GitHub.

## Контейнеры
```bash
docker build -t secdev-app .
docker run --rm -p 8000:8000 secdev-app
# или
docker compose up --build
```

## Эндпойнты
- `GET /health` → `{"status": "ok"}`
- `GET: /wishes?price=5` - списки желаний с опциональной фильтрацией по цене;
- `GET: /wishes/5` - подробные данные и списке желаний;
- `GET: /wishes/user/3` - списки желаний конкретного пользователя;
- `POST: /wishes` - создание нового списка желаний;
- `PUT: /wishes/5` - обновление информации о списке желаний;
- `DELETE: /wishes/5` - удаление списка желаний;
- `POST: /wishes/5/notes` - создание новых позиций в списке желаний;
- `PUT: /wishes/5/notes` - обновление позиций в списке желаний;
- `DELETE: /wishes/5/notes?ids=1&ids=2` - удаление позиций из списка желаний.

## Формат ошибок
Все ошибки — JSON-обёртка:
```json
{
  "error": {"code": "not_found", "message": "item not found"}
}
```

См. также: `SECURITY.md`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`.
