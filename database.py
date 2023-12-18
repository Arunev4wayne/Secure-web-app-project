from sqlalchemy import create_engine, text

db_connection_string="mysql+pymysql://2coiltgxc43qne0dxs88:pscale_pw_rW29zVrsv2FI74y4d67xIJDBApSS2MsWpQwA099XMCA@aws.connect.psdb.cloud/swd?charset=utf8mb4"
engine = create_engine(
 db_connection_string, 
 connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
 })