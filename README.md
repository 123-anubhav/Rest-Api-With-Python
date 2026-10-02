# Rest-Api-With-Python
crud operation using fast api, uvicorn server, pydantic data validation and sqlalchemy orm framework

🚀 Project Flow: Spring Boot → FastAPI / Python

If you're coming from Spring Boot, you can think of a typical FastAPI + SQLAlchemy project as following almost the same layered architecture.

🔄 Request Flow
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
│    Repository       │
│   user_repository   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    SQLAlchemy       │
│       Model         │
└──────────┬──────────┘
           │
           ▼
        MySQL

🧠 The Mental Model

Spring Boot architecture translated to FastAPI/Python

Spring Boot	FastAPI / Python
@RestController	APIRouter
Controller	controllers/
@Service	services/
Service class	services/
@Repository	repositories/
JpaRepository	Repository class using SQLAlchemy
@Entity	SQLAlchemy model
Entity	models/
DTO	Pydantic schema
JPA / Hibernate	SQLAlchemy
@Autowired	Dependency Injection / constructor dependency
@GetMapping	@router.get()
@PostMapping	@router.post()
@PathVariable	Path parameter
@RequestBody	Pydantic request model
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

Responsibility of Each Layer
Layer	Responsibility
Controller	Handles HTTP requests and responses
Service	Contains business logic
Repository	Handles database operations
Model	Represents database tables
Schema	Validates request/response data
Database	Manages SQLAlchemy/MySQL connection
🔁 Example Request Flow

Suppose the client sends:

POST /users


with:

{
  "name": "John",
  "email": "john@example.com"
}


The request flows through the application like this:

HTTP Request
     │
     ▼
user_controller.py
     │
     │  validates request
     ▼
user_service.py
     │
     │  business logic
     ▼
user_repository.py
     │
     │  database operation
     ▼
SQLAlchemy Model
     │
     ▼
MySQL

🆚 Spring Boot vs FastAPI
Spring Boot
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

🗄️ SQLAlchemy Model

Spring Boot's:

@Entity
public class User {

    @Id
    private Long id;

    private String name;
    private String email;
}


is conceptually similar to:

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.connection import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255))

📦 Pydantic Schema = DTO

In Spring Boot, you might have:

public class UserDto {

    private String name;
    private String email;
}


In FastAPI:

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str


The important distinction is:

SQLAlchemy Model
       │
       │ represents database
       ▼
     MySQL


Pydantic Schema
       │
       │ represents API data
       ▼
HTTP Request / Response

🧩 Complete Architecture
                    ┌───────────────┐
                    │ HTTP Request  │
                    └───────┬───────┘
                            │
                            ▼
                 ┌────────────────────┐
                 │     Controller     │
                 │  FastAPI Router    │
                 └─────────┬──────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │      Service       │
                 │   Business Logic   │
                 └─────────┬──────────┘
                           │
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

🎯 Simple Rule to Remember

If you already know Spring Boot, remember this mapping:

Spring Boot                  FastAPI
────────────────────────────────────────────
@RestController       →      APIRouter
Controller            →      controllers/
@Service              →      services/
@Repository           →      repositories/
@Entity               →      SQLAlchemy Model
DTO                   →      Pydantic Schema
JPA/Hibernate         →      SQLAlchemy
@GetMapping           →      @router.get()
@PostMapping          →      @router.post()
@PathVariable         →      Path Parameter
@RequestBody          →      Pydantic Model
@Autowired            →      Depends() / Dependency Injection


In short:
Controller → Service → Repository → SQLAlchemy Model → MySQL

This is a useful mental model for structuring a FastAPI application if you're coming from a Spring Boot background.
