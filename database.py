from sqlalchemy import create_engine, text

db_connection_string="mysql+pymysql://bp8jj0lq3uyxts2bb3o1:pscale_pw_6bTIFKXUCjNUUrqpEdeyeGP0IKTZNt0CvNTdtaHKq9X@aws.connect.psdb.cloud/swd?charset=utf8mb4"
engine = create_engine(
 db_connection_string, 
 connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
    }
 })