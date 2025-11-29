# Service Marketplace Platform

## Project Overview
This is a full-featured web application built using **Django**, designed to act as a two-sided service marketplace. It connects **clients (buyers)** looking for services with **sellers (freelancers)** offering their expertise.

The platform includes user authentication, separate profiles for clients and sellers, a service listing system, and dashboard views for managing listings and transactions.

## Features

- **Two-Sided Registration:** Separate registration and profile flows for Clients and Sellers.  
- **User Authentication:** Secure login and logout functionality.  
- **Service Listings:** Sellers can create, view, edit, and manage their service listings.  
- **Service Browsing:** Clients can browse and view all available services.  
- **User Dashboards:** Dedicated dashboards for clients and sellers to view relevant data, orders, and messages.  
- **Real-time Messaging (Planned):** Integration for private messaging between clients and sellers.  
- **Responsive Design:** Utilizes Bootstrap for a modern, mobile-friendly interface.  
- **Profile Management:** Users can update profile information, including avatar/profile image.  


## Setup and Installation

### 1. Prerequisites
Ensure you have the following installed:

- Python 3.9+
- pip (Python package installer)
- Virtual environment tool (recommended: `venv` or `conda`)

### 2. Clone the Repository
```bash
git clone https://github.com/codedbyasim/Service-Marketplace
cd Service-Marketplace
````

### 3. Create and Activate Virtual Environment

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**Linux/macOS:**

```bash
python -m venv venv
source venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt`, install key dependencies manually:

```bash
pip install django pillow
```

---

### 5. Database Migrations

Run database migrations to set up necessary tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Create Superuser (Admin)

Create an administrative user for accessing the Django admin panel:

```bash
python manage.py createsuperuser
```

---

### 7. Configure Static and Media Files

Ensure your `settings.py` is configured for static and media file handling:

```python
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

### 8. Run the Development Server

Start the application:

```bash
python manage.py runserver
```

The application will be accessible at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Usage

* **Register:** Navigate to `/accounts/register/` and choose to register as a Client or Seller.
* **Login:** Log in with your credentials.
* **Seller Actions:** Use the "Sell a Service" link or dashboard to create new listings.
* **Client Actions:** Browse services on the homepage (`/`) and engage with sellers.
* **Profile Update:** Use "Edit Profile" to upload an avatar/profile image.

---

## Project Structure

```
Service-Marketplace/
├── accounts/            # User authentication, registration, profiles (Seller/Client models)
├── services/            # Service listing management (Service model, views for creation, viewing)
├── service_marketplace/ # Project settings and URL configurations
├── templates/           # Base templates including base.html and messages.html
└── media/               # Directory for user-uploaded files (profile/service images)
```

---

## Technologies Used

* **Backend:** Python 3.9.12, Django
* **Database:** SQLite (default), PostgreSQL (production)
* **Frontend:** HTML5, CSS3, JavaScript
* **Styling:** Bootstrap 5
* **File Handling:** Django's ImageField (requires Pillow)

