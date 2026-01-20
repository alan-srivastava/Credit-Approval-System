import pandas as pd
from celery import shared_task
from .models import Customer, Loan

@shared_task
def load_customers():
    df = pd.read_excel("data/customer_data.xlsx")
    print("Customer columns:", df.columns.tolist())
    for _, row in df.iterrows():
        try:
            Customer.objects.create(
                id=row['Customer ID'],
                first_name=row['First Name'],
                last_name=row['Last Name'],
                phone_number=row['Phone Number'],
                monthly_salary=row['Monthly Salary'],
                approved_limit=row['Approved Limit'],
                current_debt=0,  # Assuming no current debt in initial data
                age=row['Age']
            )
        except Exception as e:
            print(f"Skipping customer {row['Customer ID']}: {e}")

@shared_task
def load_loans():
    df = pd.read_excel("data/loan_data.xlsx")
    print("Loan columns:", df.columns.tolist())
    for _, row in df.iterrows():
        try:
            Loan.objects.create(
                id=row['Loan ID'],
                customer_id=row['Customer ID'],
                loan_amount=row['Loan Amount'],
                tenure=row['Tenure'],
                interest_rate=row['Interest Rate'],
                monthly_installment=row['Monthly payment'],
                emis_paid_on_time=row['EMIs paid on Time'],
                start_date=row['Date of Approval'],
                end_date=row['End Date'],
            )
        except Exception as e:
            print(f"Skipping loan {row['Loan ID']}: {e}")
