# 🚀 REST API with Python, FastAPI & SQLAlchemy

> **Spring Boot → FastAPI / Python**
>
> A practical REST API project demonstrating **CRUD operations, FastAPI, Uvicorn, Pydantic validation, SQLAlchemy ORM, Repository pattern, Service layer, and MySQL**.

---

## 📌 Project Overview

This project demonstrates how to build a **layered REST API using Python and FastAPI**, following an architecture that is very familiar to **Spring Boot developers**.

### 🛠️ Technologies Used

| Technology              | Purpose                     |
| ----------------------- | --------------------------- |
| 🐍 Python               | Programming language        |
| ⚡ FastAPI               | REST API framework          |
| 🚀 Uvicorn              | ASGI application server     |
| 🧩 Pydantic             | Request/response validation |
| 🗄️ SQLAlchemy          | ORM / database interaction  |
| 🐬 MySQL                | Relational database         |
| 📦 REST API             | CRUD operations             |
| 💉 Dependency Injection | FastAPI `Depends()`         |

---

# 🏗️ Project Architecture

If you already know Spring Boot, the easiest way to understand this project is:

```text
Spring Boot
     │
     │  Same architectural thinking
     ▼
FastAPI + SQLAlchemy
```

The application follows:

```text
Client
  │
  ▼
Controller
  │
  ▼
Service
  │
  ▼
Repository
  │
  ▼
SQLAlchemy Model
  │
  ▼
MySQL
```

---

# 🔄 Application Request Flow

```mermaid
flowchart TD

    A["🌐 Client<br/>Postman / Browser / Frontend"]
    B["⚡ FastAPI Router<br/>Controller"]
    C["🧠 Service Layer<br/>Business Logic"]
    D["📦 Repository Layer<br/>Database Operations"]
    E["🗄️ SQLAlchemy ORM<br/>Model"]
    F["🐬 MySQL Database"]

    A -->|"HTTP Request"| B
    B -->|"Validated Data"| C
    C -->|"Business Operation"| D
    D -->|"ORM Query"| E
    E -->|"SQL"| F

    F -->|"Result"| E
    E -->|"Mapped Object"| D
    D -->|"Data"| C
    C -->|"Response"| B
    B -->|"HTTP Response"| A
```

### ⭐ Remember the flow

> **Client → Controller → Service → Repository → SQLAlchemy → MySQL**

And the response travels back in the opposite direction.

---

# 📁 Project Structure

```text
rest-api-with-python/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── controllers/
│   │   └── user_controller.py
│   │
│   ├── services/
│   │   └── user_service.py
│   │
│   ├── repositories/
│   │   └── user_repository.py
│   │
│   ├── models/
│   │   └── user.py
│   │
│   ├── schemas/
│   │   └── user_schema.py
│   │
│   └── database/
│       └── connection.py
│
├── requirements.txt
├── .env
└── README.md
```

---

# 🧩 Responsibility of Each Layer

| Layer         | Responsibility                      |
| ------------- | ----------------------------------- |
| 🌐 Controller | Handles HTTP requests and responses |
| 🧠 Service    | Contains business logic             |
| 📦 Repository | Performs database operations        |
| 🗄️ Model     | Represents database tables          |
| ✅ Schema      | Validates API request/response data |
| 🔌 Database   | Creates and manages DB connection   |
| ⚡ Uvicorn     | Runs the FastAPI application        |

---

# 🔁 Complete POST Request Flow

Suppose the client sends:

### `POST /users`

```json
{
  "name": "John",
  "email": "john@example.com"
}
```

The request moves through the application:

```mermaid
flowchart LR

    A["🌐 POST /users<br/>JSON Request"]
    B["⚡ Controller<br/>user_controller.py"]
    C["✅ Pydantic<br/>UserCreate"]
    D["🧠 Service<br/>user_service.py"]
    E["📦 Repository<br/>user_repository.py"]
    F["🗄️ SQLAlchemy<br/>User Model"]
    G["🐬 MySQL"]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
```

