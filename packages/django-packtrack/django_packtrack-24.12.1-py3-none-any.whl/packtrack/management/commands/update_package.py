from django.core.management.base import BaseCommand, CommandError
from packtrack.models import OutdatedPackage, UpdateLog
import subprocess


class Command(BaseCommand):
    help = "Update the given package to the most recent version available in the PackTrack cache"

    def add_arguments(self, parser):
        parser.add_argument(
            "package_name", type=str, help="The name of the package to update"
        )

    def handle(self, *args, **kwargs):
        package_name = kwargs["package_name"]

        # Fetch the outdated package entry
        outdated_package = OutdatedPackage.objects.filter(name=package_name).first()

        if not outdated_package:
            raise CommandError(f"Package '{package_name}' does not exist.")

        old_version = outdated_package.installed_version
        latest_version = outdated_package.latest_version

        # Check if the package is already up to date
        if old_version == latest_version:
            self.stdout.write(
                self.style.SUCCESS(f"Package {package_name} is already up to date.")
            )
            return

        self.stdout.write(
            f'Updating "{package_name}" from {old_version} to {latest_version}...'
        )

        # Capture the output from the pip command
        try:
            # Run pip install with output capture
            result = subprocess.run(
                ["pip", "install", "--upgrade", package_name],
                capture_output=True,
                text=True,
            )

            # If the pip install was successful, update the database
            if result.returncode == 0:
                outdated_package.installed_version = latest_version
                outdated_package.save()

                # Log the update in UpdateLog
                UpdateLog.objects.create(
                    package_name=package_name,
                    old_version=old_version,
                    new_version=latest_version,
                    console_output=result.stdout
                    + result.stderr,  # Capture both stdout and stderr
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Package {package_name} updated to version {latest_version}"
                    )
                )
            else:
                # Handle failure and log the error output
                raise CommandError(
                    f"Error occurred while upgrading '{package_name}':\n{result.stderr}"
                )

        except subprocess.CalledProcessError as e:
            raise CommandError(
                f"Error occurred while upgrading '{package_name}': {str(e)}"
            )
