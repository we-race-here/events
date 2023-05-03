from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from .wrh import WrhAccountUser

User = get_user_model()


class Command(BaseCommand):
    help = "Migrate WrhAccountUser data to User model in destination database"

    def handle(self, *args, **options):
        # Fetch data from source database
        source_data = WrhAccountUser.objects.using("wrh").all()

        # Save data to the destination database
        for record in source_data:
            # Map fields from WrhAccountUser to User
            destination_record = User(
                id=record.id,
                password=record.password,
                last_login=record.last_login,
                is_superuser=record.is_superuser,
                email=record.email,
                first_name=record.first_name,
                last_name=record.last_name,
                is_staff=record.is_staff,
                is_active=record.is_active,
                date_joined=record.date_joined,
                gender=record.gender,
                birth_date=record.birth_date,
                avatar=record.avatar,
                phone=None,  # No equivalent field in WrhAccountUser
                phone_verified=None,  # No equivalent field in WrhAccountUser
                address1=None,  # No equivalent field in WrhAccountUser
                address2=None,  # No equivalent field in WrhAccountUser
                country=None,  # No equivalent field in WrhAccountUser
                city=None,  # No equivalent field in WrhAccountUser
                state=None,  # No equivalent field in WrhAccountUser
                zipcode=None,  # No equivalent field in WrhAccountUser
                weight=None,  # No equivalent field in WrhAccountUser
                height=None,  # No equivalent field in WrhAccountUser
                social_media=None,  # No equivalent field in WrhAccountUser
                opt_in_email=record.opt_in_email,
                terms_of_service=record.terms_of_service,
                user_agreement_waiver=record.user_agreement_waiver,
                user_agreement_waiver_record=None,  # No equivalent field in WrhAccountUser
                # Add any other fields or mapping as needed
            )
            destination_record.save()
