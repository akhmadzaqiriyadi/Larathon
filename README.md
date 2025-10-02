# Getting Started with Larathon

Larathon is a lightweight, Laravel-inspired web framework built with Python and FastAPI, designed to streamline modern web application development using familiar conventions.

## Requirements

* Python 3.11.3
* pip (Python package manager)

---

## 1. Create a Virtual Environment

Initialize a virtual environment using Python 3.11.3:

```bash
python3 -m venv env
```

This will create an `env/` directory containing the isolated environment.

---

## 2. Activate the Environment

Activate the virtual environment based on your OS:

**macOS / Linux**

```bash
source env/bin/activate
```

**Windows (CMD)**

```cmd
env\Scripts\activate
```

**Windows (PowerShell)**

```powershell
.\env\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

Once the environment is active, install all required packages:

```bash
pip install -r requirements.txt
```

---

## 4. Run Database Migrations

Larathon uses an artisan-style CLI tool for managing the project. To apply all database migrations:

```bash
python artisan.py migrate
```

---

## 5. Generate a Model (Optional)

To generate a model, resource-style controller, and a migration file, run:

```bash
python artisan.py make:model ModelName -r -m
```

Replace `ModelName` with your desired class name.

---

## 6. Define Your Routes

HTTP routes are defined in:

```text
routes/web.py
```

Example:

```python
from vendor.Illuminate.Support.Facades.Route import Route
from app.Http.Controllers.WelcomeController import WelcomeController

Route.get("/", WelcomeController.index)
```

---

## 7. Start the Development Server

Launch the built-in development server:

```bash
python artisan.py serve
```

The application will be available at:

```
http://127.0.0.1:8000
```
# Larathon
