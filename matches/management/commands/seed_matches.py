from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Command for seeding the match table in the database"

    def handle(self, *args, **options) -> None:
        """
        Executes the command
        """

        self.stdout.write("To be implemented...")
