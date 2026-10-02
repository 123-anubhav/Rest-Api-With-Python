from configuration.database import Base, engine
from models.User import User


print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("Tables created!")
