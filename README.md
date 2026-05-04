# ⚡ TaskFlow — Team Task Manager

A full-stack Django web application for managing projects, assigning tasks, and tracking team progress with **role-based access control**.

## 🚀 Live Demo
> Deploy URL goes here after Railway deployment

## ✨ Features

- **Authentication** — Signup, Login, Logout, Profile management
- **Role-Based Access Control** — Global Admin / Member roles + per-project roles (Admin / Member / Viewer)
- **Project Management** — Create, edit, delete projects with status, priority, deadlines
- **Team Management** — Add/remove members per project, toggle global roles
- **Task Tracking** — Create tasks, assign to members, set due dates, track status
- **Dashboard** — Stats overview, recent tasks, overdue alerts, completion rate
- **Comments** — Comment threads on each task
- **Filters** — Filter tasks/projects by status and priority
- **AJAX Status Updates** — Update task status inline without page reload

## 🛠️ Tech Stack

- **Backend:** Django 4.2, Python 3.11
- **Database:** SQLite (dev) / PostgreSQL (production)
- **Frontend:** Django Templates, Bootstrap 5, Custom CSS (dark theme)
- **Static Files:** Whitenoise
- **Deployment:** Railway + Gunicorn

## 📁 Folder Structure

```
taskmanager/
├── taskmanager/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/             # User auth & profiles
│   ├── models.py         # Custom User model
│   ├── views.py          # Auth views
│   ├── dashboard_views.py
│   ├── forms.py
│   ├── urls.py
│   ├── dashboard_urls.py
│   └── admin.py
├── projects/             # Project & team management
│   ├── models.py         # Project, ProjectMember
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── tasks/                # Task management
│   ├── models.py         # Task, TaskComment
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── templates/            # All HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── accounts/
│   ├── projects/
│   └── tasks/
├── static/               # CSS, JS, images
├── requirements.txt
├── Procfile
├── railway.json
└── manage.py
```

## ⚙️ Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/taskflow.git
cd taskflow

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env
# Edit .env and set SECRET_KEY and DEBUG=True

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Start server
python manage.py runserver
```

Open http://127.0.0.1:8000


## 🔐 Role System

| Feature | Admin | Member | Viewer |
|---------|-------|--------|--------|
| Create projects | ✅ | ❌ | ❌ |
| Edit/Delete projects | ✅ | ❌ | ❌ |
| Add/Remove members | ✅ (project admin) | ❌ | ❌ |
| Create tasks | ✅ | ✅ | ❌ |
| Edit tasks | ✅ | Own tasks | ❌ |
| View all data | ✅ | Joined projects | Joined projects |
| Toggle user roles | ✅ | ❌ | ❌ |

## 📡 API Endpoints (URL Reference)

| URL | Method | Description |
|-----|--------|-------------|
| `/accounts/signup/` | GET/POST | Register |
| `/accounts/login/` | GET/POST | Login |
| `/accounts/logout/` | GET | Logout |
| `/accounts/profile/` | GET/POST | View/Update profile |
| `/accounts/members/` | GET | List all members (Admin) |
| `/dashboard/` | GET | Main dashboard |
| `/projects/` | GET | List projects |
| `/projects/create/` | GET/POST | Create project |
| `/projects/<id>/` | GET | Project detail + tasks |
| `/projects/<id>/edit/` | GET/POST | Edit project |
| `/projects/<id>/delete/` | POST | Delete project |
| `/projects/<id>/members/add/` | POST | Add member |
| `/tasks/my/` | GET | My assigned tasks |
| `/tasks/create/<project_id>/` | GET/POST | Create task |
| `/tasks/<id>/` | GET/POST | Task detail + comments |
| `/tasks/<id>/edit/` | GET/POST | Edit task |
| `/tasks/<id>/status/` | POST | AJAX status update |
| `/admin/` | GET | Django admin panel |
