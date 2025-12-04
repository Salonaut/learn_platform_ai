# Users App Tests

This directory contains comprehensive tests for the users app, rewritten according to Django and DRF testing best practices.

## Test Files Structure

The tests are organized into separate files for better clarity and maintainability:

### Model Tests
- **test_model.py** - Tests for the User model
  - Real User instances instead of mocks
  - Parameterized tests for full_name property
  - Edge cases (None, whitespace, empty values)

### Serializer Tests (Split by Serializer)
- **test_registration_serializer.py** - UserRegistrationSerializer
  - Valid registration flow
  - Password mismatch validation
  - Invalid email formats
  - Duplicate email/username
  - Weak password validation
  - Write-only field verification
  
- **test_login_serializer.py** - UserLoginSerializer
  - Successful authentication
  - Invalid credentials
  - Inactive user handling
  - Proper mock path (`users.serializers.authenticate`)
  - Error structure assertions (not exact messages)
  
- **test_profile_serializer.py** - UserProfileSerializer
  - Read-only field verification
  - Progress status logic with edge cases
  - Full serialization output
  - Password field exclusion
  
- **test_update_serializer.py** - UserUpdateSerializer
  - Partial updates
  - Field-level updates
  - Protection against updating restricted fields
  - Return value verification
  
- **test_change_password_serializer.py** - UserChangePasswordSerializer
  - Successful password change
  - Old password validation
  - New password mismatch
  - Weak password detection
  - Write-only field verification

## Test Infrastructure

### Factories (`factories.py`)
Uses `factory_boy` for efficient test data creation:
- **UserFactory** - Creates test users with sensible defaults
- Automatic password hashing
- Faker integration for realistic data

### Shared Fixtures (`conftest.py`)
Contains pytest fixture examples for future migration.

## Key Improvements

### ✅ Real Instances Over Mocks
```python
# Before (using MagicMock)
user_mock = MagicMock(spec=User)
user_mock.first_name = "John"

# After (using real instances)
user = UserFactory(first_name="John")
```

### ✅ Parameterized Tests
```python
@parameterized.expand([
    ("John", "Doe", "John Doe"),
    ("Jane", "", "Jane"),
    ("", "", ""),
])
def test_full_name_property(self, first_name, last_name, expected):
    user = User(first_name=first_name, last_name=last_name)
    self.assertEqual(user.full_name, expected)
```

### ✅ Proper Mock Paths
```python
# Correct: Mock where it's imported
@patch('users.serializers.authenticate')
def test_login(self, mock_authenticate):
    ...
```

### ✅ Error Structure Assertions
```python
# Before (brittle)
self.assertEqual(str(error), 'User not found')

# After (flexible)
error_message = str(errors['non_field_errors'][0])
self.assertIn('not found', error_message.lower())
```

### ✅ Edge Cases Covered
- Invalid email formats
- Duplicate users
- Weak passwords
- None/whitespace values
- Empty strings
- Missing required fields

### ✅ Field Property Tests
- Read-only fields cannot be written
- Write-only fields not in output
- Sensitive data (passwords) excluded

### ✅ Return Value Verification
```python
user = serializer.save()
self.assertEqual(user.id, expected_id)
self.assertTrue(user.check_password("password"))
```

## Running Tests

### All Tests
```bash
python manage.py test users.tests
```

### Specific Test File
```bash
python manage.py test users.tests.test_registration_serializer
```

### Specific Test Class
```bash
python manage.py test users.tests.test_model.TestUserModel
```

### Specific Test Method
```bash
python manage.py test users.tests.test_model.TestUserModel.test_full_name_property
```

### With Coverage
```bash
coverage run --source='users' manage.py test users.tests
coverage report
coverage html
```

## Dependencies

Required packages (in requirements.txt):
- `factory-boy==3.3.0` - Test data factories
- `parameterized==0.9.0` - Parameterized tests
- `coverage` (optional) - Test coverage

## Future Improvements

### Migration to pytest
The tests are written in a way that makes migration to pytest easy:
1. Convert `TestCase` to use pytest fixtures
2. Use `conftest.py` fixtures (already prepared)
3. Replace `@parameterized.expand` with `@pytest.mark.parametrize`
4. Use `pytest-django` for database fixtures

### Example pytest migration:
```python
# Current (unittest)
class TestUserModel(TestCase):
    def test_something(self):
        user = UserFactory()
        ...

# pytest style
def test_something(user):  # user from conftest.py fixture
    ...
```

## Best Practices Followed

1. ✅ Use `setUpTestData` for shared data (faster)
2. ✅ Use factories instead of manual object creation
3. ✅ Mock only external dependencies
4. ✅ Assert error structure, not exact messages
5. ✅ Test both happy path and edge cases
6. ✅ Verify side effects (database changes, return values)
7. ✅ Test field properties (read_only, write_only)
8. ✅ Keep tests independent and isolated
9. ✅ Use descriptive test names
10. ✅ One test file per serializer/model

## Code Quality

To maintain code quality, run:
```bash
# Format code
black users/tests/

# Check style
flake8 users/tests/

# Type checking (if using mypy)
mypy users/tests/
```
