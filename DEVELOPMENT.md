# 🧑‍💻 Development Experience

This document details the development experience, challenges, and learnings from building the Library Management System API, as requested by the assignment guidelines.

---

### What challenges did you face while building this?

During development, two major challenges stood out that tested my understanding of backend systems beyond basic feature implementation:

1.  **Database Integrity on Deletion:** The most significant challenge was a `500 Internal Server Error` when trying to delete a `Book` that had been borrowed. The application would crash with a `sqlite3.IntegrityError`. This occurred because the application was trying to orphan a `BorrowRecord` by setting its `book_id` to `NULL`, which the database schema correctly forbids.

2.  **Environment Variable Type Mismatches:** The application would fail when creating JWTs, throwing a `TypeError`. This was because the token expiration time, loaded from the `.env` file via `os.getenv()`, was being read as a string (`"30"`) instead of the required integer (`30`), which the `timedelta` function could not process.

### How did you solve them?

I solved these challenges by diagnosing the root cause from the traceback and implementing robust, standard-practice solutions:

1.  **Solving the IntegrityError:** The solution was to establish a proper cascade behavior for the database relationship. I configured `ondelete="CASCADE"` on the `ForeignKey` constraints in the `Borrow` model (`app/models.py`). This tells the database to automatically delete child `Borrow` records whenever their parent `Book` is deleted, ensuring data integrity is always maintained.

2.  **Solving the TypeError:** The fix was to explicitly cast the environment variable to its correct type immediately after loading it. In `app/security.py`, I changed the call from `os.getenv(...)` to `int(os.getenv(...))`, ensuring that the application logic always receives data in the format it expects.

### What would you do differently if you had more time?

Given more time, I would focus on performance, scalability, and maintainability:

-   **Advanced Project Structure:** While the current structure is good, for a larger application I would implement a more advanced, domain-driven structure. I would create a top-level `app/` directory and organize the code into sub-packages by feature (e.g., `app/users/`, `app/books/`, `app/core/`). Each package would contain its own `models.py`, `schemas.py`, `crud.py`, and `router.py`. This would make the application much more modular and easier to scale.

-   **Implement True Asynchronous Operations:** My entire application is currently synchronous (`def`). The biggest performance improvement would be to refactor all database-dependent endpoints and `crud` functions to be fully asynchronous (`async def`). This would involve using an async database driver (like `asyncpg` for PostgreSQL) to prevent blocking the event loop on database calls, dramatically increasing the API's concurrency and speed.

### What did you learn from this assignment?

This assignment provided several critical insights into modern web development and best practices:

-   **Stateless (JWT) vs. Stateful (Session) Auth:** I learned the difference between the two main auth methods even in depth for python ecosystem. The PDF required an "access token" (JWT), which is a **stateless** method. This is the standard for modern, "decoupled" APIs (like for mobile apps) because the server doesn't need to store session data. The token *is* the proof of identity.

-   **Data Integrity (`ForeignKey` vs. `relationship`):** I learned that `ForeignKey` is the *physical database rule* that prevents "orphan" records, while `relationship` is the *Python/ORM helper* that lets me write clean code like `my_book.author`. I also learned how `cascade="all, delete-orphan"` works as a "parent-to-child" delete instruction within the ORM.

-   **Pydantic V2 & PATCH Logic:** I learned that `.model_dump(exclude_unset=True)` is the *only* correct way to handle a `PATCH` request. It creates a dictionary of *only* the fields the user actually sent, which prevents me from accidentally erasing other fields with `NULL` or default values.

-   **Login: `form-data` vs. JSON:** I learned that while the "official" FastAPI/OAuth2 docs use `x-www-form-urlencoded` data for login, it's cleaner for modern frontends (like React or mobile apps) to send a simple JSON body. I implemented the JSON method by creating a `UserLogin` schema and using it directly, which simplified the process for the client.
