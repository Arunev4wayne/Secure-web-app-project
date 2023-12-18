from sqlalchemy import create_engine, text

db_connection_string="mysql+pymysql://yyg7sar80ajo40rdx44l:pscale_pw_NtfWrHNH8yF0dxxssueZSQ0VoEpl7wBbDztIZLwpz8u@aws.connect.psdb.cloud/swd?charset=utf8mb4"
engine = create_engine(
 db_connection_string, 
 connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
 })
