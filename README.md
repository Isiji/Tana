Tana River Office and Event Management System
Overview
The Tana River Office and Event Management System is a comprehensive web application designed to streamline the management of office tasks and events. This system is equipped with features for handling bills, statements, employee registers, committee records, motions, reminders, and event management. The project aims to enhance operational efficiency by providing a centralized platform for managing office and event-related activities.

Features
User Management: Secure user authentication and role-based access control.
Document Management: Upload, store, and download documents related to bills, statements, and other records.
Event Management: Create, view, and manage events on a calendar interface.
Employee Register: Track employee attendance and status (Present, Absent, Leave).
Committee Records: Manage and access records for various committees.
Motions: Add, edit, and view motions within the system.
Reminders: Set up and manage reminders for important tasks and events.
Technology Stack
Frontend:
HTML, CSS, Bootstrap
JavaScript for dynamic interactions
Backend:
Flask (Python web framework)
SQLAlchemy for ORM (Object-Relational Mapping)
Database:
SQLite or MySQL (depending on deployment needs)
Version Control:
Git (Repository hosted on GitHub)
Deployment:
Can be deployed on a local server or cloud services (e.g., Heroku, AWS)
Installation
Prerequisites
Before you begin, ensure you have the following installed:

Python 3.x
pip (Python package installer)
Virtualenv (recommended)
Steps
Clone the Repository:

bash
Copy code
git clone https://github.com/isiji/tana
cd tana-river-office-management-system
Create a Virtual Environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Set Up the Database:

Ensure your database is set up and configured in config.py. If using SQLite, the database will be created automatically. For MySQL or other databases, ensure your credentials are correctly set.


Usage
User Authentication:

Sign up or log in using the provided user interface.
Access different features based on user roles (Admin, Researcher, etc.).
Managing Documents:

Upload new documents or view existing ones through the dashboard.
Edit or delete documents as needed.
Event Management:

Add events to the calendar.
Hover over events to view details.
Edit or delete events directly from the calendar interface.
Employee Register:

Track employee attendance and manage their status.
Filter records by date or employee name.
Committee Records:

View and manage records for different committees.
Add new records or update existing ones.
Setting Reminders:

Create reminders for important tasks and deadlines.
Manage and view all reminders from the reminders page.