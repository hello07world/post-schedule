import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from scheduler.models import Post  # Adjust import based on your app name

class Command(BaseCommand):
    help = 'Create 50 fake Post objects'

    def handle(self, *args, **options):
        fake = Faker()
        status_choices = ['created', 'draft', 'scheduled', 'published', 'deleted']
        post_type_choices = ['simple', 'image', 'video']

        for i in range(50):
            user = fake.user_name()
            post_type = random.choice(post_type_choices)
            caption = fake.text(max_nb_chars=100)
            image_url = fake.image_url() if post_type == 'image' else None
            video_url = fake.url() if post_type == 'video' else None
            status = random.choice(status_choices)

            # If the status is "scheduled", generate a random future date
            scheduled_time = None
            if status == 'scheduled':
                scheduled_time = timezone.now() + timedelta(days=random.randint(1, 30))

            post = Post.objects.create(
                user=user,
                post_type=post_type,
                caption=caption,
                image_url=image_url,
                video_url=video_url,
                status=status,
                scheduled_time=scheduled_time,
            )

            self.stdout.write(self.style.SUCCESS(f"Created post {post.id}"))

        self.stdout.write(self.style.SUCCESS("Successfully created 50 fake posts."))
