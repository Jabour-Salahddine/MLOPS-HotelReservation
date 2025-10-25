import os

#****************************** DATA INGESTION ***********************

DATA_DIR = "artifacts/data"
DATA_FILE_PATH = os.path.join(DATA_DIR,"raw.csv")
TRAIN_FILE_PATH = os.path.join(DATA_DIR,"train.csv")
TEST_FILE_PATH = os.path.join(DATA_DIR,"test.csv")
CONFIG_PATH = "config/config.yaml"


# ********* Section for Data Processing *********   

DATA_PROCESSING_DIR = "artifacts/processed"
PROCESSED_TRAIN_FILE_PATH = os.path.join(DATA_PROCESSING_DIR,"processed_train.csv")
PROCESSED_TEST_FILE_PATH = os.path.join(DATA_PROCESSING_DIR,"processed_test.csv")


# ********* Section for Model Training *********

MODEL_TRAINED_PATH = "artifacts/model/LGBM_model.pkl"
