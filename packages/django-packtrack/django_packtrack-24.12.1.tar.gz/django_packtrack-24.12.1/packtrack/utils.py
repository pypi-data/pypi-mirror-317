import requests
import importlib.metadata
from django.conf import settings
from django.utils import timezone
from .models import PackageCache
from .models import OutdatedPackage


def get_installed_packages():
    packages = []
    for dist in importlib.metadata.distributions():
        packages.append(
            {
                "name": dist.metadata["Name"],
                "version": dist.version,
            }
        )
    return packages


def get_latest_version(package_name):
    # Try to get the package info from the cache
    try:
        package_cache = PackageCache.objects.get(name=package_name)
        cache_expiration_time = package_cache.last_checked + getattr(
            settings, "PACKTRACK_LATEST_VERSION_CACHE_TIME", timezone.timedelta(hours=1)
        )

        # If the cache is still valid, return the cached version
        if timezone.now() < cache_expiration_time:
            return package_cache.latest_version
    except PackageCache.DoesNotExist:
        package_cache = None  # No cache exists, we need to fetch from PyPI

    # Fetch the latest version from PyPI
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        latest_version = data["info"]["version"]

        # Update or create a cache entry
        if package_cache:
            package_cache.latest_version = latest_version
            package_cache.last_checked = timezone.now()
            package_cache.save()
        else:
            PackageCache.objects.create(
                name=package_name,
                latest_version=latest_version,
                last_checked=timezone.now(),
            )

        return latest_version
    else:
        return None  # Return None if unable to fetch from PyPI


def find_dependent_apps(package_name):
    dependent_apps = []

    # Loop over all installed packages and check if they depend on the given package
    for dist in importlib.metadata.distributions():
        requires = dist.metadata.get_all("Requires-Dist", [])

        # Check if the given package is a requirement
        if any(package_name in req for req in requires):
            dependent_apps.append(dist.metadata["Name"])

    return dependent_apps


def update_outdated_packages_list():
    # Clear the outdated packages table
    OutdatedPackage.objects.all().delete()

    installed_packages = get_installed_packages()

    for package in installed_packages:
        latest_version = get_latest_version(package["name"])
        if latest_version and package["version"] != latest_version:
            # Find all apps that depend on this package
            dependent_apps = find_dependent_apps(package["name"])
            dependent_apps_str = ", ".join(dependent_apps)

            # Create a new OutdatedPackage record in the database
            OutdatedPackage.objects.create(
                name=package["name"],
                installed_version=package["version"],
                latest_version=latest_version,
                last_checked=timezone.now(),
                dependent_apps=dependent_apps_str,
            )
