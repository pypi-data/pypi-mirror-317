import os

from dotenv import load_dotenv
from pydantic import BaseSettings


class Settings(BaseSettings):

    AWS_DEFAULT_REGION: str
    AWS_DEFAULT_REGION = "ap-southeast-2"
    DATABRICKS_CLUSTER_HOST: str
    DATABRICKS_CLUSTER_HOST = os.getenv("DATABRICKS_PROD_CLUSTER_HOST")
    DATABRICKS_PAT_TOKEN: str
    DATABRICKS_PAT_TOKEN = os.getenv("DATABRICKS_PAT_TOKEN")
    DATABRICKS_SQL_CLUSTER_PATH: str
    DATABRICKS_SQL_CLUSTER_PATH = os.getenv("DATABRICKS_SQL_CLUSTER_PATH")
    ONFS_PREFIX: str
    ONFS_PREFIX = "ponyta"
    UNITY_CATALOG: str
    UNITY_CATALOG = os.getenv("UNITY_CATALOG")
    DATABRICKS_TOKEN_URL: str
    DATABRICKS_TOKEN_URL = os.getenv("DATABRICKS_TOKEN_URL")
    DATABRICKS_CLIENT_ID: str
    DATABRICKS_CLIENT_ID = os.getenv("DATABRICKS_CLIENT_ID")
    DATABRICKS_CLIENT_SECRET: str
    DATABRICKS_CLIENT_SECRET = os.getenv("DATABRICKS_CLIENT_SECRET")


load_dotenv()
settings = Settings()
