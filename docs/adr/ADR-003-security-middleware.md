# ADR-003: Security Headers and Middleware
Дата: 2025-01-19
Статус: Accepted

## Context

Текущая реализация Wish List Service имеет базовую middleware для ограничения размера запросов, но отсутствуют важные security заголовки и защитные механизмы:

- Отсутствуют security headers (HSTS, CSP, X-Frame-Options, etc.)
- Нет rate limiting для защиты от DDoS атак
- Отсутствует CORS конфигурация
- Нет защиты от clickjacking и XSS
- Отсутствует логирование security событий

Это создает риски:
- R4: DDoS атаки через отсутствие rate limiting
- R7: Переполнение памяти через большие запросы
- F1-D: Denial of Service атаки
- F1-I: Information Disclosure через отсутствие security headers

## Decision

Реализовать комплексную security middleware систему:

1. **Security Headers Middleware**:
   - `Strict-Transport-Security` для принуждения HTTPS
   - `Content-Security-Policy` для предотвращения XSS
   - `X-Frame-Options` для защиты от clickjacking
   - `X-Content-Type-Options` для предотвращения MIME sniffing
   - `Referrer-Policy` для контроля referrer информации

2. **Rate Limiting Middleware**:
   - Ограничение запросов по IP (100 req/min)
   - Ограничение по endpoint (50 req/min для POST)
   - Sliding window алгоритм для точного контроля

3. **CORS Middleware**:
   - Ограничение origins только для доверенных доменов
   - Контроль методов и заголовков
   - Настройка credentials policy

4. **Security Logging Middleware**:
   - Логирование подозрительной активности
   - Трекинг rate limit violations
   - Мониторинг больших запросов

## Alternatives

### Альтернатива 1: Только базовые заголовки (отклонена)
- **Плюсы**: Простота реализации
- **Минусы**: Недостаточная защита от современных атак

### Альтернатива 2: Внешний reverse proxy (отклонена)
- **Плюсы**: Вынос security логики из приложения
- **Минусы**: Дополнительная инфраструктура, сложность настройки

### Альтернатива 3: Комплексная middleware система (принята)
- **Плюсы**: Полный контроль, интеграция с приложением
- **Минусы**: Больше кода для поддержки

## Consequences

### Положительные:
- **Безопасность**: Значительное повышение уровня защиты
- **Соответствие стандартам**: Реализация OWASP рекомендаций
- **Мониторинг**: Улучшенная видимость security событий
- **Производительность**: Защита от перегрузки системы

### Отрицательные:
- **Сложность**: Больше middleware для настройки и поддержки
- **Производительность**: Небольшое увеличение latency на каждый запрос
- **Конфигурация**: Необходимость настройки security политик

### Влияние на производительность:
- Ожидаемое увеличение latency на 2-5ms на запрос
- Дополнительная нагрузка на память для rate limiting кэша

## Security Impact

- **NFR-05**: Защита от перегрузки через rate limiting
- **NFR-07**: Предотвращение XSS через CSP заголовки
- **R4**: Снижение риска DDoS атак
- **R7**: Защита от переполнения памяти
- **F1-D**: Защита от Denial of Service
- **F1-I**: Предотвращение утечки информации через заголовки

## Rollout Plan

1. **Этап 1**: Реализовать Security Headers Middleware
2. **Этап 2**: Добавить Rate Limiting Middleware
3. **Этап 3**: Настроить CORS Middleware
4. **Этап 4**: Реализовать Security Logging
5. **Этап 5**: Добавить тесты и мониторинг
6. **Этап 6**: Обновить документацию

## Links

- NFR-05 (защита от перегрузки)
- NFR-07 (защита от XSS)
- R4, R7 (риски DDoS и переполнения памяти)
- F1-D, F1-I (угрозы DoS и Information Disclosure)
- tests/test_security_middleware.py::test_security_headers
- tests/test_security_middleware.py::test_rate_limiting
- tests/test_security_middleware.py::test_cors_configuration
