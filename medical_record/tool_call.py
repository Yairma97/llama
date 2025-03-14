import pymssql
from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session

from medical_record import data_models

# DATABASE_URL = "mssql+pyodbc://sa:1qaz%40WSX@172.16.33.69:1433/LR_HDR_BAK?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no"

ASYNC_SQLALCHEMY_URI = "mssql+aioodbc://sa:1qaz%40WSX@172.16.33.69:1433/LR_HDR_BAK?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no"
async_engine = create_async_engine(ASYNC_SQLALCHEMY_URI, echo=True)
async_session = sessionmaker(async_engine, class_=AsyncSession)

async def get_all_medical_records_by_pat_id(pat_id: str):
    # 1.获取数据库连接

    # 2.获取患者全部就诊号 VISITING_SEQ_NO

    # 3.根据患者就诊号查询病历信息

    # 4.返回病历信息
    pass


async def get_visiting_seq_no(pat_id: str):
    async with async_session() as session:
        stmt = select(data_models.t_ADMSN_INPAT_RFP.columns.VISITING_SEQ_NO).where(data_models.t_ADMSN_INPAT_RFP.columns.PAT_ID == pat_id)
        # 执行查询
        result = await session.execute(stmt)
        # 提取字段值
        pat_ids = result.scalars().all()
        return pat_ids


if __name__ == '__main__':
    import asyncio
    pat_ids = asyncio.run(get_visiting_seq_no('1130184'))
    print(pat_ids)

