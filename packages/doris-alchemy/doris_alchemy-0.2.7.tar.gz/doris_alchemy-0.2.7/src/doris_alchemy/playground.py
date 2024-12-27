import base64
import gzip
from typing import Optional
from sqlalchemy import Boolean, Enum, Integer, Numeric
from doris_alchemy.orm_base import DorisBase
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import create_engine, Engine


class Tst(DorisBase):
    __tablename__ = 'test_doris_table_1'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data: Mapped[float] = mapped_column(Numeric(12, 2))

ENC = 'utf-8'


if __name__ == '__main__':
    eng: Engine = create_engine('doris+pymysql://root:MA5fRnxhsLCVs5sm@10.0.100.115:9030/mpu_procurement_data')
    Tst.create(eng)

    # with Session(eng) as s:
    #     pass