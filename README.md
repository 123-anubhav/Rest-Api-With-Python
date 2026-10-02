# Rest-Api-With-Python
crud operation using fast api, uvicorn server, pydantic data validation and sqlalchemy orm framework

🚀 Spring Boot → FastAPI / Python

If you are coming from Spring Boot, you can think of a typical FastAPI + SQLAlchemy project as following a very similar layered architecture.

🔄 Project Flow

The basic request flow is:

HTTP Request
     │
     ▼
┌─────────────────────┐
│     Controller      │
│   user_controller   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      Service        │
│    user_service     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     Repository      │
│   user_repository   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     SQLAlchemy      │
│        Model        │
└──────────┬──────────┘
           │
           ▼
        ┌───────┐
        │ MySQL │
        └───────┘

🧠 Spring Boot Mental Model → FastAPI

If you already understand Spring Boot, the following mapping makes FastAPI easier to understand.

Spring Boot	FastAPI / Python
@RestController	APIRouter
Controller	controllers/
@Service	services/
Service class	services/
@Repository	repositories/
JpaRepository	Repository class using SQLAlchemy
@Entity	SQLAlchemy Model
Entity	models/
DTO	Pydantic Schema
JPA / Hibernate	SQLAlchemy
@Autowired	Dependency Injection / Depends()
@GetMapping	@router.get()
@PostMapping	@router.post()
@PathVariable	Path Parameter
@RequestBody	Pydantic Request Model
📁 Typical FastAPI Project Structure

A clean FastAPI project can be organized like this:

app/
│
├── main.py
│
├── controllers/
│   └── user_controller.py
│
├── services/
│   └── user_service.py
│
├── repositories/
│   └── user_repository.py
│
├── models/
│   └── user.py
│
├── schemas/
│   └── user_schema.py
│
└── database/
    └── connection.py

📦 Layer Responsibilities
Layer	Responsibility
Controller	Handles HTTP requests and responses
Service	Contains business logic
Repository	Handles database operations
Model	Represents database tables
Schema	Validates request and response data
Database	Manages SQLAlchemy/MySQL connection
🔁 Complete Request Flow

Suppose the client sends:

POST /users


with the following JSON body:

{
  "name": "John",
  "email": "john@example.com"
}


The request flows through the application like this:

                    HTTP Request
                         │
                         ▼
              ┌────────────────────┐
              │     Controller     │
              │  FastAPI Router    │
              └─────────┬──────────┘
                        │
                        │ Request validation
                        ▼
              ┌────────────────────┐
              │      Service       │
              │   Business Logic   │
              └─────────┬──────────┘
                        │
                        │ Database request
                        ▼
              ┌────────────────────┐
              │    Repository      │
              │ Database Operations│
              └─────────┬──────────┘
                        │
                        ▼
              ┌────────────────────┐
              │    SQLAlchemy      │
              │       Model        │
              └─────────┬──────────┘
                        │
                        ▼
                   ┌─────────┐
                   │  MySQL  │
                   └─────────┘

🎯 Controller

In Spring Boot, you commonly use:

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


The FastAPI equivalent is:

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

Responsibility

The controller should mainly handle:

HTTP Request
     │
     ▼
Request Validation
     │
     ▼
Call Service
     │
     ▼
HTTP Response


Avoid putting heavy business logic inside the controller.

🧠 Service

The service layer contains your business logic.

Example:

from schemas.user_schema import UserCreate
from repositories.user_repository import UserRepository


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user: UserCreate):

        # Business logic
        # Example:
        # Check whether email already exists

        existing_user = self.repository.find_by_email(user.email)

        if existing_user:
            raise ValueError("Email already exists")

        return self.repository.create(user)


The service sits between the controller and repository:

Controller
    │
    ▼
 Service
    │
    ▼
Repository

🗄️ Repository

The repository handles database-related operations.

For example:

from sqlalchemy.orm import Session

