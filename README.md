# AI-Powered Learning Platform

An intelligent learning platform that helps users efficiently master any topic through structured, AI-generated study plans with progress tracking and interactive elements.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [API Endpoints](#api-endpoints)
- [Data Models](#data-models)
- [Installation and Setup](#installation-and-setup)
- [Documentation](#documentation)

---

## Project Overview

**Learn Platform AI** is a modern web platform that leverages OpenAI GPT capabilities to create personalized learning plans. The system analyzes user's knowledge level, time availability and generates structured lessons with theory, practical tasks, quizzes, and projects.

### Key Advantages:
- **Personalization**: AI-generated plans tailored to knowledge level (beginner/intermediate/experienced)
- **Analytics**: Progress tracking, learning time monitoring and statistics
- **Gamification**: Study streaks system for motivation
- **Interactivity**: Notes, quizzes with AI-generated questions
- **Adaptability**: Different lesson types (theory, practice, quiz, project)

---

## Key Features

### 1. Learning Plan Management
- Generation of personalized learning plans using OpenAI GPT
- Specify topic, knowledge level (beginner/intermediate/experienced) and time commitment
- Automatic progress calculation
- View list of all user's learning plans

### 2. Lesson System
- **Lesson types**: theory, practice, quizzes, projects
- Detailed content in Markdown format with theory
- Practical tasks for each lesson
- Time estimates for completion
- Lessons numbered by study day
- Additional links for deeper study

### 3. Intelligent Quiz System
- AI-generated quizzes based on lesson theory
- Multiple choice questions (A, B, C, D)
- Automatic answer verification
- Detailed explanations for correct answers
- Quiz attempt history
- Percentage score calculation

### 4. Progress Tracking
- Mark lessons as completed
- Track time spent on each lesson
- Lesson completion dates
- Automatic learning plan progress recalculation
- Detailed analytics with metrics:
  - Overall progress (%)
  - Time spent
  - Number of completed lessons/quizzes
  - Average quiz scores

### 5. Notes System
- Create personal notes for lessons
- Edit and delete notes
- Timestamps for creation/updates
- Link notes to specific lessons

### 6. Study Streaks
- Track daily learning activity
- Calculate consecutive learning days
- Activity heatmap for last 365 days
- Metrics: lessons, quizzes, notes, learning time
- Activity score system for visualization

### 7. Analytics and Statistics
- Overall progress across all plans
- Total learning time
- Lesson and quiz statistics
- Quiz success rates
- Data visualization

### 8. User System
- Registration and JWT authentication
- User profile with avatar
- Biography and social media links
- Password change
- Automatic token refresh

---

## Technology Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|------------|
| **Python** | 3.10+ | Core programming language |
| **Django** | 5.0+ | Web framework |
| **Django REST Framework** | 3.14+ | REST API |
| **PostgreSQL** | 14+ | Relational database |
| **JWT (SimpleJWT)** | 5.3+ | Authentication |
| **OpenAI API** | 1.0+ | AI content generation |
| **Pillow** | 10.0+ | Image processing (avatars) |

**Additional packages:**
- `drf-spectacular` - automatic OpenAPI documentation generation
- `django-cors-headers` - CORS support
- `python-dotenv` - environment variables management
- `psycopg2-binary` - PostgreSQL driver

### Frontend
| Technology | Version | Purpose |
|-----------|---------|------------|
| **React** | 18.2+ | UI library |
| **Vite** | 5.0+ | Build tool and dev server |
| **React Router** | 6.20+ | Routing |
| **Axios** | 1.6+ | HTTP client |
| **Material-UI (MUI)** | 5.14+ | UI components |
| **React Markdown** | 9.0+ | Markdown rendering |
| **Emotion** | 11.11+ | CSS-in-JS |

### Development Tools
- **Doxygen** - documentation generation for Python (backend)
- **JSDoc** - documentation generation for JavaScript (frontend)
- **GitHub Pages** - documentation hosting
- **Git** - version control

---

## System Architecture

### Project Structure

```
learn_platform_ai/
├── backend/                    # Django backend
│   ├── config/                # Django configuration
│   │   ├── settings.py       # Configuration (DB, JWT, CORS, DRF)
│   │   ├── urls.py           # Main routing
│   │   └── wsgi.py / asgi.py # WSGI/ASGI entry points
│   ├── learning_plan/         # Learning plans app
│   │   ├── models.py         # Models (LearningPlan, Lesson, Quiz, etc.)
│   │   ├── serializers.py    # DRF serializers
│   │   ├── views.py          # API views
│   │   ├── services.py       # Business logic (AI generation)
│   │   ├── urls.py           # URL routes
│   │   └── tests/            # Tests
│   ├── users/                 # Users app
│   │   ├── models.py         # User model
│   │   ├── serializers.py    # Serializers (registration, profile)
│   │   ├── views.py          # Authentication and profile
│   │   └── tests/            # Tests
│   ├── requirements.txt       # Python dependencies
│   └── manage.py             # Django CLI
│
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── api/              # API client (axios)
│   │   ├── components/       # Reusable components
│   │   ├── context/          # React Context (AuthContext)
│   │   ├── pages/            # Application pages
│   │   ├── App.jsx           # Main component
│   │   └── index.jsx         # Entry point
│   ├── package.json          # npm dependencies
│   └── vite.config.js        # Vite configuration
│
├── LICENSE
└── README.md                  # This file
```

### Data Flow

```
User → React Frontend → Axios → Django REST API → PostgreSQL
                                      ↓
                                  OpenAI API
```

---

## API Endpoints

### Authentication & Users (`/api/v1/auth/`)

| Method | Endpoint | Description | Auth |
|--------|----------|------|------|
| POST | `/register/` | Register new user | No |
| POST | `/login/` | Login (get JWT tokens) | No |
| POST | `/logout/` | Logout | Yes |
| GET/PUT/PATCH | `/profile/` | View/update profile | Yes |
| POST | `/change_password/` | Change password | Yes |
| POST | `/token/refresh/` | Refresh access token | No |

### Learning Plans (`/api/v1/learning/`)

| Method | Endpoint | Description | Auth |
|--------|----------|------|------|
| POST | `/plans/generate/` | Generate learning plan via AI | Yes |
| GET | `/plans/` | List all user's plans | Yes |
| GET | `/plans/<id>/lessons/` | List lessons for specific plan | Yes |

### Lessons (`/api/v1/learning/`)

| Method | Endpoint | Description | Auth |
|--------|----------|------|------|
| GET | `/lessons/<id>/` | Detailed lesson information | Yes |
| POST | `/lessons/<id>/complete/` | Mark lesson as completed | Yes |

### Quiz System (`/api/v1/learning/`)

| Method | Endpoint | Description | Auth |
|--------|----------|------|------|
| POST | `/lessons/<id>/quiz/generate/` | Generate quiz for lesson via AI | Yes |
| GET | `/quiz/<id>/` | Get quiz questions | Yes |
| POST | `/quiz/<id>/submit/` | Submit answers and get results | Yes |

### Notes System (`/api/v1/learning/`)

| Method | Endpoint | Description | Auth |
|--------|----------|------|------|
| GET/POST | `/lessons/<id>/notes/` | List/create notes for lesson | Yes |
| GET/PUT/DELETE | `/notes/<id>/` | View/edit/delete note | Yes |

### Analytics & Progress (`/api/v1/learning/`)

| Method | Endpoint | Description | Auth |
|--------|----------|------|------|
| GET | `/analytics/` | Detailed user progress analytics | Yes |
| GET | `/streak/` | Study streak and activity heatmap info | Yes |

### API Documentation

| Endpoint | Description |
|----------|------|
| `/api/schema/` | OpenAPI schema (JSON) |
| `/api/docs/` | Swagger UI interface |
| `/api/redoc/` | ReDoc interface |

---

## Data Models

### User
```python
- email (unique, used for login)
- username
- first_name, last_name
- avatar (ImageField)
- bio (text field)
- social_media
- created_at, updated_at
- is_active
```

### LearningPlan
```python
- user (ForeignKey → User)
- topic (learning topic)
- time_commitment_per_week (hours per week)
- knowledge_level (beginner/intermediate/experienced)
- progress (completion percentage, 0-100)
- created_at
```

### Lesson
```python
- plan (ForeignKey → LearningPlan)
- title
- theory_md (theory in Markdown)
- task (practical assignment)
- lesson_type (theory/practice/quiz/project)
- time_estimate (minutes)
- day_number (day number)
- extra_links (JSONField, additional resources)
```

### UserProgress
```python
- user (ForeignKey → User)
- lesson (ForeignKey → Lesson)
- is_completed (completed or not)
- completed_at (completion date)
- time_spent (time spent in minutes)
```

### Quiz
```python
- lesson (ForeignKey → Lesson)
- title
- created_at
- questions (related QuizQuestion)
```

### QuizQuestion
```python
- quiz (ForeignKey → Quiz)
- question_text
- option_a, option_b, option_c, option_d
- correct_answer (A/B/C/D)
- explanation (explanation of correct answer)
```

### QuizAttempt
```python
- user (ForeignKey → User)
- quiz (ForeignKey → Quiz)
- score (score in percentage)
- answers (JSONField, user answers)
- completed_at
```

### LessonNote
```python
- user (ForeignKey → User)
- lesson (ForeignKey → Lesson)
- content (note text)
- created_at, updated_at
```

### StudyStreak
```python
- user (ForeignKey → User)
- date (activity date)
- lessons_completed (number of completed lessons)
- quizzes_taken (number of quizzes taken)
- notes_created (number of notes created)
- total_time_spent (total time in minutes)
- activity_score (calculated activity score)
```

---

## Installation and Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- OpenAI API key

### Backend Setup

1. **Clone repository**
```bash
git clone https://github.com/salonaut/learn_platform_ai.git
cd learn_platform_ai/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create `.env` file in `backend/` folder:
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
OPEN_API_KEY=your-openai-api-key

POSTGRES_DB=learn_platform
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

5. **Database migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run server**
```bash
python manage.py runserver
```
Backend will be available at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend folder**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Run dev server**
```bash
npm run dev
```
Frontend will be available at: `http://localhost:3000`

---

## Documentation

This project uses automated documentation generation for backend and frontend code:

### Backend Documentation (Python)
- **Tool**: Doxygen with Python support
- **Format**: Doxygen-style comments with `@brief`, `@param`, `@return`, `@throws`, `@example` tags
- **Coverage**: Models, views, serializers, and services

### Frontend Documentation (JavaScript)
- **Tool**: JSDoc
- **Format**: JSDoc comments with standard tags
- **Coverage**: React components, context providers, API clients

### Viewing Documentation
Documentation is automatically generated and published to GitHub Pages on every push to the main branch.

**Live Documentation**: https://salonaut.github.io/learn_platform_ai/

### Local Documentation Generation

#### Backend (Doxygen)
```bash
cd backend
doxygen Doxyfile
# Open docs/backend/html/index.html in your browser
```

#### Frontend (JSDoc)
```bash
cd frontend
npm run docs
# Open docs/frontend/index.html in your browser
```

---

## Usage Examples

### Generate Learning Plan

**Request:**
```bash
POST /api/v1/learning/plans/generate/
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "topic": "Python Programming",
  "knowledge_level": "beginner",
  "time_commitment_per_week": 10
}
```

**Response:**
```json
{
  "id": 1,
  "topic": "Python Programming",
  "knowledge_level": "beginner",
  "time_commitment_per_week": 10,
  "progress": 0.0,
  "created_at": "2026-01-05T12:00:00Z",
  "items": [
    {
      "id": 1,
      "title": "Introduction to Python",
      "lesson_type": "theory",
      "day_number": 1,
      "time_estimate": 60,
      "theory_md": "# Python Basics\n\nPython is...",
      "task": "Install Python and write your first program",
      "extra_links": ["https://python.org"]
    }
  ]
}
```

### Mark Lesson as Completed

**Request:**
```bash
POST /api/v1/learning/lessons/1/complete/
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "time_spent": 45
}
```

**Response:**
```json
{
  "message": "Lesson marked as completed",
  "progress": {
    "lesson_id": 1,
    "is_completed": true,
    "completed_at": "2026-01-05T14:30:00Z",
    "time_spent": 45
  },
  "plan_progress": 12.5
}
```

### Generate and Take Quiz

**Generate Quiz:**
```bash
POST /api/v1/learning/lessons/1/quiz/generate/
Authorization: Bearer <access_token>
```

**Submit Quiz:**
```bash
POST /api/v1/learning/quiz/1/submit/
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "answers": {
    "1": "A",
    "2": "C",
    "3": "B",
    "4": "D"
  }
}
```

**Response:**
```json
{
  "score": 75.0,
  "total_questions": 4,
  "correct_answers": 3,
  "results": [
    {
      "question_id": 1,
      "user_answer": "A",
      "correct_answer": "A",
      "is_correct": true,
      "explanation": "Correct! Variables store data..."
    }
  ]
}
```

---

## Security Configuration

### JWT Authentication
The system uses JWT tokens for authentication:
- **Access Token**: valid for 60 minutes
- **Refresh Token**: valid for 7 days
- Automatic refresh token rotation
- Blacklist for expired tokens

### CORS Configuration
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
```

### Production Recommendations:
1. Set `DEBUG=False`
2. Configure proper `SECRET_KEY`
3. Set up `ALLOWED_HOSTS`
4. Use HTTPS
5. Configure rate limiting
6. Use separate environment variables for different environments

---

## Testing

The project includes comprehensive backend tests:

```bash
cd backend
python manage.py test
```

### Test Coverage:
- **users app**: models, serializers, views, permissions
- **learning_plan app**: models, serializers, views, services, utils
- Factory patterns for creating test data
- Permission and authentication tests

Test documentation: [backend/learning_plan/tests/QUICK_REFERENCE.md](backend/learning_plan/tests/QUICK_REFERENCE.md)

---

## Deployment

### Backend (Django)
Recommended platforms:
- **Heroku** with PostgreSQL addon
- **DigitalOcean App Platform**
- **Railway**
- **AWS EC2** with RDS PostgreSQL

Additional configuration:
```bash
# Collect static files
python manage.py collectstatic

# Gunicorn for production
pip install gunicorn
gunicorn config.wsgi:application
```

### Frontend (React)
Recommended platforms:
- **Vercel**
- **Netlify**
- **GitHub Pages**

Build command:
```bash
npm run build
```

---

## Contributing

Contributions welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Add docstrings and JSDoc comments
- Write tests for new features

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## Author

**GitHub**: [@salonaut](https://github.com/salonaut)

**Documentation**: [https://salonaut.github.io/learn_platform_ai/](https://salonaut.github.io/learn_platform_ai/)

---

## Acknowledgments

- [OpenAI](https://openai.com/) for GPT API
- [Django REST Framework](https://www.django-rest-framework.org/)
- [React](https://react.dev/)
- [Material-UI](https://mui.com/)
- All project contributors

---

## Contact and Support

If you have questions or suggestions:
- Create an [Issue](https://github.com/salonaut/learn_platform_ai/issues)
- Start a [Discussion](https://github.com/salonaut/learn_platform_ai/discussions)

---

<div align="center">

Made with AI

</div>
