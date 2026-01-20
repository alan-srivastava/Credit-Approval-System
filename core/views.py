from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Customer, Loan
import math
from datetime import date
from dateutil.relativedelta import relativedelta

def calculate_emi(P, R, N):
    r = R / (12 * 100)
    return P * r * ((1 + r) ** N) / (((1 + r) ** N) - 1)

def calculate_credit_score(customer):
    loans = Loan.objects.filter(customer=customer)
    past_loans = loans.filter(end_date__lt=date.today())
    current_loans = loans.filter(end_date__gte=date.today())

    # Component 1: Past loans paid on time (10 points per fully paid loan)
    paid_on_time_score = sum(10 for l in past_loans if l.emis_paid_on_time >= l.tenure)

    # Component 2: Number of loans taken in past (5 points per loan, max 20)
    num_loans_score = min(len(past_loans) * 5, 20)

    # Component 3: Loan activity in current year (5 points per loan, max 20)
    current_year = date.today().year
    current_year_loans = loans.filter(start_date__year=current_year)
    activity_score = min(len(current_year_loans) * 5, 20)

    # Component 4: Loan approved volume (2 points per lakh, max 20)
    total_volume = sum(l.loan_amount for l in loans)
    volume_score = min(total_volume / 100000 * 2, 20)

    score = paid_on_time_score + num_loans_score + activity_score + volume_score

    # If sum of current loans > approved limit, score = 0
    current_debt = sum(l.loan_amount for l in current_loans)
    if current_debt > customer.approved_limit:
        score = 0

    return min(score, 100)

def check_eligibility_logic(customer, loan_amount, interest_rate, tenure):
    credit_score = calculate_credit_score(customer)
    current_loans = Loan.objects.filter(customer=customer, end_date__gte=date.today())
    total_emi = sum(l.monthly_installment for l in current_loans)

    # Check EMI condition
    emi_condition = total_emi < 0.5 * customer.monthly_salary

    approval = credit_score > 50 and emi_condition
    corrected_rate = interest_rate

    if credit_score <= 50 and credit_score > 30:
        corrected_rate = max(interest_rate, 12)
        approval = approval and True  # already checked
    elif credit_score <= 30 and credit_score > 10:
        corrected_rate = max(interest_rate, 16)
        approval = approval and True
    elif credit_score <= 10:
        approval = False

    emi = calculate_emi(loan_amount, corrected_rate, tenure)

    return {
        "customer_id": customer.id,
        "approval": approval,
        "interest_rate": interest_rate,
        "corrected_interest_rate": corrected_rate,
        "tenure": tenure,
        "monthly_installment": round(emi, 2)
    }

@api_view(['POST'])
def register(request):
    try:
        salary = request.data['monthly_income']
        approved_limit = round((36 * salary) / 100000) * 100000

        customer = Customer.objects.create(
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            age=request.data['age'],
            phone_number=request.data['phone_number'],
            monthly_salary=salary,
            approved_limit=approved_limit
        )

        return Response({
            "customer_id": customer.id,
            "name": f"{customer.first_name} {customer.last_name}",
            "age": customer.age,
            "monthly_income": salary,
            "approved_limit": approved_limit,
            "phone_number": customer.phone_number
        })
    except KeyError as e:
        return Response({"error": f"Missing field: {e}"}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def check_eligibility(request):
    try:
        customer = Customer.objects.get(id=request.data['customer_id'])
        result = check_eligibility_logic(
            customer,
            request.data['loan_amount'],
            request.data['interest_rate'],
            request.data['tenure']
        )
        return Response(result)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)
    except KeyError as e:
        return Response({"error": f"Missing field: {e}"}, status=400)

@api_view(['POST'])
def create_loan(request):
    try:
        customer = Customer.objects.get(id=request.data['customer_id'])
        eligibility = check_eligibility_logic(
            customer,
            request.data['loan_amount'],
            request.data['interest_rate'],
            request.data['tenure']
        )
        if not eligibility['approval']:
            return Response({
                "loan_id": None,
                "customer_id": customer.id,
                "loan_approved": False,
                "message": "Loan not approved due to eligibility criteria",
                "monthly_installment": eligibility['monthly_installment']
            })

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=request.data['loan_amount'],
            tenure=request.data['tenure'],
            interest_rate=eligibility['corrected_interest_rate'],
            monthly_installment=eligibility['monthly_installment'],
            start_date=date.today(),
            end_date=date.today() + relativedelta(months=request.data['tenure'])
        )

        return Response({
            "loan_id": loan.id,
            "customer_id": customer.id,
            "loan_approved": True,
            "message": "",
            "monthly_installment": loan.monthly_installment
        })
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)
    except KeyError as e:
        return Response({"error": f"Missing field: {e}"}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        customer = loan.customer
        return Response({
            "loan_id": loan.id,
            "customer": {
                "id": customer.id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "phone_number": customer.phone_number,
                "age": customer.age
            },
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_installment,
            "tenure": loan.tenure
        })
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found"}, status=404)

@api_view(['GET'])
def view_loans(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        loans = Loan.objects.filter(customer=customer)
        loan_data = []
        for loan in loans:
            repayments_left = loan.tenure - loan.emis_paid_on_time
            loan_data.append({
                "loan_id": loan.id,
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_installment,
                "repayments_left": repayments_left
            })
        return Response(loan_data)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)


@api_view(['GET'])
def api_root(request):
    return Response({
        "message": "Credit Approval System API",
        "endpoints": [
            "register",
            "check-eligibility",
            "create-loan",
            "view-loan/<loan_id>",
            "view-loans/<customer_id>"
        ]
    })
