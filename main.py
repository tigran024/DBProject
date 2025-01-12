from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Part, Car, Modification

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/parts/")
def create_part(
    name: str,
    price: int,
    car_section: str,
    company: str,
    warranty: str,
    db: Session = Depends(get_db),
):
    part = Part(name=name, price=price, car_section=car_section, company=company, warranty=warranty)
    db.add(part)
    db.commit()
    db.refresh(part)
    return part

@app.get("/parts/")
def get_parts(sort_by: str = Query("part_id"), order: str = Query("asc"), db: Session = Depends(get_db)):
    sort_columns = {
        "part_id": Part.part_id,
        "name": Part.name,
        "price": Part.price,
        "car_section": Part.car_section,
        "company": Part.company,
        "warranty": Part.warranty,
    }

    if sort_by not in sort_columns:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by value: {sort_by}")

    sort_order = asc if order == "asc" else desc
    return db.query(Part).order_by(sort_order(sort_columns[sort_by])).all()

@app.post("/cars/")
def create_car(
    appearance: str,
    power: int,
    year_of_manufacture: int,
    brand: str,
    owner: str,
    max_speed: int,
    db: Session = Depends(get_db),
):
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

@app.get("/cars/")
def get_cars(sort_by: str = Query("car_id"), order: str = Query("asc"), db: Session = Depends(get_db)):
    sort_columns = {
        "car_id": Car.car_id,
        "appearance": Car.appearance,
        "power": Car.power,
        "year_of_manufacture": Car.year_of_manufacture,
        "brand": Car.brand,
        "owner": Car.owner,
        "max_speed": Car.max_speed,
    }

    if sort_by not in sort_columns:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by value: {sort_by}")

    sort_order = asc if order == "asc" else desc
    return db.query(Car).order_by(sort_order(sort_columns[sort_by])).all()

@app.post("/modifications/")
def create_modification(
    modification_type: str,
    mechanic: str,
    date: str,
    max_speed_change: int,
    power_change: int,
    part_id: int,
    car_id: int,
    db: Session = Depends(get_db),
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

@app.get("/modifications/")
def get_modifications(sort_by: str = Query("modification_id"), order: str = Query("asc"), db: Session = Depends(get_db)):
    sort_columns = {
        "modification_id": Modification.modification_id,
        "modification_type": Modification.modification_type,
        "mechanic": Modification.mechanic,
        "date": Modification.date,
        "max_speed_change": Modification.max_speed_change,
        "power_change": Modification.power_change,
        "part_id": Modification.part_id,
        "car_id": Modification.car_id,
    }

    if sort_by not in sort_columns:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by value: {sort_by}")

    sort_order = asc if order == "asc" else desc
    return db.query(Modification).order_by(sort_order(sort_columns[sort_by])).all
    
@app.get("/modifications/filter/")
def filter_modifications(modification_type: str = None, mechanic: str = None, db: Session = Depends(get_db)):
    query = db.query(Modification)
    if modification_type:
        query = query.filter(Modification.modification_type == modification_type)
    if mechanic:
        query = query.filter(Modification.mechanic == mechanic)
    return query.all()

@app.get("/modifications/join/")
def join_modifications(db: Session = Depends(get_db)):
    return db.query(Modification, Part, Car).join(Part).join(Car).all()

@app.put("/modifications/update/")
def update_modifications(new_mechanic: str, old_modification_type: str, db: Session = Depends(get_db)):
    modifications = db.query(Modification).filter(Modification.modification_type == old_modification_type).all()
    if not modifications:
        raise HTTPException(status_code=404, detail="Modifications not found")
    for modification in modifications:
        modification.mechanic = new_mechanic
    db.commit()
    return {"updated": len(modifications)}

@app.get("/parts/group_by/")
def group_by_parts(db: Session = Depends(get_db)):
    return db.query(Part.company, func.count(Part.part_id).label("total")).group_by(Part.company).all()

@app.delete("/parts/")
def delete_all_parts(db: Session = Depends(get_db)):
    db.query(Part).delete()
    db.commit()
    return {"message": "All parts deleted"}

@app.delete("/cars/")
def delete_all_cars(db: Session = Depends(get_db)):
    db.query(Car).delete()
    db.commit()
    return {"message": "All cars deleted"}

@app.delete("/modifications/")
def delete_all_modifications(db: Session = Depends(get_db)):
    db.query(Modification).delete()
    db.commit()
    return {"message": "All modifications deleted"}
