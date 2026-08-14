# Campus Connect 
## Unified College Portal with AI Study Assistant

5th Semister major project — Diploma in Computer Engineering & IoT, Government Polytechnic Angul.

**Group:** PawBytes

<!-- ## Theme — Cat Branding 🐾

The portal follows a light cat theme for personality and visual identity in the demo/presentation, layered on top of the same dark minimal aesthetic — no impact on functionality or build complexity.

- **Logo/favicon:** paw print or cat silhouette
- **Loading states:** paw-print spinner
- **Empty states:** playful cat-toned copy (e.g. "purr-fectly quiet here — no notices yet")
- **AI Study Assistant persona:** framed as a "study buddy cat" giving feedback — cosmetic copy layer over the same API calls
- **Color palette:** dark theme with an orange-tabby or black-cat accent, consistent with existing dark navy/amber preference -->

## Idea

A single web portal that replaces scattered offline/manual processes (attendance registers, notice boards, result sheets) with one role-based system for students, faculty, and admin — plus an AI-powered study assistant that generates practice questions and gives instant feedback on answers.

The goal is a project that's genuinely useful day-to-day on campus, buildable by a 5-person team new to frontend development, and includes one standout technical feature (AI integration) without requiring any machine learning background.

## Tech Stack

- **Backend:** Django 
- **Frontend:** Django templates + HTML + CSS +JS
- **Database:** PostgreSQL
- **AI:** External LLM API 
- **Deployment:** Vercel 

## Modules & Team Split (5 people)

| # | Module | Description | Owner |
|---|--------|-------------|-------|
| 1 | **FrontEnd** | Full FrontEnd with UI | TBD |
| 2 | **Attendance** | Mark/view attendance, extends existing Student Tracker | TBD |
| 3 | **Documentation** | Post/view announcements, filter by department/year | TBD |
| 4 | **Exams & Results** | Exam schedules, upload/view results (Exam, ExamResult models) | TBD |
| 5 | **BackEnd & AI Study Assistant** | Topic-based question generation + AI answer feedback | Deba |

## Data Models (high level)

**accounts**
- `User` (extend Django's built-in) — role: student / faculty / admin
- `Profile` — department, year, roll number

**attendance**
- `AttendanceRecord` — student, date, subject, status (present/absent)

**notices**
- `Notice` — title, body, posted_by, department, created_at

**exams**
- `Exam` — subject, date, max_marks
- `ExamResult` — student, exam, marks_obtained

**ai_assistant**
- `Question` — topic, text, generated_at
- `Answer` — question, student, answer_text, ai_feedback, score

## AI Study Assistant — How It Works

1. Student picks a topic (e.g. DBMS, OOP, Networking, IoT etc.)
2. Django view calls the AI API with a prompt: *"Generate one interview question about {topic}"*
3. Question is saved to DB and rendered on the page
4. Student submits an answer
5. Django sends the answer back to the AI API asking for feedback/score
6. Feedback is displayed and saved to `Answer` model


## MVP Scope ( Mark ✓ If Complet a Task)

**Must-have (MVP):**
- [ ] Login/signup with role-based redirect (student/faculty/admin dashboards)
- [ ] Student can view their attendance %
- [ ] Faculty/admin can mark attendance
- [ ] Notices board — post (faculty/admin) and view (all)
- [ ] Exam results — admin uploads, student views their own
- [ ] AI Study Assistant — pick topic → get question → submit answer → get AI feedback
- [ ] Basic responsive UI, consistent theme across all modules

**Nice-to-have (if time permits):**
- [ ] AI feedback includes a score out of 10, not just text
- [ ] Student dashboard shows AI practice history
- [ ] Notice filtering by department/year
- [ ] Simple search across notices/results
- [ ] Email notification on new notice (Django email backend)

**Explicitly out of scope for this project:**
- Fee payment / financial modules
- Mobile app
- Real-time chat/notifications (WebSockets)
- Any custom-trained ML model

## Repo Structure (suggested)

Each app has its own **namespaced** templates and static folders (app name repeated inside, e.g. `attendance/templates/attendance/`) so filenames never collide across apps. Shared layout (navbar, footer, global theme) lives once at the project root in `templates/base.html`, and every app template extends it.

```
campus-connect/
├── accounts/
│   ├── templates/
│   │   └── accounts/
│   │       ├── login.html
│   │       └── signup.html
│   ├── static/
│   │   └── accounts/
│   │       └── style.css
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── attendance/
│   ├── templates/
│   │   └── attendance/
│   │       ├── mark.html
│   │       └── view.html
│   ├── static/
│   │   └── attendance/
│   │       └── style.css
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── notices/
│   ├── templates/
│   │   └── notices/
│   │       └── list.html
│   ├── static/
│   │   └── notices/
│   │       └── style.css
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── exams/
│   ├── templates/
│   │   └── exams/
│   │       ├── results.html
│   │       └── schedule.html
│   ├── static/
│   │   └── exams/
│   │       └── style.css
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── ai_assistant/
│   ├── templates/
│   │   └── ai_assistant/
│   │       ├── topic_select.html
│   │       └── question.html
│   ├── static/
│   │   └── ai_assistant/
│   │       └── style.css
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── templates/                  # project-level, shared across all apps
│   └── base.html                # navbar, footer, global theme — every app template extends this
│
├── static/                     # project-level, shared across all apps
│   └── css/
│       └── main.css             # global theme: colors, fonts, layout
│
├── campus_connect/              # project settings
│   ├── settings.py
│   ├── urls.py                  # includes each app's urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md
```

**⚠️Note on `settings.py`:** set `TEMPLATES[0]['DIRS'] = [BASE_DIR / "templates"]` so Django finds the shared `base.html`, and keep `APP_DIRS: True` so it also finds each app's own namespaced templates.