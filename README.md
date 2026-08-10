# Software License Management System

A full-stack web application for tracking and managing software licenses, vendors, and users within an organization. Built with a relational MySQL schema featuring stored procedures, triggers, and functions to automate license lifecycle management.

## Features

- **License Management** — Add, update, and track software licenses with automatic status handling (active/expired) via database triggers
- **Vendor Management** — Maintain vendor records with contact details and active status
- **User Management** — Track users associated with license usage
- **License Renewal** — One-click renewal via a MySQL stored procedure
- **Dashboard Analytics** — Vendor-wise license counts, active/expired breakdowns
- **Advanced Queries** — Nested subqueries, joins, and aggregate reporting on license usage

## Tech Stack

- **Backend:** Python, Flask
- **Alternative UI:** Streamlit
- **Database:** MySQL (stored procedures, triggers, functions)
- **Frontend:** HTML, CSS, Jinja2 templates

## Project Structure

```
├── app.py              # Flask application and routes
├── main.py             # Streamlit alternative interface
├── db_config.py        # Database connection configuration
├── static/
│   └── style.css        # Stylesheet
├── templates/
│   ├── base.html         # Base layout with navigation
│   ├── dashboard.html    # Analytics dashboard
│   ├── licenses.html     # License listing
│   ├── vendors.html      # Vendor listing
│   ├── users.html        # User listing
│   ├── add_license.html  # Add license form
│   ├── add_vendor.html   # Add vendor form
│   └── add_user.html     # Add user form
└── requirements.txt
```

## Database Design

The system uses a normalized relational schema with the following core tables:

- `LICENSE` — license records with auto-managed status
- `VENDOR` — vendor/supplier records
- `USER` — application users
- `SOFTWARE_PRODUCT` — products tied to licenses
- `USER_BUYS_PRODUCT`, `USER_MANAGES_LICENSE` — relationship tables

**Database logic includes:**
- A trigger to automatically update `license_status` on insert/update
- A stored procedure (`renew_license`) to handle license renewal
- A stored procedure (`add_software_product`) to register new products
- A function (`get_license_days_left`) to calculate remaining license validity

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a MySQL database named `software_license_management` and set up tables matching the structure described above, along with the trigger, stored procedures, and function referenced in the code
4. Update the database credentials in `db_config.py` (for the Flask app) and `main.py` (for the Streamlit app) to match your local MySQL setup
5. Run the Flask app:
   ```bash
   python app.py
   ```
   or the Streamlit interface:
   ```bash
   streamlit run main.py
   ```

## Notes

This project was built to explore relational database design patterns — particularly using triggers, stored procedures, and functions to move business logic (status updates, renewal handling) into the database layer rather than the application layer.
