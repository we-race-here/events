from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.event.models import Event
from events.users.management.commands.brac import AcaEvent
from events.users.management.commands.brac import AcaEventtype
from config.helpers.Exception import exception


class Command(BaseCommand):
    help = 'Migrate data from AcaEvent model to Event model'
    def get_event_type(self, type):
        if type:
            try:
                type = AcaEventtype.objects.using('archive').get(id=type).type
                if type == 'Road':
                    return 'Road'
                # Todo: Add Mapping for all type of archive
                # Check in aca_eventtype table
                else:
                    return 'Road'
            except Exception as e:
                exception(e)
                return 'Road'
    @transaction.atomic
    def handle(self, *args, **options):
        aca_events = AcaEvent.objects.using('archive').all()

        for aca_event in aca_events:

            # convert Unix timestamp to Python datetime object
            if aca_event.eventdate is not None:
                event_date = datetime.fromtimestamp(aca_event.eventdate)
            else:
                event_date = None


            # We get or create an Event object for each AcaEvent
            event, created = Event.objects.get_or_create(
                name=aca_event.name,
                description=aca_event.description,
                start_date=event_date,
                end_date=event_date,
                website=aca_event.url,
                tags=[self.get_event_type(aca_event.eventtype)],
                city=aca_event.eventcity,
                state=aca_event.eventstate,
                # Todo: What is iac_event in archive

            )

            if created:
                self.stdout.write(self.style.SUCCESS('Successfully migrated event "%s"' % event.name))
            else:
                self.stdout.write(self.style.WARNING('Event "%s" already exists' % event.name))
