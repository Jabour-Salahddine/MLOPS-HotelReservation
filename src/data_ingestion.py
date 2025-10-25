import os
import pandas as pd
#from google.cloud import storage

import boto3
from botocore.exceptions import NoCredentialsError, ClientError

from sklearn.model_selection import train_test_split # type: ignore
from src.applogger import get_logger
from src.specialExceptionHandling import CustException
from config.paths import *
from utils.fonctions_common import read_yaml

logger = get_logger(__name__) # Initialize logger


class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(DATA_DIR , exist_ok=True)

        logger.info(f"Data Ingestion started with {self.bucket_name} and file is  {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            #client = storage.Client()
            #bucket = client.bucket(self.bucket_name)
            #blob = bucket.blob(self.file_name)

            s3 = boto3.client('s3')
        
            # Téléchargement du fichier depuis S3
            s3.download_file(self.bucket_name, self.file_name, DATA_FILE_PATH) 

            logger.info(f"CSV file is sucesfully downloaded to {DATA_FILE_PATH}")

        except FileNotFoundError:
            logger.error(" The specified local path was not found.")
    
        except NoCredentialsError:
            logger.error(" AWS credentials not available. Run 'aws configure' or set environment variables.")
    
        except ClientError as e:
            logger.error(f" Failed to download file from S3: {e}")
        
    def split_data(self):
        try:
            logger.info("Starting the splitting process")
            data = pd.read_csv(DATA_FILE_PATH)
            train_data , test_data = train_test_split(data , test_size=1-self.train_test_ratio , random_state=42)

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)

            logger.info(f"Train data saved to {TRAIN_FILE_PATH}")
            logger.info(f"Test data saved to {TEST_FILE_PATH}")
        
        except Exception as e:
            logger.error("Error while splitting data")
            raise CustException("Failed to split data into training and test sets ", e)
        
    def run(self):

        try:
            logger.info("Starting data ingestion process")

            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data ingestion completed sucesfully")
        
        except CustException as ce:
            logger.error(f"CustomException : {str(ce)}")
        
        finally:
            logger.info("Data ingestion completed")

if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()

