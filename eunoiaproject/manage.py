#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eunoiaproject.settings')
    if 'DEV' in os.environ.get('EUNOIA_ENV'):
        print("===========================================")
        print("ENVIRONMENT SET TO DEV")
        print("===========================================")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eunoiaproject.devsettings')
    elif 'PROD' in os.environ.get('EUNOIA_ENV'):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eunoiaproject.prodsettings')
        print("===========================================")
        print("ENVIRONMENT SET TO PROD")
        print("===========================================")
    elif 'LOCAL' in os.environ.get('EUNOIA_ENV'):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eunoiaproject.localsettings')
        print("===========================================")
        print("ENVIRONMENT SET TO LOCAL ENV")
        print("===========================================")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
