#!/usr/bin/env python
from os import environ
from sys import argv

from django.core.management import execute_from_command_line


def main():
    environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    execute_from_command_line(argv)


if __name__ == '__main__':
    main()
