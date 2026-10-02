import os
from pathlib import Path
import tempfile
from unittest import TestCase
from unittest.mock import Mock, patch
from tempfile import TemporaryDirectory

from swytchit import SwytchitApp

from wizlib.test_case import WizLibTestCase

from swytchit.command.start_command import StartCommand
from swytchit.error import SwytchitError


class TestCommandStart(TestCase):

    def setUp(self):
        cwd = Path.cwd().resolve()
        home = Path.home().resolve()
        dir = tempfile.TemporaryDirectory()
        temp = Path(dir.name).resolve()

        def revert():
            os.environ['HOME'] = str(home)
            os.chdir(str(cwd))
            dir.cleanup()
        self.addCleanup(revert)
        os.environ['HOME'] = str(temp)
        os.chdir(str(temp))

    @patch('sys.stdin.isatty', Mock(return_value=True))
    @patch('subprocess.run', Mock())
    def test_takes_argument(self):
        (Path.cwd() / 'f').mkdir()
        SwytchitApp.start('start', 'f', debug=True)

    @patch('sys.stdin.isatty', Mock(return_value=False))
    @patch('subprocess.run', Mock())
    def test_error_if_not_tty(self):
        with self.assertRaises(Exception):
            (Path.cwd() / 'f').mkdir()
            SwytchitApp.start('start', 'f', debug=True)

    @patch('sys.stdin.isatty', Mock(return_value=True))
    @patch('subprocess.run', Mock())
    def test_error_if_not_valid_dir(self):
        with self.assertRaises(Exception):
            SwytchitApp.start('start', 'f', debug=True)

    @patch('sys.stdin.isatty', Mock(return_value=True))
    def test_error_if_outside_home(self):
        with \
                TemporaryDirectory() as d, \
                self.assertRaises(SwytchitError):
            c = StartCommand(directory=d)
            c.handle_vals()

    @patch('sys.stdin.isatty', Mock(return_value=True))
    def test_calls_shell(self):
        with \
                TemporaryDirectory() as d, \
                patch('subprocess.run', Mock()) as s:
            d2 = Path.cwd() / 'f'
            d2.mkdir()
            with open(d2 / '.swytchitrc.sh', 'w') as f:
                f.write('F=g')
            SwytchitApp.start('start', 'f', debug=True)
            x = s.call_args.args[0]
            self.assertEqual(1, len(x))

    @patch('sys.stdin.isatty', Mock(return_value=True))
    def test_changes_pwd(self):
        with \
                TemporaryDirectory() as d, \
                patch('subprocess.run', Mock()) as s:
            d2 = Path.cwd() / 'f'
            d2.mkdir()
            SwytchitApp.start('start', 'f', debug=True)
            self.assertEqual(str(d2), str(Path.cwd()))
