import re
import psycopg2
from datetime import datetime
import requests


log_pattern = r'(?P<ip>\S+) - - $begin:math:display$(?P<timestamp>.?)$end:math:display$ "(?P<method>\S+) (?P<url>\S+) HTTP/1.1" (?P<status>\d{3}) \d+ "-" "(?P<user_agent>.)"'


conn = psycopg2.connect(
    dbname="apache_logs_db",  
    user="postgres",         
    password="anushka", 
    host="localhost"         
)
cursor = conn.cursor()

# Function to parse and insert log data into the database
def parse_and_insert_log(line):
    match = re.match(log_pattern, line)
    if match:
        log_data = match.groupdict()
        ip = log_data['ip']
        timestamp = datetime.strptime(log_data['timestamp'], '%d/%b/%Y:%H:%M:%S %z')
        method = log_data['method']
        url = log_data['url']
        status = int(log_data['status'])
        user_agent = log_data['user_agent']
        
        # Simple agent parsing for Browser and OS (you can refine this further)
        browser = "Mozilla" if "Mozilla" in user_agent else "Unknown"
        os = "Windows" if "Windows" in user_agent else "Unknown"
        
        # Insert the parsed data into PostgreSQL table
        cursor.execute("""
            INSERT INTO apache_logs (ip_address, timestamp, http_method, url_path, status_code, browser, os, user_agent)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (ip, timestamp, method, url, status, browser, os, user_agent))
        
        conn.commit()  # Save the data

# Sample log data URL
log_file_url = 'https://github.com/elastic/examples/raw/master/Common%20Data%20Formats/apache_logs/apache_logs'
log_lines = requests.get(log_file_url).text.splitlines()  # Get logs as a list of lines

# Parse and insert each log entry
for line in log_lines:
    parse_and_insert_log(line)

# Close the connection
cursor.close()
conn.close()