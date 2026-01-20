Credit Approval System
A comprehensive Django REST Framework application for credit approval and loan management, built as part of an internship assignment. The system evaluates loan applications based on customer credit scores, historical payment data, and financial metrics.

Direct command for run:
Single Command Startup: docker-compose up --build starts everything
Data Loading: Run docker-compose run --rm web python [manage.py](http://_vscodecontentref_/0) load_data to load Excel data
API Testing: Use the provided cURL examples or tools like Postman
Database Access: Use the psql commands above to inspect data
Error Handling: All APIs include proper validation and error responses
Background Tasks: Celery processes Excel data asynchronously 

🚀 Features
Customer Registration: Register new customers with automatic credit limit calculation
Credit Score Evaluation: Advanced scoring based on payment history, loan activity, and current debt
Loan Approval Logic: Intelligent approval/rejection with interest rate adjustments
RESTful APIs: Complete API suite for all operations
Background Data Processing: Celery-powered Excel data ingestion
Database Management: PostgreSQL with proper relationships
Containerization: Fully dockerized for easy deployment
🛠 Tech Stack
Backend: Django 5.2, Django REST Framework
Database: PostgreSQL
Task Queue: Celery with Redis
Containerization: Docker & Docker Compose
Data Processing: Pandas, OpenPyXL
Development: Python 3.10
📋 Prerequisites
Docker and Docker Compose installed
Git (for cloning the repository)
🏁 Quick Start
1. Clone the Repository:
git clone https://github.com/yourusername/credit-approval-system.git
cd credit-approval-system

2. Start the Application
Everything runs from a single command!
docker-compose up --build

This command will:
Build all Docker images
Start PostgreSQL database
Start Redis for Celery
Run Django migrations
Start the web server on http://localhost:8000
Start Celery worker for background tasks
3. Load Sample Data (Optional)
In a new terminal:
docker-compose run --rm web python manage.py load_data
This loads customer and loan data from customer_data.xlsx and loan_data.xlsx using background tasks.

📖 API Documentation
The API is available at http://localhost:8000. All endpoints return JSON responses.

Endpoints
1. Register Customer
POST /register
{
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "monthly_income": 50000,
    "phone_number": 1234567890
}
Response:
{
    "customer_id": 1,
    "name": "John Doe",
    "age": 30,
    "monthly_income": 50000,
    "approved_limit": 1800000,
    "phone_number": 1234567890
}

2. Check Loan Eligibility
POST /check-eligibility
{
    "customer_id": 1,
    "loan_amount": 100000,
    "interest_rate": 10,
    "tenure": 12
}
Response:
{
    "customer_id": 1,
    "approval": true,
    "interest_rate": 10,
    "corrected_interest_rate": 10,
    "tenure": 12,
    "monthly_installment": 8791.59
}

3. Create Loan
POST /create-loan
{
    "customer_id": 1,
    "loan_amount": 100000,
    "interest_rate": 10,
    "tenure": 12
}
Response:
{
    "loan_id": 1,
    "customer_id": 1,
    "loan_approved": true,
    "message": "Loan approved",
    "monthly_installment": 8791.59
}

4. View Loan Details
GET /view-loan/<loan_id>
Response:
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

5. View Customer Loans
GET /view-loans/<customer_id>
Response:
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

Database Inspection:
# View customers
docker-compose exec db psql -U postgres -d creditdb -c "SELECT * FROM core_customer LIMIT 5;"

# View loans
docker-compose exec db psql -U postgres -d creditdb -c "SELECT * FROM core_loan LIMIT 5;"

# Count records
docker-compose exec db psql -U postgres -d creditdb -c "SELECT COUNT(*) FROM core_customer; SELECT COUNT(*) FROM core_loan;"

📊 Credit Score Logic
The system calculates credit scores based on:

Past Loans Paid on Time: Higher scores for better payment history
Number of Loans Taken: Balanced loan activity
Loan Activity in Current Year: Recent borrowing patterns
Loan Approved Volume: Total approved amounts
Approval Criteria:

Credit Score > 50: Approve loan
50 > Score > 30: Approve with interest rate > 12%
30 > Score > 10: Approve with interest rate > 16%
Score ≤ 10: Reject loan
Additional checks: Current debt ≤ approved limit, EMI ≤ 50% of monthly salary
🗄 Database Schema
Customer Model
id: Primary key
first_name, last_name: Customer name
age: Customer age
phone_number: Contact number
monthly_salary: Monthly income
approved_limit: Calculated credit limit (36 × monthly_salary)
current_debt: Sum of outstanding loan amounts
Loan Model
id: Primary key
customer_id: Foreign key to Customer
loan_amount: Approved loan amount
tenure: Loan duration in months
interest_rate: Annual interest rate
monthly_installment: Calculated EMI
emis_paid_on_time: Number of timely payments
start_date, end_date: Loan period
repayments_left: Remaining EMIs

🛑 Stopping the Application
docker-compose down

🤝 Contributing
Fork the repository
Create a feature branch
Make changes and test
Submit a pull request
