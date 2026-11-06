# Django OYO

A small Django web application with a Tailwind CSS-based landing page. The current app serves a single home page; hotel search, booking, and other OYO-style workflows are not implemented yet.

## Requirements

- Python with `pip`
- PostgreSQL
- Node.js and npm (to build or watch Tailwind CSS)

## Set up the project

Run these commands from the project root (the directory containing `manage.py`).

### 1. Create and activate a Python environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Python dependencies

```bash
python -m pip install --upgrade pip
python -m pip install Django "psycopg[binary]"
```

### 3. Configure PostgreSQL

The project uses PostgreSQL. Create a database named `oyoclone_db`, or change the database name in `oyo_clone/settings.py` to one you have created. Update the connection settings there to match your local PostgreSQL server before continuing.

Database connection values are currently configured directly in `oyo_clone/settings.py`. Do not put real or production credentials in a public repository; move secrets to environment-based configuration before deploying or sharing a production configuration.

### 4. Install Tailwind dependencies

```bash
npm ci
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

## Run the application

Start Django from the project root:

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the home page. The Django admin is available at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/). Create an administrator account with:

```bash
python manage.py createsuperuser
```

For development, run the Tailwind watcher in a separate terminal so CSS changes are rebuilt automatically:

```bash
npm run dev
```

To generate a minified stylesheet instead, run:

```bash
npm run build
```

The generated stylesheet is written to `static/css/output.css`, which is loaded by the shared base template.

## Tests

Run the Django test suite with:

```bash
python manage.py test
```

## Project layout

```text
home/                  Home page app, URL route, view, and app templates
oyo_clone/             Django project settings and root URL configuration
static/src/input.css   Tailwind CSS source
static/css/output.css  Compiled stylesheet served by Django
templates/             Shared base layout, navigation, and footer
manage.py              Django management command entry point
package.json           Tailwind development and build scripts
```

The home page is routed from `/` through `home/urls.py` and rendered by `home/views.py` using `home/templates/home/index.html`.
