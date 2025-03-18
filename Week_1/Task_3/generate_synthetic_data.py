import random
from faker import Faker

# Initialize Faker to generate random data
fake = Faker()

# Generate SQL commands for creating tables
create_tables_sql = """
CREATE TABLE Staff (
    staff_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50)
);

CREATE TABLE Author (
    author_id SERIAL PRIMARY KEY,
    author_name VARCHAR(100)
);

CREATE TABLE Book (
    book_id SERIAL PRIMARY KEY,
    book_name VARCHAR(100),
    genre VARCHAR(50),
    published_date DATE,
    author_id INT REFERENCES Author(author_id)
);

CREATE TABLE Customer (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    phone_no VARCHAR(20),
    address TEXT,
    dob DATE,
    membership_date DATE,
    membership_status VARCHAR(20)
);

CREATE TABLE Transaction (
    transaction_id SERIAL PRIMARY KEY,
    book_id INT REFERENCES Book(book_id),
    customer_id INT REFERENCES Customer(customer_id),
    issue_date DATE,
    due_date DATE,
    status VARCHAR(20)
);
"""

# Insert data commands
def generate_insert_staff(num_records=10):
    sql = "INSERT INTO Staff (first_name, last_name) VALUES\n"
    values = []
    for _ in range(num_records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        values.append(f"('{first_name}', '{last_name}')")
    return sql + ",\n".join(values) + ";"

def generate_insert_author(num_records=10):
    sql = "INSERT INTO Author (author_name) VALUES\n"
    values = []
    for _ in range(num_records):
        author_name = fake.name()
        values.append(f"('{author_name}')")
    return sql + ",\n".join(values) + ";"

def generate_insert_books(num_records=20):
    sql = "INSERT INTO Book (book_name, genre, published_date, author_id) VALUES\n"
    values = []
    for _ in range(num_records):
        book_name = fake.sentence(nb_words=3)
        genre = random.choice(['Fiction', 'Non-Fiction', 'Mystery', 'Sci-Fi', 'Biography', 'Romance'])
        published_date = fake.date_between(start_date='-10y', end_date='today')
        author_id = random.randint(1, 10)  # Assuming 10 authors
        values.append(f"('{book_name}', '{genre}', '{published_date}', {author_id})")
    return sql + ",\n".join(values) + ";"

def generate_insert_customers(num_records=20):
    sql = "INSERT INTO Customer (customer_name, email, phone_no, address, dob, membership_date, membership_status) VALUES\n"
    values = []
    for _ in range(num_records):
        customer_name = fake.name()
        email = fake.email()
        phone_no = fake.phone_number()
        address = fake.address().replace("\n", ", ")
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
        membership_date = fake.date_between(start_date='-5y', end_date='today')
        membership_status = random.choice(['Active', 'Inactive'])
        values.append(f"('{customer_name}', '{email}', '{phone_no}', '{address}', '{dob}', '{membership_date}', '{membership_status}')")
    return sql + ",\n".join(values) + ";"

def generate_insert_transactions(num_records=30):
    sql = "INSERT INTO Transaction (book_id, customer_id, issue_date, due_date, status) VALUES\n"
    values = []
    for _ in range(num_records):
        book_id = random.randint(1, 20)  # Assuming 20 books
        customer_id = random.randint(1, 20)  # Assuming 20 customers
        issue_date = fake.date_between(start_date='-1y', end_date='today')
        due_date = fake.date_between(start_date=issue_date, end_date='+30d')
        status = random.choice(['Issued', 'Returned'])
        values.append(f"({book_id}, {customer_id}, '{issue_date}', '{due_date}', '{status}')")
    return sql + ",\n".join(values) + ";"

# Generate and print SQL insert commands
if __name__ == "__main__":
    print("Table creation SQL:\n")
    print(create_tables_sql)
    
    print("\n\nInsert Staff Data:\n")
    print(generate_insert_staff(10))

    print("\n\nInsert Author Data:\n")
    print(generate_insert_author(10))

    print("\n\nInsert Book Data:\n")
    print(generate_insert_books(20))

    print("\n\nInsert Customer Data:\n")
    print(generate_insert_customers(20))

    print("\n\nInsert Transaction Data:\n")
    print(generate_insert_transactions(30))