### What happens?

1. Client sends HTTP request.
2. FastAPI receives the request.
3. Pydantic validates the JSON.
4. Controller calls the service.
5. Service executes business logic.
6. Repository performs database operation.
7. SQLAlchemy generates SQL.
8. MySQL stores the data.
9. Response travels back to the client.

---

# 🧠 Spring Boot → FastAPI Mental Model

This is the most important section if you're a **Java/Spring Boot developer learning Python**.

| ☕ Spring Boot     | 🐍 FastAPI / Python                |
| ----------------- | ---------------------------------- |
| `@RestController` | `APIRouter`                        |
| Controller        | `controllers/`                     |
| `@Service`        | `services/`                        |
| Service class     | Service module/class               |
| `@Repository`     | `repositories/`                    |
| `JpaRepository`   | Repository using SQLAlchemy        |
| `@Entity`         | SQLAlchemy Model                   |
| Entity package    | `models/`                          |
| DTO               | Pydantic Schema                    |
| JPA / Hibernate   | SQLAlchemy                         |
| `@Autowired`      | `Depends()` / Dependency Injection |
| `@GetMapping`     | `@router.get()`                    |
| `@PostMapping`    | `@router.post()`                   |
| `@PutMapping`     | `@router.put()`                    |
| `@DeleteMapping`  | `@router.delete()`                 |
| `@PathVariable`   | Path Parameter                     |
| `@RequestParam`   | Query Parameter                    |
| `@RequestBody`    | Pydantic Model                     |
| `ResponseEntity`  | FastAPI Response                   |
| Tomcat            | Uvicorn / ASGI Server              |

---

# 🎯 Spring Boot vs FastAPI Architecture

```mermaid
flowchart LR

    A["☕ Spring Boot"]
    B["🐍 FastAPI"]

    A1["@RestController"]
    A2["@Service"]
    A3["@Repository"]
    A4["@Entity"]
    A5["DTO"]
    A6["JPA / Hibernate"]

    B1["APIRouter"]
    B2["Service Layer"]
    B3["Repository Layer"]
    B4["SQLAlchemy Model"]
    B5["Pydantic Schema"]
    B6["SQLAlchemy"]

    A1 -.->|"Equivalent Concept"| B1
    A2 -.->|"Equivalent Concept"| B2
    A3 -.->|"Equivalent Concept"| B3
    A4 -.->|"Equivalent Concept"| B4
    A5 -.->|"Equivalent Concept"| B5
    A6 -.->|"Equivalent Concept"| B6
```

---

# 🌐 Controller Layer

In FastAPI, the controller is commonly implemented using `APIRouter`.

### Spring Boot

```java
@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping
    public User createUser(@RequestBody UserDto user) {
        return userService.createUser(user);
    }
}
```

### FastAPI

```python
from fastapi import APIRouter, Depends

from schemas.user_schema import UserCreate
from services.user_service import UserService


router = APIRouter(prefix="/users")


@router.post("/")
def create_user(
    user: UserCreate,
    service: UserService = Depends()
):
    return service.create_user(user)
```

### Mental model

```text
Spring Boot

@RestController
       │
       ▼
Controller Method
       │
       ▼
Service


FastAPI

APIRouter
   │
   ▼
Route Function
   │
   ▼
Service
```

---

# 🧠 Service Layer

The service layer contains **business logic**.

Example:

```python
class UserService:

    def __init__(self, repository):
        self.repository = repository

    def create_user(self, user):

        existing_user = self.repository.find_by_email(
            user.email
        )

        if existing_user:
            raise ValueError(
                "User already exists"
            )

        return self.repository.save(user)
```

### Why Service Layer?

Don't put business logic directly inside the controller.

❌ Avoid:

```text
Controller
   │
   ├── Validation
   ├── Business Logic
   ├── SQL Query
   └── Response
```

Prefer:

```text
Controller
    │
    ▼
Service
    │
    ▼
Repository
```

