from django.test import SimpleTestCase
from psycopg2 import OperationalError as Psycopg2OperationalError
from django.db.utils import OperationalError
from django.core.management import call_command
from unittest.mock import patch


@patch("core.management.commands.wait_for_db.Command.check")
class TestWaitForDbCommand(SimpleTestCase):
    def test_wait_for_db_ready(self, patched_check):
        patched_check.return_value = True
        call_command("wait_for_db")
        patched_check.assert_called_once_with(databases=["default"])

    @patch("time.sleep")
    def test_wait_for_db_not_ready(self, patched_time, patched_check):
        patched_check.side_effect = [Psycopg2OperationalError, OperationalError, True]
        call_command("wait_for_db")
        self.assertEqual(patched_check.call_count, 3)
        patched_check.assert_called_with(databases=["default"])