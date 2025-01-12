import requests
import random
from faker import Faker

faker = Faker()

BASE_URL = "http://127.0.0.1:8000"

def create_parts(num_parts=1):
    print(f"Creating {num_parts} parts...")
    for _ in range(num_parts):
        params = {
            "name": f"Part {random.randint(10000, 99999)}",
            "price": random.randint(1000, 50000),
            "car_section": f"Section {random.randint(1, 25)}",
            "company": random.choice(["Autoof", "PepeGroup", "Mark Auto", "AutoMAX"]),
            "warranty": f"{random.randint(1, 5)} years"
        }
        response = requests.post(f"{BASE_URL}/parts/", params=params)
        if response.status_code == 200:
            print(f"Part created: {params}")
        else:
            print(f"Failed to create part: {response.status_code} - {response.text}")

def create_cars(num_cars=1):
    print(f"Creating {num_cars} cars...")
    for _ in range(num_cars):
        params = {
            "appearance": faker.color_name(),
            "power": random.randint(100, 500),
            "year_of_manufacture": random.randint(2000, 2023),
            "brand": random.choice(["BMW", "Audi", "Ford", "Toyota"]),
            "owner": f"Owner {random.randint(1, 50)}",
            "max_speed": random.randint(150, 300)
        }
        response = requests.post(f"{BASE_URL}/cars/", params=params)
        if response.status_code == 200:
            print(f"Car created: {params}")
        else:
            print(f"Failed to create car: {response.status_code} - {response.text}")

def create_modifications(num_modifications=1):
    for _ in range(num_modifications):
        data = {
            "modification_type": random.choice(["Upgrade", "Repair"]),
            "mechanic": faker.name(),
            "date": str(faker.date_this_century()),
            "max_speed_change": random.randint(0, 50),
            "power_change": random.randint(0, 30),
            "part_id": _,
            "car_id": _
        }
        print(data)
        response = requests.post(f"{BASE_URL}/modifications/", params=data)
        if response.status_code == 200:
            print(f"Modification created: {data}")
        else:
            print(f"Failed to create modification: {response.status_code} - {response.text}")

if __name__ == "__main__":
    num_of_parts = 3
    num_of_cars = 2
    create_parts(num_of_parts)
    create_cars(num_of_cars)
    create_modifications(min(num_of_cars, num_of_parts))