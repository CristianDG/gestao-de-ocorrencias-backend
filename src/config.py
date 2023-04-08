from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config:
    PSQL_DB_HOST = os.
    PSQL_DB_PORT = "5432"
    PSQL_DB_NAME = "prod-es"
    PSQL_DB_USER = "postgres"
    PSQL_DB_PASSWORD = "14022002"
