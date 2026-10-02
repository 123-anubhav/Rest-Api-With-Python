# Rest-Api-With-Python crud operation using fast api, uvicorn server, pydantic data validation and sqlalchemy orm framework

🚀 Spring Boot → FastAPI / Python

If you are coming from Spring Boot, you can think of a typical FastAPI + SQLAlchemy project using a very similar layered architecture.

📌 Project Flow

The basic request flow is:

Step	Layer	Responsibility
1	HTTP Request	Client sends the request
2	Controller	Receives and handles the HTTP request
3	Service	Contains business logic
4	Repository	Handles database operations
5	SQLAlchemy Model	Maps Python objects to database tables
6	MySQL	Stores the actual data
Flow

HTTP Request → Controller → Service → Repository → SQLAlchemy Model → MySQL

🧠 Spring Boot Mental Model → FastAPI / Python

If you already know Spring Boot, this is the easiest way to map the concepts.

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
@PutMapping	@router.put()
@DeleteMapping	@router.delete()
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
1. Controller

Location:

controllers/


Responsibility:

Handles HTTP requests

Defines API endpoints

Receives request data

Validates request data through Pydantic

Calls the service layer

Returns the HTTP response

Example:

from fastapi import APIRouter

router = APIRouter(prefix="/users")


@router.get("/")
def get_users():
    pass

2. Service

Location:

services/


Responsibility:

Contains business logic

Coordinates application operations

Calls repositories

Should not directly handle HTTP details

Example:

class UserService:

    def __init__(self, repository):
        self.repository = repository

    def create_user(self, user):
        # Business logic
        return self.repository.create(user)

3. Repository

Location:

repositories/


Responsibility:

Handles database operations

Queries the database

Creates records

Updates records

Deletes records

Finds records

Example:

class UserRepository:

    def __init__(self, db):
        self.db = db

    def find_by_id(self, user_id):
        return self.db.query(User).filter(
            User.id == user_id
        ).first()

4. SQLAlchemy Model

Location:

models/


Responsibility:

Represents database tables

Defines columns

Defines relationships

Used by SQLAlchemy ORM

Example:

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

5. Pydantic Schema

Location:

schemas/


Responsibility:

Validates API request data

Defines API response structure

Acts similarly to a DTO in Spring Boot

Example:

from pydantic import BaseModel


class UserCreate(BaseModel):

    name: str
    email: str

🔍 Model vs Schema

This is one of the most important differences to understand.

SQLAlchemy Model

The SQLAlchemy model represents the database.

SQLAlchemy Model
       ↓
 Database Table
       ↓
     MySQL


Example:

class User(Base):

    __tablename__ = "users"

    id: Mapped[int]
    name: Mapped[str]
    email: Mapped[str]

Pydantic Schema

The Pydantic schema represents API data.

Pydantic Schema
       ↓
 API Request / Response
       ↓
      HTTP


Example:

class UserCreate(BaseModel):

    name: str
    email: str

Simple Rule
Pydantic Schema
    ↓
API Data


SQLAlchemy Model
    ↓
Database Data

🔄 Complete Request Flow

Suppose the client sends:

POST /users


with this request body:

{
  "name": "John",
  "email": "john@example.com"
}


The request flows through the application:

HTTP Request
     ↓
Controller
     ↓
Service
     ↓
Repository
     ↓
SQLAlchemy Model
     ↓
MySQL


The response travels back:

MySQL
  ↓
SQLAlchemy Model
  ↓
Repository
  ↓
Service
  ↓
Controller
  ↓
HTTP Response

🎯 Controller Example
Spring Boot
@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping
    public User createUser(
        @RequestBody UserDto user
    ) {
        return userService.createUser(user);
    }
}

FastAPI
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

Mapping
Spring Boot                         FastAPI
────────────────────────────────────────────────
@RestController              →      APIRouter

@RequestMapping              →      APIRouter(prefix=...)

@PostMapping                  →      @router.post()

@RequestBody                  →      Pydantic Model

🧠 Service Example
Spring Boot
@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(
        UserRepository userRepository
    ) {
        this.userRepository = userRepository;
    }

    public User createUser(UserDto user) {

        // Business logic

        return userRepository.save(user);
    }
}

FastAPI
from schemas.user_schema import UserCreate
from repositories.user_repository import UserRepository


class UserService:

    def __init__(
        self,
        repository: UserRepository
    ):
        self.repository = repository

    def create_user(
        self,
        user: UserCreate
    ):

        # Business logic

        return self.repository.create(user)

🗄️ Repository Example
Spring Boot
@Repository
public interface UserRepository
        extends JpaRepository<User, Long> {

}

FastAPI + SQLAlchemy
from sqlalchemy.orm import Session

