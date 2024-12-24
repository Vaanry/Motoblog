# Django Motorcycle Blog Application

## Overview
This Django-based web application integrates a blog, personal accounts, personal messaging, and a motorcycle price calculator powered by CatBoost.

## Features

### Blog
- **Categories and Posts**: Users can create, edit, and browse blog posts categorized for better navigation.
- **Comments**: Registered users can engage with posts by commenting and replying.

### Personal Account
- **User Profiles**: Each user has a personal profile showcasing their activity.
- **Media Uploads**: Users can upload profile pictures and manage them.

### Messaging
- **Private Messages**: Users can exchange private messages, securely stored and accessible in their dialogs.

### Motorcycle Price Calculator
- **Price Estimation**: Utilizes CatBoost machine learning models to estimate motorcycle prices.
- **Dynamic Inputs**: Users can enter motorcycle details, and the application provides instant price predictions.

### Admin Panel
- **Content Management**: Manage blog posts, categories, and user accounts.
- **Calculator Management**: Update CatBoost models and related data files.

## Technologies Used

- **Framework**: Django
- **Machine Learning**: CatBoost
- **Database**: PostgreSQL (can be replaced with SQLite or MySQL)
- **Frontend**: Bootstrap, Jinja2 templates
- **Server Configuration**: Docker, Nginx

## Installation

### Prerequisites
- Python 3.8+
- Docker & Docker Compose (for containerized deployment)
- A virtual environment tool (e.g., `venv` or `virtualenv`)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/django-motorcycle-app.git
   cd django-motorcycle-app
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file with the following variables:
   ```env
   DB_ENGINE=django.db.backends.postgresql or another
   DB_NAME=your db name
   POSTGRES_USER=your database username
   POSTGRES_PASSWORD=your database password
   DJANGO_SECRET_KEY=your_secret_key
   DB_HOST=your database host
   DB_PORT=your database port
   ```

5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

6. Load initial data (optional):
   ```bash
   python manage.py loaddata dump.json
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

## Running with Docker

1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

2. Access the application at:
   ```
   http://localhost
   ```

## Running Tests
To execute the test suite:
```bash
python3 manage.py test
```

## Project Structure
```
|-- .env                     # Environment configuration
|-- .github                  # GitHub workflows
|-- custom_blog              # Main application directory
    |-- api                  # API functionality
    |-- blog                 # Blog functionality
    |-- calculators          # Price calculator with CatBoost model
    |-- chat                 # Messaging and chat
    |-- core                 # Core app logic
    |-- motobikes            # Motorcycle-related features
    |-- pages                # Static pages
    |-- templates            # HTML templates
    |-- users                # User account management
|-- docker-compose.yaml      # Docker Compose configuration
|-- Dockerfile               # Docker image configuration
|-- nginx                    # Nginx configuration files
|-- README.md                # Project README
|-- requirements.txt         # Python dependencies
|-- setup.cfg                # Linter and test configuration
```
