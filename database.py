from sqlalchemy import create_engine, text

<<<<<<< HEAD
db_connection_string="mysql+pymysql://dsis161qa17e6ojjy41w:pscale_pw_7V9GBZruXMw8Kv2tZUtlStSdWMT3Vpz3osUthNCHVEp@eu-west.connect.psdb.cloud/swd?charset=utf8mb4"
engine = create_engine(
 db_connection_string, 
 connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
 })