from models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, user_id: int):

        return (
            self.db
            .query(User)
            .filter(User.id == user_id)
            .first()
        )

    def find_by_email(self, email: str):

        return (
            self.db
            .query(User)
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

🏛️ Entity → SQLAlchemy Model
Spring Boot
@Entity
@Table(name = "users")
public class User {

    @Id
    private Long id;

    private String name;

    private String email;
}

FastAPI / SQLAlchemy
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

Mapping
Spring Boot                         FastAPI
──────────────────────────────────────────────
@Entity                       →     SQLAlchemy Model

@Table                        →     __tablename__

@Id                           →     primary_key=True

@Column                       →     mapped_column()

JPA / Hibernate               →     SQLAlchemy

📋 DTO → Pydantic Schema
Spring Boot DTO
public class UserDto {

    private String name;

    private String email;
}

FastAPI Pydantic Schema
from pydantic import BaseModel


class UserCreate(BaseModel):

    name: str
    email: str

Mapping
Spring Boot                         FastAPI
──────────────────────────────────────────────
DTO                           →     Pydantic Schema

String name                   →     name: str

String email                  →     email: str

💉 Dependency Injection

Spring Boot uses dependency injection:

@Autowired
private UserService userService;


Or constructor injection:

public UserController(
    UserService userService
) {
    this.userService = userService;
}


FastAPI commonly uses Depends():

from fastapi import Depends


@router.get("/")
def get_users(
    service: UserService = Depends()
):
    return service.get_users()

Mapping
Spring Boot

@Autowired
    ↓
Dependency Injection

FastAPI

Depends()
    ↓
Dependency Injection

🌐 HTTP Mapping
Spring Boot	FastAPI
@GetMapping("/users")	@router.get("/users")
@PostMapping("/users")	@router.post("/users")
@PutMapping("/users/{id}")	@router.put("/users/{id}")
@DeleteMapping("/users/{id}")	@router.delete("/users/{id}")
🛣️ Path Variable → Path Parameter
Spring Boot
@GetMapping("/users/{id}")
public User getUser(
    @PathVariable Long id
) {
    return userService.getUser(id);
}

FastAPI
@router.get("/users/{id}")
def get_user(id: int):

    return user_service.get_user(id)

Mapping
Spring Boot                         FastAPI
──────────────────────────────────────────────
@PathVariable Long id         →     id: int

@PathVariable String name     →     name: str

📥 Request Body → Pydantic Model
Spring Boot
@PostMapping("/users")
public User createUser(
    @RequestBody UserDto user
) {
    return userService.createUser(user);
}

FastAPI
@router.post("/users")
def create_user(
    user: UserCreate
):

    return user_service.create_user(user)


Request:

{
  "name": "John",
  "email": "john@example.com"
}


FastAPI validates the request using:

class UserCreate(BaseModel):

    name: str
    email: str

🧩 Complete Architecture

For maximum compatibility with Markdown viewers, the architecture is represented using a table instead of Unicode box-drawing characters.

Layer	FastAPI Component	Spring Boot Equivalent
🌐 HTTP	HTTP Request	HTTP Request
🎮 Controller	APIRouter	@RestController
🧠 Service	Service class	@Service
📦 Repository	Repository class	@Repository / JpaRepository
🏛️ ORM	SQLAlchemy Model	@Entity + JPA/Hibernate
📝 API Data	Pydantic Schema	DTO
🗄️ Database	MySQL	MySQL
Request Direction

HTTP Request

↓

Controller / APIRouter

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

Response Direction

MySQL

↓

SQLAlchemy Model

↓

Repository

↓

Service

↓

Controller / APIRouter

↓

HTTP Response

📚 Final Cheat Sheet
Concept	Spring Boot	FastAPI / Python
API Controller	@RestController	APIRouter
Controller Folder	controller/	controllers/
Business Logic	@Service	services/
Database Access	@Repository	repositories/
ORM Entity	@Entity	SQLAlchemy Model
ORM	JPA / Hibernate	SQLAlchemy
DTO	Java DTO	Pydantic Schema
Dependency Injection	@Autowired	Depends()
GET	@GetMapping	@router.get()
POST	@PostMapping	@router.post()
PUT	@PutMapping	@router.put()
DELETE	@DeleteMapping	@router.delete()
Path Variable	@PathVariable	Path Parameter
Request Body	@RequestBody	Pydantic Model
Repository	JpaRepository	Repository Class
Database	MySQL	MySQL
🎯 The Mental Model

If you know Spring Boot, remember this:

SPRING BOOT

Controller
    ↓
Service
    ↓
Repository
    ↓
JPA / Hibernate
    ↓
Database


The FastAPI equivalent:

FASTAPI

Controller / APIRouter
        ↓
     Service
        ↓
   Repository
        ↓
   SQLAlchemy
        ↓
      MySQL


And for data:

Pydantic Schema
      ↓
   API Data


SQLAlchemy Model
      ↓
 Database Data

🚀 One Sentence to Remember

Controller handles HTTP → Service handles business logic → Repository handles database access → SQLAlchemy handles ORM → MySQL stores the data.