This keeps the application easier to maintain and test.

---

# 📦 Repository Layer

The repository is responsible for **database operations**.

Example:

```python
class UserRepository:

    def __init__(self, db):
        self.db = db

    def save(self, user):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def find_by_id(self, user_id):

        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def find_all(self):

        return self.db.query(User).all()
```

### Mental model

```text
Service
   │
   │ "I need user data"
   ▼
Repository
   │
   │ SQLAlchemy
   ▼
Database
```

---

# 🗄️ SQLAlchemy Model

A SQLAlchemy model represents a **database table**.

### Spring Boot Entity

```java
@Entity
public class User {

    @Id
    private Long id;

    private String name;

    private String email;
}
```

### SQLAlchemy Model

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    email: Mapped[str] = mapped_column(
        String(255)
    )
```

---

# 🔐 Pydantic Schema = DTO

Pydantic is mainly responsible for **API data validation and serialization**.

### Spring Boot DTO

```java
public class UserDto {

    private String name;

    private String email;
}
```

### FastAPI Pydantic Schema

```python
from pydantic import BaseModel


class UserCreate(BaseModel):

    name: str

    email: str
```

---

# 🆚 SQLAlchemy Model vs Pydantic Schema

This distinction is extremely important.

```mermaid
flowchart TD

    A["🌐 HTTP Request"]
    B["✅ Pydantic Schema<br/>API Validation"]
    C["🧠 Service"]
    D["🗄️ SQLAlchemy Model<br/>Database Representation"]
    E["🐬 MySQL"]

    A --> B
    B --> C
    C --> D
    D --> E
```

### Simple rule

```text
Pydantic
   │
   └── API data
       Request / Response


SQLAlchemy
   │
   └── Database data
       Tables / Rows
```

### Never confuse them

| Pydantic               | SQLAlchemy            |
| ---------------------- | --------------------- |
| API validation         | Database mapping      |
| Request data           | Database row          |
| Response serialization | ORM operations        |
| DTO equivalent         | Entity equivalent     |
| `BaseModel`            | Declarative ORM Model |

---

# 🔄 CRUD Operations

This project follows the standard CRUD pattern.

```mermaid
flowchart LR

    A["🌐 Client"]

    B["➕ CREATE<br/>POST"]
    C["📖 READ<br/>GET"]
    D["✏️ UPDATE<br/>PUT"]
    E["🗑️ DELETE<br/>DELETE"]

    F["⚡ FastAPI"]
    G["🧠 Service"]
    H["📦 Repository"]
    I["🗄️ SQLAlchemy"]
    J["🐬 MySQL"]

    A --> B
    A --> C
    A --> D
    A --> E

    B --> F
    C --> F
    D --> F
    E --> F

    F --> G
    G --> H
    H --> I
    I --> J

    J --> I
    I --> H
    H --> G
    G --> F
    F --> A
```

---

# 📋 REST API Endpoints

| HTTP Method | Endpoint      | Purpose        |
| ----------- | ------------- | -------------- |
| `POST`      | `/users`      | Create user    |
| `GET`       | `/users`      | Get all users  |
| `GET`       | `/users/{id}` | Get user by ID |
| `PUT`       | `/users/{id}` | Update user    |
| `DELETE`    | `/users/{id}` | Delete user    |

---

# 🚀 Uvicorn Server

FastAPI needs an ASGI server to run.

The commonly used server is **Uvicorn**.

```bash
uvicorn app.main:app --reload
```

### Meaning

```text
uvicorn
   │
   └── ASGI Server

app.main
   │
   └── main.py

app
   │
   └── FastAPI application object
```

Example:

```python
from fastapi import FastAPI

app = FastAPI()
```

Run:

```bash
uvicorn app.main:app --reload
```

---

# 📚 FastAPI Automatic Documentation

FastAPI automatically provides API documentation.

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

The documentation allows you to:

* View API endpoints
* See request models
* See response models
* Send API requests
* Test CRUD operations

---

# 🔒 Pydantic Validation Example

Suppose our schema is:

```python
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):

    name: str

    email: EmailStr
