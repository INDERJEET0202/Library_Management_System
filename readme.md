# Library Management System

This repository contains a Library Management System (LMS) designed to facilitate efficient library operations. It offers distinct functionalities for users, librarians, and administrators.

## About Project

The Library Management System is a comprehensive application designed to streamline library operations efficiently. With distinct sections for users, librarians, and administrators, it offers a range of functionalities.

Users can create accounts, request books, read allocated books, and access personalized activity statistics. Librarians have control over library inventory, including adding/deleting sections and books, managing user requests, and assigning/restricting book access. Administrators oversee user roles and permissions.

Implemented with Vue3 for the frontend, Flask for the backend, and SQLite3 for the database, the system ensures smooth performance and reliability. Celery manages scheduled tasks such as sending reminders and activity reports, while Redis optimizes data caching for enhanced performance.

To start the application, follow the provided instructions for both frontend and backend setup.

## Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![NPM](https://img.shields.io/badge/NPM-%23CB3837.svg?style=for-the-badge&logo=npm&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)

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
    - Create a `.env` file and add the required environment variables (for now only add the remote redis url).
    - Run `python3 app.py` to start the backend server.

For detailed instructions, refer to the documentation of each sections.

## Contributors

    - [Indrajit (Me only)]
    - [With the help of some resources like CHAT GPT, Stack Overflow, etc.]

## License

This project is licensed under the MIT License 
MIT License

Copyright (c) [2024] [Indrajit]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
