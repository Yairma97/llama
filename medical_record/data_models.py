from typing import Optional

from sqlalchemy import Column, Date, DateTime, Index, Integer, Numeric, PrimaryKeyConstraint, String, Table, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime
import decimal


class Base(DeclarativeBase):
    pass


class EMRCLINDOCU(Base):
    __tablename__ = 'EMR_CLIN_DOCU'
    __table_args__ = (
        PrimaryKeyConstraint('VISITING_SEQ_NO', 'ORG_CODE', 'VISITING_CATEGORY', 'EMR_SERIAL', 'SYSTEM_FLAG',
                             name='PK_EMR_CLIN_DOCU'),
    )

    VISITING_SEQ_NO: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), primary_key=True, comment='就诊流水号')
    ORG_CODE: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'), primary_key=True, comment='医疗机构代码')
    ORG_NAME: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='医疗机构名称')
    VISITING_CATEGORY: Mapped[str] = mapped_column(String(10, 'Chinese_PRC_BIN'), primary_key=True, comment='就诊类别')
    PAT_ID: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='患者ID')
    PAT_NAME: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='患者姓名')
    EMR_SERIAL: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), primary_key=True, comment='病历序号')
    DOCU_NAME: Mapped[str] = mapped_column(String(800, 'Chinese_PRC_BIN'), comment='未定义')
    DOCU_VERSION: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='未定义')
    DOCU_CATEGORY_CODE: Mapped[str] = mapped_column(String(4, 'Chinese_PRC_BIN'), comment='文档内容')
    DOCU_CATEGORY_NAME: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='未定义')
    DOCU_DTL_CATEGORY_CODE: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='未定义')
    DOCU_DTL_CATEGORY_NAME: Mapped[str] = mapped_column(String(512, 'Chinese_PRC_BIN'), comment='未定义')
    PDF_FLAG: Mapped[str] = mapped_column(String(1, 'Chinese_PRC_BIN'), comment='PDF标志')
    DOCUMENT_STRUCTURE_FLAG: Mapped[str] = mapped_column(String(1, 'Chinese_PRC_BIN'), comment='未定义')
    NONSTRUCTURE_FLAG: Mapped[str] = mapped_column(String(1, 'Chinese_PRC_BIN'), comment='未定义')
    AUDITOR_ID: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='审核师代码')
    AUDITOR_NAME: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_BIN'), comment='审核师姓名')
    CREATOR_ID: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='创建人代码')
    CREATOR_NAME: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='创建人姓名')
    CREATE_TIME: Mapped[datetime.datetime] = mapped_column(DateTime, comment='创建时间')
    AUDIT_TIME: Mapped[datetime.datetime] = mapped_column(DateTime, comment='审核时间')
    FILE_SAVE_FLAG: Mapped[str] = mapped_column(String(10, 'Chinese_PRC_BIN'), comment='文件存储标志')
    EMR_STATUS: Mapped[str] = mapped_column(String(10, 'Chinese_PRC_BIN'), comment='病历状态')
    REC_STATUS: Mapped[str] = mapped_column(String(10, 'Chinese_PRC_BIN'), comment='记录状态')
    DATA_STATUS: Mapped[str] = mapped_column(String(2, 'Chinese_PRC_BIN'), comment='数据状态')
    SYSTEM_FLAG: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_BIN'), primary_key=True, comment='数据来源')
    DATA_UPDATE_TIME: Mapped[datetime.datetime] = mapped_column(DateTime, comment='更新日期时间')
    RECEIVE_TIME: Mapped[datetime.datetime] = mapped_column(DateTime, comment='接收日期时间')
    DOCU_CREATE_TIME: Mapped[datetime.datetime] = mapped_column(DateTime, comment='未定义')
    ADMISSION_NO: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='住院号')
    OUTPATIENT_NO: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='门(急)诊号')
    BABY_SERIAL: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='婴儿序号')
    REPORT_URL: Mapped[Optional[str]] = mapped_column(String(128, 'Chinese_PRC_BIN'), comment='报告链接')
    CURR_EMR_LOC_IN_PDF: Mapped[Optional[str]] = mapped_column(String(10, 'Chinese_PRC_BIN'), comment='未定义')
    BATCH_NO: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='批号')


class EMRCLINDOCUSECTION(Base):
    __tablename__ = 'EMR_CLIN_DOCU_SECTION'
    __table_args__ = (
        PrimaryKeyConstraint('VISITING_SEQ_NO', 'ORG_CODE', 'VISITING_CATEGORY', 'EMR_SERIAL', 'DOCU_SECTION_CODE',
                             'SYSTEM_FLAG', name='PK_EMR_CLIN_DOCU_SUMMARY'),
    )

    VISITING_SEQ_NO: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), primary_key=True, comment='就诊流水号')
    ORG_CODE: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'), primary_key=True, comment='医疗机构代码')
    ORG_NAME: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='医疗机构名称')
    VISITING_CATEGORY: Mapped[str] = mapped_column(String(10, 'Chinese_PRC_BIN'), primary_key=True, comment='就诊类别')
    PAT_ID: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='患者ID')
    PAT_NAME: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='患者姓名')
    EMR_SERIAL: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), primary_key=True, comment='未定义')
    DOCU_SECTION_CODE: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), primary_key=True, comment='未定义')
    DOCU_SECTION_NAME: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='未定义')
    DOCU_FORMAT: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='文档格式')
    NATURAL_LANGUAGE_DOCU: Mapped[str] = mapped_column(String(collation='Chinese_PRC_BIN'), comment='未定义')
    DOCU_DISPLAY_SEQ: Mapped[str] = mapped_column(String(10, 'Chinese_PRC_BIN'), comment='未定义')
    REC_STATUS: Mapped[str] = mapped_column(String(10, 'Chinese_PRC_BIN'), comment='记录状态')
    DATA_STATUS: Mapped[str] = mapped_column(String(2, 'Chinese_PRC_BIN'), comment='数据状态')
    SYSTEM_FLAG: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_BIN'), primary_key=True, comment='数据来源')
    DATA_UPDATE_TIME: Mapped[datetime.datetime] = mapped_column(DateTime, comment='更新日期时间')
    RECEIVE_TIME: Mapped[datetime.datetime] = mapped_column(DateTime, comment='接收日期时间')
    ADMISSION_NO: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='住院号')
    OUTPATIENT_NO: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='门(急)诊号')
    BATCH_NO: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='批号')


