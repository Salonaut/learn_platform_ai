# Quick Start Guide - Документація проєкту

## 🚀 Швидкий старт

### Крок 1: Активація GitHub Pages (одноразово)

1. Перейдіть: https://github.com/Salonaut/learn_platform_ai/settings/pages
2. **Source**: Виберіть `GitHub Actions`
3. Збережіть

### Крок 2: Запуск генерації документації

**Автоматично:**
```bash
git add .
git commit -m "docs: add code documentation"
git push origin main
```

**Вручну:**
1. Перейдіть: https://github.com/Salonaut/learn_platform_ai/actions
2. Виберіть "Generate and Deploy Documentation"
3. Клікніть "Run workflow"

### Крок 3: Перегляд документації

Документація буде доступна за ~2-3 хвилини:
- **Головна**: https://salonaut.github.io/learn_platform_ai/
- **Backend**: https://salonaut.github.io/learn_platform_ai/backend/html/
- **Frontend**: https://salonaut.github.io/learn_platform_ai/frontend/

## 📝 Локальна генерація

### Backend (Doxygen)
```bash
cd backend
doxygen Doxyfile
start ../docs/backend/html/index.html
```

### Frontend (JSDoc)
```bash
cd frontend
npm install
npx jsdoc -c jsdoc.json
start ../docs/frontend/index.html
```

## 📚 Як додати документацію до нового коду

### Python (Backend)
```python
def my_function(param1, param2):
    """
    @brief Короткий опис функції.
    
    @details Детальний опис того, що робить функція.
    
    @param param1 Опис першого параметра
    @param param2 Опис другого параметра
    
    @return Опис того, що повертає функція
    
    @example
    result = my_function("test", 123)
    print(result)
    """
    pass
```

### JavaScript/React (Frontend)
```javascript
/**
 * @brief Короткий опис компонента або функції.
 * 
 * @param {string} param1 - Опис першого параметра
 * @param {number} param2 - Опис другого параметра
 * 
 * @return {Object} Опис того, що повертається
 * 
 * @example
 * const result = myFunction("test", 123);
 */
function myFunction(param1, param2) {
  // код
}
```

## 🔧 Налаштування (вже виконано)

Всі необхідні файли вже створені:
- ✅ `backend/Doxyfile` - конфігурація Doxygen
- ✅ `frontend/jsdoc.json` - конфігурація JSDoc
- ✅ `.github/workflows/docs.yml` - CI/CD для документації
- ✅ `README.md` - оновлено з розділом Documentation

## ❓ Проблеми?

Детальна інструкція: [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md)

Типові проблеми:
1. **Документація не оновлюється?** → Очистіть кеш браузера (Ctrl+F5)
2. **Workflow failed?** → Перевірте логи в Actions
3. **404 помилка?** → Перевірте налаштування Pages в Settings

---

Документація оновлюється автоматично при кожному push в main! 🎉
