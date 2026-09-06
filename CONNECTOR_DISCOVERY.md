# Airbyte Connector — Connector Discovery

**Official Documentation:** https://airbyte.com  
**Base URL:** https://api.airbyte.com/v1  
**Auth Model:** Bearer Token / Client Credentials  

## Основные сущности вендора
- источники (/sources), приемники (/destinations), соединения (/connections), задания репликации (/jobs)

## Лимиты и особенности API
- Соблюдение Rate Limits вендора, обработка HTTP 429 с экспоненциальным backoff.
- Валидация входных данных по Pydantic-схемам вендора до отправки запроса.
- Тестовая точка проверки подключения: `GET /v1/workspaces`.
