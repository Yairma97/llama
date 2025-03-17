import pymssql
from sqlalchemy import create_engine, select
from medical_record.database import get_visiting_seq_no


async def get_all_medical_records_by_pat_id(pat_id: str):
    # 1.获取患者全部就诊号 VISITING_SEQ_NO
    visiting_seq_no = await get_visiting_seq_no(pat_id)
    # 2.根据患者就诊号查询病历信息

    # 3.返回病历信息
    pass


if __name__ == '__main__':
    import asyncio

    pat_ids = asyncio.run(get_visiting_seq_no('1130184'))
    print(pat_ids)
