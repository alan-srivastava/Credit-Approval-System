[THIS PROJECT IS MADE TO RUN LOCALLY]

🚀 Credit Approval System

A comprehensive Django REST Framework application for credit approval and loan management, built as part of an internship assignment.
The system evaluates loan applications based on customer credit scores, historical payment data, and financial metrics, with full support for background processing and containerized deployment.

📌 Key Highlights

Single-command startup using Docker Compose

Automated credit score evaluation

Intelligent loan approval & interest rate adjustment

Asynchronous Excel data ingestion using Celery

RESTful API design with proper validation

Production-ready PostgreSQL schema

🛠 Tech Stack

Backend: Django 5.2, Django REST Framework

Database: PostgreSQL

Task Queue: Celery

Message Broker: Redis

Containerization: Docker & Docker Compose

Data Processing: Pandas, OpenPyXL

Language: Python 3.10

📋 Prerequisites

Ensure the following are installed:

Docker

Docker Compose

Git

🏁 Quick Start

1️⃣ Clone the Repository
git clone https://github.com/yourusername/credit-approval-system.git
cd credit-approval-system

2️⃣ Start the Application (Single Command)
docker-compose up --build


This single command will:

Build all Docker images

Start PostgreSQL database

Start Redis for Celery

Run Django migrations

Start the Django web server at http://localhost:8000

Start Celery workers for background tasks

3️⃣ Load Sample Data (Optional)

In a new terminal:

docker-compose run --rm web python manage.py load_data


This command loads customer and loan data from:

customer_data.xlsx

loan_data.xlsx

The ingestion runs asynchronously using Celery.

📖 API Documentation

Base URL:

http://localhost:8000


All endpoints return JSON responses.

🔹 1. Register Customer

POST /register

{
  "first_name": "John",
  "last_name": "Doe",
  "age": 30,
  "monthly_income": 50000,
  "phone_number": 1234567890
}


Response

{
  "customer_id": 1,
  "name": "John Doe",
  "age": 30,
  "monthly_income": 50000,
  "approved_limit": 1800000,
  "phone_number": 1234567890
}

🔹 2. Check Loan Eligibility

POST /check-eligibility

{
  "customer_id": 1,
  "loan_amount": 100000,
  "interest_rate": 10,
  "tenure": 12
}


Response

{
  "customer_id": 1,
  "approval": true,
  "interest_rate": 10,
  "corrected_interest_rate": 10,
  "tenure": 12,
  "monthly_installment": 8791.59
}

🔹 3. Create Loan

POST /create-loan

{
  "customer_id": 1,
  "loan_amount": 100000,
  "interest_rate": 10,
  "tenure": 12
}


Response

{
  "loan_id": 1,
  "customer_id": 1,
  "loan_approved": true,
  "message": "Loan approved",
  "monthly_installment": 8791.59
}

🔹 4. View Loan Details

GET /view-loan/<loan_id>

{
  "loan_id": 1,
  "customer": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": 1234567890,
    "age": 30
  },
  "loan_amount": 100000,
  "interest_rate": 10,
  "monthly_installment": 8791.59,
  "tenure": 12
}

🔹 5. View Customer Loans

GET /view-loans/<customer_id>

[
  {
    "loan_id": 1,
    "loan_amount": 100000,
    "interest_rate": 10,
    "monthly_installment": 8791.59,
    "repayments_left": 12
  }
]

🧪 Testing the Application
API Testing with cURL
# Register customer
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Alice","last_name":"Smith","age":28,"monthly_income":60000,"phone_number":9876543210}'

# Check eligibility
curl -X POST http://localhost:8000/check-eligibility \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"loan_amount":200000,"interest_rate":12,"tenure":24}'

# Create loan
curl -X POST http://localhost:8000/create-loan \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"loan_amount":200000,"interest_rate":12,"tenure":24}'

# View loans
curl http://localhost:8000/view-loans/1

🗄 Database Inspection
# View customers
docker-compose exec db psql -U postgres -d creditdb -c "SELECT * FROM core_customer LIMIT 5;"

# View loans
docker-compose exec db psql -U postgres -d creditdb -c "SELECT * FROM core_loan LIMIT 5;"

# Count records
docker-compose exec db psql -U postgres -d creditdb -c "SELECT COUNT(*) FROM core_customer; SELECT COUNT(*) FROM core_loan;"

📊 Credit Score Logic
Credit Score Factors

Past loans paid on time

Number of loans taken

Loan activity in the current year

Total approved loan volume

Approval Rules
Credit Score	Decision
> 50	Loan Approved
30–50	Approved with interest rate > 12%
10–30	Approved with interest rate > 16%
≤ 10	Loan Rejected
Additional Constraints

Current debt ≤ approved credit limit

EMI ≤ 50% of monthly salary

🗄 Database Schema
Customer Model

id (Primary Key)

first_name, last_name

age

phone_number

monthly_salary

approved_limit (36 × monthly salary)

current_debt

Loan Model

id (Primary Key)

customer_id (Foreign Key)

loan_amount

tenure

interest_rate

monthly_installment

emis_paid_on_time

start_date, end_date

repayments_left

🛑 Stopping the Application
docker-compose down

🤝 Contributing

Fork the repository

Create a feature branch

Make changes and test

Submit a pull request
