from typing import Optional
from sqlalchemy import Boolean, Enum, Integer
from doris_alchemy.orm_base import DorisBase
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import create_engine, Engine


class Tst(DorisBase):
    __tablename__ = 'test_doris_table'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data: Mapped[bytes]



if __name__ == '__main__':
    eng: Engine = create_engine('doris+pymysql://root:MA5fRnxhsLCVs5sm@10.0.100.115:9030/mpu_procurement_data')
    Tst.create(eng)
    
    # with Session(eng) as s:
    #     row1 = Tst(id=1, bool_flag=True)
    #     row2 = Tst(id=2, bool_flag=False)
    #     s.add(row1)
    #     s.add(row2)
    #     s.commit()