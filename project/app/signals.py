from .models import UserProfile, LoanRequest
import csv
from django.db.models.signals import post_migrate
from django.dispatch import receiver

def add_users():
    """
    Adds specific users to the database with first name, last name, and staff status for advisors.
    """
    users_to_add = [
        # Advisors
        {"username": "DorotheeAdvisor", "email": "dorothee@advisor.fr", "password": "doropass", "role": "advisor", "first_name": "Dorothée", "last_name": "Advisor", "is_staff": True},
        {"username": "DavidAdvisor", "email": "david@advisor.fr", "password": "davidpass", "role": "advisor", "first_name": "David", "last_name": "Advisor", "is_staff": True},
        {"username": "SamiAdvisor", "email": "sami@advisor.fr", "password": "samipass", "role": "advisor", "first_name": "Sami", "last_name": "Advisor", "is_staff": True},

        # Clients
        {"username": "DorotheeUser", "email": "dorothee@user.fr", "password": "doropass", "role": "client", "first_name": "Dorothée", "last_name": "User", "is_staff": False},
        {"username": "DavidUser", "email": "david@user.fr", "password": "davidpass", "role": "client", "first_name": "David", "last_name": "User", "is_staff": False},
        {"username": "SamiUser", "email": "sami@user.fr", "password": "samipass", "role": "client", "first_name": "Sami", "last_name": "User", "is_staff": False},
    ]

    for user_data in users_to_add:
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
            print(f"User {user.username} ({user.role}) added successfully.")
        else:
            print(f"User {user_data['username']} already exists.")


def add_loans():
    """
    Adds loans to the database from a CSV file.
    """
    # Path to the CSV file
    file_path = 'project/project/data/data_django.csv'

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)  # Use DictReader to read columns by name
            loans_to_add = []

            for row in reader:
                # Retrieve the user associated with the loan
                try:
                    default_user = UserProfile.objects.get(username="DorotheeUser")
                except UserProfile.DoesNotExist:
                    print(f"User with ID {row['user_id']} not found. Skipped.")
                    continue

                # Add loan data to the list
                loans_to_add.append({
                    'user': default_user,
                    'amount': float(row['GrAppv']),
                    'term': float(row['Term']),
                    'low_doc': row['LowDoc'],
                    'rev_line_cr': row['RevLineCr'],
                    'no_emp': float(row['NoEmp']),
                    'naics': row['NAICS_Sectors'],
                    'new': row['New'],
                    'franchise': row['Franchise'],
                    'state': row['State'],
                    'rural': row['Rural'],
                    'status': row['PIF'],
                })
                
            # Create LoanRequest objects in the database
            for loan_data in loans_to_add:
                loan = LoanRequest.objects.create(**loan_data)
                loan.save()
                print(f"Loan of {loan.amount} € added successfully for user {loan.user.id}.")

    except FileNotFoundError:
        print(f"The file {file_path} is not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        
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