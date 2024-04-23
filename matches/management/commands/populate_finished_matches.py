from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populate finished matches"

    def handle(self, *args, **options) -> None:
        """
        Execute the command to populate finished matches
        """

        self.stdout.write(self.style.SUCCESS(self.help))
