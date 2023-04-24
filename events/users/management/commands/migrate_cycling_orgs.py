from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
import json
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from apps.membership.models import Organization
from .wrh import  CyclingOrgOrganization


class Command(BaseCommand):
    help = 'Migrates data from CyclingOrgOrganization to Organization model'

    def migrate_cycling_org_organizations(self):
        # Get all the instances of CyclingOrgOrganization
        source_orgs = CyclingOrgOrganization.objects.using('wrh').all()

        # Loop through each instance
        for src_org in source_orgs:
            # Check if the organization with the same name already exists in the Organization model
            existing_org = Organization.objects.filter(name=src_org.name).first()

            if existing_org:
                print(f"Organization {src_org.name} already exists. Skipping migration.")
                continue

            # Create a new instance of the Organization model
            dest_org = Organization()

            # Map the fields from the source model to the destination model
            dest_org.name = src_org.name
            dest_org.type = src_org.type
            dest_org.social_media = json.loads(src_org.social_media) if src_org.social_media else None
            dest_org.about = src_org.about

            if src_org.logo:
                logo_url = src_org.logo
                try:
                    with NamedTemporaryFile(delete=True) as temp_logo:
                        temp_logo.write(requests.get(logo_url).content)
                        temp_logo.flush()
                        dest_org.logo.save(f"{src_org.name}_logo", File(temp_logo))
                except Exception as e:
                    print(f"Error saving logo for organization {src_org.name}: {e}")

            dest_org.signup_config = json.loads(src_org.signup_config) if src_org.signup_config else None
            # dest_org.member_fields_schema = json.loads(src_org.member_fields_schema) if src_org.member_fields_schema else None
            dest_org.verified = src_org.verified
            dest_org.website = src_org.website
            dest_org.address = src_org.address
            dest_org.city = src_org.city
            dest_org.country = src_org.country
            dest_org.email = src_org.email
            dest_org.email_verified = src_org.email_verified
            dest_org.phone = src_org.phone
            dest_org.phone_verified = src_org.phone_verified
            dest_org.state = src_org.state
            dest_org.zipcode = src_org.zipcode
            dest_org.membership_open = src_org.membership_open
            dest_org.approved = src_org.approved
            dest_org.waiver_text = src_org.waiver_text

            # Save the new instance
            try:
                dest_org.save()
                print(f"Organization {src_org.name} migrated successfully.")
            except ValidationError as e:
                print(f"Error migrating organization {src_org.name}: {e}")

    def handle(self, *args, **options):
        self.migrate_cycling_org_organizations()
