import os

try:
    HOST = os.environ["POSTGRES_HOST"]
    USER = os.environ["POSTGRES_USER"]
    PASSWORD = os.environ["POSTGRES_PASSWORD"]
except:
    HOST = str("localhost")
    USER = str("postgres")
    PASSWORD = str("joaovitorcafe")

DATABASE = str("adm_simcc")
