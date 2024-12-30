from datetime import datetime, timezone
from django.utils import timezone as dj_timezone
from unittest.mock import patch, MagicMock
from django.test import TestCase
from packtrack.utils import (
    get_installed_packages,
    get_latest_version,
    find_dependent_apps,
    update_outdated_packages_list,
)
from packtrack.models import PackageCache, OutdatedPackage

from importlib.metadata import Distribution


class UtilsTestCase(TestCase):

    @patch("packtrack.utils.importlib.metadata.distributions")
    def test_get_installed_packages(self, mock_distributions):
        # Mock a distribution package
        mock_dist = MagicMock(spec=Distribution)
        mock_dist.metadata = {"Name": "Django"}
        mock_dist.version = "3.2"

        # Set the return value of distributions to our mock
        mock_distributions.return_value = [mock_dist]

        # Call the function
        packages = get_installed_packages()

        # Assert that the installed packages are correctly retrieved
        self.assertEqual(len(packages), 1)
        self.assertEqual(packages[0]["name"], "Django")
        self.assertEqual(packages[0]["version"], "3.2")

    @patch("packtrack.utils.requests.get")
    @patch("packtrack.utils.PackageCache.objects.get")
    def test_get_latest_version_from_cache(self, mock_get_cache, mock_requests):
        # Simulate a cache hit
        mock_cache = MagicMock()
        mock_cache.latest_version = "3.2"
        mock_cache.last_checked = dj_timezone.now()
        mock_get_cache.return_value = mock_cache

        # Call the function
        version = get_latest_version("Django")

        # Assert it returns the cached version
        self.assertEqual(version, "3.2")
        mock_requests.assert_not_called()  # No request to PyPI should be made

    @patch("packtrack.utils.requests.get")
    @patch("packtrack.utils.PackageCache.objects.get")
    def test_get_latest_version_from_pypi(self, mock_get_cache, mock_requests):
        # Simulate a cache miss (PackageCache.DoesNotExist)
        mock_get_cache.side_effect = PackageCache.DoesNotExist

        # Mock PyPI API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"info": {"version": "3.3"}}
        mock_requests.return_value = mock_response

        # Call the function
        version = get_latest_version("Django")

        # Assert it returns the PyPI version
        self.assertEqual(version, "3.3")
        mock_requests.assert_called_once()

    @patch("packtrack.utils.importlib.metadata.distributions")
    def test_find_dependent_apps(self, mock_distributions):
        # Mock two distributions, one with a dependency on Django and one without

        # Mock first distribution, which depends on Django
        mock_dist1 = MagicMock(spec=Distribution)
        mock_dist1.metadata = MagicMock()  # Mock metadata as an object
        mock_dist1.metadata.get_all.return_value = ["Django"]

        # Mock second distribution, which does not depend on Django
        mock_dist2 = MagicMock(spec=Distribution)
        mock_dist2.metadata = MagicMock()
        mock_dist2.metadata.get_all.return_value = []

        # Set the return value of distributions to our mock distributions
        mock_distributions.return_value = [mock_dist1, mock_dist2]

        # Call the function
        dependent_apps = find_dependent_apps("Django")

        # Assert that only 'SomeApp' (from dist1) is returned
        self.assertEqual(dependent_apps, [mock_dist1.metadata["Name"]])

    @patch("packtrack.utils.get_latest_version")
    @patch("packtrack.utils.get_installed_packages")
    @patch("packtrack.utils.find_dependent_apps")
    @patch("packtrack.utils.OutdatedPackage.objects.create")
    @patch("packtrack.utils.OutdatedPackage.objects.all")
    @patch("packtrack.utils.timezone.now")
    def test_update_outdated_packages_list(
        self,
        mock_timezone_now,
        mock_all,
        mock_create,
        mock_find_dependent_apps,
        mock_installed_packages,
        mock_get_latest_version,
    ):
        # Set a fixed timestamp for timezone.now
        fixed_now = datetime(2024, 9, 6, 9, 0, 0, tzinfo=timezone.utc)
        mock_timezone_now.return_value = fixed_now

        # Mock installed packages
        mock_installed_packages.return_value = [{"name": "Django", "version": "3.1"}]

        # Mock latest version from PyPI
        mock_get_latest_version.return_value = "3.2"

        # Mock find_dependent_apps to return a dependency
        mock_find_dependent_apps.return_value = ["pytest-django"]

        # Call the function
        update_outdated_packages_list()

        # Ensure the outdated package entry was created with the correct dependent app and fixed timestamp
        mock_create.assert_called_once_with(
            name="Django",
            installed_version="3.1",
            latest_version="3.2",
            last_checked=fixed_now,  # Fixed timestamp
            dependent_apps="pytest-django",  # Expected dependent app
        )
