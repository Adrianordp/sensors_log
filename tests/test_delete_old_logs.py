# tests/test_delete_old_logs.py
import datetime
import unittest
from unittest.mock import MagicMock, patch

import pytest

from src.sensors_log.__main__ import (
    date_format,
    delete_old_logs,
    log_file,
    oldest_date,
)


@pytest.fixture
def mock_file():
    """Mock the file content"""
    mock_file = MagicMock()
    mock_file.readlines.return_value = [
        "2024-10-13 10:04:56 723,771,60.0\n",
        "2024-10-13 10:04:56 723,771,60.0\n",
    ]
    return mock_file


@pytest.fixture
def mock_open(mock_file):
    """Mock the file open"""
    mock_open = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file
    return mock_open


# def test_delete_old_logs_no_old_logs(mock_open):
#     """Test that delete_old_logs doesn't delete any logs if all logs are newer than 31 days"""
#     with patch("src.sensors_log.__main__.open", mock_open):
#         delete_old_logs()

#     mock_open.assert_called_once_with(log_file, "r+")
#     print(mock_file.__dict__)
#     mock_file.seek.assert_not_called()
#     mock_file.truncate.assert_not_called()


def test_delete_old_logs_file_not_found(mock_open):
    # Mock the file not found error
    mock_open.side_effect = FileNotFoundError()

    # Call the function
    delete_old_logs()

    # Assert that the function prints an error message
    assert mock_open.call_count == 1


# def test_delete_old_logs(mock_open):
#     """Test that delete_old_logs deletes old logs"""
#     time_40days_ago = (
#         datetime.datetime.now() - datetime.timedelta(days=40)
#     ).strftime(date_format)
#     time_31days_1min_ago = (
#         datetime.datetime.now() - datetime.timedelta(days=31, minutes=1)
#     ).strftime(date_format)
#     time_almost_31days_ago = (
#         datetime.datetime.now()
#         - datetime.timedelta(days=30, hours=23, minutes=59, seconds=59)
#     ).strftime(date_format)
#     # Mock the file content
#     mock_file = MagicMock()
#     # mock_file.readlines.return_value = [
#     #     f"{time_40days_ago} fan_speed_1,fan_speed_2,cpu_temp\n",
#     #     f"{time_31days_1min_ago} fan_speed_1,fan_speed_2,cpu_temp\n",
#     #     f"{time_almost_31days_ago} fan_speed_1,fan_speed_2,cpu_temp\n",
#     # ]

#     mock_file = mock_open.return_value.__enter__.return_value
#     mock_file.readlines.return_value = [
#         f"{time_40days_ago} fan_speed_1,fan_speed_2,cpu_temp\n",
#         f"{time_31days_1min_ago} fan_speed_1,fan_speed_2,cpu_temp\n",
#         f"{time_almost_31days_ago} fan_speed_1,fan_speed_2,cpu_temp\n",
#     ]

#     with patch("src.sensors_log.__main__.open", mock_open):
#         delete_old_logs()

#     mock_open.assert_called_once_with(log_file, "r+")
#     mock_file.seek.assert_called_once_with(0)
#     mock_file.truncate.assert_called_once_with(0)
#     mock_file.write.assert_called_once_with(
#         "2024-10-13 10:04:56 723,771,60.0\n"
#     )


class TestDeleteOldLogs(unittest.TestCase):
    #     @patch("src.sensors_log.__main__.open")
    #     def test_delete_old_logs(self, mock_open):
    #         time_4days_ago = (
    #             datetime.datetime.now() - datetime.timedelta(days=40)
    #         ).strftime(date_format)
    #         time_31days_1min_ago = (
    #             datetime.datetime.now() - datetime.timedelta(days=31, minutes=1)
    #         ).strftime(date_format)
    #         time_almost_31days_ago = (
    #             datetime.datetime.now()
    #             - datetime.timedelta(days=30, hours=23, minutes=59, seconds=59)
    #         ).strftime(date_format)
    #         # Mock the file content
    #         mock_file = MagicMock()
    #         mock_file.readlines.return_value = [
    #             f"{time_4days_ago} fan_speed_1,fan_speed_2,cpu_temp\n",
    #             f"{time_31days_1min_ago} fan_speed_1,fan_speed_2,cpu_temp\n",
    #             f"{time_almost_31days_ago} fan_speed_1,fan_speed_2,cpu_temp\n",
    #         ]
    #         mock_open.return_value.__enter__.return_value = mock_file

    #         # Call the function
    #         delete_old_logs()

    #         # Assert that the file was truncated and written to
    #         mock_file.seek.assert_called_once_with(0)
    #         mock_file.truncate.assert_called_once_with(0)
    #         mock_file.write.assert_called_once_with(
    #             f"{time_almost_31days_ago} fan_speed_1,fan_speed_2,cpu_temp\n"
    # )

    @patch("src.sensors_log.__main__.open")
    def test_delete_old_logs_file_not_found(self, mock_open):
        # Mock the file not found error
        mock_open.side_effect = FileNotFoundError()

        # Call the function
        delete_old_logs()

        # Assert that the function prints an error message
        self.assertEqual(mock_open.call_count, 1)

    # @patch("src.sensors_log.__main__.time")
    # def test_delete_old_logs_no_old_logs(self, mock_open):
    #     time_28days_ago = (
    #         datetime.datetime.now() - datetime.timedelta(days=28)
    #     ).strftime(date_format)
    #     time_29days_ago = (
    #         datetime.datetime.now() - datetime.timedelta(days=29)
    #     ).strftime(date_format)
    #     time_30days_ago = (
    #         datetime.datetime.now() - datetime.timedelta(days=30)
    #     ).strftime(date_format)

    #     # Mock the file content
    #     mock_file = MagicMock()
    #     mock_file.readlines.return_value = [
    #         f"{time_28days_ago} fan_speed_1,fan_speed_2,cpu_temp\n",
    #         f"{time_29days_ago} fan_speed_1,fan_speed_2,cpu_temp\n",
    #         f"{time_30days_ago} fan_speed_1,fan_speed_2,cpu_temp\n",
    #     ]
    #     mock_open.return_value.__enter__.return_value = mock_file

    #     mock_file.seek.assert_not_called()
    #     mock_file.truncate.assert_not_called()
