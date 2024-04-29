from apps.users.models import User, Address, Organization
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Populate the database with users'

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int, help='Number of users to create')

    def handle(self, *args, **options):
        num_users = options['num_users']
        address_data = {
            "address_line_1": "street 4, block 4",
            "address_line_2": "dha phase 2",
            "city": "Islamabad",
            "state": "Federal",
            "country": "Pakistan",
            "phone_number": "090078601",
            "role": "Backend Developer"
        }
        org = Organization.objects.create(name="dummy organization")
        address = Address.objects.create(**address_data)

        user_instances = []
        for i in range(num_users):
            password = f"dummyuser{i}"
            user_data = {
                "name": f"User {i}",
                "username": f"dummyuser{i}",
                "email": f"dummyuser{i}@yopmail.com",
                "organization": org,
                "password": make_password(password)
            }
            user_instances.append(User(**user_data))
            print(i)
        users = User.objects.bulk_create(user_instances)
        for user in users:
            user.addresses.set([1])
        print("Users Created Successfully")
