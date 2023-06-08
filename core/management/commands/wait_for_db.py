"""
    CREATING A MANAGEMENT COMMAND WHICH MAKES SURE DB IS READY FOR CONNECTION
"""
import time

from typing import Any, Optional
from django.core.management.base import BaseCommand

from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError

class Command(BaseCommand):
    '''
        Django commmand
    '''

    def handle(self, *args, **options):
        """
            Entry point for command
        """
        self.stdout.write('Waiting for database....')
        db_up = False
        
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (OperationalError, Psycopg2Error):
                self.stdout.write('Database Unavailable......')
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS('Database  Available....'))
