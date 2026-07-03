# ShopBox

ShopBox is a Django-based online shop project with user authentication, product catalog, cart/order pages, and a Telegram bot for showing available products.

## Features

- Email-based user login with a custom Django user model.
- Product and category models.
- Burger menu pages for profile, orders, cart, and settings.
- "Buy" button that creates an order and order item for the logged-in user.
- Telegram bot built with aiogram.
- Environment-based configuration for secrets and deployment settings.

## Tech Stack

- Python
- Django
- SQLite
- aiogram
- Pillow
- PythonAnywhere deployment

## Project Structure

```text
ShopBox/
├── final_proj/
│   ├── bot/
│   │   └── main.py
│   ├── configuration/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── templates/
│   ├── core/
│   │   ├── settings.py
│   │   └── urls.py
│   ├── manage.py
│   └── .env
└── README.md
```

## Environment Variables

Create `final_proj/.env` locally or on the server:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

For production on PythonAnywhere:

```env
DJANGO_SECRET_KEY=your-production-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

Do not commit `.env` to git.

## Local Setup

From the project root:

```bash
cd final_proj
python -m venv .venv
source .venv/Scripts/activate
pip install --upgrade pip
pip install django pillow aiogram asgiref
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

On macOS/Linux, activate the virtual environment with:

```bash
source .venv/bin/activate
```

Open the site:

```text
http://127.0.0.1:8000/
```

## Running Tests

```bash
cd final_proj
python manage.py test configuration
```

## Running the Telegram Bot

Make sure `TELEGRAM_BOT_TOKEN` is set in `final_proj/.env`, then run:

```bash
cd final_proj
python bot/main.py
```

Available bot commands:

- `/start`
- `/help`
- `/items`
- `/become_a_part_of_the_team`

## PythonAnywhere Deployment

Clone the repository:

```bash
cd ~
git clone https://github.com/zacKerman112/final_project.git ShopBox
cd ~/ShopBox/final_proj
```

Create and activate a virtual environment:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install django pillow aiogram asgiref
```

Create `.env`, run migrations, and create an admin user:

```bash
nano .env
python manage.py migrate
python manage.py createsuperuser
python manage.py check
```

PythonAnywhere Web settings:

```text
Source code: /home/yourusername/ShopBox/final_proj
Working directory: /home/yourusername/ShopBox/final_proj
Virtualenv: /home/yourusername/ShopBox/final_proj/.venv
```

WSGI file:

```python
import os
import sys

path = '/home/yourusername/ShopBox/final_proj'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Static/media mapping:

```text
URL: /media/
Directory: /home/yourusername/ShopBox/final_proj/media
```

After changes, reload the web app in the PythonAnywhere Web tab.

## Security Notes

- Keep `DJANGO_SECRET_KEY` and `TELEGRAM_BOT_TOKEN` only in `.env`.
- Keep `DJANGO_DEBUG=False` in production.
- Add the deployed domain to `DJANGO_ALLOWED_HOSTS`.
- If a Telegram token was ever committed, revoke it in BotFather and create a new one.
