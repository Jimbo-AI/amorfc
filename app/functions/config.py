import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

config_db = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_DATABASE"),
    "charset": "utf8mb4",
}

onedrive_config = {
    "client_id": os.getenv("CLIENT_ID"),
    "scope": os.getenv("SCOPE"),
    "client_secret": os.getenv("CLIENT_SECRET"),
    "tenant_id": os.getenv("TENANT_ID"),
    "user_id": os.getenv("USER_ID"),
    "file_name": os.getenv("FILE_NAME"),
    "path": os.getenv("ONEDRIVE_PATH"),
}

openai_api_key = os.getenv("OPENAI_API_KEY")

persist_directory = os.getenv("PERSIST_DIRECTORY")

# config_db_mvp2 = {
#     'dbname': os.getenv("DBNAME_MVP2"),
#     'user': os.getenv("USER_MVP2"),
#     'password': os.getenv("PASSWORD_MVP2"),
#     'host': os.getenv("HOST_MVP2"),
#     'port': os.getenv("PORT_MVP2"),
# }
# config_db_mvp2 = {
#     'dbname': 'MattiProductionDb',
#     'user': 'fernando.torres',
#     'password': 'X0TyyuZUWmDpSK8',
#     'host': 'matti-production-aurora-cluster.cluster-ro-cu0j0dopeo4q.us-east-1.rds.amazonaws.com',
#     'port': '5432',
# }
def connect_db():
    db = mysql.connector.connect(**config_db)
    return db
