# Student Portal (Ustacky)

A web-based student application and management portal built with **Flask**, **MySQL**, **Bootstrap**, and **jQuery**. The portal enables prospective students to register, upload passport photographs, specify personal and academic details (including Nigerian State and Local Government Areas), and view their application profile. Administrators and staff can browse, search, and filter applicant records dynamically.

---

## Features

- **Applicant Registration**:
  - Personal Information (Names, Email, Phone, Date of Birth, Gender, Address, Next of Kin).
  - Academic Information (JAMB UTME score).
  - Passport / Profile image upload support (`static/uploads/`).
  - Dynamic State & Local Government Area (LGA) dependent dropdown (auto-populates LGAs based on selected Nigerian state using AJAX).
  - Form validation with flash message alerts.
- **Applicant Directory & Records Dashboard**:
  - Responsive table displaying applicant records.
  - Multi-criteria real-time search & filter using AJAX:
    - Search by full name.
    - Filter by admission status (*Admitted*, *Undecided*).
    - Filter by gender (*Male*, *Female*).
    - Filter by JAMB score.
- **Individual Student Profile View**:
  - Detailed student profile card showing photo, bio-data, state of origin, LGA, JAMB score, and admission status.

---

## Tech Stack

- **Backend**: Python 3, [Flask](https://flask.palletsprojects.com/)
- **Configuration**: [python-dotenv](https://github.com/theskumar/python-dotenv) for environment variables
- **Database**: [MySQL](https://www.mysql.com/) with `mysql-connector-python`
- **Frontend**: HTML5, CSS3, [Bootstrap 3](https://getbootstrap.com/), [jQuery](https://jquery.com/), [SweetAlert2](https://sweetalert2.github.io/)
- **Utilities**: `Werkzeug` (secure file uploads)

---

## Project Structure

```text
student portal/
├── app.py                  # Main Flask application and API routes
├── states_lgas.py          # Dictionary containing Nigerian States and LGAs
├── requirements.txt        # Project dependencies
├── .env.example            # Template for environment variables
├── .env                    # Local environment variables (git-ignored)
├── .gitignore              # Files ignored by Git
├── static/
│   ├── css/                # Bootstrap and custom stylesheets
│   ├── fonts/              # Glyphicons Halflings fonts
│   ├── js/                 # Bootstrap, jQuery, and custom AJAX logic (java.js)
│   └── uploads/            # Uploaded student passport images
├── templates/
│   ├── base.html           # Base layout template with navbar and footer
│   ├── index.html          # Landing / home page
│   ├── form.html           # Student registration form
│   ├── information.html    # Applicant list & search dashboard
│   └── profile.html        # Individual student profile view
└── README.md               # Project documentation
```

---

## Prerequisites

Ensure you have the following installed on your machine:
- **Python 3.10+** (Python 3.13 recommended)
- **MySQL Server** (local or remote)
- **Git**

---

## Database Setup

1. Start your MySQL server.
2. Log in to your MySQL terminal or GUI (e.g., MySQL Workbench, phpMyAdmin).
3. Create the database and table using the following SQL script:

```sql
CREATE DATABASE IF NOT EXISTS Flask_app;
USE Flask_app;

CREATE TABLE IF NOT EXISTS applicants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    dob DATE,
    gender VARCHAR(10),
    phone VARCHAR(20),
    address TEXT,
    state VARCHAR(50),
    lga VARCHAR(100),
    next_of_kin VARCHAR(150),
    jamb_score INT,
    admission_status VARCHAR(50) DEFAULT 'Undecided',
    image VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Installation & Setup

### 1. Clone or Open the Project
Open a terminal in the project directory:
```bash
cd "student portal"
```

### 2. Create and Activate a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**
```cmd
python -m venv venv
.\venv\Scripts\activate.bat
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all required libraries using `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the `.env.example` file to create your `.env` file:

```bash
cp .env.example .env
```
*(On Windows PowerShell: `Copy-Item .env.example .env`)*

Open `.env` and fill in your settings:
```env
# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_DEBUG=True
PORT=5000

# MySQL Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=Flask_app
DB_PORT=3306
```

### 5. Run the Application
Start the Flask development server:
```bash
python app.py
```

The app will start at:
```text
http://127.0.0.1:5000/
```

---

## Application Routes

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Home / landing page |
| `GET`, `POST` | `/form` | Student registration form |
| `POST` | `/submit` | Process application registration and file upload |
| `GET` | `/information` | View all submitted applicants in a table |
| `GET` | `/profile/<id>` | View details of a specific applicant |
| `GET` | `/get_lgas?state=<state_name>` | API returning JSON list of LGAs for a state |
| `GET` | `/search_students?...` | AJAX search endpoint filtering applicants dynamically |

---

## License

This project is licensed under the MIT License - feel free to adapt and build upon it.
