import os
import pandas as pd
import numpy as np
from src.applogger import get_logger
from src.specialExceptionHandling import CustException
from utils.fonctions_common import read_yaml, load_data
from config.paths import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE


logger = get_logger(__name__) 

class DataProcessing:
    def __init__(self,train_path,test_path,processing_dir,config):
        self.train_path = train_path
        self.test_path = test_path
        self.processing_dir = processing_dir
        
        self.config = read_yaml(config)
        
        if not os.path.exists(self.processing_dir):
            os.makedirs(self.processing_dir)

    def preprocessing_data(self,data):
        try :
            logger.info("We Are In God's Hands Now : Data Preprocessing Started")
            
            logger.info("Dropping useless columns...")
            data.drop(columns=["Booking_ID"], inplace=True)
            data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

            logger.info("Dropping duplicated rows...")
            data.drop_duplicates(inplace=True)

            cat_columns = self.config["data_processing"]["categorical_columns"]
            num_columns = self.config["data_processing"]["numerical_columns"]

            logger.info("label encodding...")

            label_encoder = LabelEncoder()

            mapping_dict = {}

            for col in cat_columns:
                data[col] = label_encoder.fit_transform(data[col])
                mapping_dict[col] = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
 
            logger.info("label mapping :")
            for col, mapping in mapping_dict.items():
                logger.info(f"{col} : {mapping}") 


            logger.info("handling skewness : asymmetric distribution of values...")

            skew_seuil = self.config["data_processing"]["skewness_threshold"]
            skewness = data[num_columns].apply(lambda x:x.skew())

            for column in skewness[skewness>skew_seuil].index:
                data[column] = np.log1p(data[column])

            return data
        except Exception as ce:
            logger.error(f"Error in preprocessing_data method  : {str(ce)}")
            #logger.error("Error in data preprocessing")
            raise CustException("Error in data preprocessing",ce)
        
    
    def handle_imbalance(self,data):
        try :
            logger.info("imbalanced data : handling started...")
            X = data.drop(columns=['booking_status'])
            y = data['booking_status']
            logger.info("splitting data into X and y : done")
            
            smote = SMOTE(random_state=42)
            X_res, y_res = smote.fit_resample(X, y)
            logger.info("imbalance handled successfully")

            data_res_df = pd.DataFrame(X_res, columns=X.columns)
            data_res_df['booking_status'] = y_res
            return data_res_df
        except Exception as e:
            #logger.error(f"Error in preprocessing_data method  : {str(e)}")
            logger.error("Error in handling imbalanced data")
            raise CustException("Error in handling imbalanced data",e)
        
    def feature_selection(self,data):
        try :
            logger.info("Feature Selection started...")

            X = data.drop(columns=['booking_status'])
            y = data['booking_status']

            model = RandomForestClassifier(random_state=42)
            model.fit(X, y)
            importances = model.feature_importances_
            feature_importance = pd.DataFrame({'Feature': X.columns, 'Importance': importances}).sort_values(by='Importance', ascending=False)
            num_features = self.config["data_processing"]["num_features"]
            selected_features = feature_importance['Feature'].head(num_features).values
            logger.info(f"Selected Features : {selected_features}")
            data_selected = data[selected_features.tolist() + ['booking_status']]
            
            logger.info("the first ligne of data after feature selection :")
            logger.info(f"{data_selected.head(1)}")

            return data_selected
        except Exception as e:
            logger.error(f"Error in feature selection: {str(e)}")
            raise CustException("Error in feature selection",e)
    
    def enregistrer_data(self,data,filepath):
        try : 
            logger.info(f"Saving processed data to {filepath}..."   )

            data.to_csv(filepath,index=False) # index false to avoid saving the index as a column : unnamed
            logger.info("Data saved successfully Hmdolah.")
        except Exception as e:
            logger.error("Error in saving processed data")
            raise CustException("Error in saving processed data",e)

    def run(self):
        try :
            logger.info("Data Processing started...")
            
            logger.info(f"Loading training data from {self.train_path}...")
            train_df = load_data(self.train_path)
            
            logger.info(f"Loading test data from {self.test_path}...")
            test_df = load_data(self.test_path)

            train_df = self.preprocessing_data(train_df)
            test_df = self.preprocessing_data(test_df)

            train_df = self.handle_imbalance(train_df)
            #test_df = self.handle_imbalance(test_df)

            train_df = self.feature_selection(train_df)
            test_df = test_df[train_df.columns]  

            self.enregistrer_data(train_df,PROCESSED_TRAIN_FILE_PATH)
            self.enregistrer_data(test_df,PROCESSED_TEST_FILE_PATH)
            logger.info("Hamdolah : Data Processing completed successfully.")
        except Exception as e:
            logger.error("Error in datapreprocessing run method")
            raise CustException("Error in datapreprocessing run method",e)


if __name__ == "__main__":
    try:
        
        data_processing = DataProcessing(
            train_path=TRAIN_FILE_PATH,
            test_path=TEST_FILE_PATH,
            processing_dir=DATA_PROCESSING_DIR,
            config=CONFIG_PATH
        )

        data_processing.run()
    except CustException as ce:
        logger.error(f"CustomException : {str(ce)}")
    except Exception as e:
        logger.error(f"Exception : {str(e)}")    










             

 



