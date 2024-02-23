# Library Management System

This repository contains a Library Management System (LMS) designed to facilitate efficient library operations. It offers distinct functionalities for users, librarians, and administrators.

## About Project

The Library Management System is a comprehensive application designed to streamline library operations efficiently. With distinct sections for users, librarians, and administrators, it offers a range of functionalities.

Users can create accounts, request books, read allocated books, and access personalized activity statistics. Librarians have control over library inventory, including adding/deleting sections and books, managing user requests, and assigning/restricting book access. Administrators oversee user roles and permissions.

Implemented with Vue3 for the frontend, Flask for the backend, and SQLite3 for the database, the system ensures smooth performance and reliability. Celery manages scheduled tasks such as sending reminders and activity reports, while Redis optimizes data caching for enhanced performance.

To start the application, follow the provided instructions for both frontend and backend setup.

## Features

- **User Section**: Users can create accounts, request books, read allocated books, view activity statistics, and search for books based on sections or titles.
- **Librarian Section**: Librarians can manage library inventory, add/delete sections and books, handle user requests, and assign/revoke book access.
- **Admin Section**: Administrators can assign roles to users, granting them privileges as admins, librarians, or regular users.
- **Technology Stack**: Frontend built with Vue3, backend with Flask, and SQLite3 for the database.
- **Scheduled Tasks**: Celery manages scheduled jobs like sending reminders and monthly activity reports.
- **Data Caching**: Redis is utilized for efficient data caching, enhancing performance.

## Getting Started

Follow these steps to set up and run the application:

1. **Frontend Setup**:

   - Navigate to the `frontend` directory and run `npm init`.
   - Run `npm run serve` to start the frontend server at `http://localhost:8080/
   - To build the frontend, run `npm run build`

2. **Backend Setup**:

    - Navigate to the `backend` directory and set up the environment.
    - Execute `scripts/start_celery.sh` and `scripts/start_redis.sh`.
    - Create a virtual environment and install dependencies from `requirements.txt`.
    - Run `python3 app.py` to start the backend server.

For detailed instructions, refer to the documentation of each sections.

## Contributors

    - [Indrajit (Me only)]
    - [With the help of some resources like CHAT GPT, Stack Overflow, etc.]

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
