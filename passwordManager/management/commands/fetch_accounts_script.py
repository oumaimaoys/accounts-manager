from ...models import User, Platform, Account
from django.core.management.base import BaseCommand


# this script runs the first time 
# you set the project and it's supposed to fetch all users 
# exsiting on all platforms and adding them to the database

class Command(BaseCommand):
    help = 'Populate the database with user accounts'
    
    def handle(self, *args, **options):
        platforms = Platform.objects.all()
        for platform in platforms:
            print(platform.platform_name)
            users = Account.get_all_users(platform=platform)
            for user in users:
                if not User.objects.filter(user_name = user["username"]).exists():
                    user_ = User.objects.create(user_name = user["username"], first_name = user["first name"], last_name = user["last name"], email = user["email"], password = "")
                else :
                    user_ = User.objects.get(user_name = user["username"])
                Account.objects.create(platform= platform, user = user_, status = user["status"], user_id_on_platform=user["id"])
            
            self.stdout.write(self.style.SUCCESS("Accounts on {platform} added to the database successfully."))

