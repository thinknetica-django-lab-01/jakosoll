from pytz import utc
from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management import BaseCommand
from main.email_sender import send_weeks_update


class Command(BaseCommand):

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=utc)
        scheduler.add_job(send_weeks_update, 'interval', days=7, id='send_emails', replace_existing=True)
        try:
            print("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            print('Stopping scheduler')
            scheduler.shutdown()
