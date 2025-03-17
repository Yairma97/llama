from collections import defaultdict
from typing import List, Mapping, Dict, Any

from sqlalchemy import text, select, bindparam
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from medical_record import data_models

ASYNC_SQLALCHEMY_URI = "mssql+aioodbc://sa:1qaz%40WSX@172.16.33.69:1433/LR_HDR_BAK?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no"
async_engine = create_async_engine(ASYNC_SQLALCHEMY_URI, echo=True)
async_session = sessionmaker(async_engine, class_=AsyncSession)


async def test_connection():
    async with async_session() as session:
        # 执行查询
        query = text("SELECT 1")
        result = await session.execute(query)
        return result


async def get_visiting_seq_no(pat_id: str):
    async with async_session() as session:
        textual_sql = text(f"SELECT VISITING_SEQ_NO from ADMSN_INPAT_RFP where PAT_ID = '{pat_id}'")
        # 执行查询
        result = await session.execute(textual_sql)
        # 提取字段值
        visiting_seq_no = result.scalars().all()
        return list(set(visiting_seq_no))


async def get_emr_diagnosis(visiting_seq_no: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    async with async_session() as session:
        # textual_sql = text(f"SELECT * from EMR_INPAT_DIAGNOSIS_INFO where VISITING_SEQ_NO in :visiting_seq_no")
        # # 执行查询
        # params = {"visiting_seq_no": visiting_seq_no}
        # # 执行查询
        # result = await session.execute(textual_sql.bindparams(bindparam('visiting_seq_no', expanding=True)), params)

        # 使用 ORM 查询
        query = select(data_models.t_EMR_INPAT_DIAGNOSIS_INFO.columns.VISITING_SEQ_NO,
                       data_models.t_EMR_INPAT_DIAGNOSIS_INFO.columns.DIAG_TIME,
                       data_models.t_EMR_INPAT_DIAGNOSIS_INFO.columns.DIAG_NAME,
                       data_models.t_EMR_INPAT_DIAGNOSIS_INFO.columns.DIAG_CODE,
                       data_models.t_EMR_INPAT_DIAGNOSIS_INFO.columns.DIAG_CATEGORY_CODE,
                       data_models.t_EMR_INPAT_DIAGNOSIS_INFO.columns.DIAG_DESC, ).where(
            data_models.t_EMR_INPAT_DIAGNOSIS_INFO.columns.VISITING_SEQ_NO.in_(visiting_seq_no)
        )
        # 执行查询
        rows = await session.execute(query)
        # 将结果转换为字典
        result = defaultdict(list)
        for row in rows.all():
            result[row.VISITING_SEQ_NO].append({
                "DIAG_TIME": row.DIAG_TIME.strftime("%Y-%m-%d %H:%M:%S"),
                "DIAG_NAME": row.DIAG_NAME,
                "DIAG_CODE": row.DIAG_CODE,
                "DIAG_CATEGORY_CODE": row.DIAG_CATEGORY_CODE,
                "DIAG_DESC": row.DIAG_DESC,
            })

        return result


async def get_lab_report(visiting_seq_no: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    async with async_session() as session:
        # 使用 ORM 查询
        query = select(data_models.t_LAB_RESULT.columns.VISITING_SEQ_NO,
                       data_models.t_LAB_RESULT.columns.LAB_INDEX_ITEM_NAME,
                       data_models.t_LAB_RESULT.columns.LAB_RESULT_VALUE,
                       data_models.t_LAB_RESULT.columns.LAB_RESULT_REF_VALUE_QLTY,
                       data_models.t_LAB_RESULT.columns.LAB_RESULT_UNIT,
                       data_models.t_LAB_RESULT.columns.ABNORMAL_FLAG,
                       data_models.t_LAB_RESULT.columns.CRITIC_VALUE_FLAG, ).where(
            data_models.t_LAB_RESULT.columns.VISITING_SEQ_NO.in_(visiting_seq_no)
        )
        # 执行查询
        rows = await session.execute(query)
        # 将结果转换为字典
        result = defaultdict(list)
        for row in rows.all():
            result[row.VISITING_SEQ_NO].append({
                "LAB_INDEX_ITEM_NAME": row.LAB_INDEX_ITEM_NAME,
                "LAB_RESULT_VALUE": row.LAB_RESULT_VALUE,
                "LAB_RESULT_REF_VALUE_QLTY": row.LAB_RESULT_REF_VALUE_QLTY,
                "ABNORMAL_FLAG": row.ABNORMAL_FLAG,
                "LAB_RESULT_UNIT": row.LAB_RESULT_UNIT,
                "CRITIC_VALUE_FLAG": row.CRITIC_VALUE_FLAG,
            })

        return result


async def main(pat_id: str):
    visiting_seq_no = await get_visiting_seq_no(pat_id)
    # emr_diagnosis = await get_emr_diagnosis(visiting_seq_no)
    # print(emr_diagnosis)
    lab_report = await get_lab_report(visiting_seq_no)
    print(lab_report)


if __name__ == '__main__':
    import asyncio

    result = asyncio.run(main("1130184"))