```

Valid request:

```json
{
    "name": "John",
    "email": "john@example.com"
}
```

Invalid request:

```json
{
    "name": "John",
    "email": "not-an-email"
}
```

FastAPI + Pydantic can reject invalid data before it reaches the business/database layer.

```text
HTTP Request
     │
     ▼
Pydantic Validation
     │
     ├── ❌ Invalid → 422 Response
     │
     └── ✅ Valid
            │
            ▼
         Service
```

---

# 💉 Dependency Injection

Spring Boot developers are already familiar with Dependency Injection.

### Spring Boot

```java
@Autowired
private UserService userService;
```

### FastAPI

FastAPI commonly uses:

```python
Depends()
```

Example:

```python
from fastapi import Depends


@router.get("/{user_id}")
def get_user(
    user_id: int,
    service: UserService = Depends()
):
    return service.get_user(user_id)
```

### Mental Model

```text
Spring Boot

@Autowired
    │
    ▼
Dependency Injection


FastAPI

Depends()
    │
    ▼
Dependency Injection
```

---

# 🏛️ Complete Architecture

```mermaid
flowchart TD

    A["🌐 Client<br/>Frontend / Postman"]

    B["⚡ FastAPI<br/>Controller / Router"]

    C["✅ Pydantic<br/>Validation"]

    D["🧠 Service Layer<br/>Business Logic"]

    E["📦 Repository Layer<br/>Database Operations"]

    F["🗄️ SQLAlchemy ORM<br/>Models"]

    G["🐬 MySQL<br/>Database"]

    A -->|"HTTP Request"| B
    B -->|"Validate"| C
    C -->|"Valid Data"| D
    D -->|"Business Operation"| E
    E -->|"ORM Operation"| F
    F -->|"SQL Query"| G

    G -->|"Database Result"| F
    F -->|"ORM Object"| E
    E -->|"Data"| D
    D -->|"Response Data"| B
    B -->|"HTTP Response"| A
```

---

# 🧠 The Most Important Mental Model

If you are a **Java Full Stack / Spring Boot developer**, remember this:

```text
             🌐 CLIENT
                 │
                 ▼
        ⚡ FASTAPI CONTROLLER
                 │
                 ▼
          🧠 SERVICE LAYER
          Business Logic
                 │
                 ▼
        📦 REPOSITORY LAYER
         Database Operations
                 │
                 ▼
          🗄️ SQLALCHEMY
              ORM
                 │
                 ▼
             🐬 MYSQL
```

### One-line memory trick

> **Controller → Service → Repository → ORM → Database**

---

# ☕ Spring Boot Developer Cheat Sheet

```text
Spring Boot                         FastAPI
────────────────────────────────────────────────────

@RestController              →      APIRouter

@RequestMapping              →      APIRouter(prefix=...)

@GetMapping                   →      @router.get()

@PostMapping                  →      @router.post()

@PutMapping                   →      @router.put()

@DeleteMapping                →      @router.delete()

@PathVariable                 →      Path Parameter

@RequestParam                 →      Query Parameter

@RequestBody                  →      Pydantic Model

@Service                      →      Service Layer

@Repository                   →      Repository Layer

@Entity                       →      SQLAlchemy Model

@Id                           →      primary_key=True

DTO                           →      Pydantic BaseModel

JPA / Hibernate               →      SQLAlchemy

@Autowired                    →      Depends()

Tomcat                        →      Uvicorn / ASGI Server
```

---

# 🎯 Why This Architecture?

A layered architecture separates responsibilities.

```text
Controller
   │
   │ HTTP responsibility
   ▼
Service
   │
   │ Business responsibility
   ▼
Repository
   │
   │ Database responsibility
   ▼
SQLAlchemy
   │
   │ ORM responsibility
   ▼
