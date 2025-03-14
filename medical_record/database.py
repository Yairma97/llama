# DATABASE_URL = "mssql+pyodbc://sa:1qaz%40WSX@172.16.33.69:1433/LR_HDR_BAK?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no"
from select import select

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

ASYNC_SQLALCHEMY_URI = "mssql+aioodbc://sa:1qaz%40WSX@172.16.33.69:1433/LR_HDR_BAK?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no"
async_engine = create_async_engine(ASYNC_SQLALCHEMY_URI, echo=True)
async_session = sessionmaker(async_engine, class_=AsyncSession)

async def test_connection():
    async with async_session() as session:
        # 执行查询
        query = text("SELECT 1")
        result = await session.execute(query)
        return result

if __name__ == '__main__':
    import asyncio
    result = asyncio.run(test_connection())
    print(result)
