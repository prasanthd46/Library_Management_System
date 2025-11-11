<div align="center">

# ✨ Library Management System API ✨

</div>

<p align="center">
  <a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://www.sqlalchemy.org/">
    <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  </a>
  <a href="https://pydantic-docs.helpmanual.io/">
    <img src="https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white" alt="Pydantic">
  </a>
</p>

<p align="center">
  A RESTful API for a digital library, built with Python and FastAPI for the CreativeScript intern assignment.
</p>

---

### ✅ Core Features

-   **Full CRUD Operations:** Create, Read, Update (`PATCH`), and Delete for Books and Authors.
-   **Secure Authentication:** JWT-based authentication using the OAuth2 Password Flow.
-   **User Management:** User registration and login with secure password hashing using `passlib` and `bcrypt`.
-   **Borrowing System:** Endpoints for users to borrow and return books, automatically updating book availability.
-   **Data Validation:** Robust request/response validation using Pydantic, ensuring data integrity.
-   **Database Integration:** SQLAlchemy ORM for seamless interaction with a SQLite database, including cascade deletes for robust data consistency.

---

## 🚀 Getting Started

Follow these instructions to get a local copy up and running for development and testing.

### Prerequisites

-   Python 3.11+
-   `pip` and `venv` for package management

### 🛠️ Installation & Setup

1.  **Clone the Repository**
    ```
    git clone https://github.com/your-username/Library_Management_System.git
    cd Library_Management_System
    ```

2.  **Create and Activate a Virtual Environment**
    -   *On Windows:*
        ```
        python -m venv venv
        .\venv\Scripts\activate
        ```
    -   *On macOS/Linux:*
        ```
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies**
    ```
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    -   Create a `.env` file by copying the example template. This holds your secrets and is ignored by Git.
        -   *On Windows:* `copy .env.example .env`
        -   *On macOS/Linux:* `cp .env.example .env`
    -   Open the new `.env` file and replace the placeholder `SECRET_KEY` with your own unique, random string. This is critical for security.

5.  **Run the Application**
    -   Start the development server with Uvicorn.
        ```
        uvicorn app.main:app --reload
        ```

6.  **Explore the API**
    -   The API is now live at `http://127.0.0.1:8000`.
    -   Navigate to **`http://127.0.0.1:8000/docs`** to access the interactive Swagger UI.

---

## ▶️ Example API Workflow

Use the interactive docs at **`http://127.0.0.1:8000/docs`** to test the full API flow.

> **Note:** All endpoints except `/register` are protected. You must authorize your session first.

1.  **👤 Register a User**
    -   Go to `POST /api/v1/auth/register` and provide an email and password.

2.  **🔑 Authorize Your Session**
    -   At the top-right of the `/docs` page, click the **"Authorize"** button.
    -   Enter the `username` (email) and `password` you just registered with and click "Authorize".
    -   The padlock icon will lock, indicating your session is active.

3.  **✒️ Create an Author**
    -   Go to `POST /api/v1/authors/` and provide the author's details.

4.  **📖 Create a Book**
    -   Go to `POST /api/v1/books/` and provide the book's details, using the `author_id` from the previous step.

5.  **🛒 Borrow a Book**
    -   Go to `POST /api/v1/borrow/` and provide the `book_id` of the book you just created.

6.  **↩️ Return the Book**
    -   Go to `POST /api/v1/return/{record_id}` using the `id` of the borrow record.

---

## 🗺️ API Endpoints Reference

All endpoints are prefixed with `/api/v1`. Endpoints marked with 🔒 are protected and require an `Authorization: Bearer <TOKEN>` header.

| Endpoint                     | Method | Description                                                                    |
| :--------------------------- | :----- | :----------------------------------------------------------------------------- |
| **Authentication**           |        |                                                                                |
| `/auth/register`             | `POST` | Creates a new user.                                                            |
| `/auth/login`                | `POST` | Logs in a user and returns a JWT access token.                                 |
| **Authors** 👨‍💼               |        |                                                                                |
| `/authors/`                  | `POST` | 🔒 Creates a new author.                                                       |
| `/authors/`                  | `GET`  | 🔒 Gets a list of all authors.                                                 |
| `/authors/{author_id}`       | `GET`  | 🔒 Gets a single author by their ID.                                           |
| **Books** 📚                   |        |                                                                                |
| `/books/`                    | `POST` | 🔒 Creates a new book (must provide a valid `author_id`).                        |
| `/books/`                    | `GET`  | 🔒 Gets a list of all books. Supports query parameters for `search` and `is_available`. |
| `/books/{book_id}`           | `GET`  | 🔒 Gets a single book by its ID.                                               |
| `/books/{book_id}`           | `PATCH`| 🔒 Partially updates a book's details (e.g., title, availability).             |
| `/books/{book_id}`           | `DELETE`| 🔒 Deletes a book by its ID.                                                   |
| **Borrowing** 🔄              |        |                                                                                |
| `/borrow`                    | `POST` | 🔒 Borrows a book, creating a `BorrowRecord` and setting the book as unavailable. |
| `/return/{record_id}`        | `POST` | 🔒 Returns a book, updating the `BorrowRecord` and setting the book as available.  |
| `/borrow/history`            | `GET`  | 🔒 Gets the current logged-in user's borrowing history.                        |

---

## 🛡️ Security Considerations

-   **Password Hashing:** User passwords are never stored in plaintext. They are hashed using the robust `bcrypt` algorithm via the `passlib` library.
-   **JWT Authentication:** Access to protected endpoints is controlled via JSON Web Tokens (JWTs), which are generated upon successful login.
-   **Dependency Injection:** FastAPI's dependency injection system is used to manage user authentication, ensuring that protected routes can only be accessed by valid, authenticated users.
-   **Environment Variables:** Sensitive information like the JWT `SECRET_KEY` is loaded from a `.env` file, which is explicitly excluded from version control in `.gitignore`.

---

## 🗄️ Database

-   The application uses **SQLite** for its database, which is lightweight and file-based.
-   The database file (`library.db`) is automatically created in the project root when the application first runs.
-   The database schema is defined and managed declaratively through SQLAlchemy ORM models in `app/models.py`.
-   Relationships between tables (e.g., Books-Authors, Users-Borrows) are configured with `ondelete="CASCADE"` rules at the database level to ensure data integrity upon deletion.
