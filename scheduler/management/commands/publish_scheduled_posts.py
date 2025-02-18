from django.core.management.base import BaseCommand
from django.utils import timezone
from scheduler.models import Post

class Command(BaseCommand):
    help = "Publish scheduled posts when their scheduled time is reached"

    def handle(self, *args, **options):
        now = timezone.now()
        # Filter posts that are scheduled and whose scheduled_time is in the past
        scheduled_posts = Post.objects.filter(status='scheduled', scheduled_time__lte=now)
        count = scheduled_posts.count()
        if count == 0:
            self.stdout.write("No scheduled posts to publish at this time.")
            return

        # Update the status of each scheduled post to 'published'
        scheduled_posts.update(status='published')

        self.stdout.write(f"Published {count} scheduled post{'s' if count > 1 else ''}.")
