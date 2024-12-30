import subprocess
import mysql.connector
import time
import os
import pyotp
from typing import Optional

class SSHTunnelMySQL:
    def __init__(self, 
                 ssh_host: str,
                 ssh_user: str,
                 pem_file: str,
                 mysql_host: str,
                 mysql_port: int,   
                 local_port: int,
                 totp_secret: str,
                 mysql_user: str,
                 mysql_password: str,
                 mysql_database: str):
        
        self.ssh_host = ssh_host
        self.ssh_user = ssh_user
        self.pem_file = os.path.expanduser(pem_file)
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.local_port = local_port
        self.totp_secret = totp_secret
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_database = mysql_database
        self.tunnel_process: Optional[subprocess.Popen] = None
        self.mysql_connection: Optional[mysql.connector.MySQLConnection] = None
        self.tunnel_active = False  # Flag to track tunnel state
        self.connection_active = False  # Flag to track MySQL connection state

    def create_expect_script(self) -> str:
        """Create temporary expect script file"""
        script_content = f'''#!/usr/bin/expect -f
set timeout -1

# Get TOTP code
set totp_code [exec oathtool --totp -b {self.totp_secret}]

spawn ssh -i {self.pem_file} \\
    -L {self.local_port}:{self.mysql_host}:{self.mysql_port} \\
    -o StrictHostKeyChecking=accept-new \\
    -o ServerAliveInterval=60 \\
    -o ExitOnForwardFailure=yes \\
    {self.ssh_user}@{self.ssh_host}

expect {{
    "Verification code:" {{
        send "$totp_code\\r"
        exp_continue
    }}
    "Are you sure you want to continue connecting" {{
        send "yes\\r"
        exp_continue
    }}
    "Permission denied" {{
        puts "Error: Permission denied"
        exit 1
    }}
    "Connection refused" {{
        puts "Error: Connection refused"
        exit 1
    }}
    timeout {{
        puts "Error: Connection timed out"
        exit 1
    }}
    eof {{
        puts "Error: Connection closed"
        exit 1
    }}
}}

# Keep tunnel active
interact
'''
        
        # Write script to temporary file
        script_path = '/tmp/ssh_tunnel.exp'
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o700)
        return script_path

    def start_tunnel(self) -> bool:
        """Start SSH tunnel using expect script"""
        if self.tunnel_active:
            print("SSH tunnel is already active. Skipping creation.")
            return True  # Tunnel is already active, no need to start it again

        try:
            script_path = self.create_expect_script()
            
            print(f"Starting SSH tunnel on local port {self.local_port}")
            self.tunnel_process = subprocess.Popen(
                [script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for tunnel to establish
            time.sleep(5)
            
            # Check if process is still running
            if self.tunnel_process.poll() is None:
                self.tunnel_active = True  # Tunnel is now active
                print("SSH tunnel established successfully")
                return True
            else:
                stdout, stderr = self.tunnel_process.communicate()
                print(f"Tunnel failed to establish:\nstdout: {stdout.decode()}\nstderr: {stderr.decode()}")
                return False
                
        except Exception as e:
            print(f"Error creating tunnel: {str(e)}")
            return False

    def tunnel_reestablish(self) ->bool:
        # if self.tunnel_process.poll() is not None:
        #     print("SSH tunnel is not getting established")
        #     self.tunnel_active=False
        #     self.start_tunnel()
        #     if self.tunnel_process.poll() is None:
        #         self.tunnel_active = True  # Tunnel is now active
        #         print("SSH tunnel established successfully")
        #         return True
        #     else:
        #         print("Failed to re-establish SSH Tunnel successfully")
        #         self.tunnel_process.terminate()
        #         return False
       if self.tunnel_process.poll() is None:
           self.start_tunnel()
           return True
       else:
           return False

           
            
    

    def connect_mysql(self, max_retries: int = 3, delay: int = 5) -> Optional[mysql.connector.MySQLConnection]:
        """Connect to MySQL through SSH tunnel with retries
        
        Args:
            max_retries: Maximum number of retry attempts
            delay: Delay in seconds between retries
        """
        if self.connection_active:
            print("MySQL connection already established. Reusing the connection.")
            return self.mysql_connection  # Return existing connection if active
        
        for attempt in range(max_retries):
            try:
                connection = mysql.connector.connect(
                    host='127.0.0.1',
                    port=self.local_port,
                    user=self.mysql_user,
                    password=self.mysql_password,
                    database=self.mysql_database
                )
                self.mysql_connection = connection  # Store connection
                self.connection_active = True  # Set connection as active
                print("MySQL connection established")
                return connection
            except mysql.connector.Error as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print("Max retries reached. Connection failed.")
                    return None

    def close(self):
        """Close tunnel and cleanup"""
        if self.tunnel_process:
            self.tunnel_process.terminate()
            self.tunnel_active = False  # Reset tunnel status
            print("SSH tunnel closed")
        
        if self.mysql_connection:
            self.mysql_connection.close()  # Close MySQL connection
            self.connection_active = False  # Reset connection status
            print("MySQL connection closed")
