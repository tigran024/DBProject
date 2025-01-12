from sqlalchemy.orm import Session
from models import Part, Car, Modification

def create_part(db: Session, name: str, price: int, car_section: str, company: str, warranty: str):
    part = Part(name=name, price=price, car_section=car_section, company=company, warranty=warranty)
    db.add(part)
    db.commit()
    db.refresh(part)
    return part

def get_parts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Part).offset(skip).limit(limit).all()

def create_car(db: Session, appearance: str, power: int, year_of_manufacture: int, brand: str, owner: str, max_speed: int):
    car = Car(
        appearance=appearance,
        power=power,
        year_of_manufacture=year_of_manufacture,
        brand=brand,
        owner=owner,
        max_speed=max_speed,
    )
    db.add(car)
    db.commit()
    db.refresh(car)
    return car

def get_cars(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Car).offset(skip).limit(limit).all()

def create_modification(
    db: Session,
    modification_type: str,
    mechanic: str,
    date: str,
    max_speed_change: int,
    power_change: int,
    part_id: int,
    car_id: int,
):

    modification = Modification(
        modification_type=modification_type,
        mechanic=mechanic,
        date=date,
        max_speed_change=max_speed_change,
        power_change=power_change,
        part_id=part_id,
        car_id=car_id,
    )
    db.add(modification)
    db.commit()
    db.refresh(modification)
    return modification

def get_modifications(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Modification).offset(skip).limit(limit).all()

def filter_modifications(db: Session, modification_type: str = None, mechanic: str = None):
    query = db.query(Modification)
    if modification_type:
        query = query.filter(Modification.modification_type == modification_type)
    if mechanic:
        query = query.filter(Modification.mechanic == mechanic)
    return query.all()

def join_modifications(db: Session):
    return db.query(Modification, Part, Car).join(Part).join(Car).all()

def update_modifications(db: Session, new_mechanic: str, old_modification_type: str):
    modifications = db.query(Modification).filter(Modification.modification_type == old_modification_type).all()
    if not modifications:
        return None
    for modification in modifications:
        modification.mechanic = new_mechanic
    db.commit()
    return modifications