t_EMR_INPAT_DIAGNOSIS_INFO = Table(
    'EMR_INPAT_DIAGNOSIS_INFO', Base.metadata,
    Column('ORG_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False, comment='医疗机构代码'),
    Column('VISITING_SEQ_NO', String(64, 'Chinese_PRC_BIN'), nullable=False, comment='就诊流水号'),
    Column('BABY_SERIAL', String(64, 'Chinese_PRC_BIN'), nullable=False, comment='婴儿序号'),
    Column('DIAG_CATEGORY_CODE', String(8, 'Chinese_PRC_BIN'), nullable=False, comment='诊断类别'),
    Column('DIAG_TYPE_CODE', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='诊断类型'),
    Column('DIAG_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False, comment='疾病诊断编码'),
    Column('DIAG_NAME', String(512, 'Chinese_PRC_BIN'), nullable=False, comment='疾病诊断名称'),
    Column('DIAG_TIME', DateTime, nullable=False, comment='未定义'),
    Column('DIAG_DOC_ID', String(32, 'Chinese_PRC_BIN'), nullable=False, comment='未定义'),
    Column('DIAG_DESC', String(256, 'Chinese_PRC_BIN'), comment='诊断描述'),
    Column('TCM_SYNDROME_TYPE_CODE', String(32, 'Chinese_PRC_BIN'), comment='中医证型代码'),
    Column('TCM_SYNDROME_TYPE_NAME', String(256, 'Chinese_PRC_BIN'), comment='中医证型名称'),
    Column('NOTE', String(128, 'Chinese_PRC_BIN'), comment='备注'),
    Column('DATA_UPDATE_TIME', DateTime, nullable=False, comment='数据更新日期时间'),
    Column('SYSTEM_FLAG', String(50, 'Chinese_PRC_BIN'), nullable=False, comment='系统标志'),
    Column('DATA_STATUS', String(10, 'Chinese_PRC_BIN'), nullable=False, comment='数据状态'),
    Column('ORG_NAME', String(128, 'Chinese_PRC_BIN'), nullable=False, server_default=text("(' ')")),
    Column('DIAG_DOC_NAME', String(65, 'Chinese_PRC_BIN'), nullable=False, server_default=text("(' ')"))
)


class EXAMREPORT(Base):
    __tablename__ = 'EXAM_REPORT'
    __table_args__ = (
        PrimaryKeyConstraint('VISITING_SEQ_NO', 'ORG_CODE', 'VISITING_CATEGORY', 'EXAM_REPORT_NO',
                             'REPORT_CATEGORY_CODE', 'SYSTEM_FLAG', name='PK_EXAM_REPORT_1'),
        Index('PK_EXAM_REPORT', 'VISITING_SEQ_NO', 'ORG_CODE', 'VISITING_CATEGORY', 'EXAM_REPORT_NO',
              'REPORT_CATEGORY_CODE', 'SYSTEM_FLAG', unique=True)
    )

    VISITING_SEQ_NO: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), primary_key=True, comment='就诊流水号')
    ORG_CODE: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'), primary_key=True, comment='医疗机构代码')
    ORG_NAME: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='医疗机构名称')
    VISITING_CATEGORY: Mapped[str] = mapped_column(String(10, 'Chinese_PRC_BIN'), primary_key=True, comment='就诊类别')
    BABY_SERIAL: Mapped[int] = mapped_column(Integer)
    PAT_ID: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'))
    PAT_NAME: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'))
    EXAM_REPORT_NO: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), primary_key=True)
    REPORT_CATEGORY_CODE: Mapped[str] = mapped_column(String(16, 'Chinese_PRC_BIN'), primary_key=True)
    REPORT_CATEGORY_NAME: Mapped[str] = mapped_column(String(256, 'Chinese_PRC_BIN'))
    APPLY_DEPT_CODE: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'))
    APPLY_DEPT_NAME: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'))
    APPLY_DOC_ID: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'))
    APPLY_DOC_NAME: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'))
    APPLY_TIME: Mapped[datetime.datetime] = mapped_column(DateTime)
    CLINICAL_DIAG_CODE: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'))
    CLINICAL_DIAG_NAME: Mapped[str] = mapped_column(String(256, 'Chinese_PRC_BIN'))
    EXAM_DEPT_CODE: Mapped[str] = mapped_column(String(200, 'Chinese_PRC_BIN'))
    EXAM_DEPT_NAME: Mapped[str] = mapped_column(String(500, 'Chinese_PRC_BIN'))
    REGISTER_TIME: Mapped[datetime.datetime] = mapped_column(DateTime)
    REGISTER_DOC_ID: Mapped[str] = mapped_column(String(256, 'Chinese_PRC_BIN'))
    REGISTER_DOC_NAME: Mapped[str] = mapped_column(String(256, 'Chinese_PRC_BIN'))
    EXAM_TIME: Mapped[datetime.datetime] = mapped_column(DateTime)
    EXAM_DOC_ID: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'))
    EXAM_DOC_NAME: Mapped[str] = mapped_column(String(500, 'Chinese_PRC_BIN'))
    REPORT_RELEASE_TIME: Mapped[datetime.datetime] = mapped_column(DateTime)
    REPORTER_ID: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'))
    REPORTER_NAME: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'))
    APPLY_FORM_NO: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'))
    OFFICIAL_REPORT_FLAG: Mapped[str] = mapped_column(String(1, 'Chinese_PRC_BIN'))
    REPORT_STATUS_CODE: Mapped[str] = mapped_column(String(4, 'Chinese_PRC_BIN'))
    REC_STATUS: Mapped[str] = mapped_column(String(10, 'Chinese_PRC_BIN'))
    DATA_STATUS: Mapped[str] = mapped_column(String(2, 'Chinese_PRC_BIN'))
    SYSTEM_FLAG: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_BIN'), primary_key=True)
    DATA_UPDATE_TIME: Mapped[datetime.datetime] = mapped_column(DateTime)
    RECEIVE_TIME: Mapped[datetime.datetime] = mapped_column(DateTime)
    SEX_NAME: Mapped[str] = mapped_column(String(10, 'Chinese_PRC_BIN'), server_default=text("('')"))
    SEX_CODE: Mapped[str] = mapped_column(String(10, 'Chinese_PRC_BIN'), server_default=text("('')"))
    BIRTH_DATE: Mapped[datetime.date] = mapped_column(Date, server_default=text("(' ')"))
    CLIN_SYMPTOM: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    RELATED_ASSAY_RESULT: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    OTHER_DIAG: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    EXAM_PARAMETER: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    EXAM_VISIBILITY: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    EXAM_RESULT: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    POSITIVE_FLAG: Mapped[int] = mapped_column(Integer, server_default=text("(' ')"))
    ATTENTION_POINT: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    REPORT_IMAGE_NO: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    NOTE: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    TRACE_ROUTE: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    HOSP_UID: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    DELIVERY_HOSP: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    DELIVERY_TIME: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    PATHOLOGY_EYE_VISIBILITY: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    PATHOLOGY_SCOPE_VISIBILITY: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), server_default=text("(' ')"))
    ADMISSION_NO: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'))
    OUTPATIENT_NO: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'))
    EXAM_ITEM_NAME: Mapped[Optional[str]] = mapped_column(String(128, 'Chinese_PRC_BIN'))
    APPLY_WARD_CODE: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'))
    APPLY_WARD_NAME: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'))
    BED_NO: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'))
    EXAM_PART: Mapped[Optional[str]] = mapped_column(String(1024, 'Chinese_PRC_BIN'))
    EXAM_SAMPLE_ID: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'))
    SAMPLE_FIXATIVE_NAME: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'))
    FROZEN_NO: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'))
    IMMUNITY_ID: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'))
    SAMPLING_TIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    SAMPLE_RECEIVE_TIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    EXAM_METHOD_NAME: Mapped[Optional[str]] = mapped_column(String(256, 'Chinese_PRC_BIN'))
    RADN_EXAM_ID: Mapped[Optional[str]] = mapped_column(String(collation='Chinese_PRC_BIN'))
    DEVICE_TYPE: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_BIN'))
    DEVICE_NAME: Mapped[Optional[str]] = mapped_column(String(100, 'Chinese_PRC_BIN'))
    US_FREQ: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_BIN'))
    IMAGE_QLTY: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_BIN'))
    IMAGING_AGENT: Mapped[Optional[str]] = mapped_column(String(50, 'Chinese_PRC_BIN'))
    INJECTION_TIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    INJECTION_DOSAGE: Mapped[Optional[decimal.Decimal]] = mapped_column(Numeric(10, 2))
    DOSAGE_UNIT: Mapped[Optional[str]] = mapped_column(String(20, 'Chinese_PRC_BIN'))
    INJECTION_PART: Mapped[Optional[str]] = mapped_column(String(40, 'Chinese_PRC_BIN'))
    REPORT_AUDIT_TIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    AUDIT_DOC_ID: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'))
    AUDIT_DOC_SIG: Mapped[Optional[str]] = mapped_column(String(500, 'Chinese_PRC_BIN'))
    REPORT_URL: Mapped[Optional[str]] = mapped_column(String(2048, 'Chinese_PRC_BIN'))
    CRITIC_VALUE_FLAG: Mapped[Optional[str]] = mapped_column(String(10, 'Chinese_PRC_BIN'))
    REPORT_NOTE: Mapped[Optional[str]] = mapped_column(String(255, 'Chinese_PRC_BIN'))
    BARCODE_NO: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'))
    BATCH_NO: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'))


