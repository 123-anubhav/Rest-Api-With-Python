# Rest-Api-With-Python
crud operation using fast api, uvicorn server, pydantic data validation and sqlalchemy orm framework

🚀 Spring Boot → FastAPI / Python

If you already know Spring Boot, you can think of a typical FastAPI + SQLAlchemy project using the same layered architecture.

🔄 Project Flow
HTTP Request
Controlleruser_controller
Serviceuser_service
Repositoryuser_repository
SQLAlchemy Model
(MySQL)

The request flows through:

HTTP Request → Controller → Service → Repository → SQLAlchemy Model → MySQL

🧠 Spring Boot Mental Model → FastAPI
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


with:

{
  "name": "John",
  "email": "john@example.com"
}


The flow is:

POST /users
User Controlleruser_controller.py
User Serviceuser_service.py
User Repositoryuser_repository.py
SQLAlchemy ModelUser
("MySQL")
🎯 Controller

In Spring Boot:

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


The FastAPI equivalent:

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

Controller Responsibility
HTTP Request
Validate Request
Call Service
Return HTTP Response

The controller should mainly handle HTTP-related concerns.

Avoid putting heavy business logic inside the controller.

🧠 Service

The service layer contains the business logic.

Example:

from schemas.user_schema import UserCreate
from repositories.user_repository import UserRepository


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user: UserCreate):

        # Business logic
        existing_user = self.repository.find_by_email(
            user.email
        )

        if existing_user:
            raise ValueError("Email already exists")

        return self.repository.create(user)


The relationship is:

Controller
Service
Repository

The service should contain rules such as:

Check whether a user already exists

Validate business rules

Calculate values

Coordinate multiple repositories

Decide what operation should happen

🗄️ Repository

The repository handles database access.

Example:

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

Service
Repository
SQLAlchemy
("MySQL")
🏛️ SQLAlchemy Model

In Spring Boot, you might have:

@Entity
@Table(name = "users")
public class User {

    @Id
    private Long id;

    private String name;

    private String email;
}


The SQLAlchemy equivalent:

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

SQLAlchemy Model
SQLAlchemy ORM
("MySQL")
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


This schema is responsible for API data validation.

🔍 Model vs Schema

This is an important concept when moving from Spring Boot.

SQLAlchemy Model

Represents the database:

SQLAlchemy Model
Database Table
("MySQL")

Example:

class User(Base):

    __tablename__ = "users"

    id: Mapped[int]
    name: Mapped[str]
    email: Mapped[str]

Pydantic Schema

Represents the API request/response:

Pydantic Schema
API Data
HTTP Request / Response

Example:

class UserCreate(BaseModel):

    name: str
    email: str


So the relationship is:

FastAPI Application
Pydantic Schema
SQLAlchemy Model
API Request / Response
Database Table
("MySQL")
💉 Dependency Injection

In Spring Boot, you may use:

@Autowired
private UserService userService;


Or constructor injection:

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

FastAPI Controller
Depends()
Service
🌐 HTTP Mapping
Spring Boot	FastAPI
@GetMapping("/users")	@router.get("/users")
@PostMapping("/users")	@router.post("/users")
@PutMapping("/users/{id}")	@router.put("/users/{id}")
@DeleteMapping("/users/{id}")	@router.delete("/users/{id}")
GET

Spring Boot:

@GetMapping("/users")


FastAPI:

@router.get("/users")

POST

Spring Boot:

@PostMapping("/users")


FastAPI:

@router.post("/users")

PUT

Spring Boot:

@PutMapping("/users/{id}")


FastAPI:

@router.put("/users/{id}")

DELETE

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

Spring Boot	FastAPI
@PathVariable Long id	id: int
@PathVariable String name	name: str
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

For Markdown files, Mermaid is recommended instead of Unicode box diagrams because Mermaid handles the layout for you.

🌐 HTTP Request
🎮 ControllerFastAPI Router
🧠 ServiceBusiness Logic
📦 RepositoryDatabase Operations
🗄️ SQLAlchemyModel
("🐬 MySQL")
🎯 One-Line Mental Model

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


FastAPI equivalent:

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

🏆 Final Cheat Sheet
Concept	Spring Boot	FastAPI
API Controller	@RestController	APIRouter
Controller folder	controller/	controllers/
Business logic	@Service	services/
Database access	@Repository	repositories/
ORM Entity	@Entity	SQLAlchemy Model
ORM	JPA / Hibernate	SQLAlchemy
DTO	Java DTO	Pydantic Schema
Dependency Injection	@Autowired	Depends()
GET	@GetMapping	@router.get()
POST	@PostMapping	@router.post()
PUT	@PutMapping	@router.put()
DELETE	@DeleteMapping	@router.delete()
Path variable	@PathVariable	Path Parameter
Request body	@RequestBody	Pydantic Model
Database	MySQL	MySQL
🚀 Final Architecture
HTTP Request
ControllerAPIRouter
Pydantic SchemaRequest Validation
ServiceBusiness Logic
RepositoryData Access
SQLAlchemy ModelORM
("MySQL")
HTTP Response
🧠 Remember

Controller → Service → Repository → SQLAlchemy → MySQL

And:

Pydantic Schema = API data
SQLAlchemy Model = Database data

This gives you a clean mental model for translating a Spring Boot layered architecture into FastAPI/Python.
