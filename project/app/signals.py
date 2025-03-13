from .models import UserProfile, LoanRequest
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from datetime import datetime, timedelta
import random
import csv

def add_users():
    """
    Adds both advisors (manually defined) and clients from a CSV file to the UserProfile table.
    """
    # List of advisors to add
    advisors = [
        {"username": "DavidAdvisor", "email": "david@advisor.fr", "password": "davidpass", "role": "advisor", "first_name": "David", "last_name": "Advisor", "is_staff": True},
        {"username": "DorotheeAdvisor", "email": "dorothee@advisor.fr", "password": "doropass", "role": "advisor", "first_name": "Dorothée", "last_name": "Advisor", "is_staff": True},
        {"username": "SamiAdvisor", "email": "sami@advisor.fr", "password": "samipass", "role": "advisor", "first_name": "Sami", "last_name": "Advisor", "is_staff": True},
    ]

    # Adding advisors
    for user_data in advisors:
        if not UserProfile.objects.filter(username=user_data["username"]).exists():
            user = UserProfile.objects.create_user(
                username=user_data["username"],
                email=user_data["email"],
                password=user_data["password"],
                role=user_data["role"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"]
            )
            user.is_staff = user_data["is_staff"]
            user.save()
            print(f"Advisor {user.username} added successfully.")
        else:
            print(f"Advisor {user_data['username']} already exists.")

    # Adding clients from the CSV
    file_path = "project/project/data/users_prepared.csv"
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            if not UserProfile.objects.filter(username=row["username"]).exists():
                advisor = UserProfile.objects.get(id=row["advisor_id"])  # Link the advisor from the advisor_id
                user = UserProfile.objects.create_user(
                    username=row["username"],
                    email=row["email"],
                    password=row["password"],
                    role=row["role"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    is_staff=row["is_staff"]
                )
                user.advisor = advisor  # Link the advisor
                user.save()
                print(f"Client {user.username} added successfully with advisor {advisor.username}.")
            else:
                print(f"Client {row['username']} already exists.")

def add_loans():
    """
    Adds loans from a CSV file and assigns them to the correct users.
    """
    file_path = "project/project/data/loans_prepared.csv"

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Check if the users and advisors exist
            try:
                user = UserProfile.objects.get(id=row['user_id'])
                advisor = UserProfile.objects.get(id=row['advisor_id'])
            except UserProfile.DoesNotExist:
                print(f"User or Advisor not found for Loan Request: user_id={row['user_id']}, advisor_id={row['advisor_id']}")
                continue

            # Generate a random date between 2010 and 2024 for more realism
            random_days = random.randint(0, 14 * 365)  # 14 years max (since 2010)
            created_at = datetime(2010, 1, 1) + timedelta(days=random_days)

            LoanRequest.objects.create(
                user=user,
                advisor=advisor,
                created_at=created_at,
                amount=float(row['GrAppv']),
                term=int(row['Term']),
                low_doc=row['LowDoc'],
                rev_line_cr=row['RevLineCr'],
                no_emp=int(row['NoEmp']),
                naics=row['NAICS_Sectors'],
                new=row['New'],
                franchise=row['Franchise'],
                state=row['State'],
                rural=row['Rural'],
                status=row['PIF'],
            )
            print(f"Loan for user {user.username} added successfully.")

        
@receiver(post_migrate)
def populate_database(sender, **kwargs):
    """
    Adds users and loans if the database is empty.
    """
    if not UserProfile.objects.exists():  # Check if the UserProfile table is empty
        print("The database is empty. Adding users...")
        add_users()
    else:
        print("Users already exist. No addition needed.")

    if not LoanRequest.objects.exists():  # Check if the LoanRequest table is empty
        print("Adding loans...")
        add_loans()
    else:
        print("Loans already exist. No addition needed.")