class LABREPORT(Base):
    __tablename__ = 'LAB_REPORT'
    __table_args__ = (
        PrimaryKeyConstraint('VISITING_SEQ_NO', 'ORG_CODE', 'VISITING_CATEGORY', 'LAB_REPORT_NO', 'LAB_FLAG',
                             'SYSTEM_FLAG', name='PK_LAB_REPORT'),
    )

    VISITING_SEQ_NO: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), primary_key=True, comment='就诊流水号')
    ORG_CODE: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'), primary_key=True, comment='医疗机构代码')
    VISITING_CATEGORY: Mapped[str] = mapped_column(String(10, 'Chinese_PRC_BIN'), primary_key=True, comment='就诊类别')
    ADMISSION_NO: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='住院号')
    OUTPATIENT_NO: Mapped[str] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='门(急)诊号')
    HEALTHCARD_NO: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='就诊卡号')
    LAB_REPORT_NO: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), primary_key=True,
                                               comment='检验报告单编号')
    ITEM_NAME: Mapped[str] = mapped_column(String(256, 'Chinese_PRC_BIN'), comment='标准项目名称')
    TEST_TUBE_BARCODE: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='未定义')
    LAB_FLAG: Mapped[str] = mapped_column(String(2, 'Chinese_PRC_BIN'), primary_key=True, comment='未定义')
    APPLY_WARD_CODE: Mapped[str] = mapped_column(String(16, 'Chinese_PRC_BIN'), comment='申请病区代码')
    APPLY_WARD_NAME: Mapped[str] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='申请病区名称')
    BED_NO: Mapped[str] = mapped_column(String(16, 'Chinese_PRC_BIN'), comment='床位号')
    LAB_METHOD: Mapped[str] = mapped_column(String(256, 'Chinese_PRC_BIN'), comment='未定义')
    OFFICIAL_REPORT_FLAG: Mapped[str] = mapped_column(String(1, 'Chinese_PRC_BIN'), comment='是否正式报告')
    REPORT_URL: Mapped[str] = mapped_column(String(128, 'Chinese_PRC_BIN'), comment='报告链接')
    CRITIC_VALUE_FLAG: Mapped[str] = mapped_column(String(1, 'Chinese_PRC_BIN'), comment='数据分类代码')
    REPORT_NOTE: Mapped[str] = mapped_column(String(255, 'Chinese_PRC_BIN'), comment='报告备注')
    SAMPLE_NOTE: Mapped[str] = mapped_column(String(512, 'Chinese_PRC_BIN'), comment='未定义')
    CHARACT_DESCRIPTION: Mapped[str] = mapped_column(String(512, 'Chinese_PRC_BIN'), comment='未定义')
    DIAG_OPINION_ADVICE: Mapped[str] = mapped_column(String(512, 'Chinese_PRC_BIN'), comment='未定义')
    SYSTEM_FLAG: Mapped[str] = mapped_column(String(50, 'Chinese_PRC_BIN'), primary_key=True, comment='数据来源')
    MICRO_REPORT_FLAG: Mapped[str] = mapped_column(String(14, 'Chinese_PRC_BIN'), server_default=text("('0')"))
    ORG_NAME: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='医疗机构名称')
    PAT_ID: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='患者ID')
    PAT_NAME: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='患者姓名')
    BABY_SERIAL: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='婴儿序号')
    SAMPLE_TYPE: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='未定义')
    REPORT_CATEGORY_CODE: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='报告类别代码')
    REPORT_CATEGORY_NAME: Mapped[Optional[str]] = mapped_column(String(256, 'Chinese_PRC_BIN'), comment='报告类别名称')
    APPLY_DEPT_CODE: Mapped[Optional[str]] = mapped_column(String(16, 'Chinese_PRC_BIN'), comment='申请科室代码')
    APPLY_DEPT_NAME: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='申请科室名称')
    APPLY_DOCTOR_ID: Mapped[Optional[str]] = mapped_column(String(16, 'Chinese_PRC_BIN'), comment='申请医生代码')
    APPLY_DOC_NAME: Mapped[Optional[str]] = mapped_column(String(256, 'Chinese_PRC_BIN'), comment='申请医生名称')
    APPLY_TIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='申请时间')
    CLINICAL_DIAG_CODE: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='临床诊断名称')
    CLINICAL_DIAG_NAME: Mapped[Optional[str]] = mapped_column(String(1024, 'Chinese_PRC_BIN'), comment='创建日期时间')
    TEST_SAMPLE_ID: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='未定义')
    DEVICE_NO: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='未定义')
    SAMPLING_TIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='标本采样日期时间')
    SAMPLING_DOC_ID: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='未定义')
    SAMPLING_DOC_NAME: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='未定义')
    DELIVERY_TIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='未定义')
    DELIVERY_DOC_ID: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='未定义')
    DELIVERY_DOC_NAME: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='未定义')
    SAMPLE_RECEIVE_TIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='接收标本日期时间')
    LAB_DEPT_CODE: Mapped[Optional[str]] = mapped_column(String(16, 'Chinese_PRC_BIN'), comment='未定义')
    LAB_DEPT_NAME: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='未定义')
    LAB_DOC_ID: Mapped[Optional[str]] = mapped_column(String(16, 'Chinese_PRC_BIN'), comment='未定义')
    LAB_DOC_NAME: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='未定义')
    LAB_TIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='未定义')
    REPORT_RELEASE_TIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='报告发布日期时间')
    REPORTER_ID: Mapped[Optional[str]] = mapped_column(String(16, 'Chinese_PRC_BIN'), comment='报告医师编码')
    REPORTER_NAME: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='报告医师姓名')
    REPORT_AUDIT_TIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='报告审核日期时间')
    AUDIT_DOC_ID: Mapped[Optional[str]] = mapped_column(String(16, 'Chinese_PRC_BIN'), comment='审核医师代码')
    AUDIT_DOC_SIG: Mapped[Optional[str]] = mapped_column(String(32, 'Chinese_PRC_BIN'), comment='审核医师签名')
    APPLY_FORM_NO: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='未定义')
    REPORT_STATUS_CODE: Mapped[Optional[str]] = mapped_column(String(4, 'Chinese_PRC_BIN'), comment='报告状态代码')
    LAB_REPORT_CORRECT: Mapped[Optional[str]] = mapped_column(String(10, 'Chinese_PRC_BIN'), comment='未定义')
    CRITIC_REPORT_STATUS: Mapped[Optional[str]] = mapped_column(String(10, 'Chinese_PRC_BIN'), comment='未定义')
    REC_STATUS: Mapped[Optional[str]] = mapped_column(String(10, 'Chinese_PRC_BIN'), comment='记录状态')
    DATA_STATUS: Mapped[Optional[str]] = mapped_column(String(2, 'Chinese_PRC_BIN'), comment='数据状态')
    DATA_UPDATE_TIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='更新日期时间')
    RECEIVE_TIME: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, comment='接收日期时间')
    BATCH_NO: Mapped[Optional[str]] = mapped_column(String(64, 'Chinese_PRC_BIN'), comment='批号')


