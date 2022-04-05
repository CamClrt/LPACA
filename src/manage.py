#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from config.settings.base import *  # noqa: F401, F403


def main():
    """Run administrative tasks."""
    if os.environ.get("PRODUCTION"):
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            "config.settings.production",
        )
    elif os.environ.get("GITHUB_WORKFLOW"):
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            "config.settings.ci",
        )
    else:
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE",
            "config.settings.local",
        )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
