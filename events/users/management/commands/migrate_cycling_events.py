from django.core.management.base import BaseCommand

from apps.event.models import Event, User
from apps.membership.models import Organization

from .wrh import CyclingOrgEvent


class Command(BaseCommand):
    help = "Migrate data from CyclingOrgEvent to Event model"

    def handle(self, *args, **options):
        Event.objects.all().delete()
        for cycling_event in CyclingOrgEvent.objects.using("wrh").all():
            org = Organization.objects.get(name=cycling_event.organization.name)
            user = User.objects.get(email=cycling_event.create_by.email)
            description = cycling_event.description
            # Panel Migration
            try:
                for panel in cycling_event.more_data.get('panels', []):
                    description += f'<p><iframe frameborder="0" height="100%" width="100%"  sandbox="" scrolling="no" src="{panel.get("url")}" "></iframe></p><br>'
            except Exception as e: pass
            event = Event(
                # Migrate fields from CyclingOrgEvent to Event
                name=cycling_event.name,
                blurb=cycling_event.description,
                # TODO: Add logic to migrate description from more_data information board
                description=description,
                start_date=cycling_event.start_date,
                end_date=cycling_event.end_date,
                email=cycling_event.organizer_email,
                country=cycling_event.country,
                city=cycling_event.city,
                state=cycling_event.state,
                website=cycling_event.website,
                registration_website=cycling_event.registration_website,
                logo=cycling_event.logo,
                hero=cycling_event.prefs.get('banner_image') if cycling_event.prefs else None,  # Add logic to migrate hero image
                tags=cycling_event.tags,
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
