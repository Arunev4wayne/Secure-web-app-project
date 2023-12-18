from sqlalchemy import create_engine, text

db_connection_string="mysql+pymysql://fmazcq43n76vlbz5c4wa:pscale_pw_CUl4Juf0tMi54XchsOTKPJKuE0HrhyNqTRcnjUm9U2y@aws.connect.psdb.cloud/swd?charset=utf8mb4"
engine = create_engine(
 db_connection_string, 
 connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
 })