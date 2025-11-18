# Настройка системы Help для Dashboard

## Описание

Система Help теперь хранит ссылки на документацию в базе данных вместо localStorage. Это позволяет централизованно управлять ссылками и синхронизировать их между всеми пользователями.

## Структура API

### Эндпоинт
```
GET/POST/PATCH/DELETE https://dashboard.api4/api_dashboard/help
```

### Структура данных
```json
{
  "id": 1,
  "component": "dashboard",
  "url": "https://dashboard.api4/docs/dashboard"
}
```

### Поля
- `id` - уникальный идентификатор записи (автоинкремент)
- `component` - идентификатор компонента/раздела меню
- `url` - ссылка на документацию

## Компоненты

### 1. Help.vue
Основной компонент для управления ссылками на документацию.

**Функции:**
- Просмотр всех существующих ссылок
- Добавление новых ссылок
- Редактирование существующих ссылок
- Удаление ссылок
- Инициализация базы данных

### 2. HelpInitializer.vue
Компонент для первоначальной настройки базы данных.

**Функции:**
- Создание записей для всех разделов меню
- Обновление существующих записей
- Автоматическое определение иконок для разделов

## Настройка базы данных

### 1. Создание таблицы
```sql
CREATE TABLE help_links (
  id SERIAL PRIMARY KEY,
  component VARCHAR(50) NOT NULL UNIQUE,
  url TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индекс для быстрого поиска по компоненту
CREATE INDEX idx_help_links_component ON help_links(component);
```

### 2. Инициализация данными
```sql
INSERT INTO help_links (component, url) VALUES
('dashboard', 'https://dashboard.api4/docs/dashboard'),
('finance', 'https://dashboard.api4/docs/finance'),
('advertisement', 'https://dashboard.api4/docs/advertisement'),
('seo', 'https://dashboard.api4/docs/seo'),
('seo-top', 'https://dashboard.api4/docs/seo/top'),
('seo-metatags', 'https://dashboard.api4/docs/seo/metatags'),
('seo-metatags-gen', 'https://dashboard.api4/docs/seo/metatags-gen'),
('market', 'https://dashboard.api4/docs/market'),
('cp', 'https://dashboard.api4/docs/cp'),
('projects', 'https://dashboard.api4/docs/projects'),
('settings', 'https://dashboard.api4/docs/settings'),
('currency-rates', 'https://dashboard.api4/docs/currency-rates');
```

## Использование

### 1. Первоначальная настройка
1. Откройте страницу Help (`/help`)
2. Нажмите кнопку "Инициализировать базу данных"
3. Подтвердите создание записей

### 2. Управление ссылками
1. В форме введите:
   - **Компонент**: идентификатор раздела (например, `dashboard`, `finance`)
   - **URL**: ссылка на документацию
2. Нажмите "Добавить" для создания новой записи
3. Используйте кнопки редактирования и удаления для управления
   - **Редактирование**: использует PATCH запрос для обновления существующих записей
   - **Удаление**: использует DELETE запрос для удаления записей

### 3. Автоматическое открытие документации
- Нажмите кнопку Help (значок вопроса) в любом разделе
- Система автоматически найдет соответствующую ссылку в базе данных
- Документация откроется в новой вкладке

## Маппинг путей

Система автоматически сопоставляет пути с компонентами:

| Путь | Компонент |
|------|-----------|
| `/` | `dashboard` |
| `/finance` | `finance` |
| `/advertisement` | `advertisement` |
| `/advertisement/queries` | `advertisement` |
| `/seo` | `seo` |
| `/seo/top` | `seo-top` |
| `/seo/metatags` | `seo-metatags` |
| `/seo/metatags-check` | `seo-metatags-gen` |
| `/market` | `market` |
| `/cp` | `cp` |
| `/projects` | `projects` |
| `/settings` | `settings` |
| `/currency-rates` | `currency-rates` |

## Тестирование API

Для тестирования API используйте Postman, curl или другие HTTP клиенты:

1. **GET** `/api_dashboard/help` - получение всех ссылок
2. **POST** `/api_dashboard/help` - создание новой ссылки
3. **PATCH** `/api_dashboard/help?id=eq.1` - обновление существующей ссылки
4. **DELETE** `/api_dashboard/help?id=eq.1` - удаление ссылки

**Важно**: Используйте PATCH для обновления записей, а не PUT, чтобы избежать ошибки "column pgrst_body.id does not exist"

## Fallback

Если база данных недоступна, система использует резервные ссылки:

```javascript
const fallbackMap = {
  '/': 'https://dashboard.api4/docs/dashboard',
  '/finance': 'https://dashboard.api4/docs/finance',
  // ... и так далее
}
```

## Безопасность

- Все операции с базой данных выполняются через API
- Валидация данных на стороне клиента и сервера
- Уникальность компонентов обеспечивается на уровне базы данных

## Технические детали

### HTTP методы
- **GET**: получение данных (без тела запроса)
- **POST**: создание новых записей (с телом запроса)
- **PATCH**: частичное обновление существующих записей (с телом запроса, но без id)
- **DELETE**: удаление записей (без тела запроса)

### Почему PATCH вместо PUT?
PostgREST (PostgreSQL REST API) ожидает, что при обновлении записи:
- `id` указывается в URL параметре (`?id=eq.1`)
- В теле запроса НЕ должно быть поля `id`
- PUT запрос пытается вставить все поля, включая `id`, что вызывает ошибку
- PATCH запрос обновляет только указанные поля, исключая `id`

## Логирование

Все операции логируются в консоль браузера:
- Поиск ссылок по компонентам
- Успешные/неуспешные запросы к API
- Ошибки сети и сервера

## Устранение неполадок

### 1. Ссылки не открываются
- Проверьте доступность базы данных
- Убедитесь, что записи созданы в таблице `help_links`
- Проверьте консоль браузера на наличие ошибок

### 2. Ошибки API
- Проверьте правильность URL эндпоинта
- Убедитесь, что таблица `help_links` существует
- Проверьте права доступа к API
- **Ошибка "column pgrst_body.id does not exist"**: возникает при использовании PUT вместо PATCH для обновления записей

### 3. Компонент не найден
- Убедитесь, что компонент добавлен в маппинг путей
- Проверьте правильность названия компонента в базе данных
- Добавьте недостающий компонент через форму

## Обновления

При добавлении новых разделов меню:

1. Добавьте путь в маппинг в `App.vue`
2. Создайте запись в базе данных через компонент Help
3. Укажите соответствующую ссылку на документацию
