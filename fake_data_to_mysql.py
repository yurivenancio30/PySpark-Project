import random

import mysql.connector
from mysql.connector import Error
from faker import Faker

Faker.seed(33422)
fake = Faker()

conn = mysql.connector.connect(
    host="insert_host", database="spark", user="root", password="password"
)
cursor = conn.cursor()

for i in range(1000000):
    row = [fake.first_name(), random.randint(0, 99)]
    cursor.execute(
        " INSERT INTO `person` (name, age) VALUES (%s, %s);",
        (row[0], row[1]),
    )
    print(f"{i}, {row}")

conn.commit()
