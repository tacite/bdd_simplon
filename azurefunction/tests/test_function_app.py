import os
import unittest
# mock is an object used for the tests
from unittest.mock import patch, call
import logging

# Import of the tested function
from function_app import scrapy_trigger

# Inherit from unit test class
class TestFunctionApp(unittest.TestCase):

    # Replace by mock objects for the tests
    @patch('function_app.os.path.exists')
    @patch('function_app.os.path.isdir')
    @patch('function_app.os.chdir')
    @patch('function_app.logging')
    def test_change_directory_success(self, mock_logging, mock_chdir, mock_isdir, mock_exists):
        # Configuration of the mock to get True when call
        mock_exists.return_value = True
        mock_isdir.return_value = True

        # Facke timer
        timer_request = None
        scrapy_trigger(timer_request)

        # Get the result of the tests with assert
        mock_chdir.assert_called_once_with('/home/site/wwwroot/simplonscrapy')
        mock_logging.info.assert_any_call('Changed directory to /home/site/wwwroot/simplonscrapy')

    # Same for failure testing
    @patch('function_app.os.path.exists')
    @patch('function_app.os.path.isdir')
    @patch('function_app.logging')
    def test_change_directory_failure(self, mock_logging, mock_isdir, mock_exists):
        # Configuration of the mock to get False when call
        mock_exists.return_value = False
        mock_isdir.return_value = False

        timer_request = None
        scrapy_trigger(timer_request)

        # Check the result if not change of directory
        mock_logging.error.assert_called_once_with('Directory /home/site/wwwroot/simplonscrapy does not exist or is not a directory')

if __name__ == '__main__':
    unittest.main()
