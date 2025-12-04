# Інструкція з налаштування GitHub Pages для проєкту

## Крок 1: Увімкнення GitHub Pages

1. Перейдіть до вашого репозиторію на GitHub: https://github.com/Salonaut/learn_platform_ai
2. Натисніть на вкладку **Settings** (Налаштування)
3. У лівому меню знайдіть розділ **Pages** (в секції Code and automation)

## Крок 2: Налаштування джерела для Pages

1. У розділі **Source** (Джерело) виберіть:
   - **Source**: `GitHub Actions`
   
2. Збережіть налаштування

## Крок 3: Перевірка прав доступу для Workflows

1. Перейдіть до **Settings** → **Actions** → **General**
2. Прокрутіть до розділу **Workflow permissions**
3. Переконайтеся, що вибрано:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**
4. Натисніть **Save**

## Крок 4: Запуск документації

### Автоматичний запуск
Документація буде автоматично генеруватися при:
- Push в гілку `main`
- Push в будь-яку гілку `docs/**`
- Створенні Pull Request в `main`

### Ручний запуск
1. Перейдіть до вкладки **Actions**
2. Виберіть workflow **Generate and Deploy Documentation**
3. Натисніть **Run workflow**
4. Виберіть гілку та натисніть зелену кнопку **Run workflow**

## Крок 5: Перегляд документації

Після успішного виконання workflow документація буде доступна за адресою:
```
https://salonaut.github.io/learn_platform_ai/
```

### Структура документації:
- **Головна сторінка**: `https://salonaut.github.io/learn_platform_ai/`
- **Backend (Python/Doxygen)**: `https://salonaut.github.io/learn_platform_ai/backend/html/index.html`
- **Frontend (React/JSDoc)**: `https://salonaut.github.io/learn_platform_ai/frontend/index.html`

## Крок 6: Моніторинг процесу

1. Відкрийте вкладку **Actions** у вашому репозиторії
2. Знайдіть останній запуск workflow **Generate and Deploy Documentation**
3. Натисніть на нього, щоб побачити детальні логи
4. Після успішного завершення (зелена галочка ✅) документація буде доступна

## Можливі проблеми та їх вирішення

### Помилка: "Pages deployment failed"
**Рішення**: Переконайтеся, що GitHub Pages увімкнено і вибрано джерело "GitHub Actions"

### Помилка: "Permission denied"
**Рішення**: Перевірте, що workflow має права на запис (Settings → Actions → Workflow permissions)

### Документація не оновлюється
**Рішення**: 
1. Перевірте, що commit був в гілку `main` або `docs/**`
2. Перегляньте логи workflow в розділі Actions
3. Очистіть кеш браузера (Ctrl+F5)

## Локальна генерація документації

### Backend (Python)
```bash
cd backend
doxygen Doxyfile
# Відкрийте ../docs/backend/html/index.html у браузері
```

### Frontend (JavaScript)
```bash
cd frontend
npm install
npm install --save-dev jsdoc docdash
npx jsdoc -c jsdoc.json
# Відкрийте ../docs/frontend/index.html у браузері
```

## Додаткова інформація

- **Workflow файл**: `.github/workflows/docs.yml`
- **Конфігурація Doxygen**: `backend/Doxyfile`
- **Конфігурація JSDoc**: `frontend/jsdoc.json`
- **Документовані файли**:
  - Backend: `models.py`, `views.py`, `services.py`, `serializers.py`
  - Frontend: `AuthContext.jsx`, `apiClient.js`, компоненти в `src/`

## Підтримка та оновлення

При додаванні нового коду не забувайте додавати документацію:
- **Python**: Використовуйте Doxygen-style коментарі з `@brief`, `@param`, `@return`
- **JavaScript/React**: Використовуйте JSDoc коментарі з `/** ... */`

Документація оновлюється автоматично при кожному push в main!