from models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_email(self, email: str):

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def create(self, user):

        db_user = User(
            name=user.name,
            email=user.email
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user


The repository should focus on data access, not business rules.

🏛️ SQLAlchemy Model

In Spring Boot, you might have an entity:

@Entity
@Table(name = "users")
public class User {

    @Id
    private Long id;

    private String name;

    private String email;
}


The SQLAlchemy equivalent is:

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


Conceptually:

Spring Boot

@Entity
   │
   ▼
JPA Entity
   │
   ▼
Hibernate
   │
   ▼
MySQL


becomes:

FastAPI

SQLAlchemy Model
       │
       ▼
   SQLAlchemy
       │
       ▼
     MySQL

📋 Pydantic Schema = DTO

In Spring Boot, you might create a DTO:

public class UserDto {

    private String name;

    private String email;
}


In FastAPI, you typically use a Pydantic model:

from pydantic import BaseModel


class UserCreate(BaseModel):

    name: str

    email: str


This schema is used for API data validation.

🔍 Model vs Schema

This is an important concept when coming from Spring Boot.

SQLAlchemy Model

Represents the database:

SQLAlchemy Model
       │
       ▼
   Database Table


Example:

class User(Base):

    __tablename__ = "users"

    id: Mapped[int]
    name: Mapped[str]
    email: Mapped[str]

Pydantic Schema

Represents the API request/response:

Pydantic Schema
       │
       ▼
HTTP Request / Response


Example:

class UserCreate(BaseModel):

    name: str
    email: str


So:

             FastAPI Application
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
 Pydantic Schema         SQLAlchemy Model
        │                       │
        │                       │
        ▼                       ▼
   API Data              Database Data
        │                       │
        ▼                       ▼
 HTTP Request/Response        MySQL

💉 Dependency Injection

In Spring Boot, you may use:

@Autowired
private UserService userService;


or constructor injection:

public UserController(UserService userService) {
    this.userService = userService;
}


FastAPI provides dependency injection using Depends().

Example:

from fastapi import Depends


@router.get("/")
def get_users(
    service: UserService = Depends()
):
    return service.get_users()


Conceptually:

Spring Boot

@Autowired
    │
    ▼
Dependency Injection


becomes:

FastAPI

Depends()
    │
    ▼
Dependency Injection

🌐 HTTP Mapping

Spring Boot:

@GetMapping("/users")


FastAPI:

@router.get("/users")


Spring Boot:

@PostMapping("/users")


FastAPI:

@router.post("/users")


Spring Boot:

@PutMapping("/users/{id}")


FastAPI:

@router.put("/users/{id}")


Spring Boot:

@DeleteMapping("/users/{id}")


FastAPI:

@router.delete("/users/{id}")

🛣️ Path Variable → Path Parameter

Spring Boot:

@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userService.getUser(id);
}


FastAPI:

@router.get("/users/{id}")
def get_user(id: int):

    return user_service.get_user(id)


Mapping:

Spring Boot                    FastAPI
────────────────────────────────────────────
@PathVariable             →    Path Parameter

@PathVariable Long id     →    id: int

📥 Request Body → Pydantic Model

Spring Boot:

@PostMapping("/users")
public User createUser(
    @RequestBody UserDto user
) {
    return userService.createUser(user);
}


FastAPI:

@router.post("/users")
def create_user(user: UserCreate):

    return user_service.create_user(user)


The Pydantic model automatically validates the incoming JSON.

Example request:

{
  "name": "John",
  "email": "john@example.com"
}


FastAPI converts and validates it using:

class UserCreate(BaseModel):

    name: str
    email: str

🧩 Complete Architecture

Keep the architecture diagram inside a fenced code block so that Markdown preserves the spacing:

                         HTTP Request
                              │
                              ▼
                 ┌──────────────────────┐
                 │      Controller      │
                 │    FastAPI Router    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │       Service        │
                 │    Business Logic    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     Repository       │
                 │  Database Operations │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     SQLAlchemy       │
                 │        Model         │
                 └──────────┬───────────┘
                            │
                            ▼
                       ┌─────────┐
                       │  MySQL  │
                       └─────────┘

🔄 Spring Boot → FastAPI Cheat Sheet
Spring Boot                         FastAPI / Python
────────────────────────────────────────────────────────

@RestController              →      APIRouter

Controller                   →      controllers/

@Service                     →      services/

@Repository                  →      repositories/

@Entity                      →      SQLAlchemy Model

JPA / Hibernate              →      SQLAlchemy

DTO                          →      Pydantic Schema

@Autowired                   →      Depends()

@GetMapping                  →      @router.get()

@PostMapping                 →      @router.post()

@PutMapping                  →      @router.put()

@DeleteMapping               →      @router.delete()

@PathVariable                →      Path Parameter

@RequestBody                 →      Pydantic Request Model

JpaRepository                →      Repository Class

application.properties      →      .env / configuration

Spring Dependency Injection →      FastAPI Dependency Injection

🎯 The One-Line Mental Model

If you are moving from Spring Boot to FastAPI, remember:

Spring Boot

Controller
    ↓
Service
    ↓
Repository
    ↓
JPA / Hibernate
    ↓
Database


The equivalent FastAPI architecture is:

FastAPI

APIRouter / Controller
        ↓
     Service
        ↓
   Repository
        ↓
   SQLAlchemy
        ↓
      MySQL


And for API data:

HTTP Request
      ↓
Pydantic Schema
      ↓
   Service
      ↓
Repository
      ↓
SQLAlchemy Model
      ↓
    MySQL


Simple rule:
Controller handles HTTP → Service handles business logic → Repository handles database access → SQLAlchemy handles ORM → MySQL stores the data.
