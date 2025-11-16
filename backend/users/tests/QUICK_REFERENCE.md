# Quick Reference - Test Commands

## Setup
```bash
# Install dependencies
pip install factory-boy==3.3.0 parameterized==0.9.0

# Or install all requirements
pip install -r requirements.txt
```

## Run Tests

### All tests
```bash
python manage.py test users.tests
```

### Verbose output
```bash
python manage.py test users.tests -v 2
```

### Specific file
```bash
python manage.py test users.tests.test_model
python manage.py test users.tests.test_registration_serializer
python manage.py test users.tests.test_login_serializer
python manage.py test users.tests.test_profile_serializer
python manage.py test users.tests.test_update_serializer
python manage.py test users.tests.test_change_password_serializer
```

### Specific class
```bash
python manage.py test users.tests.test_model.TestUserModel
```

### Specific test
```bash
python manage.py test users.tests.test_model.TestUserModel.test_full_name_property
```

### Keep test database (faster for multiple runs)
```bash
python manage.py test users.tests --keepdb
```

### Parallel execution (faster)
```bash
python manage.py test users.tests --parallel
```

## Coverage

### Install coverage
```bash
pip install coverage
```

### Run with coverage
```bash
coverage run --source='users' manage.py test users.tests
```

### Show report
```bash
coverage report
```

### Generate HTML report
```bash
coverage html
start htmlcov/index.html  # Windows
# open htmlcov/index.html  # Mac
# xdg-open htmlcov/index.html  # Linux
```

### Show missing lines
```bash
coverage report -m
```

### Coverage for specific file
```bash
coverage run --source='users.serializers' manage.py test users.tests
coverage report
```

## Code Quality

### Format code
```bash
pip install black
black users/tests/
```

### Check style
```bash
pip install flake8
flake8 users/tests/
```

### Type checking
```bash
pip install mypy django-stubs djangorestframework-stubs
mypy users/tests/
```

## Debugging Tests

### Run with pdb debugger
```bash
python manage.py test users.tests --pdb
```

### Show print statements
```bash
python manage.py test users.tests -v 2 --debug-mode
```

### Run only failed tests
```bash
python manage.py test users.tests --failed
```

## Test Files Overview

| File | Tests | Purpose |
|------|-------|---------|
| test_model.py | 7 | User model behavior |
| test_registration_serializer.py | 13 | User registration |
| test_login_serializer.py | 12 | User authentication |
| test_profile_serializer.py | 11 | User profile display |
| test_update_serializer.py | 13 | User profile updates |
| test_change_password_serializer.py | 16 | Password changes |

**Total: 72 tests**

## Common Patterns

### Create test user
```python
from users.tests.factories import UserFactory

user = UserFactory()  # Random data
user = UserFactory(email="specific@example.com")  # Custom data
user = UserFactory(password="TestPass123!")  # Custom password
```

### Test serializer
```python
serializer = MySerializer(data=test_data)
self.assertTrue(serializer.is_valid())
instance = serializer.save()
```

### Test with mock
```python
from unittest.mock import patch

@patch('users.serializers.authenticate')
def test_something(self, mock_auth):
    mock_auth.return_value = self.user
    # test code
    mock_auth.assert_called_once()
```

### Parameterized test
```python
from parameterized import parameterized

@parameterized.expand([
    ("input1", "expected1"),
    ("input2", "expected2"),
])
def test_something(self, input_val, expected):
    result = function(input_val)
    self.assertEqual(result, expected)
```

## CI/CD Integration

### GitHub Actions
```yaml
- name: Run tests
  run: |
    python manage.py test users.tests
    
- name: Coverage
  run: |
    coverage run --source='users' manage.py test users.tests
    coverage report --fail-under=80
```

### GitLab CI
```yaml
test:
  script:
    - pip install -r requirements.txt
    - python manage.py test users.tests
    - coverage run --source='users' manage.py test users.tests
    - coverage report
```

## Troubleshooting

### Import errors
```bash
# Make sure dependencies are installed
pip list | grep factory-boy
pip list | grep parameterized

# Reinstall if needed
pip install --force-reinstall factory-boy parameterized
```

### Database errors
```bash
# Apply migrations
python manage.py migrate

# Or use test database
python manage.py test users.tests --keepdb
```

### Factory errors
```bash
# Check factories.py exists
ls users/tests/factories.py

# Check __init__.py exists
ls users/tests/__init__.py
```

## Documentation

- **README.md** - Full test documentation
- **SUMMARY_EN.md** - English summary of changes
- **SUMMARY_UA.md** - Ukrainian summary (Резюме українською)
- **INSTALLATION.md** - Setup instructions
- **QUICK_REFERENCE.md** - This file

## Links

- [Django Testing Docs](https://docs.djangoproject.com/en/stable/topics/testing/)
- [DRF Testing Docs](https://www.django-rest-framework.org/api-guide/testing/)
- [Factory Boy Docs](https://factoryboy.readthedocs.io/)
- [Parameterized Docs](https://github.com/wolever/parameterized)
- [Coverage.py Docs](https://coverage.readthedocs.io/)
