from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models, schemas, database

app = FastAPI()

# Create tables (run separately with alembic/migrations ideally)
# But for testing:
@app.on_event("startup")
async def on_startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.post("/users/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[schemas.UserResponse])
async def read_users(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.User))
    return result.scalars().all()
