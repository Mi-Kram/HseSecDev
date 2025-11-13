# DFD — Data Flow Diagram для Wish List Service

## Диаграмма (Mermaid)
```mermaid
flowchart LR
  U[User/Client] -->|F1: HTTPS| API[FastAPI App]
  subgraph Edge[Trust Boundary: Edge]
    API --> CTRL[Wish List Controller]
    CTRL --> SVC[WishListService]
  end
  subgraph Core[Trust Boundary: Core]
    SVC --> WISH_STORE[(WishListMemoryStorage)]
    SVC --> NOTE_STORE[(WishNotesMemoryStorage)]
  end

  %% Trust boundaries styling
  style Edge stroke:#ff6b6b,stroke-width:3px,stroke-dasharray: 5 5
  style Core stroke:#4ecdc4,stroke-width:3px,stroke-dasharray: 5 5
  style API stroke:#45b7d1,stroke-width:2px
  style SVC stroke:#96ceb4,stroke-width:2px
```

## Список потоков
| ID | Откуда → Куда | Канал/Протокол | Данные/PII | Комментарий |
|----|---------------|-----------------|------------|-------------|
| F1 | U → API | HTTPS | JSON requests/responses | Основной API трафик |
| F2 | API → CTRL | Internal call | Request objects | Маршрутизация запросов |
| F3 | CTRL → SVC | Internal call | Domain models | Бизнес-логика |
| F4 | SVC → WISH_STORE | Internal call | WishList entities | CRUD операции wish list |
| F5 | SVC → NOTE_STORE | Internal call | WishNote entities | CRUD операции заметок |
| F6 | WISH_STORE → SVC | Internal call | WishList data | Возврат данных |
| F7 | NOTE_STORE → SVC | Internal call | WishNote data | Возврат данных |
| F8 | SVC → CTRL | Internal call | Response objects | Результаты обработки |
| F9 | CTRL → API | Internal call | HTTP responses | Формирование ответов |
| F10 | API → U | HTTPS | JSON responses | Ответы клиенту |

## Компоненты системы
- **User/Client**: Внешний пользователь, взаимодействующий с системой
- **FastAPI App**: Веб-приложение на FastAPI
- **Wish List Controller**: Контроллер для обработки HTTP запросов
- **WishListService**: Сервисный слой с бизнес-логикой
- **WishListMemoryStorage**: Хранилище списков желаний в памяти
- **WishNotesMemoryStorage**: Хранилище заметок в памяти

## Trust Boundaries
- **Edge Boundary**: Граница между внешним миром и внутренней системой
- **Core Boundary**: Граница между сервисным слоем и слоем данных
