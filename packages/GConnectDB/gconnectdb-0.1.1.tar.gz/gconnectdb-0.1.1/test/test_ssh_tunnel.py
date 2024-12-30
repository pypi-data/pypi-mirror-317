import unittest
from gconnectdb.ssh_tunnel import SSHTunnelMySQL
from unittest.mock import patch, MagicMock

class TestSSHTunnelMySQL(unittest.TestCase):

    @patch('subprocess.Popen')
    def test_start_tunnel(self, mock_popen):
        # Mock the Popen object
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        mock_process.poll.return_value = None  # Simulate the tunnel is open

        tunnel = SSHTunnelMySQL(
            ssh_host="1.1.1.1",
            ssh_user="test_user",
            pem_file="/path/to/pem_file.pem",
            mysql_host="mysql_host",
            mysql_port=3306,
            local_port=13307,
            totp_secret="sample_totp_secret",
            mysql_user="mysql_user",
            mysql_password="mysql_password",
            mysql_database="mysql_db"
        )

        result = tunnel.start_tunnel()
        self.assertTrue(result)

    @patch('mysql.connector.connect')
    def test_connect_mysql(self, mock_connect):
        # Mock MySQL connection
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        tunnel = SSHTunnelMySQL(
            ssh_host="1.1.1.1",
            ssh_user="test_user",
            pem_file="/path/to/pem_file.pem",
            mysql_host="mysql_host",
            mysql_port=3306,
            local_port=13307,
            totp_secret="sample_totp_secret",
            mysql_user="mysql_user",
            mysql_password="mysql_password",
            mysql_database="mysql_db"
        )

        conn = tunnel.connect_mysql()
        self.assertIsNotNone(conn)