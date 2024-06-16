from sqlalchemy import BigInteger, Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def create_address_model(currency_name):
    class Address(Base):
        __tablename__ = f"{currency_name}_addresses"
        __table_args__ = {"extend_existing": True}

        address = Column(String(255), primary_key=True)
        block_number = Column(Integer)

    return Address


def create_utxo_model(currency_name):
    class UTXO(Base):
        __tablename__ = f"{currency_name}_utxo"
        __table_args__ = {"extend_existing": True}

        tx_id = Column(String(255), primary_key=True)
        output_n = Column(Integer, primary_key=True)
        address = Column(String(255))
        amount_satoshi = Column(BigInteger)
        used = Column(Boolean, default=False)

    return UTXO


def create_last_block_model(currency_name):
    class LastBlock(Base):
        __tablename__ = f"{currency_name}_last_block"
        __table_args__ = {"extend_existing": True}

        block_number = Column(Integer, primary_key=True)

    return LastBlock
