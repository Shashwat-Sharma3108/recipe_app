"""
    Test custom management commands
"""
#40 >>>>

from unittest.mock import patch

from psycopg2 import OperationalError as Pyscopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.check') #mocking the command
class CommandTests(SimpleTestCase):
    def test_wait_for_db_ready(self, patched_check): #patched_check due to @patch() decorator
        patched_check.return_value = True

        call_command('wait_for_db') #checks if command is callable or not and checks if db is ready for connections

        patched_check.assert_called_once_with(databases=['default'])
    
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check): #inside out applying first is patch(time.sleep) then @patch('core.management.commands.wait_for_db.Command.check')
        """ Checking for OperationalError """
        patched_check.side_effect = [Pyscopg2Error] * 2 + \
            [OperationalError] * 3 + [True] #side_effect >>> raise Exception
        
        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6) #checking the above logic to check if the function was called 6 times

        patched_check.assert_called_with(databases=['default'])