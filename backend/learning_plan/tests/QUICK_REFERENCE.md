# Quick Reference - Learning Plan Tests

## Run Tests

### All learning_plan tests
```bash
python manage.py test learning_plan.tests
```

### Specific file
```bash
python manage.py test learning_plan.tests.test_models
python manage.py test learning_plan.tests.test_serializers
python manage.py test learning_plan.tests.test_utils
```

### Verbose output
```bash
python manage.py test learning_plan.tests -v 2
```

### Keep database (faster)
```bash
python manage.py test learning_plan.tests --keepdb
```

### With coverage
```bash
coverage run --source='learning_plan' manage.py test learning_plan.tests
coverage report
coverage html
start htmlcov/index.html
```

## Test Statistics

| File | Tests | Focus |
|------|-------|-------|
| test_models.py | 27 | LearningPlan, Lesson, UserProgress models |
| test_serializers.py | 25 | All serializers |
| test_utils.py | 15 | generate_learning_plan service |
| test_permissions.py | 0 | Template for future tests |

**Total: 67 tests**

## Using Factories

### LearningPlanFactory
```python
from learning_plan.tests.factories import LearningPlanFactory

# Default values
plan = LearningPlanFactory()

# Custom values
plan = LearningPlanFactory(
    user=user,
    topic="Django Advanced",
    knowledge_level="intermediate",
    time_commitment_per_week=10
)
```

### LessonFactory
```python
from learning_plan.tests.factories import LessonFactory

# With auto-generated plan
lesson = LessonFactory()

# With specific plan
lesson = LessonFactory(
    plan=plan,
    title="Introduction",
    day_number=1,
    lesson_type="theory",
    time_estimate=45
)

# Batch creation
lessons = LessonFactory.create_batch(10, plan=plan)
```

### UserProgressFactory
```python
from learning_plan.tests.factories import UserProgressFactory

# Not completed
progress = UserProgressFactory(
    user=user,
    lesson=lesson
)

# Completed
from django.utils import timezone

progress = UserProgressFactory(
    user=user,
    lesson=lesson,
    is_completed=True,
    completed_at=timezone.now()
)
```

## Common Test Patterns

### Test calculate_progress
```python
def test_calculate_progress(self):
    plan = LearningPlanFactory(user=self.user)
    lessons = LessonFactory.create_batch(4, plan=plan)
    
    # Mark half as completed
    for lesson in lessons[:2]:
        UserProgressFactory(
            user=self.user,
            lesson=lesson,
            is_completed=True
        )
    
    progress = plan.calculate_progress()
    self.assertEqual(progress, 50.0)
```

### Test serializer with context
```python
def test_lesson_completed(self):
    lesson = LessonFactory()
    UserProgressFactory(
        user=self.user,
        lesson=lesson,
        is_completed=True
    )
    
    serializer = LessonItemSerializer(
        instance=lesson,
        context={'user': self.user}
    )
    
    self.assertTrue(serializer.data['is_completed'])
```

### Mock API calls
```python
@patch("learning_plan.services.client.responses.create")
def test_generate_plan(self, mock_create):
    fake_response = '[{"day":1,"title":"Test"}]'
    mock_create.return_value = MagicMock(output_text=fake_response)
    
    result = generate_learning_plan("Python", "beginner", 2)
    
    self.assertIsInstance(result, list)
    mock_create.assert_called_once()
```

## Model Choices

### Knowledge Levels
```python
'beginner'
'intermediate'
'experienced'
```

### Lesson Types
```python
'theory'
'practice'
'quiz'
'project'
```

## Key Test Methods

### Models
- `test_calculate_progress_*` - Progress calculation variations
- `test_str_representation` - String representation
- `test_*_choices` - Valid choice values
- `test_default_*` - Default field values

### Serializers
- `test_serialization` - Basic serialization
- `test_all_expected_fields_present` - Field coverage
- `test_*_excluded` - Sensitive field exclusion
- `test_get_is_completed_*` - Completion status

### Services
- `test_generate_learning_plan_parses_*` - JSON parsing
- `test_generate_learning_plan_strips_*` - Text cleanup
- `test_generate_learning_plan_*_raises` - Error handling

## Debugging

### Run single test
```bash
python manage.py test learning_plan.tests.test_models.TestLearningPlanModel.test_calculate_progress_no_lessons
```

### With debugger
```bash
python manage.py test learning_plan.tests --pdb
```

### Show SQL queries
```python
from django.test import TestCase
from django.test.utils import override_settings

@override_settings(DEBUG=True)
class MyTest(TestCase):
    def test_something(self):
        from django.db import connection
        print(connection.queries)
```

## Coverage Goals

Target coverage: 90%+

Check current coverage:
```bash
coverage run --source='learning_plan' manage.py test learning_plan.tests
coverage report --show-missing
```

## Documentation

- **SUMMARY.md** - Full summary of changes
- **QUICK_REFERENCE.md** - This file
- **factories.py** - Factory definitions
- **test_*.py** - Individual test files

## Related Tests

Also check `users.tests` for:
- `UserFactory` - User creation
- User model tests
- Authentication tests

## Tips

1. Use `setUpTestData` for data shared across tests (faster)
2. Use `setUp` for data that changes in each test
3. Use factories over manual object creation
4. Mock external APIs (OpenAI)
5. Test edge cases (empty, None, extreme values)
6. Use parameterized for similar test cases
7. Keep tests independent and isolated
8. Use descriptive test names

## Next Steps

1. Run all tests: `python manage.py test learning_plan.tests`
2. Check coverage: `coverage run && coverage report`
3. Read SUMMARY.md for detailed changes
4. Add custom permission tests when needed
