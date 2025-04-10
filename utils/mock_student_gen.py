import json
import random
import os
from faker import Faker

fake = Faker()

def generate_students(n=10):
    students = []
    for _ in range(n):
        student = {
            "name": fake.name(),
            "dob": fake.date_of_birth(minimum_age=17, maximum_age=22).isoformat(),
            "marks": random.randint(60, 95),
            "documents": {
                "marksheet": "uploaded",
                "id_proof": "uploaded"
            },
            "loan_request": random.choice([0, 50000, 100000, 150000]),
            "email": fake.email()
        }
        students.append(student)
    return students

def save_to_files(students, path="data"):
    os.makedirs(path, exist_ok=True)
    for i, student in enumerate(students):
        with open(f"{path}/student_{i+1}.json", "w") as f:
            json.dump(student, f, indent=2)

# Generate and save 10 students
if __name__ == "__main__":
    students = generate_students(10)
    save_to_files(students)
    print("✅ 10 sample student applications generated in /data")
