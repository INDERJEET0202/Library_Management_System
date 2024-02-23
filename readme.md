# Library Management System

This repository contains a Library Management System (LMS) designed to facilitate efficient library operations. It offers distinct functionalities for users, librarians, and administrators.

## About Project

The Library Management System is a comprehensive application designed to streamline library operations efficiently. With distinct sections for users, librarians, and administrators, it offers a range of functionalities.

Users can create accounts, request books, read allocated books, and access personalized activity statistics. Librarians have control over library inventory, including adding/deleting sections and books, managing user requests, and assigning/restricting book access. Administrators oversee user roles and permissions.

Implemented with Vue3 for the frontend, Flask for the backend, and SQLite3 for the database, the system ensures smooth performance and reliability. Celery manages scheduled tasks such as sending reminders and activity reports, while Redis optimizes data caching for enhanced performance.

To start the application, follow the provided instructions for both frontend and backend setup.

## Tech Stack
<img alt="Static Badge" src="https://img.shields.io/badge/Python-blue?style=plastic&logo=python&logoColor=yellow"> 
<img alt="Static Badge" src="https://img.shields.io/badge/SQLite_3-brightgreen?style=plastic&logo=sqlite&logoColor=white" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white" height="25"> 
<img alt="Static Badge" src="https://img.shields.io/badge/Flask_Security_too-black?style=plastic&logo=flask&logoColor=white" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/Redis-%23ae1710?style=plastic&logo=redis&logoColor=white" height="25"> 
<img alt="Static Badge" src="https://img.shields.io/badge/Celery-brightgreen?style=plastic&logo=celery&logoColor=black" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/Messaging_Queues-orange?style=plastic&logo=stackexchange&logoColor=white" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/Git-%23ae1710?style=plastic&logo=git&logoColor=white" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/NPM-magenta?style=plastic&logo=npm&logoColor=white" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/Javascript-yellow?style=plastic&logo=Javascript&logoColor=black" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/VueJS-grey?style=plastic&logo=vue.js&logoColor=green" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/REST_API-%23f4f8af?style=plastic&logo=academia&logoColor=purple" height="25">
<img alt="Static Badge" src="https://img.shields.io/badge/Postman-white?style=plastic&logo=postman&logoColor=red" height="25">

## Features

- **User Section**: Users can create accounts, request books, read allocated books, view activity statistics, and search for books based on sections or titles.
- **Librarian Section**: Librarians can manage library inventory, add/delete sections and books, handle user requests, and assign/revoke book access.
- **Admin Section**: Administrators can assign roles to users, granting them privileges as admins, librarians, or regular users.
- **Technology Stack**: Frontend built with Vue3, backend with Flask, and SQLite3 for the database.
- **RESTful API**: The system is equipped with a robust API, ensuring seamless communication between the frontend and backend.
- **Authentication and Authorization**: User login and registration are secured with authentication and authorization using Flask JWT.
- **Asynchronous Task Processing**: Celery is used for asynchronous task processing, ensuring efficient performance.
- **Scheduled Tasks**: Celery manages scheduled jobs like sending reminders and monthly activity reports.
- **Data Caching**: Redis is utilized for efficient data caching, enhancing performance.

## Getting Started

Follow these steps to set up and run the application (make sure you have `npm` , `python3` and `redis` installed):

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