MySQL
```

### Benefits

✅ Separation of concerns
✅ Easier unit testing
✅ Easier maintenance
✅ Reusable business logic
✅ Cleaner controllers
✅ Database logic stays isolated
✅ Easy for large applications to scale

---

# 🛠️ Installation

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy pymysql pydantic python-dotenv
```

Or:

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

Start the FastAPI application:

```bash
uvicorn app.main:app --reload
```

Application:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# 🗄️ Database Configuration

Example `.env`:

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/mydatabase
```

Database connection:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from os import getenv


DATABASE_URL = getenv("DATABASE_URL")


engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
```

---

# 🔌 Database Dependency

A database session can be provided to API operations using FastAPI dependency injection.

```python
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
```

Then:

```python
@router.get("/users")
def get_users(
    db = Depends(get_db)
):
    ...
```

### Flow

```text
HTTP Request
     │
     ▼
FastAPI
     │
     ▼
Depends(get_db)
     │
     ▼
Create DB Session
     │
     ▼
Repository
     │
     ▼
MySQL
     │
     ▼
Close DB Session
```

---

# 📊 End-to-End Architecture

```mermaid
flowchart TB

    Client["🌐 Client<br/>Browser / Postman / Frontend"]

    API["⚡ FastAPI Application"]

    Router["🎯 Controller / APIRouter"]

    Validation["✅ Pydantic<br/>Request Validation"]

    Service["🧠 Service Layer<br/>Business Logic"]

    Repository["📦 Repository Layer<br/>CRUD / Queries"]

    ORM["🗄️ SQLAlchemy ORM"]

    DB["🐬 MySQL"]

    Client -->|"HTTP"| API
    API --> Router
    Router --> Validation
    Validation --> Service
    Service --> Repository
    Repository --> ORM
    ORM --> DB

    DB --> ORM
    ORM --> Repository
    Repository --> Service
    Service --> Router
    Router --> API
    API -->|"JSON Response"| Client
```

---

# 🎓 What This Project Teaches

By working on this project, you learn:

* Python REST API development
* FastAPI fundamentals
* Uvicorn / ASGI
* CRUD API development
* Pydantic validation
* SQLAlchemy ORM
* MySQL integration
* Dependency Injection
* Repository pattern
* Service layer
* Controller layer
* Request/response handling
* API documentation
* Layered architecture
* Spring Boot → FastAPI architectural mapping

---

# 💼 Interview Perspective

For a Java/Spring Boot developer moving toward Python and GenAI, this project helps establish the following mental mapping:

```text
Java Backend
     │
     ├── Spring Boot
     ├── REST
     ├── JPA/Hibernate
     ├── MySQL
     └── Dependency Injection
             │
             ▼
Python Backend
     │
     ├── FastAPI
     ├── REST
     ├── SQLAlchemy
     ├── MySQL
     └── Depends()
```

The **framework syntax changes**, but the backend architecture remains largely familiar.

---

# ⭐ Final Architecture to Remember

```text
                  🌐 CLIENT
                     │
                     ▼
             ⚡ FASTAPI ROUTER
                     │
                     ▼
              ✅ PYDANTIC
              VALIDATION
                     │
                     ▼
              🧠 SERVICE
           BUSINESS LOGIC
                     │
                     ▼
             📦 REPOSITORY
          DATABASE OPERATIONS
                     │
                     ▼
             🗄️ SQLALCHEMY
                    ORM
                     │
                     ▼
                 🐬 MYSQL
```

## 🚀 In One Line

> **FastAPI handles the API → Pydantic validates the data → Service handles business logic → Repository handles database operations → SQLAlchemy communicates with MySQL.**

---

## 📌 Spring Boot Developer Memory Trick

```text
@RestController  →  APIRouter
@Service         →  Service
@Repository      →  Repository
@Entity          →  SQLAlchemy Model
DTO              →  Pydantic Schema
JPA/Hibernate    →  SQLAlchemy
@Autowired       →  Depends()
Tomcat           →  Uvicorn
```

**Controller → Service → Repository → ORM → Database** 🚀
