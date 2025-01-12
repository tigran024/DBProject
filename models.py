from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Part(Base):
    __tablename__ = "parts"

    part_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    car_section = Column(String, nullable=False)
    company = Column(String, nullable=False)
    warranty = Column(String, nullable=False)

    modifications = relationship("Modification", back_populates="part")

class Car(Base):
    __tablename__ = "cars"

    car_id = Column(Integer, primary_key=True, index=True)
    appearance = Column(String, nullable=False)
    power = Column(Integer, nullable=False)
    year_of_manufacture = Column(Integer, nullable=False)
    brand = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    max_speed = Column(Integer, nullable=False)

    modifications = relationship("Modification", back_populates="car")

class Modification(Base):
    __tablename__ = "modifications"

    modification_id = Column(Integer, primary_key=True, index=True)
    modification_type = Column(String, nullable=False)
    mechanic = Column(String, nullable=False)
    date = Column(String, nullable=False)
    max_speed_change = Column(Integer, nullable=False)
    power_change = Column(Integer, nullable=False)

    part_id = Column(Integer, ForeignKey("parts.part_id"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.car_id"), nullable=False)

    part = relationship("Part", back_populates="modifications")
    car = relationship("Car", back_populates="modifications")
