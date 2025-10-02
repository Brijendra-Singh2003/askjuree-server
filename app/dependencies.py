from app.core.db_connect import SessionLocal

async def get_db():
    async with SessionLocal() as session:
        yield session
