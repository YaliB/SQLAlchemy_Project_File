from fastapi import FastAPI
from db import Base, engine

def init_db():
    Base.metadata.create_all(engine)


def main():
    print("Project started successfully!")
    
    app = FastAPI()
    
    
    @app.get("/")
    def root():
        return "This is the Root routh"
    
        
if __name__ == "__main__":
    main()