# insid the folder pipline we have created a file __init__.py to make it a package so that we can import from it

from src.data_ingestion import  DataIngestion
from src.data_preprocessing import DataProcessing
from src.model_tranning import Training

from utils.fonctions_common import read_yaml
from config import paths


if __name__ == "__main__":

    dataIngestion = DataIngestion(read_yaml(paths.CONFIG_PATH))
    dataIngestion.run()


    data_processing = DataProcessing(
            train_path=paths.TRAIN_FILE_PATH,
            test_path=paths.TEST_FILE_PATH,
            processing_dir=paths.DATA_PROCESSING_DIR,
            config=paths.CONFIG_PATH
        )
    data_processing.run()

    
    training = Training(train_path=paths.PROCESSED_TRAIN_FILE_PATH,
                        test_path=paths.PROCESSED_TEST_FILE_PATH,
                        model_path=paths.MODEL_TRAINED_PATH)  
    training.run_training_pipeline()  

