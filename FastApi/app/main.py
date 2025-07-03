from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .graphql.schema import schema
import json
from starlette.responses import JSONResponse
from app.database.database import engine, Base, get_db
from app.models.user import User

async def graphql_endpoint(request: Request):
    if request.method == "GET":
        return JSONResponse({"status": "ok"})
    
    query = await request.json()
    result = schema.execute(query["query"])
    
    if result.errors:
        return JSONResponse(
            {"errors": [str(error) for error in result.errors]},
            status_code=400
        )
    
    return JSONResponse(result.data)

app = FastAPI()

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Agregamos middleware para CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregamos el endpoint GraphQL
app.add_route("/graphql", graphql_endpoint, methods=["GET", "POST"])

@app.get("/")
async def read_root():
    return {"message": "¡Bienvenido a FastAPI con GraphQL!"}

# Endpoint para crear un usuario
@app.post("/users")
async def create_user(user: dict):
    db = next(get_db())
    try:
        new_user = User(
            name=user["name"],
            last_name=user["last_name"],
            age=user["age"]
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
