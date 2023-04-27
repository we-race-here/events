from django.core.management.base import BaseCommand

from apps.event.models import Event, User
from apps.membership.models import Organization

from .wrh import CyclingOrgEvent


class Command(BaseCommand):
    help = "Migrate data from CyclingOrgEvent to Event model"

    def handle(self, *args, **options):
        for cycling_event in CyclingOrgEvent.objects.using("wrh").all():
            org = Organization.objects.get(name=cycling_event.organization.name)
            user = User.objects.get(email=cycling_event.create_by.email)
            event = Event(
                # Migrate fields from CyclingOrgEvent to Event
                name=cycling_event.name,
                blurb=cycling_event.description,
                description=cycling_event.description,
                start_date=cycling_event.start_date,
                end_date=cycling_event.end_date,
                email=cycling_event.organizer_email,
                country=cycling_event.country,
                city=cycling_event.city,
                state=cycling_event.state,
                website=cycling_event.website,
                registration_website=cycling_event.registration_website,
                logo=cycling_event.logo,
                # hero=cycling_event.hero,  # Add logic to migrate hero image if needed
                tags=cycling_event.tags,
                # panels=cycling_event.more_data,  # Add logic to migrate panels from more_data if needed
                organization=org,
                create_by=user,
                location_lat=cycling_event.location_lat,
                location_lon=cycling_event.location_lon,
                permit_no=cycling_event.permit_no,
                is_usac_permitted=cycling_event.is_usac_permitted,
                featured_event=cycling_event.featured_event,
                approved=cycling_event.approved,
                publish_type=cycling_event.publish_type,
            )
            event.save()
            self.stdout.write(self.style.SUCCESS(f"Migrated event: {cycling_event.name}"))

        self.stdout.write(self.style.SUCCESS("Migration completed successfully"))