t_LAB_RESULT = Table(
    'LAB_RESULT', Base.metadata,
    Column('VISITING_SEQ_NO', String(64, 'Chinese_PRC_BIN'), comment='就诊流水号'),
    Column('ORG_CODE', String(32, 'Chinese_PRC_BIN'), comment='医疗机构代码'),
    Column('ORG_NAME', String(64, 'Chinese_PRC_BIN'), comment='医疗机构名称'),
    Column('ADMISSION_NO', String(32, 'Chinese_PRC_BIN'), nullable=False, comment='住院号'),
    Column('OUTPATIENT_NO', String(32, 'Chinese_PRC_BIN'), nullable=False, comment='门(急)诊号'),
    Column('PAT_ID', String(64, 'Chinese_PRC_BIN'), comment='患者ID'),
    Column('HEALTHCARD_NO', String(64, 'Chinese_PRC_BIN'), nullable=False, comment='就诊卡号'),
    Column('PAT_NAME', String(64, 'Chinese_PRC_BIN'), comment='患者姓名'),
    Column('VISITING_CATEGORY', String(10, 'Chinese_PRC_BIN'), comment='就诊类别'),
    Column('LAB_REPORT_NO', String(64, 'Chinese_PRC_BIN'), comment='检验报告单编号'),
    Column('REPORT_CATEGORY_CODE', String(64, 'Chinese_PRC_BIN'), comment='报告类别代码'),
    Column('REPORT_CATEGORY_NAME', String(256, 'Chinese_PRC_BIN'), comment='报告类别名称'),
    Column('LAB_REPORT_DTL_NO', String(64, 'Chinese_PRC_BIN'), comment='检查报告单明细编号'),
    Column('LAB_INDEX_ITEM_CODE', String(32, 'Chinese_PRC_BIN'), comment='检查指标项目代码'),
    Column('LAB_INDEX_ITEM_NAME', String(128, 'Chinese_PRC_BIN'), comment='检查指标项目名称'),
    Column('LAB_INDEX_ITEM_ABBR', String(128, 'Chinese_PRC_BIN'), nullable=False, comment='检查指标项目简称'),
    Column('HIS_CHARGE_ITEM_CODE', String(64, 'Chinese_PRC_BIN'), comment='HIS收费项目代码'),
    Column('HIS_CHARGE_ITEM_NAME', String(128, 'Chinese_PRC_BIN'), comment='HIS收费项目名称'),
    Column('HIS_CHARGE_ITEM_TYPE', String(64, 'Chinese_PRC_BIN'), comment='HIS收费项目类型'),
    Column('LAB_RESULT_VALUE', String(1500, 'Chinese_PRC_BIN'), comment='检查结果值'),
    Column('LAB_RESULT_UNIT', String(32, 'Chinese_PRC_BIN'), comment='检查结果单位'),
    Column('ABNORMAL_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='异常标志'),
    Column('CRITIC_VALUE_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='数据分类代码'),
    Column('LAB_RESULT_REF_VALUE_QLTY', String(256, 'Chinese_PRC_BIN'), comment='检验结果参考值（定性）'),
    Column('LAB_RESULT_REF_VALUE_LL', String(64, 'Chinese_PRC_BIN'), comment='检验结果正常参考值下限'),
    Column('LAB_RESULT_REF_VALUE_UL', String(64, 'Chinese_PRC_BIN'), comment='检验结果正常参考值上限'),
    Column('PRINT_GROUP', String(64, 'Chinese_PRC_BIN'), nullable=False, comment='打印分组'),
    Column('DISPLAY_SEQ', String(20, 'Chinese_PRC_BIN'), comment='显示顺序'),
    Column('REC_STATUS', String(10, 'Chinese_PRC_BIN'), comment='记录状态'),
    Column('DATA_STATUS', String(2, 'Chinese_PRC_BIN'), comment='数据状态'),
    Column('SYSTEM_FLAG', String(50, 'Chinese_PRC_BIN'), comment='数据来源'),
    Column('DATA_UPDATE_TIME', DateTime, comment='更新日期时间'),
    Column('RECEIVE_TIME', DateTime, comment='接收日期时间'),
    Column('BATCH_NO', String(64, 'Chinese_PRC_BIN'), comment='批号'),
    Index('PK_LAB_RESULT', 'VISITING_SEQ_NO', 'ORG_CODE', 'LAB_REPORT_NO', 'LAB_REPORT_DTL_NO', 'LAB_INDEX_ITEM_CODE',
          'SYSTEM_FLAG', unique=True)
)

t_OPERANA_REC_INFO = Table(
    'OPERANA_REC_INFO', Base.metadata,
    Column('VISITING_SEQ_NO', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('ORG_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('ORG_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('VISITING_CATEGORY', String(10, 'Chinese_PRC_BIN'), nullable=False),
    Column('ADMISSION_NO', String(32, 'Chinese_PRC_BIN')),
    Column('OUTPATIENT_NO', String(32, 'Chinese_PRC_BIN')),
    Column('PAT_ID', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('PAT_NAME', String(50, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_SERIAL', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_ORDER_SERIAL', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('WARD_CODE', String(32, 'Chinese_PRC_BIN')),
    Column('WARD_NAME', String(64, 'Chinese_PRC_BIN')),
    Column('BED_NO', String(32, 'Chinese_PRC_BIN')),
    Column('APPLY_TIME', DateTime, nullable=False),
    Column('ARRANGE_TIME', DateTime, nullable=False),
    Column('OPER_CNT', Integer, nullable=False),
    Column('OPER_ROOM_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_BEGIN_TIME', DateTime, nullable=False),
    Column('OPER_END_TIME', DateTime, nullable=False),
    Column('OPER_CODE', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_NAME', String(256, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_DEPT_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_DEPT_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('ANA_METHOD_CODE', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('ANA_METHOD_NAME', String(256, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_PART_NAME', String(128, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_POSITION_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_POSITION_NAME', String(128, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_RANK_CODE', String(16, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_RANK_NAME', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('INCISION_TYPR_CODE', String(16, 'Chinese_PRC_BIN'), nullable=False),
    Column('INCISION_TYPE_NAME', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_TYPE_CODE', String(16, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_TYPE_NAME', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('PREOPER_DIAG_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('PREOPER_DIAG_NAME', String(128, 'Chinese_PRC_BIN'), nullable=False),
    Column('POSTOPER_DIAG_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('POSTOPER_DIAG_NAME', String(128, 'Chinese_PRC_BIN'), nullable=False),
    Column('INTERVENTION_NAME', String(128, 'Chinese_PRC_BIN')),
    Column('OH_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False),
    Column('SKIN_DISINFECT_DESC', String(128, 'Chinese_PRC_BIN')),
    Column('DRAIN_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False),
    Column('PREOPER_FASTING', String(10, 'Chinese_PRC_BIN'), nullable=False),
    Column('PREOPER_SPECIAL_CASE', String(1024, 'Chinese_PRC_BIN')),
    Column('OPER_SUCCESS_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False),
    Column('POSTOPER_DESTI_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('POSTOPER_DESTI_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('GUIDE_DOC_ID', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('GUIDE_DOC_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('CHIEF_SURGEON_ID', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('CHIEF_SURGEON_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('SURGEON_ASSIST1_ID', String(32, 'Chinese_PRC_BIN')),
    Column('SURGEON_ASSIST1_NAME', String(64, 'Chinese_PRC_BIN')),
    Column('SURGEON_ASSIST2_ID', String(32, 'Chinese_PRC_BIN')),
    Column('SURGEON_ASSIST2_NAME', String(64, 'Chinese_PRC_BIN')),
    Column('INST_NURSE_ID', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('INST_NURSE_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('TOUR_NURSE_ID', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('TOUR_NURSE_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('ANA_EXEC_DEPT_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('ANA_EXEC_DEPT_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('ANESTHESIOLOGIST_ID', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('ANESTHESIOLOGIST_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False),
    Column('ANESTHESIOLOGIST_ASSIST1_ID', String(32, 'Chinese_PRC_BIN')),
    Column('ANESTHESIOLOGIST_ASSIST1_NAME', String(64, 'Chinese_PRC_BIN')),
    Column('ANESTHESIOLOGIST_ASSIST2_ID', String(32, 'Chinese_PRC_BIN')),
    Column('ANESTHESIOLOGIST_ASSIST2_NAME', String(64, 'Chinese_PRC_BIN')),
    Column('OPER_ARRANGE_REC_STATUS', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('POSTOPER_SITUATION', String(500, 'Chinese_PRC_BIN')),
    Column('PATHOLOGY_EXAM', String(500, 'Chinese_PRC_BIN')),
    Column('PICK_DAY_OPER_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False),
    Column('DAY_OPER_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_STATUS', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('REC_STATUS', String(10, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_INCISION_HEALING_GRADE', String(20, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_T_LIMIT_TYPE_CODE', String(4, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_T_LIMIT_TYPE_NAME', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('DATA_STATUS', String(2, 'Chinese_PRC_BIN'), nullable=False),
    Column('SYSTEM_FLAG', String(50, 'Chinese_PRC_BIN'), nullable=False),
    Column('DATA_UPDATE_TIME', DateTime, nullable=False),
    Column('RECEIVE_TIME', DateTime, nullable=False),
    Column('BATCH_NO', String(64, 'Chinese_PRC_BIN')),
    Column('OPER_REG_NO', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('OPER_ICD_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('ENTER_OPER_ROOM_TIME', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('OUT_OPER_ROOM_TIME', String(32, 'Chinese_PRC_BIN'), nullable=False),
    Column('SEX_CODE', String(2, 'Chinese_PRC_BIN'), nullable=False, server_default=text("('')")),
    Column('SEX_NAME', String(16, 'Chinese_PRC_BIN'), nullable=False, server_default=text("('')")),
    Column('DEPT_CODE', String(10, 'Chinese_PRC_BIN'), nullable=False, server_default=text("('')")),
    Column('DEPT_NAME', String(50, 'Chinese_PRC_BIN'), nullable=False, server_default=text("('')")),
    Column('ROOM_NO', String(10, 'Chinese_PRC_BIN'), nullable=False, server_default=text("('')")),
    Column('WEIGHT', Numeric(6, 2)),
    Column('ABO_BLT_CODE', String(16, 'Chinese_PRC_BIN'), nullable=False, server_default=text("('')")),
    Column('ABO_BLT_NAME', String(32, 'Chinese_PRC_BIN'), nullable=False, server_default=text("('')")),
    Column('RH_BLT_CODE', String(16, 'Chinese_PRC_BIN'), nullable=False, server_default=text("('')")),
    Column('RH_BLT_NAME', String(32, 'Chinese_PRC_BIN'), nullable=False, server_default=text("('')")),
    Column('BIRTH_DATE', Date, nullable=False, server_default=text("('')")),
    Index('PK_OPERANA_REC_INFO', 'VISITING_SEQ_NO', 'ORG_CODE', 'VISITING_CATEGORY', 'OPER_SERIAL', 'SYSTEM_FLAG',
          unique=True)
)
t_ADMSN_INPAT_RFP = Table(
    'ADMSN_INPAT_RFP', Base.metadata,
    Column('ORG_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False, comment='医疗机构代码'),
    Column('PAT_ID', String(64, 'Chinese_PRC_BIN'), nullable=False, comment='患者ID'),
    Column('VISITING_SEQ_NO', String(64, 'Chinese_PRC_BIN'), nullable=False, comment='就诊流水号'),
    Column('EMR_NO', String(24, 'Chinese_PRC_BIN'), nullable=False, comment='疾病诊断编码'),
    Column('OUTPATIENT_NO', String(24, 'Chinese_PRC_BIN'), comment='门(急)诊号'),
    Column('PAT_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False, comment='患者姓名'),
    Column('SEX_NAME', String(8, 'Chinese_PRC_BIN'), nullable=False, comment='性别名称'),
    Column('BIRTH_TIME', DateTime, nullable=False, comment='出生日期时间'),
    Column('BIRTH_DATE', Date, comment='出生日期'),
    Column('EMPLOYER_CODE', String(32, 'Chinese_PRC_BIN'), comment='工作单位编码'),
    Column('IDCARD_NO', String(20, 'Chinese_PRC_BIN'), nullable=False, comment='身份证件号码'),
    Column('CONTACTER', String(64, 'Chinese_PRC_BIN'), comment='联系人姓名'),
    Column('CONTACTER_PAT_REL_CODE', String(2, 'Chinese_PRC_BIN'), comment='联系人与患者的关系代码'),
    Column('CONTACTER_TEL_NO', String(16, 'Chinese_PRC_BIN'), comment='联系人电话号码'),
    Column('CONTACTER_ADDR', String(256, 'Chinese_PRC_BIN'), comment='联系人地址'),
    Column('INSUR_CERT_NO', String(32, 'Chinese_PRC_BIN'), comment='医保凭证号'),
    Column('MAIN_CARD_NO', String(32, 'Chinese_PRC_BIN'), comment='主要卡号'),
    Column('HEALTHCARD_TYPE_CODE', String(2, 'Chinese_PRC_BIN'), comment='就诊卡类型'),
    Column('SOCIAL_INSUR_CARD_NO', String(32, 'Chinese_PRC_BIN'), comment='社保卡号'),
    Column('OTHER_CARD_NO', String(32, 'Chinese_PRC_BIN'), comment='其他卡号'),
    Column('PAT_STATUS', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='病人状态'),
    Column('PAT_TYPE_CODE', String(2, 'Chinese_PRC_BIN'), comment='患者类型代码'),
    Column('CURR_SEVERE_GRADE', String(2, 'Chinese_PRC_BIN'), nullable=False, comment='当前危重级别'),
    Column('MAIN_DIAG_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False, comment='疾病诊断编码'),
    Column('ER_OBS_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='急观标志'),
    Column('BABY_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='婴儿标志'),
    Column('INSUR_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False, comment='医疗保险类别代码'),
    Column('INSUR_FIXED_AMT', Numeric(14, 2), nullable=False, comment='医保定额'),
    Column('DEPT_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False, comment='科室代码'),
    Column('WARD_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False, comment='病区代码'),
    Column('DOC_ID', String(32, 'Chinese_PRC_BIN'), nullable=False, comment='医师编码'),
    Column('BED_NO', String(32, 'Chinese_PRC_BIN'), nullable=False, comment='床位号'),
    Column('NURSING_RANK_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False, comment='护理等级代码'),
    Column('NURSING_RANK_NAME', String(128, 'Chinese_PRC_BIN'), nullable=False, comment='护理等级名称'),
    Column('DIET_CODE', String(32, 'Chinese_PRC_BIN'), comment='饮食代码'),
    Column('DIET_ORDER', String(128, 'Chinese_PRC_BIN'), comment='饮食医嘱'),
    Column('OPERATOR_ID', String(32, 'Chinese_PRC_BIN'), comment='操作员号'),
    Column('RECORD_TIME', DateTime, nullable=False, comment='记录日期时间'),
    Column('INPATIENT_SEVERE_GRADE', String(2, 'Chinese_PRC_BIN'), nullable=False, comment='入院危重级别'),
    Column('ADMISSION_WAY_CODE', String(2, 'Chinese_PRC_BIN'), nullable=False, comment='入院途径代码'),
    Column('DISC_WAY_CODE', String(2, 'Chinese_PRC_BIN'), nullable=False, comment='出院方式'),
    Column('INPATIENT_CNT', Integer, nullable=False, comment='住院次数(次)'),
    Column('ADMISSION_TIME', DateTime, nullable=False, comment='入院日期时间'),
    Column('IN_WARD_TIME', DateTime, nullable=False, comment='入区日期时间'),
    Column('DISC_TIME', DateTime, comment='出院日期时间'),
    Column('OUT_WARD_TIME', DateTime, comment='出区日期时间'),
    Column('DISC_DIAG_CODE', String(32, 'Chinese_PRC_BIN'), comment='出院诊断编码'),
    Column('DISC_DIAG_NAME', String(256, 'Chinese_PRC_BIN'), comment='出院诊断名称'),
    Column('INSUR_CENTER_NO', String(36, 'Chinese_PRC_BIN'), comment='医保中心编号'),
    Column('INSUR_DISCHARGE_TYPE_CODE', String(4, 'Chinese_PRC_BIN'), comment='医保出院类型'),
    Column('FOLLOW_UP_VISIT_PAT_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='随访病人标志'),
    Column('PAT_ON_LEAVE_DISCHARGE_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='病人请假出院标志'),
    Column('BABY_TRANS_BED_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='婴儿转床标志'),
    Column('CADRE_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='干保标志'),
    Column('CLINICAL_PATH_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='临床路径标志'),
    Column('OUT_WARD_CALLBACK_AUDIT_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='出区召回审核标志'),
    Column('OUT_WARD_CALLBACK_REASON', String(1000, 'Chinese_PRC_BIN'), comment='出区召回原因'),
    Column('EMR_SEAL_UP_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='病历封存标志'),
    Column('EMR_SEAL_UP_TIME', DateTime, comment='病历封存日期时间'),
    Column('EMR_ARCHIVE_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='病历归档标志'),
    Column('EMR_ARCHIVE_TIME', DateTime, comment='病历归档日期时间'),
    Column('OUTPAT_DIAG_DOC_ID', String(32, 'Chinese_PRC_BIN'), comment='门诊诊断医生'),
    Column('OUTPAT_DIAG_DOC_2ND_ID', String(32, 'Chinese_PRC_BIN'), comment='门诊诊断医生2'),
    Column('NURSING_GROUP_CODE', String(32, 'Chinese_PRC_BIN'), comment='护理组代码'),
    Column('MED_GROUP_CODE', String(32, 'Chinese_PRC_BIN'), comment='医疗组代码'),
    Column('WEIGHT', String(16, 'Chinese_PRC_BIN'), comment='体重(kg)'),
    Column('SINGLE_DISEASE_DIAG_CODE', String(32, 'Chinese_PRC_BIN'), comment='单病种诊断代码'),
    Column('NRCMS_CODE', String(20, 'Chinese_PRC_BIN'), comment='新农合编号'),
    Column('RESP_NURSING_ID', String(32, 'Chinese_PRC_BIN'), comment='责任护士编码'),
    Column('SUPDOC_ID', String(32, 'Chinese_PRC_BIN'), comment='上级医师编码'),
    Column('ACCOUNT_FLAG', String(1, 'Chinese_PRC_BIN'), nullable=False, comment='账户标志'),
    Column('GUARANTOR_NAME', String(64, 'Chinese_PRC_BIN'), comment='担保人'),
    Column('GUARANTEE_AMT', Numeric(14, 2), comment='担保金额'),
    Column('DEPOSIT_STOP_DRUG_LINE', Numeric(14, 2), comment='押金停药线'),
    Column('DEPOSIT_ALERT_LINE', Numeric(14, 2), comment='押金报警线'),
    Column('ACCOUNT_BALANCE', Numeric(14, 2), comment='账户余额'),
    Column('WHOLE_TOT_AMT', Numeric(14, 2), comment='统筹累计金额'),
    Column('NOTE', String(128, 'Chinese_PRC_BIN'), comment='备注'),
    Column('DATA_UPDATE_TIME', DateTime, nullable=False, comment='数据更新日期时间'),
    Column('SYSTEM_FLAG', String(50, 'Chinese_PRC_BIN'), nullable=False, comment='系统标志'),
    Column('DATA_STATUS', String(10, 'Chinese_PRC_BIN'), nullable=False, comment='数据状态'),
    Column('ORG_NAME', String(128, 'Chinese_PRC_BIN'), nullable=False, server_default=text("(' ')")),
    Column('MAIN_DIAG_NAME', String(256, 'Chinese_PRC_BIN'), nullable=False, server_default=text("(' ')")),
    Column('DEPT_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False, server_default=text("(' ')")),
    Column('ADMISSION_DEPT_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False, server_default=text("(' ')")),
    Column('ADMISSION_DEPT_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False, server_default=text("(' ')")),
    Column('DISC_DEPT_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False, server_default=text("(' ')")),
    Column('DISC_DEPT_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False, server_default=text("(' ')")),
    Column('WARD_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False, server_default=text("(' ')")),
    Column('DOC_NAME', String(64, 'Chinese_PRC_BIN'), nullable=False, server_default=text("(' ')")),
    Column('OPERATOR_NAME', String(64, 'Chinese_PRC_BIN')),
    Column('OUTPAT_DIAG_DOC_NAME', String(64, 'Chinese_PRC_BIN')),
    Column('OUTPAT_DIAG_DOC_2ND_NAME', String(64, 'Chinese_PRC_BIN')),
    Column('RESP_NURSINGNAME', String(64, 'Chinese_PRC_BIN')),
    Column('SUPDOC_NAME', String(64, 'Chinese_PRC_BIN')),
    Column('SEX_CODE', String(32, 'Chinese_PRC_BIN'), nullable=False, server_default=text("(' ')")),
    Column('PREMIUM_NURSE_FLAG', String(128, 'Chinese_PRC_BIN')),
    Index('PK_ADMSN_INPAT_RFP', 'ORG_CODE', 'VISITING_SEQ_NO', 'SYSTEM_FLAG', unique=True)
)
